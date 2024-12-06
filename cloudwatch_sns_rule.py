import boto3
import os

cloudwatch_client = boto3.client('events', region_name=os.environ['AWS_REGION'])

def create_rule():
    response = cloudwatch_client.put_rule(
        Name='ReadReminderRule',
        ScheduleExpression='rate(5 minutes)',
        State='ENABLED',
    )
    rule_arn = response['RuleArn']
    print(f'CloudWatch Rule ARN: {rule_arn}')
    return rule_arn

def create_target(rule_arn):
    lambda_client = boto3.client('lambda', region_name=os.environ['AWS_REGION'])
    
    # Add target to trigger send_sns_notification.py Lambda function
    response = cloudwatch_client.put_targets(
        Rule='ReadReminderRule',
        Targets=[
            {
                'Id': '1',
                'Arn': os.environ['LAMBDA_FUNCTION_ARN']
            }
        ]
    )
    print(f'Target added to rule: {response}')

if __name__ == '__main__':
    rule_arn = create_rule()
    create_target(rule_arn)
