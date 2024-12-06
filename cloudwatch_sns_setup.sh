#!/bin/bash

# Set up environment variables
source .env

# Create CloudWatch Rule
echo "Creating CloudWatch Rule..."
aws events put-rule \
    --name "ReadingTrackerRule" \
    --schedule-expression "rate(5 minutes)" \
    --state "ENABLED" \
    --region $AWS_REGION

# Add Lambda function as target for the CloudWatch Rule
echo "Adding Lambda function as target for CloudWatch Rule..."
aws events put-targets \
    --rule "ReadingTrackerRule" \
    --targets "Id"="1","Arn"="arn:aws:lambda:$AWS_REGION:YOUR_ACCOUNT_ID:function:ReadingTrackerNotificationFunction" \
    --region $AWS_REGION

# Add permissions for CloudWatch to invoke Lambda
echo "Adding permissions for CloudWatch to invoke Lambda..."
aws lambda add-permission \
    --function-name "ReadingTrackerNotificationFunction" \
    --principal events.amazonaws.com \
    --statement-id "CloudWatchInvokeLambda" \
    --action "lambda:InvokeFunction" \
    --region $AWS_REGION

echo "CloudWatch Rule Created and Linked to Lambda"
