import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get region and email from environment variables
AWS_REGION = os.getenv("AWS_REGION")
USER_EMAIL = os.getenv("USER_EMAIL")

# Initialize SNS client
sns_client = boto3.client('sns', region_name=AWS_REGION)

# Step 1: Create SNS Topic
topic_response = sns_client.create_topic(Name='ReadingReminderTopic')
topic_arn = topic_response['TopicArn']

print(f"SNS Topic created: {topic_arn}")

# Step 2: Subscribe the user email to the SNS Topic
subscribe_response = sns_client.subscribe(
    TopicArn=topic_arn,
    Protocol='email',
    Endpoint=USER_EMAIL
)

print(f"Subscription request sent to {USER_EMAIL}. Check your inbox to confirm.")

# Save the topic ARN for later use (for the CloudWatch Rule setup)
with open("sns_topic_arn.txt", "w") as file:
    file.write(topic_arn)
