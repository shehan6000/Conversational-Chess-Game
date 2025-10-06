# Conversational Chess Game - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [API Reference](#api-reference)
7. [Development Guide](#development-guide)
8. [Troubleshooting](#troubleshooting)
9. [Contributing](#contributing)

## Overview

The Conversational Chess Game is an AI-powered chess application where two AI agents play chess against each other while engaging in natural conversation. The game combines chess logic with large language model capabilities to create an entertaining and interactive experience.

### Key Features

- **AI vs AI Chess**: Two LLM-powered agents play chess against each other
- **Conversational Interface**: Agents engage in friendly banter during gameplay
- **Visual Board**: Real-time SVG board visualization with move highlights
- **Production Ready**: Comprehensive error handling, logging, and configuration
- **Extensible Architecture**: Modular design for easy customization

## Architecture

### System Architecture Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Main Game     │◄──►│  Chess Agents    │◄──►│  Board Manager  │
│   Controller    │    │   (White/Black)  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Configuration  │    │   AutoGen Framework  │    │  Chess Engine  │
│     Manager     │    │                    │    │   (python-chess)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Core Components

1. **ChessGame**: Main game controller orchestrating the entire gameplay
2. **ChessGameAgents**: Manages the AI player agents (White and Black)
3. **ChessBoardManager**: Handles chess board state and move validation
4. **Config**: Configuration management for LLM settings and game parameters

### Data Flow

1. Game initialization loads configuration and creates agents
2. White agent requests legal moves from board manager
3. White agent selects and executes a move
4. Agents engage in conversational banter
5. Black agent repeats the process
6. Game continues until checkmate, stalemate, or turn limit

## Installation

### Prerequisites

- Python 3.8 or higher
- LLM API key (OpenAI GPT-4 recommended)

### Step-by-Step Installation

1. **Clone or create the project structure**:
```bash
mkdir chess_game
cd chess_game
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
export LLM_API_KEY="your-api-key-here"
export LLM_MODEL="gpt-4-turbo"
export GAME_MAX_TURNS=50
```

### Requirements File

```txt
# requirements.txt
autogen>=0.2.0
python-chess>=1.0.0
PyYAML>=6.0
typing-extensions>=4.0.0
```

## Configuration

### Configuration Methods

The application supports multiple configuration methods:

1. **Environment Variables** (Highest priority)
2. **YAML Configuration File**
3. **Command Line Arguments**
4. **Default Values**

### Environment Variables

```bash
# LLM Configuration
export LLM_API_KEY="sk-..."                    # Required
export LLM_MODEL="gpt-4-turbo"                 # Optional
export LLM_TEMPERATURE="0.7"                   # Optional
export LLM_MAX_TOKENS="1000"                   # Optional

# Game Configuration
export GAME_MAX_TURNS="50"                     # Optional
export GAME_MAX_NESTED_TURNS="5"               # Optional
```

### Configuration File

Create `config.yaml`:

```yaml
# config.yaml
llm:
  model: "gpt-4-turbo"
  api_key: "your-api-key"  # Can be omitted if using env var
  temperature: 0.7
  max_tokens: 1000

game:
  max_turns: 50
  max_nested_turns: 5
  board_size: 200
```

### Configuration Precedence

1. Command line arguments
2. Environment variables
3. Configuration file
4. Default values

## Usage

### Basic Usage

```bash
# Using environment variables
python main.py

# Using configuration file
python main.py --config config.yaml

# Custom game length
python main.py --turns 20 --model gpt-4-turbo

# Specify API key directly
python main.py --api-key "sk-..." --turns 30
```

### Command Line Options

```bash
python main.py --help
```

```
usage: main.py [-h] [--config CONFIG] [--turns TURNS] [--model MODEL] [--api-key API_KEY]

Conversational Chess Game

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Path to config file
  --turns TURNS, -t TURNS
                        Maximum number of turns
  --model MODEL, -m MODEL
                        LLM model to use
  --api-key API_KEY, -k API_KEY
                        LLM API key
```

### Programmatic Usage

```python
from src.chess_game import ChessGame
from src.config import Config

# Custom configuration
config = Config()
config.llm_config.model = "gpt-4"
config.game_config.max_turns = 25

# Start game
game = ChessGame(config)
result = game.start_game()

if result["success"]:
    print("Game completed successfully!")
    print(f"Final FEN: {result['final_state']['fen']}")
```

### Example Game Output

```
Starting Conversational Chess Game...
Using model: gpt-4-turbo
Maximum turns: 50
--------------------------------------------------
Player_Black: Let's play an exciting game of chess! I'll be playing black. 
You have the white pieces and the first move. Good luck and have fun!

Player_White: get_legal_moves() -> Possible moves: e2e4, d2d4, g1f3, ...
Player_White: make_move(e2e4) -> Moved Pawn (♙) from e2 to e4.
Player_White: A classic King's Pawn opening! The board is now open for some exciting middle game tactics. Your move!

Player_Black: get_legal_moves() -> Possible moves: e7e5, c7c5, ...
Player_Black: make_move(e7e5) -> Moved Pawn (♟) from e7 to e5.
Player_Black: Ah, the Open Game! This should lead to some interesting positions. Let the battle begin!

==================================================
GAME COMPLETED
==================================================
Checkmate! White wins!
Final position: r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 0 1
```

## API Reference

### ChessGame Class

Main game controller class.

```python
class ChessGame:
    def __init__(self, config: Optional[Config] = None)
    def start_game(self, max_turns: Optional[int] = None) -> Dict[str, Any]
    def get_current_state(self) -> Dict[str, Any]
    def is_game_over(self) -> bool
    def get_winner(self) -> Optional[str]
```

**Methods**:

- `start_game(max_turns)`: Starts a new game with optional turn limit
- `get_current_state()`: Returns current game state including FEN
- `is_game_over()`: Checks if game has ended
- `get_winner()`: Returns winner ("white", "black", "draw") or None

### ChessBoardManager Class

Manages chess board operations and state.

```python
class ChessBoardManager:
    def reset_board(self) -> None
    def get_legal_moves(self) -> str
    def make_move(self, move: str) -> MoveResult
    def get_game_state(self) -> Dict[str, Any]
    def check_made_move(self, msg: Any) -> bool
```

**Key Methods**:

- `make_move(move)`: Executes a move and returns MoveResult
- `get_legal_moves()`: Returns formatted string of legal moves
- `get_game_state()`: Comprehensive game state dictionary

### MoveResult Dataclass

```python
@dataclass
class MoveResult:
    success: bool
    message: str
    svg_data: Optional[str] = None
    is_check: bool = False
    is_checkmate: bool = False
    is_stalemate: bool = False
```

### Configuration Classes

```python
@dataclass
class LLMConfig:
    model: str
    api_key: str
    temperature: float
    max_tokens: int

@dataclass
class GameConfig:
    max_turns: int
    max_nested_turns: int
    board_size: int
```

## Development Guide

### Project Structure

```
chess_game/
├── src/
│   ├── __init__.py
│   ├── chess_game.py      # Main game controller
│   ├── agents.py          # Agent management
│   ├── board_manager.py   # Chess board operations
│   └── config.py          # Configuration management
├── tests/
│   ├── __init__.py
│   ├── test_chess_game.py
│   └── test_agents.py
├── requirements.txt
├── config.yaml           # Example configuration
└── main.py              # CLI entry point
```

### Adding New Features

#### 1. Custom Agent Personalities

```python
# In agents.py
def create_agent_with_personality(name: str, personality: str, color: str):
    system_message = f"""
    You are {name}, a chess player with {personality}.
    You are playing as {color}.
    {get_chess_instructions()}
    """
    
    return ConversableAgent(
        name=name,
        system_message=system_message,
        llm_config=llm_config
    )
```

#### 2. Custom Move Validators

```python
# In board_manager.py
def validate_move_strategy(self, move: str, strategy: str) -> bool:
    """Validate move against specific strategy."""
    if strategy == "aggressive":
        return self._is_aggressive_move(move)
    elif strategy == "defensive":
        return self._is_defensive_move(move)
    return True
```

#### 3. Game Analytics

```python
# Add to chess_game.py
def get_game_analytics(self) -> Dict[str, Any]:
    """Generate game analytics and statistics."""
    return {
        "moves_count": len(self.board_manager.board.move_stack),
        "captures": self._count_captures(),
        "check_count": self._count_checks(),
        "game_duration": time.time() - self.start_time,
        "opening": self._identify_opening()
    }
```

### Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

Or run specific tests:

```bash
python -m pytest tests/test_chess_game.py -v
python -m pytest tests/test_agents.py -v
```

### Logging

The application uses Python's built-in logging module. Logs are written to both console and `chess_game.log` file.

**Log Levels**:
- `DEBUG`: Detailed debug information
- `INFO`: Game progress and major events
- `WARNING`: Warning messages
- `ERROR`: Error messages

## Troubleshooting

### Common Issues

#### 1. API Key Errors

**Problem**: `Error: LLM API key is required`

**Solution**:
```bash
export LLM_API_KEY="your-actual-api-key"
# Or use command line:
python main.py --api-key "your-actual-api-key"
```

#### 2. Model Not Available

**Problem**: `Model gpt-4-turbo not found`

**Solution**:
- Check model name spelling
- Ensure your API key has access to the model
- Use a different model: `--model gpt-4`

#### 3. Illegal Moves

**Problem**: Agents attempting illegal moves

**Solution**:
- The system automatically validates moves
- Agents receive legal moves list before each turn
- Check agent system messages for proper instructions

#### 4. Game Hangs

**Problem**: Game stops responding

**Solution**:
- Check API rate limits
- Verify internet connection
- Reduce `max_nested_turns` in configuration
- Enable debug logging for more information

### Performance Optimization

1. **Reduce Token Usage**:
   - Set lower `max_tokens` in configuration
   - Use more concise system messages

2. **Improve Response Time**:
   - Use faster models (gpt-3.5-turbo)
   - Reduce `max_turns` for shorter games

3. **Memory Management**:
   - Games are stateless between sessions
   - Reset board manager for new games

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests: `python -m pytest tests/`
5. Ensure code quality: `flake8 src/ tests/`
6. Commit changes: `git commit -m 'Add amazing feature'`
7. Push to branch: `git push origin feature/amazing-feature`
8. Create Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all function signatures
- Write docstrings for all public methods
- Include unit tests for new features
- Update documentation for API changes

### Testing Guidelines

- Write tests for new functionality
- Maintain test coverage above 80%
- Include both unit and integration tests
- Test edge cases and error conditions


## Support

For support and questions:

1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with:
   - Error messages
   - Configuration details
   - Steps to reproduce
   - Log files (if applicable)

## Changelog

### Version 1.0.0
- Initial production release
- AI vs AI chess with conversation
- Comprehensive configuration system
- Production-ready error handling
- Complete test suite

---

