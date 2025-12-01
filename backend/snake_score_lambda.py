# import the JSON utility package
import json
import time
# import the AWS SDK (for Python the package name is boto3)
import boto3
# import two packages to help us with dates and date formatting
from time import gmtime, strftime

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
table = dynamodb.Table('SnakeScores')

# define the handler function that the Lambda service will use as entry point
def lambda_handler(event, context):
    
    # Get action type from event
    action = event.get('action')
    
    if action == 'save_score':
        # Extract score data from the event object
        player_id = event.get('player_id', 'anonymous')
        score = event.get('score', 0)
        snake_length = event.get('snake_length', 0)
        
        # Create timestamp for sort key
        timestamp = int(time.time() * 1000)  # milliseconds
        # Get human-readable date
        game_date = strftime("%Y-%m-%d %H:%M:%S +0000", gmtime())
        
        # Write score to DynamoDB table
        response = table.put_item(
            Item={
                'player_id': player_id,
                'timestamp': timestamp,
                'score': score,
                'snake_length': snake_length,
                'game_date': game_date
            }
        )
        
        # Return success response
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'message': 'Score saved successfully!',
                'score': score,
                'timestamp': timestamp
            })
        }
    
    elif action == 'get_high_score':
        # Scan table to get highest score
        # Note: For production, use a GSI with score as sort key for better performance
        try:
            response = table.scan()
            items = response.get('Items', [])
            
            if not items:
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'high_score': 0
                    })
                }
            
            # Find the highest score - convert Decimal to int for comparison
            high_score_item = max(items, key=lambda x: int(x.get('score', 0)))
            high_score_value = int(high_score_item.get('score', 0))
            
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'high_score': high_score_value,
                    'player_id': high_score_item.get('player_id', 'unknown'),
                    'game_date': high_score_item.get('game_date', '')
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': str(e),
                    'high_score': 0
                })
            }
    
    else:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps('Invalid action. Use "save_score" or "get_high_score"')
        }
