if aws lambda delete-function --function-name snsLambda >/dev/null 2>&1 ; then
    echo "DONE"
else
    echo "Function does not exist"
fi