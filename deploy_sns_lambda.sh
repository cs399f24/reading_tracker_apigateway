#!/bin/bash

# Check if the 'sendScheduledSNSFunction' Lambda already exists
if aws lambda get-function --function-name sendSNSFunction >/dev/null 2>&1; then
    echo "Function 'sendSNSFunction' already exists"
    exit 1
fi    

# Create the SNS Topic
SNS_TOPIC_NAME="ScheduledSNSTopic"
SNS_TOPIC_ARN=$(aws sns create-topic --name "$SNS_TOPIC_NAME" --query "TopicArn" --output text)
echo "Created SNS Topic: $SNS_TOPIC_ARN"

# Get the IAM Role ARN for 'labRole'
ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)

# Ensure the Lambda function file exists before zipping
if [ ! -f "sns_lambda.py" ]; then
    echo "Error: sns_lambda.py not found!"
    exit 1
fi

# Zip the Lambda function code
zip sns_lambda.zip sns_lambda.py

# Create the Lambda function
aws lambda create-function --function-name sendSNSFunction \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://sns_lambda.zip \
  --handler sns_lambda.lambda_handler \
  --environment Variables="{SNS_TOPIC_ARN=$SNS_TOPIC_ARN}"

# Wait for the function to be active
aws lambda wait function-active --function-name sendSNSFunction

# Create the EventBridge rule to trigger Lambda every 3 days
RULE_NAME="SendSNSEveryMinute"
aws events put-rule --name "$RULE_NAME" --schedule-expression "cron(* * * * ? *)"
RULE_ARN=$(aws events describe-rule --name "$RULE_NAME" --query "Arn" --output text)

# Grant EventBridge permission to invoke the Lambda function
aws lambda add-permission \
  --function-name sendSNSFunction \
  --statement-id "EventBridgeInvokePermission" \
  --action "lambda:InvokeFunction" \
  --principal "events.amazonaws.com" \
  --source-arn "$RULE_ARN"

# Add the Lambda function as a target for the EventBridge rule
FUNCTION_ARN=$(aws lambda get-function --function-name sendSNSFunction --query 'Configuration.FunctionArn' --output text)

aws events put-targets --rule "$RULE_NAME" \
  --targets "Id=1,Arn=$FUNCTION_ARN"

echo "Deployment of 'sendSNSFunction' and scheduling complete."
