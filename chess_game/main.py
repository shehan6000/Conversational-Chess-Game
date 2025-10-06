#!/usr/bin/env python3
"""
Main entry point for the Conversational Chess Game.
"""

import sys
import argparse
from src.chess_game import ChessGame
from src.config import Config


def main():
    parser = argparse.ArgumentParser(description="Conversational Chess Game")
    parser.add_argument("--config", "-c", type=str, help="Path to config file")
    parser.add_argument("--turns", "-t", type=int, default=50, help="Maximum number of turns")
    parser.add_argument("--model", "-m", type=str, help="LLM model to use")
    parser.add_argument("--api-key", "-k", type=str, help="LLM API key")
    
    args = parser.parse_args()
    
    try:
        # Initialize configuration
        config = Config(args.config)
        
        # Override with command line arguments
        if args.turns:
            config.game_config.max_turns = args.turns
        if args.model:
            config.llm_config.model = args.model
        if args.api_key:
            config.llm_config.api_key = args.api_key
        
        # Check for API key
        if not config.llm_config.api_key:
            print("Error: LLM API key is required. Set LLM_API_KEY environment variable or use --api-key")
            sys.exit(1)
        
        # Start the game
        print("Starting Conversational Chess Game...")
        print(f"Using model: {config.llm_config.model}")
        print(f"Maximum turns: {config.game_config.max_turns}")
        print("-" * 50)
        
        game = ChessGame(config)
        result = game.start_game(max_turns=args.turns)
        
        if result["success"]:
            final_state = result["final_state"]
            print("\n" + "=" * 50)
            print("GAME COMPLETED")
            print("=" * 50)
            
            if final_state["is_checkmate"]:
                winner = "Black" if final_state["turn"] == "white" else "White"
                print(f"Checkmate! {winner} wins!")
            elif final_state["is_stalemate"]:
                print("Stalemate! The game is a draw.")
            elif final_state["is_game_over"]:
                print("Game over!")
            else:
                print(f"Game stopped after {args.turns} turns.")
            
            print(f"Final position: {final_state['fen']}")
        else:
            print(f"Game ended with error: {result['error']}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()