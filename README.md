# Conversational Chess Game 

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
