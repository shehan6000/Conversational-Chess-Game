import chess
import chess.svg
from typing import Optional, List, Tuple
import logging
from dataclasses import dataclass
from typing_extensions import Annotated


@dataclass
class MoveResult:
    success: bool
    message: str
    svg_data: Optional[str] = None
    is_check: bool = False
    is_checkmate: bool = False
    is_stalemate: bool = False


class ChessBoardManager:
    def __init__(self):
        self.board = chess.Board()
        self.made_move = False
        self.logger = logging.getLogger(__name__)
    
    def reset_board(self) -> None:
        """Reset the board to initial state."""
        self.board.reset()
        self.made_move = False
        self.logger.info("Chess board reset")
    
    def get_legal_moves(self) -> Annotated[str, "A list of legal moves in UCI format"]:
        """Get all legal moves for the current position."""
        try:
            moves = [str(move) for move in self.board.legal_moves]
            moves_str = ", ".join(moves) if moves else "No legal moves available"
            self.logger.debug(f"Retrieved {len(moves)} legal moves")
            return f"Possible moves are: {moves_str}"
        except Exception as e:
            self.logger.error(f"Error getting legal moves: {e}")
            return "Error retrieving legal moves. The game might be over."
    
    def make_move(self, move: Annotated[str, "A move in UCI format."]) -> MoveResult:
        """Make a move on the chess board."""
        try:
            # Validate move format
            if not self._is_valid_uci_format(move):
                return MoveResult(
                    success=False,
                    message=f"Invalid move format: {move}. Please use UCI format (e.g., 'e2e4')."
                )
            
            chess_move = chess.Move.from_uci(move)
            
            # Check if move is legal
            if chess_move not in self.board.legal_moves:
                return MoveResult(
                    success=False,
                    message=f"Illegal move: {move}. Use get_legal_moves() to see available moves."
                )
            
            # Execute the move
            self.board.push(chess_move)
            self.made_move = True
            
            # Create SVG visualization
            svg_data = chess.svg.board(
                self.board,
                arrows=[(chess_move.from_square, chess_move.to_square)],
                fill={chess_move.from_square: "gray"},
                size=200
            )
            
            # Get move description
            piece = self.board.piece_at(chess_move.to_square)
            piece_symbol = piece.unicode_symbol()
            piece_name = (
                chess.piece_name(piece.piece_type).capitalize()
                if piece_symbol.isupper()
                else chess.piece_name(piece.piece_type)
            )
            
            message = (
                f"Moved {piece_name} ({piece_symbol}) from "
                f"{chess.SQUARE_NAMES[chess_move.from_square]} to "
                f"{chess.SQUARE_NAMES[chess_move.to_square]}."
            )
            
            # Check game state
            is_check = self.board.is_check()
            is_checkmate = self.board.is_checkmate()
            is_stalemate = self.board.is_stalemate()
            
            if is_checkmate:
                message += " Checkmate!"
            elif is_check:
                message += " Check!"
            elif is_stalemate:
                message += " Stalemate!"
            
            self.logger.info(f"Move executed: {move} - {message}")
            
            return MoveResult(
                success=True,
                message=message,
                svg_data=svg_data,
                is_check=is_check,
                is_checkmate=is_checkmate,
                is_stalemate=is_stalemate
            )
            
        except ValueError as e:
            self.logger.error(f"Invalid move format: {move} - {e}")
            return MoveResult(
                success=False,
                message=f"Invalid move format: {move}. Please use UCI format (e.g., 'e2e4')."
            )
        except Exception as e:
            self.logger.error(f"Error making move {move}: {e}")
            return MoveResult(
                success=False,
                message=f"Error executing move: {str(e)}"
            )
    
    def _is_valid_uci_format(self, move: str) -> bool:
        """Validate UCI move format."""
        if len(move) != 4 and len(move) != 5:  # Normal moves and promotions
            return False
        
        try:
            # Basic format validation
            if not all(c in 'abcdefgh12345678' for c in move[:2]):
                return False
            if not all(c in 'abcdefgh12345678' for c in move[2:4]):
                return False
            return True
        except:
            return False
    
    def get_game_state(self) -> Dict[str, Any]:
        """Get current game state."""
        return {
            "fen": self.board.fen(),
            "is_check": self.board.is_check(),
            "is_checkmate": self.board.is_checkmate(),
            "is_stalemate": self.board.is_stalemate(),
            "is_game_over": self.board.is_game_over(),
            "turn": "white" if self.board.turn else "black",
            "fullmove_number": self.board.fullmove_number
        }
    
    def check_made_move(self, msg: Any) -> bool:
        """Check if a move was made in the last operation."""
        current_state = self.made_move
        if current_state:
            self.made_move = False
        return current_state