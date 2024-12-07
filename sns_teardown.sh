#!/bin/bash

# Get the SNS topic ARN dynamically
SNS_TOPIC_ARN=$(aws sns list-topics --query "Topics[?contains(TopicArn, 'ReadingTracker')].TopicArn" --output text)

# Get the Lambda function name dynamically
LAMBDA_FUNCTION_NAME=$(aws lambda list-functions --query "Functions[?contains(FunctionName, 'ReadingTrackerNotification')].FunctionName" --output text)

# Get the CloudWatch rule ARN dynamically
CLOUDWATCH_RULE_ARN=$(aws events list-rules --query "Rules[?contains(Name, 'ReadingTrackerRule')].Arn" --output text)

# Get the Target ID dynamically for the CloudWatch rule
TARGET_ID=$(aws events list-targets-by-rule --rule "ReadingTrackerRule" --query "Targets[0].Id" --output text)

# Delete SNS topic if it exists
if [ "$SNS_TOPIC_ARN" != "None" ]; then
  aws sns delete-topic --topic-arn "$SNS_TOPIC_ARN"
  echo "SNS topic deleted."
else
  echo "SNS topic does not exist."
fi

# Delete Lambda function if it exists
if [ "$LAMBDA_FUNCTION_NAME" != "None" ]; then
  aws lambda delete-function --function-name "$LAMBDA_FUNCTION_NAME"
  echo "Lambda function deleted."
else
  echo "Lambda function does not exist."
fi

# Remove targets from the CloudWatch rule before deletion
if [ "$CLOUDWATCH_RULE_ARN" != "None" ]; then
  # Remove Lambda as the target of the CloudWatch rule
  if [ "$TARGET_ID" != "None" ]; then
    aws events remove-targets --rule "ReadingTrackerRule" --id "$TARGET_ID"
    echo "Lambda function removed as target from CloudWatch rule."
  else
    echo "No target found for CloudWatch rule."
  fi
  # Now delete the CloudWatch rule
  aws events delete-rule --name "ReadingTrackerRule"
  echo "CloudWatch rule deleted."
else
  echo "CloudWatch rule does not exist."
fi

