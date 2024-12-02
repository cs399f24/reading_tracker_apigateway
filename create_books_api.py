import boto3
import json
import sys

# Initialize clients
client = boto3.client('apigateway', region_name='us-east-1')
lambda_client = boto3.client('lambda', region_name='us-east-1')
iam_client = boto3.client('iam')

# Fetch LabRole ARN once
lab_role_arn = iam_client.get_role(RoleName='LabRole')['Role']['Arn']

# Check if the API already exists
response = client.get_rest_apis()
apis = response.get('items', [])

for api in apis:
    if api.get('name') == 'BooksAPI':
        print('API already exists')
        sys.exit(0)

# Create the API
response = client.create_rest_api(
    name='BooksAPI',
    description='API to manage books in the bookshelf.',
    endpointConfiguration={
        'types': ['REGIONAL']
    }
)
api_id = response["id"]

resources = client.get_resources(restApiId=api_id)
root_id = [resource for resource in resources["items"] if resource["path"] == "/"][0]["id"]

# Create Cognito authorizer
authorizer_response = client.create_authorizer(
    restApiId=api_id,
    name='BooksPoolAuthorizer',
    type='COGNITO_USER_POOLS',
    providerARNs=[
        'arn:aws:cognito-idp:us-east-1:715365186374:userpool/us-east-1_JTD6bNQbq'  # Replace with actual ARN
    ],
    identitySource='method.request.header.Authorization'
)
authorizer_id = authorizer_response['id']

# ----------------------------- /search Resource ----------------------------- #
# Create /search resource
search_resource = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='search'
)
search_resource_id = search_resource["id"]

# Define GET method for /search
client.put_method(
    restApiId=api_id,
    resourceId=search_resource_id,
    httpMethod='GET',
    authorizationType='NONE',
)

# Attach Lambda function to /search
search_function_arn = lambda_client.get_function(FunctionName='searchBooksFunction')['Configuration']['FunctionArn']
search_uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{search_function_arn}/invocations'

client.put_integration(
    restApiId=api_id,
    resourceId=search_resource_id,
    httpMethod='GET',
    credentials=lab_role_arn,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=search_uri
)

# Add CORS support to /search
client.put_method_response(
    restApiId=api_id,
    resourceId=search_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    },
    responseModels={'application/json': 'Empty'}
)

client.put_integration_response(
    restApiId=api_id,
    resourceId=search_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
        'method.response.header.Access-Control-Allow-Origin': "'*'",
        'method.response.header.Access-Control-Allow-Methods': "'GET,OPTIONS'"
    },
    responseTemplates={'application/json': ''}
)

# Add OPTIONS method for CORS preflight
client.put_method(
    restApiId=api_id,
    resourceId=search_resource_id,
    httpMethod='OPTIONS',
    authorizationType='NONE'
)

client.put_integration(
    restApiId=api_id,
    resourceId=search_resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={'application/json': '{"statusCode": 200}'}
)

# ----------------------------- /save_book Resource ----------------------------- #
# Create /save_book resource
save_book_resource = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='save_book'
)
save_book_resource_id = save_book_resource["id"]

# Define POST method for /save_book
client.put_method(
    restApiId=api_id,
    resourceId=save_book_resource_id,
    httpMethod='POST',
    authorizationType='COGNITO_USER_POOLS',
    authorizerId=authorizer_id
)

# Attach Lambda function to /save_book
save_book_function_arn = lambda_client.get_function(FunctionName='savedBooksFunction')['Configuration']['FunctionArn']
save_book_uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{save_book_function_arn}/invocations'

client.put_integration(
    restApiId=api_id,
    resourceId=save_book_resource_id,
    httpMethod='POST',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri=save_book_uri,
    credentials=lab_role_arn
)

# Add CORS support to /save_book
client.put_method_response(
    restApiId=api_id,
    resourceId=save_book_resource_id,
    httpMethod='POST',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    }
)

client.put_integration_response(
    restApiId=api_id,
    resourceId=save_book_resource_id,
    httpMethod='POST',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
        'method.response.header.Access-Control-Allow-Origin': "'*'",
        'method.response.header.Access-Control-Allow-Methods': "'POST,OPTIONS'"
    },
    responseTemplates={'application/json': ''}
)

# Add OPTIONS method for CORS preflight
client.put_method(
    restApiId=api_id,
    resourceId=save_book_resource_id,
    httpMethod='OPTIONS',
    authorizationType='NONE'
)

client.put_integration(
    restApiId=api_id,
    resourceId=save_book_resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={'application/json': '{"statusCode": 200}'}
)

client.put_method_response(
    restApiId=api_id,
    resourceId=save_book_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    }
)

client.put_integration_response(
    restApiId=api_id,
    resourceId=save_book_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
        'method.response.header.Access-Control-Allow-Origin': "'*'",
        'method.response.header.Access-Control-Allow-Methods': "'POST,OPTIONS'"
    },
    responseTemplates={'application/json': ''}
)

# ----------------------------- /shelved_books Resource ----------------------------- #
# Create /shelved_books resource
shelved_books_resource = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='shelved_books'
)
shelved_books_resource_id = shelved_books_resource["id"]

# Define GET method for /shelved_books
client.put_method(
    restApiId=api_id,
    resourceId=shelved_books_resource_id,
    httpMethod='GET',
    authorizationType='COGNITO_USER_POOLS',
    authorizerId=authorizer_id
)

# Attach Lambda function to /shelved_books
shelved_books_function_arn = lambda_client.get_function(FunctionName='shelvedBooksFunction')['Configuration']['FunctionArn']
shelved_books_uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{shelved_books_function_arn}/invocations'

client.put_integration(
    restApiId=api_id,
    resourceId=shelved_books_resource_id,
    httpMethod='GET',
    type='AWS_PROXY',
    integrationHttpMethod='POST',  # Must match Lambda integration method
    uri=shelved_books_uri,
    credentials=lab_role_arn
)

# Add CORS support to GET method response
client.put_method_response(
    restApiId=api_id,
    resourceId=shelved_books_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    }
)

client.put_integration_response(
    restApiId=api_id,
    resourceId=shelved_books_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
        'method.response.header.Access-Control-Allow-Origin': "'*'",
        'method.response.header.Access-Control-Allow-Methods': "'GET,OPTIONS'"
    },
    responseTemplates={'application/json': ''}
)

# Add OPTIONS method for CORS preflight
client.put_method(
    restApiId=api_id,
    resourceId=shelved_books_resource_id,
    httpMethod='OPTIONS',
    authorizationType='NONE'
)

client.put_integration(
    restApiId=api_id,
    resourceId=shelved_books_resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={'application/json': '{"statusCode": 200}'}
)

client.put_method_response(
    restApiId=api_id,
    resourceId=shelved_books_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    }
)

client.put_integration_response(
    restApiId=api_id,
    resourceId=shelved_books_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
        'method.response.header.Access-Control-Allow-Origin': "'*'",
        'method.response.header.Access-Control-Allow-Methods': "'GET,OPTIONS'"
    },
    responseTemplates={'application/json': ''}
)

# Print success message
print("API Gateway setup complete!")
