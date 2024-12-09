#!/bin/bash

# Take down portions of the system that change
./deletion_scripts/delete_api.sh

./deletion_scripts/delete_savedBooks_Lambda.sh

./deletion_scripts/delete_shelvedBooks_Lambda.sh

./deletion_scripts/delete_searchBooks_Lambda.sh


# Bring up updated portions of the system
./creation_scripts/create_saved_books_lambda.sh

./creation_scripts/create_search_books_lambda.sh

./creation_scripts/create_shelved_books_lambda.sh

python3 create_books_api.py

./deploy.sh

./update_index.sh