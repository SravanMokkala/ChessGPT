import os
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response_data = {
            'message': 'ChessGPT API is working!',
            'api_key_configured': bool(os.environ.get("OPENAI_API_KEY")),
            'method': 'GET',
            'status': 'ready_for_chess_analysis'
        }
        
        self.wfile.write(json.dumps(response_data).encode())
    
    def do_POST(self):
        try:
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            pgn_text = data.get('pgn', '')
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            if not pgn_text:
                response_data = {'error': 'No PGN text provided'}
            elif not os.environ.get("OPENAI_API_KEY"):
                response_data = {'error': 'OpenAI API key not configured'}
            else:
                # For now, return a mock analysis to test the flow
                response_data = {
                    'analysis': f'''**Chess Game Analysis**

**Opening Assessment**: This appears to be a {len(pgn_text.split())} move game. The opening shows typical development patterns.

**Critical Moments**: Several key positions were reached where tactical opportunities may have been present.

**Strategic Themes**: The game demonstrates standard chess principles of piece development, center control, and king safety.

**Move Quality**: The moves show reasonable understanding of chess fundamentals.

**Overall Assessment**: This is a solid game that demonstrates good chess understanding.

**Learning Points**: 
1. Focus on piece development in the opening
2. Look for tactical opportunities in the middlegame
3. Practice endgame technique

*Note: This is a test analysis. Full AI analysis will be enabled once the backend is stable.*''',
                    'status': 'test_mode'
                }
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': f'Server error: {str(e)}'}).encode())