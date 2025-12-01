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
    
    # Basic validation
    if not action or not username:
        return create_response(400, {'error': 'Missing required fields'})
    
    if action == 'get_progress':
        return get_campaign_progress(username)
    elif action == 'update_progress':
        level = body.get('level')
        score = body.get('score')
        if level is None:
            return create_response(400, {'error': 'Missing level'})
        return update_campaign_progress(username, level, score)
    else:
        return create_response(400, {'error': 'Invalid action'})

def get_campaign_progress(username):
    """Get the current campaign progress for a user"""
    try:
        response = table.get_item(Key={'username': username})
        
        if 'Item' not in response:
            return create_response(404, {'error': 'User not found'})
        
        user = response['Item']
        campaign_progress = int(user.get('campaign_progress', 0))
        
        return create_response(200, {
            'username': username,
            'campaign_progress': campaign_progress
        })
        
    except Exception as e:
        print(f"Error getting campaign progress: {str(e)}")
        return create_response(500, {'error': 'Internal server error'})

def update_campaign_progress(username, level, score=None):
    """Update the campaign progress for a user"""
    try:
        # First, get current progress to validate
        response = table.get_item(Key={'username': username})
        
        if 'Item' not in response:
            return create_response(404, {'error': 'User not found'})
        
        user = response['Item']
        current_progress = int(user.get('campaign_progress', 0))
        
        # Validate that the user is advancing to the next level
        # (prevent skipping ahead)
        new_level = int(level)
        if new_level > current_progress + 1:
            return create_response(400, {
                'error': 'Cannot skip levels',
                'current_progress': current_progress
            })
        
        # Update progress only if advancing
        if new_level > current_progress:
            table.update_item(
                Key={'username': username},
                UpdateExpression='SET campaign_progress = :level, last_updated = :timestamp',
                ExpressionAttributeValues={
                    ':level': new_level,
                    ':timestamp': int(time.time())
                }
            )
            
            return create_response(200, {
                'message': 'Campaign progress updated',
                'username': username,
                'campaign_progress': new_level,
                'score': score
            })
        else:
            return create_response(200, {
                'message': 'Progress unchanged',
                'username': username,
                'campaign_progress': current_progress
            })
        
    except Exception as e:
        print(f"Error updating campaign progress: {str(e)}")
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
