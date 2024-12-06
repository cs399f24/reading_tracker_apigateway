import boto3
import os
import json

sns_client = boto3.client('sns')

def lambda_handler(event, context):
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
    email_address = os.environ.get('SUBSCRIBER_EMAIL')

    if not sns_topic_arn or not email_address:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'SNS_TOPIC_ARN or SUBSCRIBER_EMAIL is not set'})
        }

    # Create a subscription if not already created
    try:
        subscriptions = sns_client.list_subscriptions_by_topic(TopicArn=sns_topic_arn)['Subscriptions']
        if not any(sub['Endpoint'] == email_address for sub in subscriptions):
            sns_client.subscribe(
                TopicArn=sns_topic_arn,
                Protocol='email',  
                Endpoint=email_address
            )
            print(f"Subscription created for: {email_address}")
    except Exception as e:
        print(f"Error creating subscription: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Error creating subscription: {e}'})
        }

    # Publish message
    message = "Have you remembered to read today?"
    subject = "Scheduled Notification"
    try:
        sns_client.publish(TopicArn=sns_topic_arn, Message=message, Subject=subject)
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

