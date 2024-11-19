#!/bin/bash

# Check if the 'searchBooksFunction' Lambda already exists
if aws lambda get-function --function-name shelvedBooksFunction >/dev/null 2>&1; then
    echo "Function 'shelvedBooksFunction' already exists"
    exit 1
fi    

# Get the IAM Role ARN for 'labRole'
ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)

# Zip the 'shelved_books_lambda.py' file
zip shelved_books_lambda.zip shelved_books_lambda.py

# Create the 'shelvedBooksFunction' Lambda function
aws lambda create-function --function-name shelvedBooksFunction \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://shelved_books_lambda.zip \
  --handler shelved_books_lambda.lambda_handler

# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name shelvedBooksFunction

# Publish a new version of the 'shelvedBooksFunction' Lambda function
aws lambda publish-version --function-name shelvedBooksFunction

echo "Deployment of 'shelvedBooksFunction' is complete."