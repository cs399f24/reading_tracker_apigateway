import boto3
import os

sns_client = boto3.client('sns', region_name=os.environ['AWS_REGION'])

def send_notification():
    message = "Have you remembered to read today?"
    subject = "Reading Reminder"
    
    response = sns_client.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'],
        Message=message,
        Subject=subject
    )
    print(f'Message sent to topic: {response["MessageId"]}')

if __name__ == '__main__':
    send_notification()


