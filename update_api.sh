#!/bin/bash

./deletion_scripts/delete_api.sh

python create_books_api.py

./deploy.sh

./update_index.sh