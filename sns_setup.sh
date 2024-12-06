#!/bin/bash

# Run the Python script to create SNS topic
echo "Creating SNS Topic..."
python3 create_sns_topic.py

# Run the Python script to subscribe the user's email to the SNS topic
echo "Subscribing user email to SNS topic..."
python3 subscribe_user_email.py

# Run the Python script to create a CloudWatch rule to trigger SNS every 5 minutes
echo "Creating CloudWatch Rule..."
python3 create_cloudwatch_rule.py

echo "SNS Setup Complete."
