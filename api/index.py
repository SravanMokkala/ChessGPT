import os
import json
from openai import OpenAI
from http.server import BaseHTTPRequestHandler

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
            
            # Check if API key is available
            if not os.environ.get("OPENAI_API_KEY"):
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'OpenAI API key not configured'}).encode())
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
                body { 
                    font-family: Arial, sans-serif; 
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 20px; 
                    background: #f8f9fa;
                }
                .container { 
                    background: white; 
                    padding: 30px; 
                    border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 { 
                    color: #333; 
                    text-align: center; 
                    margin-bottom: 10px;
                }
                .subtitle {
                    text-align: center;
                    color: #666;
                    margin-bottom: 30px;
                }
                textarea { 
                    width: 100%; 
                    height: 200px; 
                    margin: 20px 0; 
                    padding: 15px; 
                    border: 2px solid #ddd; 
                    border-radius: 8px; 
                    font-family: monospace;
                    font-size: 14px;
                    resize: vertical;
                }
                button { 
                    background: #007bff; 
                    color: white; 
                    padding: 15px 30px; 
                    border: none; 
                    border-radius: 8px; 
                    cursor: pointer; 
                    font-size: 16px; 
                    width: 100%;
                    transition: background 0.3s;
                }
                button:hover { 
                    background: #0056b3; 
                }
                button:disabled {
                    background: #6c757d;
                    cursor: not-allowed;
                }
                .result { 
                    margin-top: 20px; 
                    padding: 20px; 
                    background: #f8f9fa; 
                    border-radius: 8px; 
                    white-space: pre-wrap; 
                    border-left: 4px solid #007bff;
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                }
                .loading {
                    text-align: center;
                    color: #007bff;
                    font-style: italic;
                }
                .error {
                    border-left-color: #dc3545;
                    background: #f8d7da;
                    color: #721c24;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>♔ ChessGPT - AI Game Analyst ♔</h1>
                <p class="subtitle">Upload your chess game in PGN format for comprehensive AI analysis</p>
                
                <textarea id="pgnInput" placeholder="Paste your PGN text here...

Example:
[Event &quot;Casual Game&quot;]
[Site &quot;Chess.com&quot;]
[Date &quot;2024.01.01&quot;]
[Result &quot;1-0&quot;]

1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.b4 Bxb4 5.c3 Ba5 6.d4 exd4 7.O-O d3 8.Qb3 Qf6 9.e5 Qg6 10.Re1 Nge7 11.Ba3 b5 12.Qxb5 Rb8 13.Qa4 Bb6 14.Nbd2 Bb7 15.Ne4 Qf5 16.Bxd3 Qh5 17.Nf6+ gxf6 18.exf6 Rg8 19.Rad1 Qxf3 20.Rxe7+ Nxe7 21.Qxd7+ Kxd7 22.Bf5+ Ke8 23.Bd7+ Kf8 24.Bxe7# 1-0"></textarea>
                
                <button id="analyzeBtn" onclick="analyzeGame()">Analyze Game</button>
                
                <div id="result" class="result" style="display: none;"></div>
            </div>
            
            <script>
                async function analyzeGame() {
                    const pgnText = document.getElementById('pgnInput').value;
                    const resultDiv = document.getElementById('result');
                    const analyzeBtn = document.getElementById('analyzeBtn');
                    
                    if (!pgnText.trim()) {
                        alert('Please enter PGN text');
                        return;
                    }
                    
                    // Show loading state
                    resultDiv.style.display = 'block';
                    resultDiv.className = 'result loading';
                    resultDiv.textContent = 'Analyzing your game... This may take a few moments.';
                    analyzeBtn.disabled = true;
                    analyzeBtn.textContent = 'Analyzing...';
                    
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
                            resultDiv.className = 'result';
                            resultDiv.textContent = data.analysis;
                        } else {
                            resultDiv.className = 'result error';
                            resultDiv.textContent = 'Error: ' + data.error;
                        }
                    } catch (error) {
                        resultDiv.className = 'result error';
                        resultDiv.textContent = 'Error: ' + error.message;
                    } finally {
                        analyzeBtn.disabled = false;
                        analyzeBtn.textContent = 'Analyze Game';
                    }
                }
            </script>
        </body>
        </html>
        '''.encode())