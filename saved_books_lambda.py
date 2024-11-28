import json
import boto3
from botocore.exceptions import ClientError
import logging
from decimal import Decimal

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

def create_user_table(user_id):
    table_name = f"bookshelf_{user_id}"
    try:
        existing_tables = dynamodb.list_tables()['TableNames']
        if table_name in existing_tables:
            logger.info(f"Table {table_name} already exists.")
            return table_name

        # Create the table
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'BookID', 'KeyType': 'HASH'},  # Partition key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'BookID', 'AttributeType': 'S'},  # String type
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        logger.info(f"Table {table_name} created successfully.")
        return table_name
    except ClientError as e:
        logger.error(f"Error creating table {table_name}: {e}")
        raise e

def lambda_handler(event, context):
    logger.info("Received headers: %s", json.dumps(event.get('headers', {})))
    logger.info("Received event: %s", json.dumps(event))

    # Extract the Authorization header
    headers = event.get('headers', {})
    auth_header = headers.get('Authorization', None)

    if not auth_header or not auth_header.startswith("Bearer "):
        return {
            'statusCode': 401,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "POST,OPTIONS",
                'Access-Control-Allow-Origin': "*",
            },
            'body': json.dumps({'message': 'Unauthorized: Missing or invalid Authorization header'})
        }

    try:
        # Decode the id_token to extract the user's Cognito unique identifier (sub)
        id_token = auth_header.split(" ")[1]
        payload = id_token.split('.')[1]
        padding = '=' * (-len(payload) % 4)  # Add padding if necessary
        payload += padding
        decoded_payload = json.loads(base64.urlsafe_b64decode(payload))
        user_id = decoded_payload['sub']
        logger.info(f"Extracted UserID: {user_id}")

        # Ensure the user's table exists
        table_name = create_user_table(user_id)

        # Parse the request body
        body = json.loads(event.get('body', '{}'))

        # Validate required fields
        required_fields = ['BookID', 'Title', 'Author', 'PageCount']
        if not all(field in body for field in required_fields):
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                    'Access-Control-Allow-Methods': "POST,OPTIONS",
                    'Access-Control-Allow-Origin': "*"
                },
                'body': json.dumps({'message': 'Missing required fields: BookID, Title, Author, or PageCount'})
            }

        # Extract and sanitize fields
        BookID = body['BookID']
        Title = body['Title'].replace('"', "'").strip()
        Author = body['Author'].replace('"', "'").strip()
        PageCount = body['PageCount']

        # Validate data types
        if not isinstance(PageCount, (int, float)) or PageCount <= 0:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                    'Access-Control-Allow-Methods': "POST,OPTIONS",
                    'Access-Control-Allow-Origin': "*"
                },
                'body': json.dumps({'message': 'Invalid PageCount: must be a positive number'})
            }

        # Prepare item for DynamoDB
        item = {
            'BookID': BookID,
            'Title': Title,
            'Author': Author,
            'PageCount': Decimal(str(PageCount))
        }

        # Save item to the user's table
        dynamodb.put_item(TableName=table_name, Item=item)
        logger.info(f"Book saved successfully in {table_name}: {json.dumps(item)}")

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "POST,OPTIONS",
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({'message': 'Book saved successfully'})
        }
    except ClientError as e:
        logger.error(f"DynamoDB ClientError: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "POST,OPTIONS",
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({'message': 'Failed to save book', 'error': e.response['Error']['Message']})
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "POST,OPTIONS",
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
