# reading_tracker_apigateway

## Overview

This project implements a web application where users can search for books using the Google Books API and store selected books in a DynamoDB table. The application serves a frontend hosted in an S3 bucket, with a backend implemented using Cloud9, AWS Lambda functions, API Gateway, and DynamoDB for data storage. The architecture is serverless, with Lambda functions handling book search, saving, and shelving operations.

## NOTE

Creation of s3 Bucket and the Dynamodb table and modification of some of the scripts are needed so that they work with and individuals respective s3 Buckets and Dynamodb tables.



## Developer Setup

### Step 1: Clone the Repository

Clone the repository into Cloud9

### Step 2: Create a Virtual Environment

Create a virtual environment to isolate dependencies.

```
python3 -m venv .venv
```
### Step 3: Activate the Virtual Environment
Activate the virtual environment.

```
source .venv/bin/activate
```

### Step 4: Install the Required Dependencies
Install the required dependencies from the requirements.txt file.

```
pip install -r requirements.txt
```
## Deploy

### Step 1: Create Lambda Functions
You need to create several Lambda functions for handling different aspects of the bookshelf application:

Create the Lambda function for saving books.

```
./create_saved_books_lambda.1.sh
```

Create the Lambda function for searching books.

```
./create_search_books_lambda.sh
```

Create the Lambda function for shelving books.

```
./create_shelved_books_lambda.sh
```

### Step 2: Create the API Gateway
Once the Lambda functions are set up, create the API Gateway and configure the backend API.

```
python create_books_api.py
```

### Step 3: Deploy the API
Deploy the API to make it accessible.


```
./deploy.sh
```

### Step 4: Update the index.html in the S3 Bucket
After deployment, update the index.html file in the S3 bucket to reflect the latest changes.

```
./update_index.sh
```

## Testing

### Step 1: Test the Lambda Functions
Once the API and Lambda functions are set up, you can test them using the provided test script.

```
./test.sh
```

### Step 2: Test the Preflight OPTIONS Request for CORS
To verify that CORS is correctly configured, test the OPTIONS request.

```
./test_options.sh
```

## Tear Down

### Step 1: Delete the API Gateway
If you need to tear down the setup, start by deleting the API Gateway.

```
./delete_api.sh
```
