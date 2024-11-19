import json
import boto3
import os
from botocore.exceptions import ClientError
from urllib.request import urlopen, Request
from urllib.parse import urlencode

def lambda_handler(event, context):
    query = event.get('queryStringParameters', {}).get('query')  # Get the query from the search request

    if not query:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Query parameter is required'})
        }

    # Encode the query to handle spaces and special characters
    encoded_query = urlencode({'q': query})

    # Retrieving Google Books API key from Secrets Manager
    secret_name = "reading_test_key"
    region_name = "us-east-1"
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        google_books_api_key = json.loads(get_secret_value_response['SecretString'])['googlebooks']
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Error retrieving secret: {e}"})
        }

    # Build Google Books API URL with the encoded query
    google_books_api = f"https://www.googleapis.com/books/v1/volumes?{encoded_query}&key={google_books_api_key}"

    # Using urllib instead of requests
    try:
        req = Request(google_books_api)
        with urlopen(req) as response:
            data = json.loads(response.read())
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Failed to fetch data from Google Books API: {e}"})
        }

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            'Access-Control-Allow-Methods': "GET",
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps(data)
    }


