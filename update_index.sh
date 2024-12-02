API_ID=$(aws apigateway get-rest-apis --query "items[?name=='BooksAPI'].id" --output text)
URL="https://$API_ID.execute-api.us-east-1.amazonaws.com/dev"
sed -i "s|^\([[:space:]]*\)const server = 'https://.*';|\1const server = '$URL';|" index.html
aws s3 cp index.html s3://cadiztmp