import unittest
from src.chess_game import ChessGame
from src.config import Config


class TestChessGame(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.llm_config.model = "test-model"
        self.config.llm_config.api_key = "test-key"
    
    def test_game_initialization(self):
        game = ChessGame(self.config)
        self.assertIsNotNone(game)
        self.assertIsNotNone(game.board_manager)
        self.assertIsNotNone(game.agents)
    
    def test_board_manager_initial_state(self):
        game = ChessGame(self.config)
        state = game.board_manager.get_game_state()
        self.assertEqual(state["turn"], "white")
        self.assertFalse(state["is_game_over"])
    
    def test_legal_moves_initial_position(self):
        game = ChessGame(self.config)
        moves = game.board_manager.get_legal_moves()
        self.assertIn("Possible moves are:", moves)
        self.assertIn("e2e4", moves)  # Should include common opening moves


if __name__ == "__main__":
    unittest.main()