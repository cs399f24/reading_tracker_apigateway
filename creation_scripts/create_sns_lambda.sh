#!/bin/bash

# Check if the 'searchBooksFunction' Lambda already exists
if aws lambda get-function --function-name snsLambda >/dev/null 2>&1; then
    echo "Function 'snsLambda' already exists"
    exit 1
fi    

# Get the IAM Role ARN for 'labRole'
ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)

# Zip the 'shelved_books_lambda.py' file
zip sns_lambda.zip sns_lambda.py

# Create the 'shelvedBooksFunction' Lambda function
aws lambda create-function --function-name snsLambda \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://sns_lambda.zip \
  --handler sns_lambda.lambda_handler

# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name snsLambda

# Publish a new version of the 'shelvedBooksFunction' Lambda function
aws lambda publish-version --function-name snsLambda

echo "Deployment of 'snsLambda' is complete."