import os
import json
from openai import OpenAI

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

def handler(request):
    try:
        if request.method == 'POST':
            # Handle POST request for PGN analysis
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
                        'body': json.dumps({'error': 'No PGN text provided'})
                    }
                
                # Check if API key is available
                if not os.environ.get("OPENAI_API_KEY"):
                    return {
                        'statusCode': 500,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'error': 'OpenAI API key not configured'})
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
        
        else:  # GET request - return simple status
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'ChessGPT API is working!',
                    'api_key_configured': bool(os.environ.get("OPENAI_API_KEY")),
                    'endpoint': 'POST /api/chess with {"pgn": "your_pgn_text"}'
                })
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Server error: {str(e)}'})
        }
