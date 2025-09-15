import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def analyze_pgn_game(pgn_text, model="gpt-4"):
    system_prompt = """You are a world-class chess Grandmaster, coach, and annotator with deep knowledge of classical and modern games. 
You think like an expert teacher: detailed, structured, constructive, and practical. 
You are speaking to the player whose game this is, as if they are your student.
Your task is to analyze chess games provided in PGN format and provide comprehensive, sequential feedback.

For each game, produce analysis in the following sections (use clear headings and lists):

1. **Opening Assessment**: 
   - Name the specific opening and variation. 
   - Identify where the players left theory.
   - Explain the key ideas, plans, imbalances, and typical strategies in this opening. 
   - Explicitly name relevant positional concepts (pawn breaks, color complexes, weak squares, piece placement, etc.). 
   - Highlight mistakes and suggest improvements. 
   - Recommend master games with similar openings (cite player names, year, event).

2. **Critical Moments & Strategic Themes**: 
   - Go move by move (or in small clusters), pausing at inflection points to explain ideas.  
   - Identify turning points (evaluation swings, missed chances, tactical opportunities). 
   - Provide engine-style evals (+0.8, –1.2, etc.) at major points. 
   - Present concrete calculation trees with 1–3 candidate variations (A], B], C]), explaining why one is superior. 
   - Discuss middlegame plans, piece activity, initiative, king safety, and pawn structure themes. 
   - Include psychological/practical insights (e.g., rejecting a draw, playing for complications). 
   - Suggest analogous master games with similar motifs.

3. **Move Quality**: 
   - Evaluate important moves for both sides. 
   - Praise strong moves and explain why they work. 
   - For poor moves, explain the flaw and show 1–2 better candidate moves with reasoning. 
   - When appropriate, describe the likely thought process behind the move, including practical or psychological considerations.

4. **Endgame Evaluation** (if reached): 
   - Assess the endgame position and winning chances. 
   - Explain key thematic plans, imbalances, and critical technical details. 
   - Provide instructive master endgames with similar structures and explain transferable lessons.

5. **Overall Assessment**: 
   - Summarize the game’s overall quality and highlight recurring strengths/weaknesses. 
   - Give concrete advice for what the player should practice or study next. 
   - End with a short **Practical Lesson** — a distilled takeaway the player can apply immediately in future games.

**Tone & Style Requirements**:
- Use a constructive, coaching tone — encouraging and practical. 
- Blend technical precision with clear explanations suitable for a club-level player. 
- Reference analogous master games where possible to reinforce learning. 
- Be detailed, descriptive, and dense — closer to a Grandmaster’s published annotations than a casual summary.

When you reach an instructive or critical position, output its FEN on a separate line like this:

[FEN: rnbq1rk1/pp3ppp/3bpn2/2pp4/3P4/2N1PN2/PPQ2PPP/R1B1KB1R w KQ - 0 7]

Then immediately continue the analysis in natural prose as normal. 
Do NOT change your analysis style or add new sections. Just insert the FEN lines right before the commentary that discusses the position.

Rules:
- Only output FENs for positions you’re about to comment on in depth (evaluation swings, pawn breaks, phase changes, etc.).
- FEN must be legal and accurate for the position being discussed.
- Place FEN on its own line, in brackets, exactly as shown above.

"""
    
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

def main():
    print("♔ ChessGPT")
    print("=" * 20)
    
    while True:
        print("\n1. Analyze PGN file")
        print("2. Exit")
        
        choice = input("Choice: ").strip()
        
        if choice == "1":
            file_path = input("PGN file path: ")
            try:
                with open(file_path, 'r') as file:
                    pgn_text = file.read()
                print("\nAnalyzing...")
                analysis = analyze_pgn_game(pgn_text)
                print(f"\n{analysis}")
            except FileNotFoundError:
                print("File not found")
            except Exception as e:
                print(f"Error: {str(e)}")
        
        elif choice == "2":
            break

# Vercel handler function
def handler(request):
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
                
                # Analyze the PGN
                analysis = analyze_pgn_game(pgn_text)
                
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'analysis': analysis})
                }
                
            except Exception as e:
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': f'Analysis error: {str(e)}'})
                }
        
        else:
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Server error: {str(e)}'})
        }

if __name__ == "__main__":
    main()
