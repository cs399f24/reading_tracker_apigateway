#!/bin/bash


aws dynamodb create-table --table-name bookshelf \
    --attribute-definitions AttributeName=BookID,AttributeType=S \
    --key-schema AttributeName=BookID,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
