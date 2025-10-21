"""
Chess piece utilities and educational piece value system.

This module provides enhanced piece evaluation based on Gotham Chess principles,
including positional bonuses and educational insights.
"""

import chess
from typing import Dict, List, Tuple
from enum import Enum


class PieceValues(Enum):
    """Standard piece values with Gotham Chess educational emphasis."""
    PAWN = 1
    KNIGHT = 3
    BISHOP = 3
    ROOK = 5
    QUEEN = 9
    KING = 0  # King has no material value but infinite importance


class GothamPieceEvaluator:
    """
    Enhanced piece evaluation system incorporating Gotham Chess principles.
    
    This evaluator considers not just material value but also:
    - Piece activity and development
    - Positional bonuses
    - Educational value of moves
    """
    
    # Piece-square tables for positional evaluation
    PAWN_TABLE = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5,  5],
        [0,  0,  0, 20, 20,  0,  0,  0],
        [5, -5,-10,  0,  0,-10, -5,  5],
        [5, 10, 10,-20,-20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]
    ]
    
    KNIGHT_TABLE = [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ]
    
    BISHOP_TABLE = [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ]
    
    ROOK_TABLE = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [0,  0,  0,  5,  5,  0,  0,  0]
    ]
    
    QUEEN_TABLE = [
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [-5,  0,  5,  5,  5,  5,  0, -5],
        [0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]
    ]
    
    KING_MIDDLE_GAME_TABLE = [
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [20, 20,  0,  0,  0,  0, 20, 20],
        [20, 30, 10,  0,  0, 10, 30, 20]
    ]
    
    KING_ENDGAME_TABLE = [
        [-50,-40,-30,-20,-20,-30,-40,-50],
        [-30,-20,-10,  0,  0,-10,-20,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-30,  0,  0,  0,  0,-30,-30],
        [-50,-30,-30,-30,-30,-30,-30,-50]
    ]
    
    @staticmethod
    def get_piece_value(piece_type: chess.PieceType) -> int:
        """
        Get the base material value of a piece.
        
        Args:
            piece_type: Type of the chess piece
            
        Returns:
            int: Material value of the piece
        """
        piece_values = {
            chess.PAWN: PieceValues.PAWN.value,
            chess.KNIGHT: PieceValues.KNIGHT.value,
            chess.BISHOP: PieceValues.BISHOP.value,
            chess.ROOK: PieceValues.ROOK.value,
            chess.QUEEN: PieceValues.QUEEN.value,
            chess.KING: PieceValues.KING.value
        }
        return piece_values.get(piece_type, 0)
    
    @staticmethod
    def get_piece_square_value(piece: chess.Piece, square: chess.Square, is_endgame: bool = False) -> int:
        """
        Get positional bonus for a piece on a specific square.
        
        Args:
            piece: The chess piece
            square: The square the piece is on
            is_endgame: Whether we're in the endgame
            
        Returns:
            int: Positional bonus value
        """
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        
        # Flip rank for black pieces (piece-square tables are from white's perspective)
        if piece.color == chess.BLACK:
            rank = 7 - rank
        
        if piece.piece_type == chess.PAWN:
            return GothamPieceEvaluator.PAWN_TABLE[rank][file]
        elif piece.piece_type == chess.KNIGHT:
            return GothamPieceEvaluator.KNIGHT_TABLE[rank][file]
        elif piece.piece_type == chess.BISHOP:
            return GothamPieceEvaluator.BISHOP_TABLE[rank][file]
        elif piece.piece_type == chess.ROOK:
            return GothamPieceEvaluator.ROOK_TABLE[rank][file]
        elif piece.piece_type == chess.QUEEN:
            return GothamPieceEvaluator.QUEEN_TABLE[rank][file]
        elif piece.piece_type == chess.KING:
            if is_endgame:
                return GothamPieceEvaluator.KING_ENDGAME_TABLE[rank][file]
            else:
                return GothamPieceEvaluator.KING_MIDDLE_GAME_TABLE[rank][file]
        
        return 0
    
    @staticmethod
    def evaluate_piece_activity(board: chess.Board, square: chess.Square) -> int:
        """
        Evaluate piece activity based on Gotham Chess principles.
        
        Args:
            board: Current board position
            square: Square of the piece to evaluate
            
        Returns:
            int: Activity bonus for the piece
        """
        piece = board.piece_at(square)
        if not piece:
            return 0
        
        activity_score = 0
        
        # Number of squares the piece can move to
        legal_moves = [move for move in board.legal_moves if move.from_square == square]
        mobility = len(legal_moves)
        
        # Mobility bonus (scaled by piece type)
        if piece.piece_type == chess.QUEEN:
            activity_score += mobility * 2
        elif piece.piece_type == chess.ROOK:
            activity_score += mobility * 3
        elif piece.piece_type == chess.BISHOP:
            activity_score += mobility * 3
        elif piece.piece_type == chess.KNIGHT:
            activity_score += mobility * 4
        elif piece.piece_type == chess.PAWN:
            activity_score += mobility * 5
        
        # Central square bonus
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        if 2 <= file <= 5 and 2 <= rank <= 5:  # Central area
            activity_score += 5
        elif 1 <= file <= 6 and 1 <= rank <= 6:  # Extended center
            activity_score += 2
        
        return activity_score
    
    @staticmethod
    def get_educational_piece_tips(piece_type: chess.PieceType) -> List[str]:
        """
        Get educational tips for piece usage based on Gotham Chess teachings.
        
        Args:
            piece_type: Type of the chess piece
            
        Returns:
            List[str]: Educational tips for the piece
        """
        tips = {
            chess.PAWN: [
                "Pawns are the soul of chess - they control key squares",
                "Always consider pawn structure before making moves",
                "Passed pawns become very strong in the endgame",
                "Don't move pawns without a purpose - they can't go backwards"
            ],
            chess.KNIGHT: [
                "Knights are best placed in the center where they control 8 squares",
                "Knights on the rim are dim - avoid edge squares when possible",
                "Knights are excellent at forking multiple pieces",
                "Develop knights before bishops in the opening"
            ],
            chess.BISHOP: [
                "Bishops love open diagonals and long-range action",
                "The bishop pair (both bishops) is a powerful advantage",
                "Don't trap your bishops behind your own pawns",
                "Bishops are better than knights in open positions"
            ],
            chess.ROOK: [
                "Rooks belong on open files and active squares",
                "Connect your rooks by castling and developing",
                "Rooks are powerful on the 7th rank attacking pawns",
                "Double rooks on files for maximum pressure"
            ],
            chess.QUEEN: [
                "Don't bring the queen out too early in the opening",
                "The queen is your most powerful piece - keep her safe",
                "Queens excel at both attack and defense",
                "Use the queen to coordinate attacks with other pieces"
            ],
            chess.KING: [
                "King safety is paramount - castle early",
                "In the endgame, the king becomes an active fighting piece",
                "Keep your king away from enemy piece attacks",
                "Use your king to support pawn advancement in endings"
            ]
        }
        return tips.get(piece_type, [])
    
    @staticmethod
    def analyze_piece_coordination(board: chess.Board, color: chess.Color) -> Dict[str, int]:
        """
        Analyze how well pieces are coordinated for the given color.
        
        Args:
            board: Current board position
            color: Color to analyze
            
        Returns:
            Dict[str, int]: Coordination analysis scores
        """
        analysis = {
            "defended_pieces": 0,
            "attacking_pieces": 0,
            "piece_harmony": 0
        }
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color == color:
                # Count how many friendly pieces defend this piece
                defenders = board.attackers(color, square)
                analysis["defended_pieces"] += len(defenders)
                
                # Count how many enemy pieces this piece attacks
                attacks = board.attacks(square)
                for attacked_square in attacks:
                    attacked_piece = board.piece_at(attacked_square)
                    if attacked_piece and attacked_piece.color != color:
                        analysis["attacking_pieces"] += 1
        
        # Calculate piece harmony (simplified)
        # This could be enhanced with more sophisticated coordination metrics
        total_pieces = len([p for p in board.piece_map().values() if p.color == color])
        if total_pieces > 0:
            analysis["piece_harmony"] = (analysis["defended_pieces"] + 
                                       analysis["attacking_pieces"]) // total_pieces
        
        return analysis


