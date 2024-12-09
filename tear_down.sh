#!/bin/bash
chmod +x ./deletion_scripts/delete_api.sh
chmod +x ./deletion_scripts/delete_dynamodb.sh
chmod +x ./deletion_scripts/delete_savedBooks_Lambda.sh
chmod +x ./deletion_scripts/delete_shelvedBooks_Lambda.sh
chmod +x ./deletion_scripts/delete_searchBooks_Lambda.sh
chmod +x ./deletion_scripts/delete_sns_lambda.sh
chmod +x ./deletion_scripts/delete_cloudwatch_rule.sh
chmod +x ./deletion_scripts/delete_cognito.sh

./deletion_scripts/delete_cognito.sh

./deletion_scripts/delete_api.sh

./deletion_scripts/delete_dynamodb.sh

./deletion_scripts/delete_savedBooks_Lambda.sh

./deletion_scripts/delete_shelvedBooks_Lambda.sh

./deletion_scripts/delete_searchBooks_Lambda.sh

./deletion_scripts/delete_sns_lambda.sh

./deletion_scripts/delete_cloudwatch_rule.sh