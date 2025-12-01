import json
import boto3
import time
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'ArcadeUsers'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    # Parse the body
    if 'body' in event and isinstance(event['body'], str):
        body = json.loads(event['body'])
    else:
        body = event
    
    action = body.get('action')
    username = body.get('username')
    password = body.get('password')
    
    # Basic validation
    if not action or not username or not password:
        return create_response(400, {'error': 'Missing required fields'})
    
    if action == 'register':
        return register_user(username, password)
    elif action == 'login':
        return login_user(username, password)
    else:
        return create_response(400, {'error': 'Invalid action'})

def register_user(username, password):
    try:
        # Check if user already exists
        response = table.get_item(Key={'username': username})
        if 'Item' in response:
            return create_response(409, {'error': 'Username already exists'})
        
        # Create new user
        # In a production app, password should be hashed!
        timestamp = int(time.time())
        table.put_item(
            Item={
                'username': username,
                'password': password, # Storing plaintext for this simple demo
                'created_at': timestamp,
                'last_login': timestamp,
                'campaign_progress': 0 # Level 0
            }
        )
        
        return create_response(200, {
            'message': 'User registered successfully',
            'username': username
        })
        
    except Exception as e:
        print(f"Error registering user: {str(e)}")
        return create_response(500, {'error': 'Internal server error'})

def login_user(username, password):
    try:
        response = table.get_item(Key={'username': username})
        
        if 'Item' not in response:
            return create_response(401, {'error': 'Invalid username or password'})
        
        user = response['Item']
        
        # Verify password (plaintext comparison for demo)
        if user.get('password') != password:
            return create_response(401, {'error': 'Invalid username or password'})
        
        # Update last login
        table.update_item(
            Key={'username': username},
            UpdateExpression='SET last_login = :val',
            ExpressionAttributeValues={':val': int(time.time())}
        )
        
        return create_response(200, {
            'message': 'Login successful',
            'username': username,
            'campaign_progress': int(user.get('campaign_progress', 0))
        })
        
    except Exception as e:
        print(f"Error logging in: {str(e)}")
        return create_response(500, {'error': 'Internal server error'})

def create_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        },
        'body': json.dumps(body)
    }
