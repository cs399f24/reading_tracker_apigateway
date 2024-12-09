#!/bin/bash

# Define the name of the Cognito User Pool and Domain
USER_POOL_NAME="BookshelfUserPool"
USER_POOL_DOMAIN="bookshelf-app-domain"

# Get the User Pool ID based on the pool name
USER_POOL_ID=$(aws cognito-idp list-user-pools --max-results 60 --query "UserPools[?Name=='$USER_POOL_NAME'].Id" --output text)

# Check if the User Pool ID is found
if [ -z "$USER_POOL_ID" ]; then
    echo "Error: User Pool with name '$USER_POOL_NAME' not found."
    exit 1
else
    echo "Found User Pool with ID: $USER_POOL_ID"
fi

# Delete the Cognito User Pool Domain
echo "Deleting User Pool domain: $USER_POOL_DOMAIN"
aws cognito-idp delete-user-pool-domain --domain $USER_POOL_DOMAIN --user-pool-id $USER_POOL_ID

# Check if the domain deletion was successful
if [ $? -eq 0 ]; then
    echo "User Pool domain '$USER_POOL_DOMAIN' deleted successfully."
else
    echo "Error: Failed to delete User Pool domain '$USER_POOL_DOMAIN'."
    exit 1
fi

# Delete the Cognito User Pool
echo "Deleting User Pool: $USER_POOL_NAME"
aws cognito-idp delete-user-pool --user-pool-id $USER_POOL_ID

# Check if the delete operation was successful
if [ $? -eq 0 ]; then
    echo "User Pool '$USER_POOL_NAME' deleted successfully."
else
    echo "Error: Failed to delete User Pool '$USER_POOL_NAME'."
    exit 1
fi
