import os
import json

def handler(request):
    # Simple test function to make sure Vercel works
    try:
        # Check if API key is available
        api_key = os.environ.get("OPENAI_API_KEY")
        
        if request.method == 'GET':
            # Return a simple test page
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html'},
                'body': f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>ChessGPT Test</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }}
                        .status {{ padding: 20px; margin: 20px 0; border-radius: 5px; }}
                        .success {{ background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }}
                        .error {{ background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }}
                        .info {{ background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }}
                    </style>
                </head>
                <body>
                    <h1>♔ ChessGPT - Test Page ♔</h1>
                    
                    <div class="info">
                        <h3>Function Status: WORKING ✅</h3>
                        <p>Your Vercel serverless function is running successfully!</p>
                    </div>
                    
                    <div class="{'success' if api_key else 'error'}">
                        <h3>API Key Status: {'CONFIGURED ✅' if api_key else 'MISSING ❌'}</h3>
                        <p>{'OpenAI API key is properly set up!' if api_key else 'Please add your OpenAI API key to Vercel environment variables.'}</p>
                    </div>
                    
                    <div class="info">
                        <h3>Next Steps:</h3>
                        <p>1. If API key is missing, add it to Vercel dashboard</p>
                        <p>2. Test the API endpoint: <code>POST /api</code> with PGN data</p>
                        <p>3. Build your frontend interface</p>
                    </div>
                    
                    <h3>Test API Endpoint:</h3>
                    <p>Send a POST request to this URL with JSON body:</p>
                    <pre>{{"pgn": "your_pgn_text_here"}}</pre>
                    
                    <p><strong>Current Time:</strong> {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </body>
                </html>
                '''
            }
        
        elif request.method == 'POST':
            # Test the API endpoint
            try:
                body = request.get('body', '{}')
                if isinstance(body, str):
                    data = json.loads(body)
                else:
                    data = body
                
                pgn_text = data.get('pgn', '')
                
                if not pgn_text:
                    return {
                        'statusCode': 400,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'error': 'No PGN text provided', 'status': 'test_mode'})
                    }
                
                if not api_key:
                    return {
                        'statusCode': 500,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'error': 'OpenAI API key not configured', 'status': 'test_mode'})
                    }
                
                # For now, just return a test response
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'message': 'API endpoint working!',
                        'pgn_received': len(pgn_text),
                        'api_key_configured': bool(api_key),
                        'status': 'test_mode',
                        'note': 'This is a test response. Add OpenAI integration next.'
                    })
                }
                
            except Exception as e:
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': f'API error: {str(e)}', 'status': 'test_mode'})
                }
        
        else:
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed', 'status': 'test_mode'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Server error: {str(e)}', 'status': 'test_mode'})
        }