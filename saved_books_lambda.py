import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('bookshelf')  # Ensure this matches the correct DynamoDB table name

def lambda_handler(event, context):
    # Parse the request body
    body = json.loads(event.get('body', '{}'))

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
