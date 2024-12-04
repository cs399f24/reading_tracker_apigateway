import boto3
import os
import json

# Initialize the SNS client
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    # Get the SNS topic ARN from environment variables
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
    if not sns_topic_arn:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'SNS_TOPIC_ARN is not set'})
        }
    
    # Message to publish
    message = "Hello! This is your scheduled notification from Amazon SNS."
    subject = "Scheduled Notification"
    
    try:
        # Publish the message to the SNS topic
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject=subject
        )
        print(f"Message published to SNS topic: {sns_topic_arn}")
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Message sent successfully'})
        }
    except Exception as e:
        print(f"Error sending message: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Error sending message: {e}'})
        }
