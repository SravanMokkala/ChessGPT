import os
import json

def handler(request):
    try:
        # Ultra-simple test - no external dependencies
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': 'ChessGPT API is working!',
                'api_key_configured': bool(os.environ.get("OPENAI_API_KEY")),
                'method': request.method if hasattr(request, 'method') else 'unknown'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }