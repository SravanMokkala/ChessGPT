import os
import json

def handler(request):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>ChessGPT - WORKING!</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
                .success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 20px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>♔ ChessGPT - SUCCESS! ♔</h1>
            <div class="success">
                <h3>✅ Vercel Function is Working!</h3>
                <p>Your serverless function is running successfully.</p>
                <p><strong>API Key Status:</strong> ''' + ('CONFIGURED ✅' if os.environ.get("OPENAI_API_KEY") else 'MISSING ❌') + '''</p>
            </div>
        </body>
        </html>
        '''
    }
