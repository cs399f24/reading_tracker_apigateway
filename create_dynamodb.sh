#!/bin/bash


aws dynamodb create-table --table-name bookshelf \
    --attribute-definitions AttributeName=UserID,AttributeType=S AttributeName=BookID,AttributeType=S \
    --key-schema AttributeName=UserID,KeyType=HASH AttributeName=BookID,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5