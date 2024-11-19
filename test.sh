#!/bin/bash

API_ID=$(aws apigateway get-rest-apis --query "items[?name=='BooksAPI'].id" --output text)
URL="https://$API_ID.execute-api.us-east-1.amazonaws.com/dev"
curl -X POST "$URL/save_book" \
-H 'Content-Type: application/json' \
-d '{"BookID": "123456800", "Title": "Sample Book 2", "Author": "John Doe", "PageCount": 100}'

