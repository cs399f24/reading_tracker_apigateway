import os
import boto3


# Initialize the SNS client
sns_client = boto3.client('sns', region_name=os.environ['AWS_REGION'])
cognito_client = boto3.client('cognito-idp', region_name='us-east-1')
sns_client = boto3.client('sns', region_name='us-east-1')

def get_user_pool_id_by_name(pool_name):
    """Retrieve the user pool ID by name."""
    user_pools = cognito_client.list_user_pools(MaxResults=50)
    for pool in user_pools['UserPools']:
        if pool['Name'] == pool_name:
            return pool['Id']
    raise Exception(f"User pool with name '{pool_name}' not found.")

def get_user_emails(user_pool_id):
    """Retrieve all email addresses from the Cognito user pool."""
    emails = []
    response = cognito_client.list_users(UserPoolId=user_pool_id)
    while response:
        for user in response['Users']:
            for attribute in user['Attributes']:
                if attribute['Name'] == 'email':
                    emails.append(attribute['Value'])
        # Handle pagination
        if 'PaginationToken' in response:
            response = cognito_client.list_users(
                UserPoolId=user_pool_id, PaginationToken=response['PaginationToken']
            )
        else:
            break
    return emails

def ensure_subscriptions(topic_arn, emails):
    """Subscribe users to the SNS topic if not already subscribed."""
    subscribed_emails = []
    
    # List current subscriptions for the topic
    response = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
    for subscription in response['Subscriptions']:
        if subscription['Protocol'] == 'email' and subscription['Endpoint']:
            subscribed_emails.append(subscription['Endpoint'])
            
    for subscription in response['Subscriptions']:
        if subscription['Protocol'] == 'email' and subscription['Endpoint'] not in emails:
            sns_client.unsubscribe(SubscriptionArn=subscription['SubscriptionArn'])
            print(f"Unsubscribed {subscription['Endpoint']} from the topic.")


    # Subscribe missing emails
    for email in emails:
        if email not in subscribed_emails:
            sns_client.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint=email
            )
            print(f"Subscription request sent to {email}. Check inbox to confirm.")

def lambda_handler(event, context):
        # Specify the topic name
    topic_name = 'ReadingTrackerTopic'
    
    # Retrieve the list of topics
    response = sns_client.list_topics()
    
    # Find the ARN for the specific topic name
    sns_topic_arn = None
    for topic in response['Topics']:
        arn = topic['TopicArn']
        if arn.endswith(f":{topic_name}"):
            sns_topic_arn = arn
            break
        
    user_pool_name = 'BookshelfUserPool' # Cognito User Pool Name from environment
    
    try:
        # Step 1: Get the user pool ID
        user_pool_id = get_user_pool_id_by_name(user_pool_name)
        
        # Step 2: Retrieve user emails
        emails = get_user_emails(user_pool_id)
        print(f"Retrieved emails: {emails}")
        
        # Step 3: Ensure subscriptions
        ensure_subscriptions(sns_topic_arn, emails)

        # Step 4: Publish notification to the topic
        message = "Have you remembered to read today?"
        subject = "Reminder to Read"
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
            'body': f'Error: {e}'
        }
