from autogen import ConversableAgent, register_function
from typing import Dict, Any, List
import logging
from .board_manager import ChessBoardManager
from .config import Config


class ChessGameAgents:
    def __init__(self, config: Config, board_manager: ChessBoardManager):
        self.config = config
        self.board_manager = board_manager
        self.logger = logging.getLogger(__name__)
        
        self.player_white = None
        self.player_black = None
        self.board_proxy = None
        
        self._initialize_agents()
        self._register_tools()
        self._register_nested_chats()
    
    def _initialize_agents(self):
        """Initialize the chess player agents."""
        llm_config = self.config.get_llm_config_dict()
        
        # Player White agent
        self.player_white = ConversableAgent(
            name="Player_White",
            system_message=(
                "You are a chess grandmaster playing as white. "
                "First call get_legal_moves() to see available moves. "
                "Then call make_move(move) to execute your move. "
                "After making a move, engage in friendly banter to make the game enjoyable. "
                "Always use proper UCI format for moves (e.g., 'e2e4', 'g1f3'). "
                "Be strategic and try to win while maintaining good sportsmanship."
            ),
            llm_config=llm_config,
            human_input_mode="NEVER",
        )
        
        # Player Black agent
        self.player_black = ConversableAgent(
            name="Player_Black",
            system_message=(
                "You are a chess grandmaster playing as black. "
                "First call get_legal_moves() to see available moves. "
                "Then call make_move(move) to execute your move. "
                "After making a move, engage in friendly banter to make the game enjoyable. "
                "Always use proper UCI format for moves (e.g., 'e2e4', 'g1f3'). "
                "Be strategic and try to win while maintaining good sportsmanship."
            ),
            llm_config=llm_config,
            human_input_mode="NEVER",
        )
        
        # Board proxy agent
        self.board_proxy = ConversableAgent(
            name="Board_Proxy",
            llm_config=False,
            is_termination_msg=self.board_manager.check_made_move,
            default_auto_reply="Please make a legal move. Use get_legal_moves() first if unsure.",
            human_input_mode="NEVER",
        )
        
        self.logger.info("Chess agents initialized")
    
    def _register_tools(self):
        """Register tools for both players."""
        for caller in [self.player_white, self.player_black]:
            register_function(
                self.board_manager.get_legal_moves,
                caller=caller,
                executor=self.board_proxy,
                name="get_legal_moves",
                description="Get all legal moves in the current position. Returns moves in UCI format.",
            )
            
            register_function(
                self._make_move_wrapper,
                caller=caller,
                executor=self.board_proxy,
                name="make_move",
                description="Make a move on the chess board. Use UCI format (e.g., 'e2e4').",
            )
        
        self.logger.info("Tools registered for chess agents")
    
    def _make_move_wrapper(self, move: str) -> str:
        """Wrapper for make_move that returns a string for the agent."""
        result = self.board_manager.make_move(move)
        return result.message
    
    def _register_nested_chats(self):
        """Register nested chats for move execution."""
        # White's nested chat with board proxy
        self.player_white.register_nested_chats(
            trigger=self.player_black,
            chat_queue=[
                {
                    "sender": self.board_proxy,
                    "recipient": self.player_white,
                    "summary_method": "last_msg",
                    "silent": True,
                    "max_turns": self.config.game_config.max_nested_turns,
                }
            ],
        )
        
        # Black's nested chat with board proxy
        self.player_black.register_nested_chats(
            trigger=self.player_white,
            chat_queue=[
                {
                    "sender": self.board_proxy,
                    "recipient": self.player_black,
                    "summary_method": "last_msg",
                    "silent": True,
                    "max_turns": self.config.game_config.max_nested_turns,
                }
            ],
        )
        
        self.logger.info("Nested chats registered")
    
    def get_agents(self) -> Dict[str, ConversableAgent]:
        """Get all agents."""
        return {
            "white": self.player_white,
            "black": self.player_black,
            "board_proxy": self.board_proxy
        }