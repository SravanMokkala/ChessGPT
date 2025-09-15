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
            'method': 'GET'
        }
        
        self.wfile.write(json.dumps(response_data).encode())
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response_data = {
            'message': 'ChessGPT API is working!',
            'api_key_configured': bool(os.environ.get("OPENAI_API_KEY")),
            'method': 'POST'
        }
        
        self.wfile.write(json.dumps(response_data).encode())