#!/bin/bash

chmod +x ./creation_scripts/create_dynamodb.sh
chmod +x ./creation_scripts/create_cognito.sh
chmod +x ./creation_scripts/create_saved_books_lambda.sh
chmod +x ./creation_scripts/create_search_books_lambda.sh
chmod +x ./creation_scripts/create_shelved_books_lambda.sh
chmod +x deploy.sh
chmod +x update_index.sh
chmod +x sns_setup.sh
chmod +x ./creation_scripts/create_sns_lambda.sh
chmod +x ./creation_scripts/cloudwatch_sns_setup.sh

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

./creation_scripts/create_dynamodb.sh

./creation_scripts/create_cognito.sh

# Wait for the Cognito setup to complete (adjust time as needed)
echo "Waiting for Cognito setup to complete..."
sleep 5  # Waits for 5 seconds, you can adjust this duration

./sns_setup.sh

./creation_scripts/create_sns_lambda.sh

./creation_scripts/cloudwatch_sns_setup.sh

./creation_scripts/create_saved_books_lambda.sh

./creation_scripts/create_search_books_lambda.sh

./creation_scripts/create_shelved_books_lambda.sh

python3 create_books_api.py

./deploy.sh

./update_index.sh

