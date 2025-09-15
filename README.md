# ChessGPT - AI Game Analyst

A chess game analysis application using OpenAI's API and prompt engineering to provide comprehensive analysis of chess games in PGN format.

## Features

- **PGN Game Analysis**: Upload chess games in PGN format for detailed AI analysis
- **Comprehensive Feedback**: Get analysis covering openings, critical moments, strategy, and learning points
- **Flexible Input**: Paste PGN text directly or provide file paths
- **General Chess Q&A**: Ask chess questions for additional guidance

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file in the root directory with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run the application**:
   ```bash
   python src/main.py
   ```

## Usage

The application provides an interactive menu where you can:

### 1. Analyze a Chess Game (PGN)
Choose between two input methods:
- **Direct PGN input**: Paste your PGN text directly into the terminal
- **File upload**: Provide the path to a `.pgn` file on your system

The AI will provide comprehensive analysis including:
- Opening assessment and improvements
- Critical moments and tactical opportunities
- Strategic themes and plans
- Move quality evaluation
- Endgame assessment
- Overall game rating
- Key learning points

### 2. Ask General Chess Questions
Get advice on chess concepts, strategies, and general questions

### 3. Exit the application

## PGN Format

PGN (Portable Game Notation) is the standard format for recording chess games. Example:

```
[Event "Casual Game"]
[Site "Berlin GER"]
[Date "1852.??.??"]
[Result "1-0"]
[White "Adolf Anderssen"]
[Black "Jean Dufresne"]
[ECO "C52"]

1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.b4 Bxb4 5.c3 Ba5 6.d4 exd4 7.O-O d3 8.Qb3 Qf6 9.e5 Qg6 10.Re1 Nge7 11.Ba3 b5 12.Qxb5 Rb8 13.Qa4 Bb6 14.Nbd2 Bb7 15.Ne4 Qf5 16.Bxd3 Qh5 17.Nf6+ gxf6 18.exf6 Rg8 19.Rad1 Qxf3 20.Rxe7+ Nxe7 21.Qxd7+ Kxd7 22.Bf5+ Ke8 23.Bd7+ Kf8 24.Bxe7# 1-0
```

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection for API calls

## Architecture

This application uses a clean, focused architecture:
- **`ai.py`**: Core AI functions with specialized PGN game analysis
- **`main.py`**: Interactive interface for game uploads and analysis
- **Standardized Prompt**: Consistent, comprehensive game analysis using carefully crafted system prompts

The system prompt ensures the AI provides structured, educational analysis that helps players improve their understanding of chess games.
