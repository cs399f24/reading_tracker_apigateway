import boto3

# Initialize CloudWatch Events client
cloudwatch_client = boto3.client('events')

# Initialize Lambda client
lambda_client = boto3.client('lambda')

# Create the CloudWatch rule
response = cloudwatch_client.put_rule(
    Name='ReadReminderRule',
    ScheduleExpression='rate(5 minutes)',  # This triggers the Lambda function every 5 minutes
    State='ENABLED',
)

rule_arn = response['RuleArn']

# Add Lambda function as the target for the CloudWatch Rule
response = cloudwatch_client.put_targets(
    Rule='ReadReminderRule',
    Targets=[
        {
            'Id': 'ReadReminderTarget',
            'Arn': 'arn:aws:lambda:your-region:your-account-id:function:your-lambda-function-name',  # Replace with your Lambda ARN
        }
    ]
)

# Add permissions to allow CloudWatch to invoke the Lambda function
lambda_client.add_permission(
    FunctionName='your-lambda-function-name',  # Replace with your Lambda function name
    Principal='events.amazonaws.com',
    StatementId='ReadReminderInvokePermission',
    Action='lambda:InvokeFunction',
    SourceArn=rule_arn
)
