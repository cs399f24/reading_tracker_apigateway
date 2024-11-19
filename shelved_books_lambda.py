import json
import boto3
from decimal import Decimal

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
    # Scan the bookshelf table to get all books
    response = table.scan()
    
    # Convert Decimal values to float
    items = decimal_to_float(response['Items'])
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            'Access-Control-Allow-Methods': "GET",
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps(items)  # Now safe to serialize as Decimal values are converted
    }
