import boto3
import os

sns_client = boto3.client('sns', region_name=os.environ['AWS_REGION'])

def lambda_handler(event, context):
    sns_topic_arn = os.environ['SNS_TOPIC_ARN'] # .env variable
    message = "Have you remembered to read today?"
    subject = "Reminder to Read"
    
    try:
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject=subject
        )
        return {
            'statusCode': 200,
            'body': 'Notification sent successfully'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error sending notification: {e}'
        }
