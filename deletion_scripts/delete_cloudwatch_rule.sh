#!/bin/bash

# Define the CloudWatch Events Rule name
RULE_NAME="ReadingTrackerRule"
REGION="us-east-1"

# Step 1: List the targets associated with the rule
TARGETS=$(aws events list-targets-by-rule --rule $RULE_NAME --region $REGION --query "Targets[*].Id" --output text)

# Check if there are any targets
if [ -z "$TARGETS" ]; then
    echo "No targets found for rule '$RULE_NAME'. Proceeding to delete the rule."
else
    echo "Removing targets for rule '$RULE_NAME'..."
    
    # Step 2: Remove targets from the rule
    aws events remove-targets --rule $RULE_NAME --ids $TARGETS --region $REGION
    
    # Check if target removal was successful
    if [ $? -eq 0 ]; then
        echo "Targets removed successfully."
    else
        echo "Error: Failed to remove targets from rule '$RULE_NAME'."
        exit 1
    fi
fi

# Step 3: Delete the CloudWatch Events Rule
echo "Deleting rule '$RULE_NAME'..."
aws events delete-rule --name $RULE_NAME --region $REGION

# Check if the rule deletion was successful
if [ $? -eq 0 ]; then
    echo "Rule '$RULE_NAME' deleted successfully."
else
    echo "Error: Failed to delete rule '$RULE_NAME'."
    exit 1
fi
