# reading_tracker_apigateway
<img width="1440" alt="Screenshot 2024-12-10 at 9 55 27 AM" src="https://github.com/user-attachments/assets/bf34eca5-fa9d-4611-9adc-93c289c0af78">

## Overview

This project implements a web application that allows users to search for books using the Google Books API, with the API key securely stored in AWS Secrets Manager. Saved books are stored in a DynamoDB table for efficient data management. The application features a frontend hosted through AWS Amplify, with HTML files stored in an S3 bucket, and a backend built using AWS Cloud9, Lambda functions, API Gateway, SNS, and DynamoDB.

The goal of the project is to create a Reading Tracker application using an AWS-based architecture. Users can sign in, search for books they have read, save their selections, and view a visual representation of their previously logged books. Additionally, users receive daily SNS notifications reminding them to update their reading activity, promoting consistent engagement.

### **Disclaimer**
- SNS may not function correctly due to possible last minute AWS updates to the service

## Project Setup and Configurations

### Cloud9 and Clone Repository
1. Open up AWS management console and head to cloud9
2. Create a cloud9 work space:
  -  In the creation screen simply click 'secure shell(SSH)' under the Network Settings heading
  -  Then click 'create'
3. Enter the cloud9 workspace after it is created
4. Clone the repository:
  -  Open a terminal window and enter the command:
```
git clone <repository URL>
```
  -  Then navigate to the repository:
```
cd reading_tracker_apigateway
```

### S3 Bucket Creation and Configuration

1. Navigate to s3 and create a bucket for the application:

  * **Name**:  Remember, names must be *globally unique*.  I recommend a name like `reading-tracker-<last name>`. 

2. After the buckets creation cp the html files into the bucket for later use:
```
aws s3 cp index.html s3://<Enter s3 bucket name>
```
```
aws s3 cp callback.html s3://<Enter s3 bucket name>
```
```
aws s3 cp sign_out.html s3://<Enter s3 bucket name>
```
3. - After the creation of the s3 bucket head to the last line in the update_index.sh file and enter your bucket name:
```
aws s3 cp index.html s3://<Enter s3 bucket name>
```
  


### Google Books
- To use application the google books api is required visit this link to see how to set it up:
```
https://rachelaemmer.medium.com/how-to-use-the-google-books-api-in-your-application-17a0ed7fa857
```

### Create a Secret in Secrets Manager:

Go to the AWS Secrets Manager Console:
- Open the AWS Secrets Manager Console.
Store the Secret:
- Click on Store a new secret.
- Name the secret: 
```
reading_test_key
```
- Choose Other type of secret.
- In the Key/value pairs section, add your secret.
```
Key: googlebooks Value: <YOUR_GOOGLE_BOOKS_API_KEY>
```
- Click Next and give the secret a name. For example: reading_test_key.
- Optionally, set a description or other settings.
- Click Next to configure permissions.
- Review and click Store to save the secret.

### Utilize Amplify using management console
- Navigate to the Amplify:
1. click "create new app"
2. Then select:
   - deploy without Git
   - click "next"
3. Enter your app name and branch name
4. Select s3 for method
   - browse the buckets and select the bucket you created for this project
5. Finally click "Save and Deploy"

**Note any changes made to the files located in the bucket need to be updated in amplify by clicking on the "deploy updates" button after you select your application name**

### **Create a Cognito User Pool**
1. Go into the create_cognito.py and fill out any info surrounded by <> examples are provided that can be used except the domain name which has to be UNIQUE
   - **NOTE** Be very careful to fill out all info needed:
   - If error occurs deletion of the UserPool has to be done through the management console
   - Make sure to use YOUR Amplify URL that you made and add on the /callback.html and /logout.html endpoints for the callback and logout sections

### Script Permissions
- If any script files give permission denied run:
```
chmod +x <name of script file>
```

## Developer Setup

### Launch entire project with one command (Can only be done after Amplify and Cognito info is filled out):
```
./launch_project.sh
```

## Updating the System
If any updates are made to the apigateway,index.html or lambda functions use:
```
./update_system.sh
```
This will update the index.html in the s3 bucket and delete and redeploy the apigateway and lambda functions to AWS

## Tear Down

To issue a complete tear down of the system:

```
./tear_down.sh
```
