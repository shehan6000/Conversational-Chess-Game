import logging
from typing import Dict, Any, Optional
import chess
from .agents import ChessGameAgents
from .board_manager import ChessBoardManager
from .config import Config


class ChessGame:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.board_manager = ChessBoardManager()
        self.agents = ChessGameAgents(self.config, self.board_manager)
        self.logger = logging.getLogger(__name__)
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('chess_game.log')
            ]
        )
    
    def start_game(self, max_turns: Optional[int] = None) -> Dict[str, Any]:
        """Start a new chess game."""
        try:
            # Reset board
            self.board_manager.reset_board()
            
            # Use provided max_turns or config default
            max_turns = max_turns or self.config.game_config.max_turns
            
            self.logger.info(f"Starting new chess game (max turns: {max_turns})")
            
            # Start the game with black inviting white to move first
            chat_result = self.agents.player_black.initiate_chat(
                self.agents.player_white,
                message=(
                    "Let's play an exciting game of chess! I'll be playing black. "
                    "You have the white pieces and the first move. Good luck and have fun!"
                ),
                max_turns=max_turns,
            )
            
            # Get final game state
            final_state = self.board_manager.get_game_state()
            
            self.logger.info(f"Game completed. Final state: {final_state}")
            
            return {
                "chat_result": chat_result,
                "final_state": final_state,
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Error starting chess game: {e}")
            return {
                "success": False,
                "error": str(e),
                "final_state": self.board_manager.get_game_state() if hasattr(self, 'board_manager') else None
            }
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current game state."""
        return self.board_manager.get_game_state()
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.board_manager.board.is_game_over()
    
    def get_winner(self) -> Optional[str]:
        """Get the winner if game is over."""
        if not self.is_game_over():
            return None
        
        state = self.board_manager.get_game_state()
        if state["is_checkmate"]:
            return "black" if state["turn"] == "white" else "white"
        elif state["is_stalemate"]:
            return "draw"
        
        return None