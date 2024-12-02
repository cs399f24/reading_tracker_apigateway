#!/bin/bash
chmod +x delete_api.sh
chmod +x delete_dynamodb.sh
chmod +x Delete_SavedBooks_Lambda.sh
chmod +x Delete_ShelvedBooks_Lambda.sh
chmod +x Delete_SearchBooks_Lambda.sh


./delete_api.sh

./delete_dynamodb.sh

./Delete_SavedBooks_Lambda.sh

./Delete_ShelvedBooks_Lambda.sh

./Delete_SearchBooks_Lambda.sh