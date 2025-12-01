# import the JSON utility package
import json
# import the Python math library
import math

# import the AWS SDK (for Python the package name is boto3)
import boto3
# import two packages to help us with dates and date formatting
from time import gmtime, strftime

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
table = dynamodb.Table('PowerOfMathDatabase')
# store the current time in a human readable format in a variable
now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

# define the handler function that the Lambda service will use an entry point
def lambda_handler(event, context):
    
    # extract the operation type and two numbers from the event object
    operation = event.get('operation', 'power')  # default to power for backwards compatibility
    num1 = float(event['num1'])
    num2 = float(event['num2'])
    
    # perform the requested operation
    if operation == 'add':
        mathResult = num1 + num2
    elif operation == 'subtract':
        mathResult = num1 - num2
    elif operation == 'multiply':
        mathResult = num1 * num2
    elif operation == 'divide':
        if num2 == 0:
            return {
                'statusCode': 400,
                'body': json.dumps('Error: Cannot divide by zero')
            }
        mathResult = num1 / num2
    elif operation == 'power':
        mathResult = math.pow(num1, num2)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Invalid operation')
        }
    
    # write result and time to the DynamoDB table using the object we instantiated and save response in a variable
    response = table.put_item(
        Item={
            'ID': str(mathResult),
            'LatestGreetingTime': now
        })
    
    # return a properly formatted JSON object
    return {
        'statusCode': 200,
        'body': json.dumps('Your result is ' + str(mathResult))
    }