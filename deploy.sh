#!/bin/bash

# Fetch the API ID of BooksAPI
API_ID=$(aws apigateway get-rest-apis --query "items[?name=='BooksAPI'].id" --output text)

# Check if the API exists
if [ -z "$API_ID" ]; then
  echo "BooksAPI not found!"
  exit 1
fi

# Deploy the API to the 'dev' stage
aws apigateway create-deployment --rest-api-id $API_ID --stage-name dev

if [ $? -eq 0 ]; then
  echo "BooksAPI successfully deployed to stage 'dev'."
else
  echo "Failed to deploy BooksAPI."
fi
