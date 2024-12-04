#!/bin/bash

# Check if the 'sendScheduledSNSFunction' Lambda already exists
if aws lambda get-function --function-name sendScheduledSNSFunction >/dev/null 2>&1; then
    echo "Function 'sendScheduledSNSFunction' already exists"
    exit 1
fi    

# Create the SNS Topic
SNS_TOPIC_NAME="ScheduledSNSTopic"
SNS_TOPIC_ARN=$(aws sns create-topic --name "$SNS_TOPIC_NAME" --query "TopicArn" --output text)
echo "Created SNS Topic: $SNS_TOPIC_ARN"

# Get the IAM Role ARN for 'labRole'
ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)

# Zip the Lambda function code
zip scheduled_sns_lambda.zip scheduled_sns_lambda.py

# Create the Lambda function
aws lambda create-function --function-name sendScheduledSNSFunction \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://scheduled_sns_lambda.zip \
  --handler scheduled_sns_lambda.lambda_handler \
  --environment Variables="{SNS_TOPIC_ARN=$SNS_TOPIC_ARN}"

# Wait for the function to be active
aws lambda wait function-active --function-name sendScheduledSNSFunction

# Create the EventBridge rule to trigger Lambda every 3 days
RULE_NAME="SendSNSEvery3Days"
aws events put-rule --name "$RULE_NAME" --schedule-expression "cron(0 12 */3 * ? *)"
RULE_ARN=$(aws events describe-rule --name "$RULE_NAME" --query "Arn" --output text)

# Grant EventBridge permission to invoke the Lambda function
aws lambda add-permission \
  --function-name sendScheduledSNSFunction \
  --statement-id "EventBridgeInvokePermission" \
  --action "lambda:InvokeFunction" \
  --principal "events.amazonaws.com" \
  --source-arn "$RULE_ARN"

# Add the Lambda function as a target for the EventBridge rule
aws events put-targets --rule "$RULE_NAME" \
  --targets "Id=1,Arn=$(aws lambda get-function --function-name sendScheduledSNSFunction --query 'Configuration.FunctionArn' --output text)"

echo "Deployment of 'sendScheduledSNSFunction' and scheduling complete."
