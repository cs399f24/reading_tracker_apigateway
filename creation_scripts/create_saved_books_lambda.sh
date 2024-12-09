
#!/bin/bash

# Check if the 'savedBooksFunction' Lambda already exists
if aws lambda get-function --function-name savedBooksFunction >/dev/null 2>&1; then
    echo "Function 'savedBooksFunction' already exists"
    exit 1
fi    

# Get the IAM Role ARN for 'labRole'
ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)

# Zip the 'saved_books.py' file
zip saved_books_lambda.zip saved_books_lambda.py

# Create the 'savedBooksFunction' Lambda function
aws lambda create-function --function-name savedBooksFunction \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://saved_books_lambda.zip \
  --handler saved_books_lambda.lambda_handler

# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name savedBooksFunction

# Publish a new version of the 'savedBooksFunction' Lambda function
aws lambda publish-version --function-name savedBooksFunction

echo "Deployment of 'savedBooksFunction' is complete."
