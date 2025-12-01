import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

# DynamoDB resource
dynamodb = boto3.resource('dynamodb')
# Main table for Pong scores
table = dynamodb.Table('PongScores')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    try:
        body = event.get('body')
        if isinstance(body, str):
            body = json.loads(body)
        elif not body:
            body = event
        
        action = body.get('action')
        if action == 'start_game':
            return start_game()
        elif action == 'save_score':
            return save_score(body)
        elif action == 'get_recent_games':
            return get_recent_games()
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid action'})
            }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def start_game():
    """Create a new game record with initial scores 0 and return its ID."""
    game_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    item = {
        'game_id': game_id,
        'created_at': now,
        'updated_at': now,
        'player_score': 0,
        'ai_score': 0,
        'result': 'IN_PROGRESS'
    }
    try:
        table.put_item(Item=item)
    except Exception as e:
        print(f"Error creating game record: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Failed to create game: {str(e)}'})
        }
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps({
            'message': 'Game started',
            'game_id': game_id,
            'backend_version': 'v6.0'
        })
    }

def save_score(data):
    player_score = data.get('player_score')
    ai_score = data.get('ai_score')
    result = data.get('result')  # "WIN", "LOSS", or "IN_PROGRESS"
    game_id = data.get('game_id')
    
    if None in (player_score, ai_score, game_id):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing required data (scores or game_id)'})
        }
    
    now = datetime.utcnow().isoformat()
    try:
        table.update_item(
            Key={'game_id': game_id},
            UpdateExpression="set player_score=:p, ai_score=:a, #r=:r, updated_at=:u",
            ExpressionAttributeNames={'#r': 'result'},
            ExpressionAttributeValues={
                ':p': int(player_score),
                ':a': int(ai_score),
                ':r': result,
                ':u': now
            }
        )
    except Exception as e:
        print(f"Error updating score: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Failed to update score: {str(e)}'})
        }
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps({
            'message': 'Score updated',
            'game_id': game_id,
            'player_score': int(player_score),
            'ai_score': int(ai_score),
            'backend_version': 'v5.0'
        })
    }

def get_recent_games():
    # Scan the table for recent games (limit 10)
    response = table.scan(Limit=10)
    items = response.get('Items', [])
    for item in items:
        for key, value in item.items():
            if isinstance(value, Decimal):
                item[key] = int(value)
    items.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps({'games': items})
    }
