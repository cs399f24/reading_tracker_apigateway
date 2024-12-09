#!/bin/bash

AWS_REGION='us-east-1'

# Get the Lambda function ARN
SNS_ARN=$(aws lambda get-function --function-name snsLambda --query 'Configuration.FunctionArn' --output text)

# Check if the ARN was retrieved successfully
if [ -z "$SNS_ARN" ]; then
    echo "Error: Unable to retrieve Lambda function ARN."
    exit 1
fi

# Create CloudWatch Rule
echo "Creating CloudWatch Rule..."
aws events put-rule \
    --name "ReadingTrackerRule" \
    --schedule-expression "rate(1 day)" \
    --state "ENABLED" \
    --region "$AWS_REGION"

# Add Lambda function as target for the CloudWatch Rule
echo "Adding Lambda function as target for CloudWatch Rule..."
aws events put-targets \
    --rule "ReadingTrackerRule" \
    --targets "[{\"Id\":\"1\",\"Arn\":\"$SNS_ARN\"}]" \
    --region "$AWS_REGION"

# Add permissions for CloudWatch to invoke Lambda
echo "Adding permissions for CloudWatch to invoke Lambda..."
aws lambda add-permission \
    --function-name "snsLambda" \
    --principal events.amazonaws.com \
    --statement-id "CloudWatchInvokeLambda" \
    --action "lambda:InvokeFunction" \
    --region "$AWS_REGION" \
    --source-arn "arn:aws:events:$AWS_REGION:$(aws sts get-caller-identity --query 'Account' --output text):rule/ReadingTrackerRule"

echo "CloudWatch Rule Created and Linked to Lambda"

