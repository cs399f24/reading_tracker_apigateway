import boto3

# Initialize the Cognito client
cognito_client = boto3.client('cognito-idp', region_name='us-east-1')

# Create a user pool
user_pool_response = cognito_client.create_user_pool(
    PoolName='<Enter user pool name>', # example: BookshelfUserPool
    Policies={
        'PasswordPolicy': {
            'MinimumLength': 8,
            'RequireUppercase': True,
            'RequireLowercase': True,
            'RequireNumbers': True,
            'RequireSymbols': True,
            'TemporaryPasswordValidityDays': 7
        }
    },
    AutoVerifiedAttributes=['email'],  # Automatically verify email attribute
    UsernameAttributes=['email'],  # Allow sign-in with email
    UsernameConfiguration={
        'CaseSensitive': False  # Case insensitive usernames
    },
    VerificationMessageTemplate={
        'DefaultEmailOption': 'CONFIRM_WITH_CODE',  # Configure email verification
        'EmailMessage': 'Your verification code is {####}',
        'EmailSubject': 'Verification Code'
    }
)

user_pool_id = user_pool_response['UserPool']['Id']
print(f"Created User Pool with ID: {user_pool_id}")

# Create a resource server for custom scopes
resource_server_response = cognito_client.create_resource_server(
    UserPoolId=user_pool_id,
    Identifier='<Enter identifier>',  # example: https://izmwmockf4.execute-api.us-east-1.amazonaws.com/dev
    Name='<Enter server name>', # example: BookshelfAPI
    Scopes=[
        {'ScopeName': '<scope name>', 'ScopeDescription': '<scope description>'} # example: {'ScopeName': 'save_books', 'ScopeDescription': 'Save books to the bookshelf'}
    ]
)

resource_server_id = resource_server_response['ResourceServer']['Identifier']
print(f"Resource server created with ID: {resource_server_id}")

# Create an app client for the user pool with the custom scope
app_client_response = cognito_client.create_user_pool_client(
    UserPoolId=user_pool_id,
    ClientName='<Enter client name>', # example: BookshelfAppClient
    GenerateSecret=False,
    AllowedOAuthFlows=['implicit'],  # OAuth flow for Implicit Grant
    AllowedOAuthScopes=[
        'email',
        'openid',
        'profile',
        '<Enter custom scope>'  # Add custom scope, example:https://izmwmockf4.execute-api.us-east-1.amazonaws.com/dev/save_books
    ],
    AllowedOAuthFlowsUserPoolClient=True,
    CallbackURLs=['<Enter callback URL>'], # example: https://dev.d1gkbe41ifhq4p.amplifyapp.com/callback.html
    LogoutURLs=['<Enter logout URL>'], # example: https://dev.d1gkbe41ifhq4p.amplifyapp.com/logout.html
    ExplicitAuthFlows=[
        'ALLOW_REFRESH_TOKEN_AUTH',
        'ALLOW_USER_SRP_AUTH',
        'ALLOW_USER_PASSWORD_AUTH',
        'ALLOW_CUSTOM_AUTH'
    ],
    SupportedIdentityProviders=['COGNITO']  # Add Cognito as the identity provider
)

app_client_id = app_client_response['UserPoolClient']['ClientId']
print(f"Created App Client with ID: {app_client_id}")

# Configure a domain for the hosted UI
domain_response = cognito_client.create_user_pool_domain(
    Domain='<Enter domain name>', # example: bookshelf-app-domain
    UserPoolId=user_pool_id
)
print(f"Configured hosted UI domain: bookshelf-app-domain")

# Generate the hosted UI login URL (with implicit flow and token response type)
hosted_ui_url = (
    f"https://<Enter domain name>.auth.us-east-1.amazoncognito.com/login?"
    f"response_type=token&client_id={app_client_id}&redirect_uri=<Enter callback URL>"
)

print(f"Hosted UI URL: {hosted_ui_url}")
