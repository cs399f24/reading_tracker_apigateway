#!/bin/bash

# Set up environment variables
source .env

# Create SNS Topic
echo "Creating SNS Topic..."
SNS_TOPIC_ARN=$(aws sns create-topic --name "ReadingTrackerTopic" --region $AWS_REGION --query 'TopicArn' --output text)

# Subscribe the user's email to the SNS Topic
echo "Subscribing user email to SNS topic..."
aws sns subscribe --topic-arn $SNS_TOPIC_ARN --protocol email --notification-endpoint $USER_EMAIL --region $AWS_REGION

echo "SNS Topic Created: $SNS_TOPIC_ARN"
echo "Subscription Sent to: $USER_EMAIL"
