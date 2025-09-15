import os
import json

def handler(request):
    try:
        # Ultra-simple test - no external dependencies
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
                    <p><strong>Time:</strong> ''' + str(__import__('datetime').datetime.now()) + '''</p>
                </div>
                <h3>Next Steps:</h3>
                <p>1. Add OpenAI API key to Vercel environment variables</p>
                <p>2. Test the chess analysis functionality</p>
            </body>
            </html>
            '''
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

# Keep the original main function for local use
def main():
    print("♔ ChessGPT")
    print("=" * 20)
    print("This is the local CLI version.")
    print("For web deployment, the handler() function is used.")

if __name__ == "__main__":
    main()