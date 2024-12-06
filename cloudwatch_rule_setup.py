import boto3
import os

# Load environment variables
AWS_REGION = os.getenv("AWS_REGION")

# Read the SNS topic ARN from the previous script
with open("sns_topic_arn.txt", "r") as file:
    topic_arn = file.read()

# Initialize CloudWatch Events and SNS client
cloudwatch_client = boto3.client('events', region_name=AWS_REGION)

# Create a CloudWatch Rule to trigger every 5 minutes
rule_response = cloudwatch_client.put_rule(
    Name="ReadingReminderRule",
    ScheduleExpression="rate(5 minutes)",
    State="ENABLED",
)

rule_arn = rule_response['RuleArn']
print(f"CloudWatch Rule created: {rule_arn}")

# Set the CloudWatch Rule to trigger SNS Topic
cloudwatch_client.put_targets(
    Rule="ReadingReminderRule",
    Targets=[
        {
            'Id': '1',
            'Arn': topic_arn
        }
    ]
)

print(f"CloudWatch Rule successfully linked to SNS Topic.")
