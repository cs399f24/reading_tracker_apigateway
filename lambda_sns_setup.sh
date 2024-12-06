#!/bin/bash

# Set up environment variables
source .env

# Create the Lambda function zip file
echo "Creating Lambda function zip..."
zip function.zip sns_notification.py

# Create Lambda function
echo "Creating Lambda function..."
aws lambda create-function \
    --function-name "ReadingTrackerNotificationFunction" \
    --zip-file fileb://function.zip \
    --handler sns_notification.lambda_handler \
    --runtime python3.8 \
    --role arn:aws:iam::YOUR_ACCOUNT_ID:role/your-lambda-role \
    --environment Variables={SNS_TOPIC_ARN=$SNS_TOPIC_ARN} \
    --region $AWS_REGION

echo "Lambda Function Created: ReadingTrackerNotificationFunction"

