"""
Core chess board representation and game logic.

This module provides the fundamental chess board representation using the
python-chess library as a foundation, with additional Gotham Chess specific
enhancements for educational value and principled play.
"""

import chess
import chess.pgn
from typing import List, Optional, Dict, Set, Tuple
from enum import Enum


class GamePhase(Enum):
    """Game phase enumeration for different strategic considerations."""
    OPENING = "opening"
    MIDDLE_GAME = "middle_game"
    ENDGAME = "endgame"


class GothamBoard(chess.Board):
    """
    Enhanced chess board with Gotham Chess specific functionality.
    
    Extends the python-chess Board class with additional features for:
    - Educational move suggestions
    - Principled play evaluation
    - Game phase detection
    - Historical pattern recognition
    """
    
    def __init__(self, fen: Optional[str] = None):
        """
        Initialize the Gotham Chess board.
        
        Args:
            fen: FEN string for custom position (optional)
        """
        if fen is None:
            super().__init__()  # Start with starting position
        else:
            super().__init__(fen)
        self.move_history: List[chess.Move] = []
        self.educational_notes: List[str] = []
        
    def get_game_phase(self) -> GamePhase:
        """
        Determine the current game phase based on material and position.
        
        Returns:
            GamePhase: Current phase of the game
        """
        # Count major pieces (Queen, Rooks)
        major_pieces = 0
        for square in chess.SQUARES:
            piece = self.piece_at(square)
            if piece and piece.piece_type in [chess.QUEEN, chess.ROOK]:
                major_pieces += 1
        
        # Count total pieces
        total_pieces = len(self.piece_map())
        
        # Opening: First 10 moves or if many pieces remain
        if len(self.move_stack) < 20 or total_pieces >= 28:
            return GamePhase.OPENING
        
        # Endgame: Few pieces remaining or no major pieces
        elif total_pieces <= 10 or major_pieces <= 2:
            return GamePhase.ENDGAME
        
        # Middle game: Everything else
        else:
            return GamePhase.MIDDLE_GAME
    
    def is_king_safe(self, color: chess.Color) -> bool:
        """
        Evaluate king safety using Gotham Chess principles.
        
        Args:
            color: Color of the king to evaluate
            
        Returns:
            bool: True if king is relatively safe
        """
        king_square = self.king(color)
        if king_square is None:
            return False
        
        # Check if king is castled
        king_file = chess.square_file(king_square)
        king_rank = chess.square_rank(king_square)
        
        # King safety factors
        safety_score = 0
        
        # 1. Castling bonus
        if color == chess.WHITE:
            if king_file in [6, 2]:  # G-file (6) or C-file (2) - castled position
                safety_score += 2
        else:
            if king_file in [6, 2]:  # G-file (6) or C-file (2) - castled position
                safety_score += 2
        
        # 2. Pawn shield
        pawn_shield_squares = []
        if color == chess.WHITE:
            if king_rank == 0:  # King on back rank
                pawn_shield_squares = [
                    chess.square(max(0, king_file - 1), 1),
                    chess.square(king_file, 1),
                    chess.square(min(7, king_file + 1), 1)
                ]
        else:
            if king_rank == 7:  # King on back rank
                pawn_shield_squares = [
                    chess.square(max(0, king_file - 1), 6),
                    chess.square(king_file, 6),
                    chess.square(min(7, king_file + 1), 6)
                ]
        
        # Count pawn shield
        for square in pawn_shield_squares:
            piece = self.piece_at(square)
            if piece and piece.piece_type == chess.PAWN and piece.color == color:
                safety_score += 1
        
        # 3. Check for immediate threats
        if self.is_check():
            safety_score -= 2
        
        # Count attackers near king
        attacker_count = 0
        for square in chess.SquareSet(chess.BB_KING_ATTACKS[king_square]):
            attackers = self.attackers(not color, square)
            attacker_count += len(attackers)
        
        if attacker_count > 2:
            safety_score -= 1
        
        return safety_score >= 1
    
    def get_development_score(self, color: chess.Color) -> int:
        """
        Calculate development score based on Gotham Chess principles.
        
        Args:
            color: Color to evaluate development for
            
        Returns:
            int: Development score (higher is better)
        """
        score = 0
        
        # Starting positions for pieces
        if color == chess.WHITE:
            knight_start_squares = [chess.B1, chess.G1]
            bishop_start_squares = [chess.C1, chess.F1]
            queen_start_square = chess.D1
            king_start_square = chess.E1
        else:
            knight_start_squares = [chess.B8, chess.G8]
            bishop_start_squares = [chess.C8, chess.F8]
            queen_start_square = chess.D8
            king_start_square = chess.E8
        
        # Knights developed
        for square in knight_start_squares:
            piece = self.piece_at(square)
            if not (piece and piece.piece_type == chess.KNIGHT and piece.color == color):
                score += 1  # Knight moved from starting square
        
        # Bishops developed
        for square in bishop_start_squares:
            piece = self.piece_at(square)
            if not (piece and piece.piece_type == chess.BISHOP and piece.color == color):
                score += 1  # Bishop moved from starting square
        
        # Castling rights (king safety and rook development)
        if color == chess.WHITE:
            if not (self.has_kingside_castling_rights(chess.WHITE) or 
                   self.has_queenside_castling_rights(chess.WHITE)):
                # King moved, check if castled
                king_square = self.king(chess.WHITE)
                if king_square is not None:
                    if king_square in [chess.G1, chess.C1]:  # Castled
                        score += 2
        else:
            if not (self.has_kingside_castling_rights(chess.BLACK) or 
                   self.has_queenside_castling_rights(chess.BLACK)):
                # King moved, check if castled
                king_square = self.king(chess.BLACK)
                if king_square is not None:
                    if king_square in [chess.G8, chess.C8]:  # Castled
                        score += 2
        
        # Penalty for early queen development
        queen_square = None
        for square in chess.SQUARES:
            piece = self.piece_at(square)
            if piece and piece.piece_type == chess.QUEEN and piece.color == color:
                queen_square = square
                break
        
        if queen_square is not None:
            if color == chess.WHITE and queen_square != queen_start_square:
                if len(self.move_stack) < 10:  # Early in game
                    score -= 1  # Penalty for early queen development
            elif color == chess.BLACK and queen_square != queen_start_square:
                if len(self.move_stack) < 10:  # Early in game
                    score -= 1  # Penalty for early queen development
        
        return score
    
    def get_center_control(self, color: chess.Color) -> int:
        """
        Evaluate center control based on Gotham Chess emphasis on center.
        
        Args:
            color: Color to evaluate center control for
            
        Returns:
            int: Center control score
        """
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        extended_center = [chess.C3, chess.C4, chess.C5, chess.C6,
                          chess.D3, chess.D6, chess.E3, chess.E6,
                          chess.F3, chess.F4, chess.F5, chess.F6]
        
        score = 0
        
        # Direct occupation of center
        for square in center_squares:
            piece = self.piece_at(square)
            if piece and piece.color == color:
                if piece.piece_type == chess.PAWN:
                    score += 2  # Pawns in center are very valuable
                else:
                    score += 1  # Other pieces in center
        
        # Control of center squares
        for square in center_squares:
            attackers = self.attackers(color, square)
            score += len(attackers) // 2  # Bonus for attacking center
        
        # Extended center control
        for square in extended_center:
            piece = self.piece_at(square)
            if piece and piece.color == color and piece.piece_type == chess.PAWN:
                score += 1  # Supporting pawns
        
        return score
    
    def add_educational_note(self, note: str) -> None:
        """
        Add an educational note about the current position or move.
        
        Args:
            note: Educational note to add
        """
        self.educational_notes.append(note)
    
    def get_educational_notes(self) -> List[str]:
        """
        Get all educational notes for this position.
        
        Returns:
            List[str]: List of educational notes
        """
        return self.educational_notes.copy()
    
    def make_educational_move(self, move: chess.Move) -> None:
        """
        Make a move and add educational context.
        
        Args:
            move: The move to make
        """
        # Store move in history
        self.move_history.append(move)
        
        # Make the move
        self.push(move)
        
        # Add educational context based on move type
        piece = self.piece_at(move.to_square)
        if piece:
            if move.promotion:
                self.add_educational_note(f"Pawn promotion to {piece.symbol().upper()} - converting advantage!")
            elif self.is_capture(move):
                self.add_educational_note("Capture made - material advantage gained!")
            elif self.is_castling(move):
                self.add_educational_note("Castling - king safety and rook development!")
    
    def is_tactical_motif_present(self) -> Dict[str, bool]:
        """
        Check for common tactical motifs in the current position.
        
        Returns:
            Dict[str, bool]: Dictionary of tactical motifs and their presence
        """
        motifs = {
            "fork": False,
            "pin": False,
            "skewer": False,
            "discovered_attack": False,
            "back_rank_mate": False
        }
        
        # This is a simplified implementation
        # A full implementation would require more sophisticated pattern recognition
        
        # Check for potential forks (piece attacking two or more enemy pieces)
        for square in chess.SQUARES:
            piece = self.piece_at(square)
            if piece:
                attacked_squares = self.attacks(square)
                enemy_pieces = 0
                for attacked_square in attacked_squares:
                    attacked_piece = self.piece_at(attacked_square)
                    if attacked_piece and attacked_piece.color != piece.color:
                        enemy_pieces += 1
                if enemy_pieces >= 2:
                    motifs["fork"] = True
        
        # Check for back rank mate threats
        for color in [chess.WHITE, chess.BLACK]:
            king_square = self.king(color)
            if king_square is not None:
                king_rank = chess.square_rank(king_square)
                back_rank = 0 if color == chess.WHITE else 7
                
                if king_rank == back_rank:
                    # Check if king is trapped by own pawns
                    escape_squares = list(self.attacks(king_square))
                    blocked_escapes = 0
                    for escape_square in escape_squares:
                        escape_piece = self.piece_at(escape_square)
                        if escape_piece and escape_piece.color == color:
                            blocked_escapes += 1
                    
                    if blocked_escapes >= 2:
                        motifs["back_rank_mate"] = True
        
        return motifs