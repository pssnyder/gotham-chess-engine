"""
Opening book implementation for Gotham Chess Engine.

This module contains the opening repertoire based on Gotham Chess teachings,
featuring solid and educational openings that emphasize principles over memorization.
"""

import chess
import chess.pgn
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class OpeningType(Enum):
    """Types of openings in the Gotham repertoire."""
    WHITE_AGGRESSIVE = "white_aggressive"
    WHITE_POSITIONAL = "white_positional"
    BLACK_SOLID = "black_solid"
    BLACK_COUNTERATTACKING = "black_counterattacking"


class GothamOpeningBook:
    """
    Opening book based on Gotham Chess principles and recommendations.
    
    Features openings that are:
    - Easy to learn and understand
    - Based on solid principles
    - Lead to typical middlegame positions
    - Suitable for players of all levels
    """
    
    def __init__(self):
        """Initialize the opening book with Gotham's recommended openings."""
        self.openings = self._initialize_openings()
        self.transpositions = self._initialize_transpositions()
    
    def _initialize_openings(self) -> Dict[str, Dict]:
        """
        Initialize the opening book with move sequences and principles.
        
        Returns:
            Dict: Opening book data structure
        """
        return {
            # WHITE OPENINGS
            "london_system": {
                "type": OpeningType.WHITE_POSITIONAL,
                "moves": ["d4", "Nf3", "Bf4", "e3", "Bd3", "Nbd2", "c3"],
                "principles": [
                    "Develop pieces harmoniously",
                    "Control the center with pawns and pieces",
                    "Castle kingside early",
                    "Create a solid pawn structure"
                ],
                "typical_plans": [
                    "Ne5 to occupy the strong central outpost",
                    "h3 and g4 for kingside attack",
                    "Qe2 and 0-0-0 for opposite-side castling",
                    "f3 and e4 for central expansion"
                ],
                "educational_notes": [
                    "The London System is Levy's #1 recommendation for beginners",
                    "It follows the same development pattern against almost any defense",
                    "Very hard for Black to go wrong against if you know the plans"
                ]
            },
            
            "vienna_gambit": {
                "type": OpeningType.WHITE_AGGRESSIVE,
                "moves": ["e4", "Nc3", "f4", "Nf3"],
                "principles": [
                    "Rapid development of pieces",
                    "Control of the center",
                    "Create attacking chances",
                    "Open lines for pieces"
                ],
                "typical_plans": [
                    "Bc4 targeting f7",
                    "d3 supporting the center",
                    "0-0 for king safety",
                    "f4-f5 advance for attack"
                ],
                "educational_notes": [
                    "Aggressive opening that creates immediate threats",
                    "Forces Black to respond accurately",
                    "Great for developing tactical skills"
                ]
            },
            
            "ruy_lopez": {
                "type": OpeningType.WHITE_POSITIONAL,
                "moves": ["e4", "Nf3", "Bb5"],
                "principles": [
                    "Develop with tempo",
                    "Control the center",
                    "Create long-term pressure",
                    "Flexible piece placement"
                ],
                "typical_plans": [
                    "Ba4 and Bxc6 to damage pawn structure",
                    "0-0, Re1, and Nbd2 for central control",
                    "c3 and d4 for space advantage",
                    "a4 for queenside expansion"
                ],
                "educational_notes": [
                    "One of the oldest and most respected openings",
                    "Teaches patience and positional understanding",
                    "Creates rich, complex positions"
                ]
            },
            
            "alapin_variant": {
                "type": OpeningType.WHITE_AGGRESSIVE,
                "moves": ["e4", "c3", "d4"],
                "principles": [
                    "Early central control",
                    "Rapid development",
                    "Prevent Black's normal Sicilian plans",
                    "Create space advantage"
                ],
                "typical_plans": [
                    "Nf3 and Bd3 for quick development",
                    "0-0 for king safety",
                    "dxc5 to open lines",
                    "Bb5+ for tempo and development"
                ],
                "educational_notes": [
                    "Anti-Sicilian system that avoids main theory",
                    "Simple and effective against c5",
                    "Creates clear plans and objectives"
                ]
            },
            
            "danish_gambit": {
                "type": OpeningType.WHITE_AGGRESSIVE,
                "moves": ["e4", "d4", "c3", "Bc4"],
                "principles": [
                    "Sacrifice material for development",
                    "Open lines for attack",
                    "Quick piece mobilization",
                    "Create immediate threats"
                ],
                "typical_plans": [
                    "Nf3 and 0-0 for rapid development",
                    "Qb3 targeting f7 and b7",
                    "Re1 for central pressure",
                    "Bg5 for more attacking pieces"
                ],
                "educational_notes": [
                    "Romantic era gambit with tactical fireworks",
                    "Great for developing attacking skills",
                    "Teaches value of piece activity over material"
                ]
            },
            
            # BLACK OPENINGS
            "scandinavian_defense": {
                "type": OpeningType.BLACK_SOLID,
                "moves": ["d5", "Qxd5", "Nc6"],
                "principles": [
                    "Challenge the center immediately",
                    "Quick development",
                    "Central queen activity",
                    "Solid piece coordination"
                ],
                "typical_plans": [
                    "Nf6, Bg4 for piece activity",
                    "0-0-0 for aggressive play",
                    "e6 and Bd7 for solid development",
                    "Rd8 for central pressure"
                ],
                "educational_notes": [
                    "Levy's top recommendation for Black",
                    "Simple to learn but powerful",
                    "Leads to active, clear positions"
                ]
            },
            
            "caro_kann": {
                "type": OpeningType.BLACK_SOLID,
                "moves": ["c6", "d5"],
                "principles": [
                    "Solid pawn structure",
                    "Safe king position",
                    "Gradual piece development",
                    "Long-term positional play"
                ],
                "typical_plans": [
                    "Bf5 developing the bishop actively",
                    "e6 and Nf6 for central control",
                    "Nbd7 and 0-0 for safety",
                    "Qc7 and Rd8 for central pressure"
                ],
                "educational_notes": [
                    "Very solid and reliable defense",
                    "Favored by many world champions",
                    "Teaches patience and technique"
                ]
            },
            
            "queens_gambit_declined": {
                "type": OpeningType.BLACK_SOLID,
                "moves": ["d5", "e6"],
                "principles": [
                    "Maintain central tension",
                    "Solid development",
                    "Control key squares",
                    "Gradual piece coordination"
                ],
                "typical_plans": [
                    "Nf6, Be7, 0-0 for safety",
                    "c6 and Nbd7 for support",
                    "b6 and Bb7 for piece activity",
                    "c5 for central counterplay"
                ],
                "educational_notes": [
                    "Classical and time-tested defense",
                    "Teaches central control principles",
                    "Leads to rich strategic battles"
                ]
            },
            
            "nimzo_indian": {
                "type": OpeningType.BLACK_SOLID,
                "moves": ["Nf6", "e6", "Bb4"],
                "principles": [
                    "Control the center with pieces",
                    "Pin the knight to restrict White",
                    "Flexible pawn structure",
                    "Active piece development"
                ],
                "typical_plans": [
                    "Bxc3+ to damage White's structure",
                    "d6 and e5 for central control",
                    "0-0 and f5 for kingside play",
                    "c5 for queenside counterplay"
                ],
                "educational_notes": [
                    "Hypermodern defense focusing on piece activity",
                    "Creates imbalanced, rich positions",
                    "Teaches importance of piece coordination"
                ]
            },
            
            "pirc_defense": {
                "type": OpeningType.BLACK_COUNTERATTACKING,
                "moves": ["d6", "Nf6", "g6", "Bg7"],
                "principles": [
                    "Flexible piece development",
                    "Fianchetto bishop for long diagonal",
                    "Allow White center then counterattack",
                    "Create dynamic imbalances"
                ],
                "typical_plans": [
                    "0-0 and c6 for solid setup",
                    "a6 and b5 for queenside expansion",
                    "e5 for central break",
                    "Nh5 and f5 for kingside attack"
                ],
                "educational_notes": [
                    "Modern hypermodern defense",
                    "Allows White big center then fights back",
                    "Great for tactical players who like complications"
                ]
            }
        }
    
    def _initialize_transpositions(self) -> Dict[str, List[str]]:
        """
        Initialize common transpositions between openings.
        
        Returns:
            Dict: Transposition table
        """
        return {
            "d4_nf3_bf4": ["london_system", "torre_attack"],
            "e4_nc3": ["vienna_gambit", "vienna_game"],
            "e4_nf3_bb5": ["ruy_lopez", "spanish_opening"]
        }
    
    def get_opening_move(self, board: chess.Board, color: chess.Color) -> Optional[chess.Move]:
        """
        Get the next opening move based on the current position.
        
        Args:
            board: Current board position
            color: Color to move
            
        Returns:
            Optional[chess.Move]: Recommended opening move or None
        """
        position_hash = self._get_position_hash(board)
        
        # Check if we're still in known opening theory
        if len(board.move_stack) > 15:  # Out of opening phase
            return None
        
        # Get candidate moves based on position
        candidate_moves = self._get_candidate_moves(board, color)
        
        if not candidate_moves:
            return None
        
        # Choose move based on Gotham Chess preferences
        return self._select_best_move(board, candidate_moves, color)
    
    def _get_position_hash(self, board: chess.Board) -> str:
        """
        Get a simple hash of the current position for opening lookup.
        
        Args:
            board: Current board position
            
        Returns:
            str: Position hash
        """
        moves = [str(move) for move in board.move_stack]
        return "_".join(moves[:10])  # First 10 moves
    
    def _get_candidate_moves(self, board: chess.Board, color: chess.Color) -> List[chess.Move]:
        """
        Get candidate opening moves for the current position.
        
        Args:
            board: Current board position
            color: Color to move
            
        Returns:
            List[chess.Move]: List of candidate moves
        """
        candidates = []
        move_count = len(board.move_stack)
        
        if color == chess.WHITE:
            candidates.extend(self._get_white_opening_moves(board, move_count))
        else:
            candidates.extend(self._get_black_opening_moves(board, move_count))
        
        # Filter legal moves
        legal_candidates = []
        for move_san in candidates:
            try:
                move = board.parse_san(move_san)
                if move in board.legal_moves:
                    legal_candidates.append(move)
            except ValueError:
                continue
        
        return legal_candidates
    
    def _get_white_opening_moves(self, board: chess.Board, move_count: int) -> List[str]:
        """
        Get White opening moves based on Gotham Chess recommendations.
        
        Args:
            board: Current board position
            move_count: Number of moves played
            
        Returns:
            List[str]: Candidate moves in SAN notation
        """
        candidates = []
        
        # First move preferences
        if move_count == 0:
            candidates = ["d4", "e4"]  # Gotham's top recommendations
        
        # Second move based on first move
        elif move_count == 2:
            if str(board.move_stack[0]) == "d2d4":
                candidates = ["Nf3", "Bf4"]  # London System setup
            elif str(board.move_stack[0]) == "e2e4":
                candidates = ["Nf3", "Nc3"]  # King's Pawn openings
        
        # Third move
        elif move_count == 4:
            # London System continuation
            if self._is_london_system(board):
                candidates = ["Bf4", "e3", "Bd3"]
            # Vienna/King's Pawn games
            elif str(board.move_stack[0]) == "e2e4":
                candidates = ["Bb5", "Bc4", "f4"]
        
        return candidates
    
    def _get_black_opening_moves(self, board: chess.Board, move_count: int) -> List[str]:
        """
        Get Black opening moves based on Gotham Chess recommendations.
        
        Args:
            board: Current board position
            move_count: Number of moves played
            
        Returns:
            List[str]: Candidate moves in SAN notation
        """
        candidates = []
        white_first_move = str(board.move_stack[0]) if board.move_stack else ""
        
        # Response to 1.e4
        if move_count == 1 and white_first_move == "e2e4":
            candidates = ["d5", "c6", "e6"]  # Scandinavian, Caro-Kann, French
        
        # Response to 1.d4
        elif move_count == 1 and white_first_move == "d2d4":
            candidates = ["d5", "Nf6", "f5"]  # QGD, Indian systems, Dutch
        
        # Second move responses
        elif move_count == 3:
            if white_first_move == "e2e4":
                # Scandinavian continuation
                if len(board.move_stack) >= 2 and str(board.move_stack[1]) == "d7d5":
                    candidates = ["Qxd5", "Nf6"]
                # Caro-Kann continuation
                elif len(board.move_stack) >= 2 and str(board.move_stack[1]) == "c7c6":
                    candidates = ["d5", "dxe4"]
            
            elif white_first_move == "d2d4":
                # Queen's Gambit Declined
                if len(board.move_stack) >= 2 and str(board.move_stack[1]) == "d7d5":
                    candidates = ["e6", "c6", "Nf6"]
        
        return candidates
    
    def _is_london_system(self, board: chess.Board) -> bool:
        """
        Check if the current position is following the London System.
        
        Args:
            board: Current board position
            
        Returns:
            bool: True if London System structure
        """
        moves = [str(move) for move in board.move_stack]
        london_moves = ["d2d4", "g1f3", "c1f4"]
        
        return all(move in moves for move in london_moves[:len(moves)//2])
    
    def _select_best_move(self, board: chess.Board, candidates: List[chess.Move], color: chess.Color) -> chess.Move:
        """
        Select the best move from candidates based on Gotham Chess principles.
        
        Args:
            board: Current board position
            candidates: List of candidate moves
            color: Color to move
            
        Returns:
            chess.Move: Selected move
        """
        if not candidates:
            return random.choice(list(board.legal_moves))
        
        # Score each candidate move
        scored_moves = []
        for move in candidates:
            score = self._score_opening_move(board, move, color)
            scored_moves.append((move, score))
        
        # Sort by score and return best move
        scored_moves.sort(key=lambda x: x[1], reverse=True)
        return scored_moves[0][0]
    
    def _score_opening_move(self, board: chess.Board, move: chess.Move, color: chess.Color) -> int:
        """
        Score an opening move based on Gotham Chess principles.
        
        Args:
            board: Current board position
            move: Move to score
            color: Color making the move
            
        Returns:
            int: Move score
        """
        score = 0
        piece = board.piece_at(move.from_square)
        
        if not piece:
            return 0
        
        # Development bonuses
        if piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
            score += 5  # Develop pieces
        
        # Central control
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        if move.to_square in center_squares:
            score += 3
        
        # Castling bonus
        if board.is_castling(move):
            score += 4
        
        # Avoid moving the same piece twice
        move_count = len(board.move_stack)
        if move_count < 10:  # Opening phase
            recent_moves = board.move_stack[-4:] if len(board.move_stack) >= 4 else board.move_stack
            same_piece_moves = [m for m in recent_moves if board.piece_at(m.from_square) == piece]
            if len(same_piece_moves) > 1:
                score -= 2
        
        # Avoid early queen development
        if piece.piece_type == chess.QUEEN and move_count < 8:
            score -= 3
        
        return score
    
    def get_opening_name(self, board: chess.Board) -> Optional[str]:
        """
        Identify the opening being played.
        
        Args:
            board: Current board position
            
        Returns:
            Optional[str]: Opening name or None
        """
        moves = [str(move) for move in board.move_stack[:8]]  # First 8 moves
        
        # London System detection
        if "d2d4" in moves and "g1f3" in moves and "c1f4" in moves:
            return "London System"
        
        # Vienna Gambit detection
        if "e2e4" in moves and "b1c3" in moves and "f2f4" in moves:
            return "Vienna Gambit"
        
        # Scandinavian Defense detection
        if "e2e4" in moves and "d7d5" in moves:
            return "Scandinavian Defense"
        
        # Caro-Kann Defense detection
        if "e2e4" in moves and "c7c6" in moves:
            return "Caro-Kann Defense"
        
        # Alapin Variant detection
        if "e2e4" in moves and "c2c3" in moves and "d2d4" in moves:
            return "Alapin Variant"
        
        # Danish Gambit detection
        if "e2e4" in moves and "d2d4" in moves and "c2c3" in moves and "f1c4" in moves:
            return "Danish Gambit"
        
        # Nimzo-Indian Defense detection
        if "d2d4" in moves and "g8f6" in moves and "f8b4" in moves:
            return "Nimzo-Indian Defense"
        
        # Pirc Defense detection
        if "e2e4" in moves and "d7d6" in moves and "g8f6" in moves and "g7g6" in moves:
            return "Pirc Defense"
        
        return None
    
    def get_opening_explanation(self, opening_name: str) -> Dict[str, List[str]]:
        """
        Get educational explanation for an opening.
        
        Args:
            opening_name: Name of the opening
            
        Returns:
            Dict: Opening explanation with principles and plans
        """
        opening_key = opening_name.lower().replace(" ", "_")
        
        if opening_key in self.openings:
            return {
                "principles": self.openings[opening_key]["principles"],
                "typical_plans": self.openings[opening_key]["typical_plans"],
                "educational_notes": self.openings[opening_key]["educational_notes"]
            }
        
        return {
            "principles": ["Follow general opening principles"],
            "typical_plans": ["Develop pieces and control center"],
            "educational_notes": ["This opening is not in our database"]
        }