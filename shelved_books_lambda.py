import json
import boto3
import base64
from decimal import Decimal
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

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

def lambda_handler(event, context):
    # Extract the Authorization header
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

    try:
        # Decode the id_token to extract the user's Cognito unique identifier (sub)
        id_token = auth_header.split(" ")[1]
        
        # Decode the JWT token to get the payload
        payload = id_token.split('.')[1]
        padding = '=' * (-len(payload) % 4)  # Add padding if necessary
        decoded_payload = base64.urlsafe_b64decode(payload)
        user_info = json.loads(decoded_payload.decode('utf-8'))
        user_id = user_info.get('sub')

        if not user_id:
            raise ValueError("UserID (sub) not found in id_token")

        # Query DynamoDB for books specific to the user
        response = table.query(
            KeyConditionExpression=Key('UserID').eq(user_id)
        )

        # Convert Decimal values to float
        items = decimal_to_float(response.get('Items', []))

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "GET,OPTIONS",
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps(items)  # Now safe to serialize as Decimal values are converted
        }

    except ValueError as e:
        return {
            'statusCode': 401,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "GET,OPTIONS",
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({'message': 'Invalid id_token', 'error': str(e)})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "GET,OPTIONS",
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({'message': 'DynamoDB query failed', 'error': e.response['Error']['Message']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "GET,OPTIONS",
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
