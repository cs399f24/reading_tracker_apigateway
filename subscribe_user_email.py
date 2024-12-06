import boto3
import os

sns_client = boto3.client('sns', region_name=os.environ['AWS_REGION'])

def subscribe_to_sns(email, topic_arn):
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email
    )
    print(f'Subscription ARN: {response["SubscriptionArn"]}')

if __name__ == '__main__':
    # Get user's email and SNS topic ARN from .env
    user_email = os.environ['USER_EMAIL']
    topic_arn = os.environ['SNS_TOPIC_ARN']
    
    subscribe_to_sns(user_email, topic_arn)

