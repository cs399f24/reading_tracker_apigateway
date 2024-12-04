import json
import boto3
import base64
import urllib.parse
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('bookshelf')  # Ensure this matches the correct DynamoDB table name

def decode_token(id_token):
    # Split the token into header, payload, and signature
    parts = id_token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid token format")
    
    # Decode header and payload (Base64 URL decoding)
    header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
    payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
    
    return header, payload

def get_cognito_public_keys(region, user_pool_id):
    # Use boto3 to get the User Pool metadata
    cognito_idp_client = boto3.client('cognito-idp', region_name=region)
    metadata = cognito_idp_client.describe_user_pool(UserPoolId=user_pool_id)
    
    # Extract the domain from the User Pool metadata
    jwks_url = metadata['UserPool']['Domain'] + '/.well-known/jwks.json'
    parsed_url = urllib.parse.urlparse(jwks_url)
    
    # Fetch the JWKs JSON from the Cognito User Pool domain
    http_client = boto3.client('apigatewayv2')
    response = http_client.get_rest_api(restApiId=parsed_url.netloc)
    jwks = json.loads(response['body'])
    
    return jwks

def lambda_handler(event, context):
    # Parse the request body
    body = json.loads(event.get('body', '{}'))
    
    headers = event.get('headers', {})
    auth_header = headers.get('Authorization', '')

    # Validate required fields
    required_fields = ['BookID', 'Title', 'Author', 'PageCount']
    if not all(field in body for field in required_fields):
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "POST",
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({'message': 'Missing required fields: BookID, Title, Author, or PageCount'})
        }
        
    
    id_token = auth_header.split(" ")[1]
    
    # Decode the token to extract payload
    header, payload = decode_token(id_token)
    user_id = payload.get("sub")
    
    if not user_id:
        raise ValueError("User ID not found in token")

    # Extract fields from the body
    BookID = body['BookID']
    Title = body['Title']
    Author = body['Author']
    PageCount = body['PageCount']

    # Replace double quotes with single quotes
    Title = Title.replace('"', "'")  # Replace double quotes with single quotes in Title
    Author = Author.replace('"', "'")  # Replace double quotes with single quotes in Author

    # Prepare item for DynamoDB
    item = {
        'UserID': user_id,
        'BookID': BookID,
        'Title': Title,
        'Author': Author,
        'PageCount': PageCount
    }

    try:
        # Save item to DynamoDB
        table.put_item(Item=item)
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "POST",
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({'message': 'Book saved successfully'})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "POST",
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({'message': 'Failed to save book', 'error': e.response['Error']['Message']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "POST",
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }

