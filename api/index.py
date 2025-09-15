import os
import json

def handler(request):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'message': 'ChessGPT API is working!',
            'api_key_configured': bool(os.environ.get("OPENAI_API_KEY"))
        })
    }