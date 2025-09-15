import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def analyze_pgn_game(pgn_text, model="gpt-4"):
    system_prompt = """You are an expert chess analyst and Grandmaster. Your task is to analyze 
    chess games provided in PGN format and provide comprehensive feedback. For each game analysis, 
    you should include:
    
    1. **Opening Assessment**: Evaluate the opening choices and identify any mistakes or improvements
    2. **Critical Moments**: Point out key turning points, tactical opportunities, and missed chances
    3. **Strategic Themes**: Identify the main strategic ideas and plans for both sides
    4. **Move Quality**: Comment on the quality of moves, highlighting both good and poor choices
    5. **Endgame Evaluation**: Assess the endgame if reached, including winning chances
    6. **Overall Assessment**: Provide a rating of the game quality and specific areas for improvement
    7. **Learning Points**: Extract 2-3 key lessons that the player can apply to future games
    
    Be constructive and educational. Focus on practical insights that will help the player improve 
    their chess understanding and play."""
    
    user_message = f"""Please analyze this chess game in detail:

{pgn_text}

Provide a comprehensive analysis following the structure outlined in your instructions."""
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing game: {str(e)}"

from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            pgn_text = data.get('pgn', '')
            
            if not pgn_text:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No PGN text provided'}).encode())
                return
            
            analysis = analyze_pgn_game(pgn_text)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'analysis': analysis}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>ChessGPT - AI Game Analyst</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                .container { background: #f5f5f5; padding: 30px; border-radius: 10px; }
                h1 { color: #333; text-align: center; }
                textarea { width: 100%; height: 200px; margin: 20px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
                button { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
                button:hover { background: #0056b3; }
                .result { margin-top: 20px; padding: 20px; background: white; border-radius: 5px; white-space: pre-wrap; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>♔ ChessGPT - AI Game Analyst ♔</h1>
                <p>Upload your chess game in PGN format for comprehensive AI analysis.</p>
                
                <textarea id="pgnInput" placeholder="Paste your PGN text here..."></textarea>
                <br>
                <button onclick="analyzeGame()">Analyze Game</button>
                
                <div id="result" class="result" style="display: none;"></div>
            </div>
            
            <script>
                async function analyzeGame() {
                    const pgnText = document.getElementById('pgnInput').value;
                    const resultDiv = document.getElementById('result');
                    
                    if (!pgnText.trim()) {
                        alert('Please enter PGN text');
                        return;
                    }
                    
                    resultDiv.style.display = 'block';
                    resultDiv.textContent = 'Analyzing your game...';
                    
                    try {
                        const response = await fetch('/api', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ pgn: pgnText })
                        });
                        
                        const data = await response.json();
                        
                        if (response.ok) {
                            resultDiv.textContent = data.analysis;
                        } else {
                            resultDiv.textContent = 'Error: ' + data.error;
                        }
                    } catch (error) {
                        resultDiv.textContent = 'Error: ' + error.message;
                    }
                }
            </script>
        </body>
        </html>
        '''.encode())
