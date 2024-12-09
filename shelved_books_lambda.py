import json
import boto3
import base64
import urllib.parse
from decimal import Decimal
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('bookshelf')  # Ensure this matches your table name

# Helper function to convert Decimal to float
def decimal_to_float(data):
    if isinstance(data, Decimal):
        return float(data)
    elif isinstance(data, dict):
        return {key: decimal_to_float(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [decimal_to_float(item) for item in data]
    return data

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
  
    
    headers = event.get('headers', {})
    auth_header = headers.get('Authorization', '')
    
    if not auth_header.startswith("Bearer "):
        return {
            'statusCode': 401,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "GET,OPTIONS",
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({'message': 'Unauthorized: Missing or invalid Authorization header'})
        }
    
    id_token = auth_header.split(" ")[1]
    
    try:
        # Decode the token to extract payload
        header, payload = decode_token(id_token)
        user_id = payload.get("sub")
        email = payload.get("email")
        
        print(f"Payload: {payload}")
        print(f"Email: {email}")
        
        if not user_id:
            raise ValueError("User ID not found in token")
        
        print(f"User ID: {user_id}")
        
        response = table.query(KeyConditionExpression=Key('UserID').eq(user_id))
        items = decimal_to_float(response.get('Items', []))
        
    except Exception as e:
        print(f"Error processing token: {e}")
        return {
            'statusCode': 401,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "GET,OPTIONS",
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({'message': 'Unauthorized: Invalid token'})
        }
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            'Access-Control-Allow-Methods': "GET,OPTIONS",
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps(items)  # Safe to serialize as Decimal values are converted
    }
