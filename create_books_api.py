import boto3
import json
import sys

client = boto3.client('apigateway', region_name='us-east-1')

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

# Create /search resource
search_resource = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='search'
)
search_resource_id = search_resource["id"]

# Define GET method for /search
search_method = client.put_method(
    restApiId=api_id,
    resourceId=search_resource_id,
    httpMethod='GET',
    authorizationType='NONE'
)

search_response = client.put_method_response(
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

# Get the ARN for the searchBooksFunction Lambda function
lambda_client = boto3.client('lambda', region_name='us-east-1')
lambda_arn = lambda_client.get_function(FunctionName='searchBooksFunction')['Configuration']['FunctionArn']
uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

# Get the ARN for the IAM LabRole
iam_client = boto3.client('iam')
lab_role = iam_client.get_role(RoleName='LabRole')['Role']['Arn']

# Integrate Lambda function with /search resource
search_integration = client.put_integration(
    restApiId=api_id,
    resourceId=search_resource_id,
    httpMethod='GET',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=uri
)

# Preflight OPTIONS for /search (CORS)
search_options_method = client.put_method(
    restApiId=api_id,
    resourceId=search_resource_id,
    httpMethod='OPTIONS',
    authorizationType='NONE'
)

search_options_response = client.put_method_response(
    restApiId=api_id,
    resourceId=search_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    },
    responseModels={'application/json': 'Empty'}
)

search_options_integration = client.put_integration(
    restApiId=api_id,
    resourceId=search_resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={'application/json': '{"statusCode": 200}'}
)

# Step 1: Lambda URI setup for savedBooksFunction
lambda_client = boto3.client('lambda', region_name='us-east-1')
lambda_arn = lambda_client.get_function(FunctionName='savedBooksFunction')['Configuration']['FunctionArn']
region = lambda_arn.split(':')[3]  # Extract the region dynamically
uri = f'arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

# Get the ARN for the IAM LabRole
iam_client = boto3.client('iam')
lab_role = iam_client.get_role(RoleName='LabRole')['Role']['Arn']

# Step 2: Create /save_book resource
save_book_resource = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='save_book'
)
save_book_resource_id = save_book_resource["id"]

# Step 3: Define POST method for /save_book
client.put_method(
    restApiId=api_id,
    resourceId=save_book_resource_id,
    httpMethod='POST',
    authorizationType='NONE'
)

# Step 4: Integrate Lambda function with POST method
client.put_integration(
    restApiId=api_id,
    resourceId=save_book_resource_id,
    httpMethod='POST',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri=uri,
    credentials=lab_role
)

# Step 5: Define method response for POST with CORS headers
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
        'method.response.header.Access-Control-Allow-Methods': "'OPTIONS,POST'"
    },
    responseTemplates={'application/json': ''}
)

# Step 6: Create OPTIONS method for /save_book (CORS Preflight)
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
        'method.response.header.Access-Control-Allow-Methods': "'OPTIONS,POST'"
    },
    responseTemplates={'application/json': ''}
)


# Create /shelved_books resource
shelved_books_resource = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='shelved_books'
)
shelved_books_resource_id = shelved_books_resource["id"]

# Define GET method for /shelved_books
shelved_books_method = client.put_method(
    restApiId=api_id,
    resourceId=shelved_books_resource_id,
    httpMethod='GET',
    authorizationType='NONE'
)

shelved_books_response = client.put_method_response(
    restApiId=api_id,
    resourceId=shelved_books_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    },
    responseModels={'application/json': 'Empty'}
)

# Get the ARN for the shelvedBooksFunction Lambda function
lambda_arn = lambda_client.get_function(FunctionName='shelvedBooksFunction')['Configuration']['FunctionArn']
uri = f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

# Integrate Lambda function with /shelved_books resource
shelved_books_integration = client.put_integration(
    restApiId=api_id,
    resourceId=shelved_books_resource_id,
    httpMethod='GET',
    credentials=lab_role,
    integrationHttpMethod='POST',
    type='AWS_PROXY',
    uri=uri
)

# Preflight OPTIONS for /shelved_books (CORS)
shelved_books_options_method = client.put_method(
    restApiId=api_id,
    resourceId=shelved_books_resource_id,
    httpMethod='OPTIONS',
    authorizationType='NONE'
)

shelved_books_options_response = client.put_method_response(
    restApiId=api_id,
    resourceId=shelved_books_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    },
    responseModels={'application/json': 'Empty'}
)

shelved_books_options_integration = client.put_integration(
    restApiId=api_id,
    resourceId=shelved_books_resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={'application/json': '{"statusCode": 200}'}
)

shelved_books_integration_response = client.put_integration_response(
    restApiId=api_id,
    resourceId=shelved_books_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
        'method.response.header.Access-Control-Allow-Methods': '\'POST\',\'OPTIONS\'',
        'method.response.header.Access-Control-Allow-Origin': '\'*\''
    }
)

# Print success message
print("API Gateway setup complete!")
