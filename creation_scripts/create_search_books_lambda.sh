#!/bin/bash

# Check if the 'searchBooksFunction' Lambda already exists
if aws lambda get-function --function-name searchBooksFunction >/dev/null 2>&1; then
    echo "Function 'searchBooksFunction' already exists"
    exit 1
fi    

# Get the IAM Role ARN for 'labRole'
ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)

# Zip the 'search_books.py' file
zip lambda_search_books.zip lambda_search_books.py

# Create the 'searchBooksFunction' Lambda function
aws lambda create-function --function-name searchBooksFunction \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://lambda_search_books.zip \
  --handler lambda_search_books.lambda_handler

# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name searchBooksFunction

# Publish a new version of the 'searchBooksFunction' Lambda function
aws lambda publish-version --function-name searchBooksFunction

echo "Deployment of 'searchBooksFunction' is complete."

