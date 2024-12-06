import boto3
import os

sns_client = boto3.client('sns', region_name=os.environ['AWS_REGION'])

def create_sns_topic():
    response = sns_client.create_topic(Name=os.environ['SNS_TOPIC_NAME'])
    topic_arn = response['TopicArn']
    
    # Save the topic ARN for later use
    print(f'SNS Topic ARN: {topic_arn}')
    return topic_arn

if __name__ == '__main__':
    create_sns_topic()

