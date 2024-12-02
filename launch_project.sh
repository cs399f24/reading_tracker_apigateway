#!/bin/bash

chmod +x create_dynamodb.sh
chmod +x create_saved_books_lambda.1.sh
chmod +x create_search_books_lambda.sh
chmod +x create_shelved_books_lambda.sh
chmod +x deploy.sh
chmod +x update_index.sh

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

./create_dynamodb.sh

./create_saved_books_lambda.1.sh

./create_search_books_lambda.sh

./create_shelved_books_lambda.sh

python3 create_books_api.py

./deploy.sh

./update_index.sh

