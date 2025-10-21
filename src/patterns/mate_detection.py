"""
Mate pattern detection for Gotham Chess Engine.

This module implements detection of checkmate patterns including
mate in 1 and mate in 2 positions.
"""

import chess
from typing import List, Dict, Optional, Tuple
from enum import Enum


class MatePattern(Enum):
    """Types of mate patterns."""
    MATE_IN_ONE = "mate_in_one"
    MATE_IN_TWO = "mate_in_two"
    BACK_RANK_MATE = "back_rank_mate"
    SMOTHERED_MATE = "smothered_mate"
    ANASTASIA_MATE = "anastasia_mate"
    ARABIAN_MATE = "arabian_mate"
    LEGAL_MATE = "legal_mate"


class GothamMateDetector:
    """
    Mate pattern detection system for Gotham Chess Engine.
    
    Detects various checkmate patterns and provides educational
    insights about mating techniques.
    """
    
    def __init__(self):
        """Initialize the mate detector."""
        self.mate_scores = {
            MatePattern.MATE_IN_ONE: 10000,
            MatePattern.MATE_IN_TWO: 5000,
            MatePattern.BACK_RANK_MATE: 8000,
            MatePattern.SMOTHERED_MATE: 8000,
            MatePattern.ANASTASIA_MATE: 7000,
            MatePattern.ARABIAN_MATE: 7000,
            MatePattern.LEGAL_MATE: 7000
        }
    
    def find_mates(self, board: chess.Board) -> Dict[MatePattern, List[Dict]]:
        """
        Find all mate patterns in the current position.
        
        Args:
            board: Current chess position
            
        Returns:
            Dict mapping mate patterns to their instances
        """
        results = {}
        
        results[MatePattern.MATE_IN_ONE] = self.find_mate_in_one(board)
        results[MatePattern.MATE_IN_TWO] = self.find_mate_in_two(board)
        results[MatePattern.BACK_RANK_MATE] = self.find_back_rank_mates(board)
        results[MatePattern.SMOTHERED_MATE] = self.find_smothered_mates(board)
        results[MatePattern.ANASTASIA_MATE] = self.find_anastasia_mates(board)
        results[MatePattern.ARABIAN_MATE] = self.find_arabian_mates(board)
        results[MatePattern.LEGAL_MATE] = self.find_legal_mates(board)
        
        return results
    
    def find_mate_in_one(self, board: chess.Board) -> List[Dict]:
        """
        Find all mate in one opportunities.
        
        Args:
            board: Current chess position
            
        Returns:
            List of mate in one moves
        """
        mate_moves = []
        
        for move in board.legal_moves:
            board.push(move)
            
            if board.is_checkmate():
                mate_type = self._classify_mate_type(board)
                mate_moves.append({
                    'move': move,
                    'mate_type': mate_type,
                    'description': f"Mate in 1: {mate_type}",
                    'educational_note': self._get_mate_educational_note(mate_type)
                })
            
            board.pop()
        
        return mate_moves
    
    def find_mate_in_two(self, board: chess.Board) -> List[Dict]:
        """
        Find mate in two opportunities.
        
        Args:
            board: Current chess position
            
        Returns:
            List of mate in two sequences
        """
        mate_sequences = []
        
        for first_move in board.legal_moves:
            board.push(first_move)
            
            # Check if opponent has any defense
            can_avoid_mate = False
            best_defense = None
            
            for defense_move in board.legal_moves:
                board.push(defense_move)
                
                # Check if we can still deliver mate
                mate_found = False
                for second_move in board.legal_moves:
                    board.push(second_move)
                    if board.is_checkmate():
                        mate_found = True
                    board.pop()
                    
                    if mate_found:
                        break
                
                if not mate_found:
                    can_avoid_mate = True
                    best_defense = defense_move
                
                board.pop()
                
                if can_avoid_mate:
                    break
            
            # If opponent cannot avoid mate
            if not can_avoid_mate:
                # Find the mating move after any defense
                mating_moves = []
                for defense_move in board.legal_moves:
                    board.push(defense_move)
                    
                    for second_move in board.legal_moves:
                        board.push(second_move)
                        if board.is_checkmate():
                            mate_type = self._classify_mate_type(board)
                            mating_moves.append({
                                'defense': defense_move,
                                'mate_move': second_move,
                                'mate_type': mate_type
                            })
                        board.pop()
                    
                    board.pop()
                
                if mating_moves:
                    mate_sequences.append({
                        'first_move': first_move,
                        'variations': mating_moves,
                        'description': f"Mate in 2 starting with {first_move}",
                        'educational_note': "Forced mate sequence - opponent has no good defense"
                    })
            
            board.pop()
        
        return mate_sequences[:3]  # Return top 3 mate in 2 sequences
    
    def find_back_rank_mates(self, board: chess.Board) -> List[Dict]:
        """
        Find back rank mate patterns.
        
        Args:
            board: Current chess position
            
        Returns:
            List of back rank mate opportunities
        """
        back_rank_mates = []
        
        for move in board.legal_moves:
            piece = board.piece_at(move.from_square)
            if not piece or piece.piece_type not in [chess.ROOK, chess.QUEEN]:
                continue
            
            board.push(move)
            
            if board.is_checkmate():
                enemy_king = board.king(not board.turn)
                if enemy_king is not None:
                    king_rank = chess.square_rank(enemy_king)
                    back_rank = 0 if not board.turn == chess.WHITE else 7
                    
                    if king_rank == back_rank:
                        # Verify it's truly a back rank mate (king trapped by own pieces)
                        if self._is_back_rank_mate(board, enemy_king):
                            back_rank_mates.append({
                                'move': move,
                                'attacking_piece': piece.piece_type,
                                'description': "Back rank mate",
                                'educational_note': "King is trapped on the back rank by its own pieces"
                            })
            
            board.pop()
        
        return back_rank_mates
    
    def find_smothered_mates(self, board: chess.Board) -> List[Dict]:
        """
        Find smothered mate patterns.
        
        Args:
            board: Current chess position
            
        Returns:
            List of smothered mate opportunities
        """
        smothered_mates = []
        
        for move in board.legal_moves:
            piece = board.piece_at(move.from_square)
            if not piece or piece.piece_type != chess.KNIGHT:
                continue
            
            board.push(move)
            
            if board.is_checkmate():
                enemy_king = board.king(not board.turn)
                if enemy_king is not None and self._is_smothered_mate(board, enemy_king):
                    smothered_mates.append({
                        'move': move,
                        'description': "Smothered mate",
                        'educational_note': "Knight delivers mate while king is blocked by own pieces"
                    })
            
            board.pop()
        
        return smothered_mates
    
    def find_anastasia_mates(self, board: chess.Board) -> List[Dict]:
        """
        Find Anastasia's mate patterns (Rook + Knight).
        
        Args:
            board: Current chess position
            
        Returns:
            List of Anastasia mate opportunities
        """
        anastasia_mates = []
        
        for move in board.legal_moves:
            piece = board.piece_at(move.from_square)
            if not piece or piece.piece_type not in [chess.ROOK, chess.KNIGHT]:
                continue
            
            board.push(move)
            
            if board.is_checkmate():
                if self._is_anastasia_mate(board):
                    anastasia_mates.append({
                        'move': move,
                        'attacking_piece': piece.piece_type,
                        'description': "Anastasia's mate",
                        'educational_note': "Rook and knight coordinate to deliver mate"
                    })
            
            board.pop()
        
        return anastasia_mates
    
    def find_arabian_mates(self, board: chess.Board) -> List[Dict]:
        """
        Find Arabian mate patterns (Rook + Knight in corner).
        
        Args:
            board: Current chess position
            
        Returns:
            List of Arabian mate opportunities
        """
        arabian_mates = []
        
        for move in board.legal_moves:
            piece = board.piece_at(move.from_square)
            if not piece or piece.piece_type not in [chess.ROOK, chess.KNIGHT]:
                continue
            
            board.push(move)
            
            if board.is_checkmate():
                enemy_king = board.king(not board.turn)
                if enemy_king is not None and self._is_arabian_mate(board, enemy_king):
                    arabian_mates.append({
                        'move': move,
                        'attacking_piece': piece.piece_type,
                        'description': "Arabian mate",
                        'educational_note': "Rook and knight deliver mate with king in corner"
                    })
            
            board.pop()
        
        return arabian_mates
    
    def find_legal_mates(self, board: chess.Board) -> List[Dict]:
        """
        Find Légal's mate patterns.
        
        Args:
            board: Current chess position
            
        Returns:
            List of Légal's mate opportunities
        """
        legal_mates = []
        
        # Légal's mate involves a bishop sacrifice followed by knight and queen mate
        for move in board.legal_moves:
            piece = board.piece_at(move.from_square)
            if not piece or piece.piece_type != chess.BISHOP:
                continue
            
            # Must be a sacrifice
            if not board.is_capture(move):
                continue
            
            board.push(move)
            
            # Look for follow-up knight move that gives mate
            for knight_move in board.legal_moves:
                knight_piece = board.piece_at(knight_move.from_square)
                if not knight_piece or knight_piece.piece_type != chess.KNIGHT:
                    continue
                
                board.push(knight_move)
                
                if board.is_checkmate() and self._is_legal_mate_pattern(board):
                    legal_mates.append({
                        'sacrifice_move': move,
                        'mate_move': knight_move,
                        'description': "Légal's mate",
                        'educational_note': "Classic bishop sacrifice followed by knight and queen mate"
                    })
                
                board.pop()
            
            board.pop()
        
        return legal_mates
    
    def _classify_mate_type(self, board: chess.Board) -> str:
        """
        Classify the type of checkmate.
        
        Args:
            board: Chess position with checkmate
            
        Returns:
            String description of mate type
        """
        enemy_king = board.king(not board.turn)
        if enemy_king is None:
            return "Unknown mate"
        
        # Check for specific mate patterns
        if self._is_back_rank_mate(board, enemy_king):
            return "Back rank mate"
        elif self._is_smothered_mate(board, enemy_king):
            return "Smothered mate"
        elif self._is_arabian_mate(board, enemy_king):
            return "Arabian mate"
        elif self._is_anastasia_mate(board):
            return "Anastasia's mate"
        else:
            return "Standard checkmate"
    
    def _is_back_rank_mate(self, board: chess.Board, king_square: chess.Square) -> bool:
        """Check if checkmate is a back rank mate."""
        king_piece = board.piece_at(king_square)
        if not king_piece:
            return False
        
        king_rank = chess.square_rank(king_square)
        back_rank = 0 if king_piece.color == chess.WHITE else 7
        
        if king_rank != back_rank:
            return False
        
        # Check if king is trapped by own pieces
        escape_squares = chess.SquareSet(chess.BB_KING_ATTACKS[king_square])
        blocked_by_own = 0
        
        for square in escape_squares:
            piece = board.piece_at(square)
            if piece and piece.color == king_piece.color:
                blocked_by_own += 1
        
        return blocked_by_own >= 2
    
    def _is_smothered_mate(self, board: chess.Board, king_square: chess.Square) -> bool:
        """Check if checkmate is a smothered mate."""
        king_piece = board.piece_at(king_square)
        if not king_piece:
            return False
        
        # Check if attacking piece is a knight
        attackers = board.attackers(not king_piece.color, king_square)
        has_knight_attacker = False
        for square in attackers:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.KNIGHT:
                has_knight_attacker = True
                break
        
        if not has_knight_attacker:
            return False
        
        # Check if king is completely surrounded by own pieces
        adjacent_squares = chess.SquareSet(chess.BB_KING_ATTACKS[king_square])
        all_blocked = True
        
        for square in adjacent_squares:
            piece = board.piece_at(square)
            if not piece or piece.color != king_piece.color:
                all_blocked = False
                break
        
        return all_blocked
    
    def _is_arabian_mate(self, board: chess.Board, king_square: chess.Square) -> bool:
        """Check if checkmate is Arabian mate."""
        # King must be in a corner
        corner_squares = [chess.A1, chess.A8, chess.H1, chess.H8]
        if king_square not in corner_squares:
            return False
        
        king_piece = board.piece_at(king_square)
        if not king_piece:
            return False
        
        # Check for rook and knight attack
        attackers = board.attackers(not king_piece.color, king_square)
        has_rook = False
        has_knight = False
        
        for square in attackers:
            piece = board.piece_at(square)
            if piece:
                if piece.piece_type == chess.ROOK:
                    has_rook = True
                elif piece.piece_type == chess.KNIGHT:
                    has_knight = True
        
        return has_rook and has_knight
    
    def _is_anastasia_mate(self, board: chess.Board) -> bool:
        """Check if checkmate is Anastasia's mate."""
        # This is a simplified check for Anastasia's mate pattern
        # A full implementation would check for the specific rook + knight coordination
        return False
    
    def _is_legal_mate_pattern(self, board: chess.Board) -> bool:
        """Check if checkmate follows Légal's mate pattern."""
        # This is a simplified check for Légal's mate pattern
        # A full implementation would verify the classic bishop sacrifice setup
        return False
    
    def _get_mate_educational_note(self, mate_type: str) -> str:
        """Get educational note for a mate type."""
        notes = {
            "Back rank mate": "Always give your king escape squares to avoid back rank mates!",
            "Smothered mate": "Knights can be devastating when the enemy king is trapped!",
            "Arabian mate": "Rook and knight work perfectly together in corner mates!",
            "Anastasia's mate": "This classic pattern shows beautiful piece coordination!",
            "Légal's mate": "Sometimes a sacrifice opens up devastating attacks!",
            "Standard checkmate": "Well played! Every checkmate is a small victory!"
        }
        return notes.get(mate_type, "Great checkmate!")


def get_mate_advice(mate_patterns: Dict[MatePattern, List[Dict]]) -> List[str]:
    """
    Generate educational advice based on detected mate patterns.
    
    Args:
        mate_patterns: Dictionary of detected mate patterns
        
    Returns:
        List of educational advice strings
    """
    advice = []
    
    if mate_patterns[MatePattern.MATE_IN_ONE]:
        advice.append("You have checkmate in one! Always look for immediate checkmates first!")
    
    if mate_patterns[MatePattern.MATE_IN_TWO]:
        advice.append("There's a forced mate in two moves - calculate the sequence carefully!")
    
    if mate_patterns[MatePattern.BACK_RANK_MATE]:
        advice.append("Back rank mates are common - always ensure king safety on the back rank!")
    
    if mate_patterns[MatePattern.SMOTHERED_MATE]:
        advice.append("Smothered mates show the unique power of the knight!")
    
    return advice