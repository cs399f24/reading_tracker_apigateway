#!/bin/bash

# Take down portions of the system that change
./delete_api.sh

./Delete_SavedBooks_Lambda.sh

./Delete_ShelvedBooks_Lambda.sh

./Delete_SearchBooks_Lambda.sh


# Bring up updated portions of the system
./create_saved_books_lambda_1.sh

./create_search_books_lambda.sh

./create_shelved_books_lambda.sh

python3 create_books_api.py

./deploy.sh

./update_index.sh