class GothamTacticalPatterns:
    """
    Tactical pattern recognition based on Gotham Chess educational content.
    """
    
    @staticmethod
    def find_forks(board: chess.Board, color: chess.Color) -> List[Tuple[chess.Square, List[chess.Square]]]:
        """
        Find potential fork opportunities for the given color.
        
        Args:
            board: Current board position
            color: Color to find forks for
            
        Returns:
            List[Tuple[chess.Square, List[chess.Square]]]: List of (attacking_square, forked_squares)
        """
        forks = []
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color == color:
                attacked_squares = board.attacks(square)
                enemy_pieces = []
                
                for attacked_square in attacked_squares:
                    attacked_piece = board.piece_at(attacked_square)
                    if attacked_piece and attacked_piece.color != color:
                        enemy_pieces.append(attacked_square)
                
                # A fork requires attacking at least 2 enemy pieces
                if len(enemy_pieces) >= 2:
                    forks.append((square, enemy_pieces))
        
        return forks
    
    @staticmethod
    def find_pins(board: chess.Board, color: chess.Color) -> List[Tuple[chess.Square, chess.Square, chess.Square]]:
        """
        Find potential pin opportunities for the given color.
        
        Args:
            board: Current board position
            color: Color to find pins for
            
        Returns:
            List[Tuple[chess.Square, chess.Square, chess.Square]]: List of (attacker, pinned_piece, target)
        """
        pins = []
        
        # Look for sliding pieces (bishops, rooks, queens) that can create pins
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if (piece and piece.color == color and 
                piece.piece_type in [chess.BISHOP, chess.ROOK, chess.QUEEN]):
                
                # Get the ray attacks for this piece
                attacks = board.attacks(square)
                
                # For each direction this piece attacks, look for pins
                # This is a simplified implementation
                # A full implementation would need to check specific ray directions
                for attacked_square in attacks:
                    attacked_piece = board.piece_at(attacked_square)
                    if attacked_piece and attacked_piece.color != color:
                        # Check if there's a more valuable piece behind this one
                        # This would require ray casting logic
                        pass
        
        return pins
    
    @staticmethod
    def find_skewers(board: chess.Board, color: chess.Color) -> List[Tuple[chess.Square, chess.Square, chess.Square]]:
        """
        Find potential skewer opportunities for the given color.
        
        Args:
            board: Current board position
            color: Color to find skewers for
            
        Returns:
            List[Tuple[chess.Square, chess.Square, chess.Square]]: List of (attacker, front_piece, back_piece)
        """
        skewers = []
        
        # Similar to pins but with the more valuable piece in front
        # This would require sophisticated ray-casting implementation
        
        return skewers