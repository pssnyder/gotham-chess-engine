#!/usr/bin/env python3
"""
Tactical Pattern Recognition - Best Practices Implementation
============================================================

This module demonstrates different approaches to implementing the exact tactical
motifs specified in the README using modern chess engine best practices.

Tactical Motifs Required (from README):
- Forks, discovered attacks, pins, skewers
- Removing the guard, deflections, sacrifices
- En passant captures
- Mate in 1/2 patterns
- Back rank mates, smothered mates, basic mating nets
"""

import chess
from typing import Dict, List, Tuple, Set, Optional
from enum import Enum


class TacticalMotif(Enum):
    """Exact tactical motifs from README requirements."""
    FORK = "fork"
    DISCOVERED_ATTACK = "discovered_attack"
    PIN = "pin" 
    SKEWER = "skewer"
    REMOVE_GUARD = "remove_guard"
    DEFLECTION = "deflection"
    SACRIFICE = "sacrifice"
    EN_PASSANT = "en_passant"
    MATE_IN_ONE = "mate_in_one"
    MATE_IN_TWO = "mate_in_two"
    BACK_RANK_MATE = "back_rank_mate"
    SMOTHERED_MATE = "smothered_mate"


class TacticalPatternRecognizer:
    """
    Modern implementation of tactical pattern recognition.
    
    Uses three best practice approaches:
    1. Move-based pattern detection (during move generation)
    2. Positional pattern analysis (static evaluation)
    3. Attack/defend relationship mapping (for pins/skewers)
    """
    
    def __init__(self):
        """Initialize the tactical recognizer."""
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 0  # King is invaluable
        }
    
    def analyze_move_tactics(self, board: chess.Board, move: chess.Move) -> Dict[TacticalMotif, float]:
        """
        Analyze a specific move for tactical motifs (Best Practice #1).
        
        This approach evaluates tactics as part of move generation,
        which is more efficient than static position analysis.
        """
        tactics_found = {}
        
        # Make the move on a copy
        temp_board = board.copy()
        temp_board.push(move)
        
        # Check for immediate mate patterns
        if temp_board.is_checkmate():
            tactics_found[TacticalMotif.MATE_IN_ONE] = 10000.0
            return tactics_found
        
        # Analyze the move for specific patterns
        moving_piece = board.piece_at(move.from_square)
        if not moving_piece:
            return tactics_found
        
        # Fork detection (README requirement)
        fork_value = self._detect_fork(temp_board, move.to_square, moving_piece.color)
        if fork_value > 0:
            tactics_found[TacticalMotif.FORK] = fork_value
        
        # Pin detection (README requirement)
        pin_value = self._detect_pin_creation(board, temp_board, move)
        if pin_value > 0:
            tactics_found[TacticalMotif.PIN] = pin_value
        
        # Skewer detection (README requirement)
        skewer_value = self._detect_skewer_creation(board, temp_board, move)
        if skewer_value > 0:
            tactics_found[TacticalMotif.SKEWER] = skewer_value
        
        # Discovered attack (README requirement)
        discovered_value = self._detect_discovered_attack(board, move)
        if discovered_value > 0:
            tactics_found[TacticalMotif.DISCOVERED_ATTACK] = discovered_value
        
        # Deflection/Remove guard (README requirement)
        deflection_value = self._detect_deflection(board, temp_board, move)
        if deflection_value > 0:
            tactics_found[TacticalMotif.DEFLECTION] = deflection_value
        
        # Sacrifice detection (README requirement)
        sacrifice_value = self._detect_sacrifice(board, move)
        if sacrifice_value > 0:
            tactics_found[TacticalMotif.SACRIFICE] = sacrifice_value
        
        # En passant (README requirement)
        if board.is_en_passant(move):
            tactics_found[TacticalMotif.EN_PASSANT] = 100.0
        
        # Back rank mate threat (README requirement)
        back_rank_value = self._detect_back_rank_threat(temp_board, moving_piece.color)
        if back_rank_value > 0:
            tactics_found[TacticalMotif.BACK_RANK_MATE] = back_rank_value
        
        return tactics_found
    
    def _detect_fork(self, board: chess.Board, square: chess.Square, color: chess.Color) -> float:
        """
        Detect fork patterns (README requirement).
        
        A fork attacks two or more enemy pieces simultaneously.
        Best practice: Use attack bitboards for efficiency.
        """
        piece = board.piece_at(square)
        if not piece or piece.color != color:
            return 0.0
        
        # Get all squares attacked by this piece
        attacked_squares = board.attacks(square)
        
        # Count valuable enemy pieces under attack
        attacked_pieces = []
        for target_square in attacked_squares:
            target = board.piece_at(target_square)
            if target and target.color != color:
                attacked_pieces.append(target)
        
        # Fork requires attacking 2+ pieces
        if len(attacked_pieces) < 2:
            return 0.0
        
        # Calculate fork value based on pieces attacked
        total_value = sum(self.piece_values[p.piece_type] for p in attacked_pieces)
        
        # Bonus for royal fork (king + other piece)
        has_king = any(p.piece_type == chess.KING for p in attacked_pieces)
        if has_king:
            return total_value * 2.0  # Royal fork is especially valuable
        
        return total_value * 0.8  # Regular fork
    
    def _detect_pin_creation(self, board_before: chess.Board, board_after: chess.Board, move: chess.Move) -> float:
        """
        Detect pin creation (README requirement).
        
        Best practice: Compare before/after board states to detect new pins.
        """
        moving_piece = board_before.piece_at(move.from_square)
        if not moving_piece:
            return 0.0
        
        # Only long-range pieces can create pins
        if moving_piece.piece_type not in [chess.BISHOP, chess.ROOK, chess.QUEEN]:
            return 0.0
        
        # Check for pins along the piece's attack lines
        return self._check_pin_lines(board_after, move.to_square, moving_piece)
    
    def _check_pin_lines(self, board: chess.Board, piece_square: chess.Square, piece: chess.Piece) -> float:
        """Check for pins along attack lines."""
        pin_value = 0.0
        
        # Get attack directions for this piece type
        directions = self._get_attack_directions(piece.piece_type)
        
        for direction in directions:
            pin_value += self._check_single_direction_pin(board, piece_square, direction, piece.color)
        
        return pin_value
    
    def _check_single_direction_pin(self, board: chess.Board, start_square: chess.Square, 
                                   direction: int, attacker_color: chess.Color) -> float:
        """Check for pin in a single direction."""
        squares_in_direction = []
        current = start_square
        
        # Trace along the direction
        for _ in range(7):  # Max 7 squares in any direction
            current += direction
            if not (0 <= chess.square_file(current) <= 7 and 0 <= chess.square_rank(current) <= 7):
                break
            squares_in_direction.append(current)
        
        # Look for pin pattern: attacker -> enemy piece -> valuable enemy piece
        pieces_found = []
        for square in squares_in_direction:
            piece = board.piece_at(square)
            if piece:
                pieces_found.append((square, piece))
                if piece.color == attacker_color:
                    break  # Our own piece blocks the line
        
        # Check if we have a pin (2 enemy pieces in line)
        if len(pieces_found) >= 2:
            enemy_pieces = [p for s, p in pieces_found if p.color != attacker_color]
            if len(enemy_pieces) >= 2:
                # Pin detected: first piece is pinned to second piece
                pinned_value = self.piece_values[enemy_pieces[0].piece_type]
                behind_value = self.piece_values[enemy_pieces[1].piece_type]
                
                if behind_value > pinned_value:
                    return pinned_value * 0.7  # Pin value
        
        return 0.0
    
    def _detect_skewer_creation(self, board_before: chess.Board, board_after: chess.Board, move: chess.Move) -> float:
        """
        Detect skewer creation (README requirement).
        
        Skewer: valuable piece in front, less valuable behind.
        """
        # Similar to pin but with value ordering reversed
        moving_piece = board_before.piece_at(move.from_square)
        if not moving_piece or moving_piece.piece_type not in [chess.BISHOP, chess.ROOK, chess.QUEEN]:
            return 0.0
        
        return self._check_skewer_lines(board_after, move.to_square, moving_piece)
    
    def _check_skewer_lines(self, board: chess.Board, piece_square: chess.Square, piece: chess.Piece) -> float:
        """Check for skewers along attack lines."""
        skewer_value = 0.0
        directions = self._get_attack_directions(piece.piece_type)
        
        for direction in directions:
            skewer_value += self._check_single_direction_skewer(board, piece_square, direction, piece.color)
        
        return skewer_value
    
    def _check_single_direction_skewer(self, board: chess.Board, start_square: chess.Square,
                                      direction: int, attacker_color: chess.Color) -> float:
        """Check for skewer in a single direction."""
        squares_in_direction = []
        current = start_square
        
        for _ in range(7):
            current += direction
            if not (0 <= chess.square_file(current) <= 7 and 0 <= chess.square_rank(current) <= 7):
                break
            squares_in_direction.append(current)
        
        pieces_found = []
        for square in squares_in_direction:
            piece = board.piece_at(square)
            if piece:
                pieces_found.append((square, piece))
                if piece.color == attacker_color:
                    break
        
        # Check for skewer pattern
        if len(pieces_found) >= 2:
            enemy_pieces = [p for s, p in pieces_found if p.color != attacker_color]
            if len(enemy_pieces) >= 2:
                front_value = self.piece_values[enemy_pieces[0].piece_type]
                back_value = self.piece_values[enemy_pieces[1].piece_type]
                
                if front_value > back_value:
                    return back_value * 0.9  # We'll likely win the back piece
        
        return 0.0
    
    def _detect_discovered_attack(self, board: chess.Board, move: chess.Move) -> float:
        """
        Detect discovered attacks (README requirement).
        
        When moving piece uncovers an attack from behind.
        """
        moving_piece = board.piece_at(move.from_square)
        if not moving_piece:
            return 0.0
        
        # Check if there's a long-range piece behind the moving piece
        from_square = move.from_square
        discovered_value = 0.0
        
        # Check all directions from the from_square
        for direction in [-9, -8, -7, -1, 1, 7, 8, 9]:  # All 8 directions
            discovered_value += self._check_discovered_in_direction(board, from_square, direction, moving_piece.color)
        
        return discovered_value
    
    def _check_discovered_in_direction(self, board: chess.Board, from_square: chess.Square,
                                      direction: int, moving_color: chess.Color) -> float:
        """Check for discovered attack in one direction."""
        # Look behind the moving piece
        current = from_square - direction
        
        # Find the piece that will be uncovered
        uncovered_piece = None
        while 0 <= chess.square_file(current) <= 7 and 0 <= chess.square_rank(current) <= 7:
            piece = board.piece_at(current)
            if piece:
                if piece.color == moving_color:
                    uncovered_piece = piece
                break
            current -= direction
        
        if not uncovered_piece or uncovered_piece.piece_type not in [chess.BISHOP, chess.ROOK, chess.QUEEN]:
            return 0.0
        
        # Check what the uncovered piece will attack
        current = from_square + direction
        attacked_value = 0.0
        
        while 0 <= chess.square_file(current) <= 7 and 0 <= chess.square_rank(current) <= 7:
            piece = board.piece_at(current)
            if piece:
                if piece.color != moving_color:
                    attacked_value += self.piece_values[piece.piece_type]
                break
            current += direction
        
        return attacked_value * 0.6  # Discovered attack bonus
    
    def _detect_deflection(self, board_before: chess.Board, board_after: chess.Board, move: chess.Move) -> float:
        """
        Detect deflection/remove guard (README requirement).
        
        Forces a defending piece to move away from what it's defending.
        """
        if not board_before.is_capture(move):
            return 0.0
        
        captured_piece = board_before.piece_at(move.to_square)
        if not captured_piece:
            return 0.0
        
        # Check if the captured piece was defending something valuable
        defended_value = self._calculate_defense_loss(board_before, board_after, move.to_square, captured_piece.color)
        
        if defended_value > 0:
            return defended_value * 0.8  # Deflection value
        
        return 0.0
    
    def _calculate_defense_loss(self, board_before: chess.Board, board_after: chess.Board,
                               defender_square: chess.Square, defender_color: chess.Color) -> float:
        """Calculate the value of pieces that lost their defender."""
        # This is complex - simplified version for now
        # In a full implementation, you'd check all pieces the defender was protecting
        return 0.0  # Placeholder - would need full implementation
    
    def _detect_sacrifice(self, board: chess.Board, move: chess.Move) -> float:
        """
        Detect tactical sacrifices (README requirement).
        
        Giving up material for positional or tactical advantage.
        """
        if not board.is_capture(move):
            return 0.0
        
        captured_piece = board.piece_at(move.to_square)
        moving_piece = board.piece_at(move.from_square)
        
        if not captured_piece or not moving_piece:
            return 0.0
        
        captured_value = self.piece_values[captured_piece.piece_type]
        moving_value = self.piece_values[moving_piece.piece_type]
        
        # Sacrifice if we're giving up more material
        if moving_value > captured_value:
            material_deficit = moving_value - captured_value
            
            # Check if sacrifice leads to immediate tactical gain
            temp_board = board.copy()
            temp_board.push(move)
            
            # Look for tactical follow-ups (simplified)
            if temp_board.is_check():
                return material_deficit * 0.5  # Sacrifice for check
            
            # Could add more sophisticated sacrifice detection here
            
        return 0.0
    
    def _detect_back_rank_threat(self, board: chess.Board, color: chess.Color) -> float:
        """
        Detect back rank mate threats (README requirement).
        """
        enemy_color = not color
        back_rank = 0 if enemy_color == chess.WHITE else 7
        
        # Check if enemy king is on back rank with limited escape squares
        enemy_king_square = board.king(enemy_color)
        if enemy_king_square is None:
            return 0.0
        
        if chess.square_rank(enemy_king_square) == back_rank:
            # Count escape squares
            escape_squares = 0
            king_file = chess.square_file(enemy_king_square)
            
            for file_offset in [-1, 0, 1]:
                for rank_offset in [0, 1] if enemy_color == chess.WHITE else [0, -1]:
                    escape_file = king_file + file_offset
                    escape_rank = back_rank + rank_offset
                    
                    if 0 <= escape_file <= 7 and 0 <= escape_rank <= 7:
                        escape_square = chess.square(escape_file, escape_rank)
                        if not board.piece_at(escape_square):
                            escape_squares += 1
            
            if escape_squares <= 1:
                return 500.0  # High value for back rank mate threat
        
        return 0.0
    
    def _get_attack_directions(self, piece_type: chess.PieceType) -> List[int]:
        """Get attack directions for piece type."""
        if piece_type == chess.ROOK:
            return [-8, 8, -1, 1]  # Vertical and horizontal
        elif piece_type == chess.BISHOP:
            return [-9, -7, 7, 9]  # Diagonals
        elif piece_type == chess.QUEEN:
            return [-9, -8, -7, -1, 1, 7, 8, 9]  # All directions
        return []


def create_enhanced_tactical_evaluator():
    """
    Create the enhanced tactical evaluation function to replace the current one.
    
    This uses the TacticalPatternRecognizer with best practices.
    """
    
    def _evaluate_tactical_factors_enhanced(self, board) -> float:
        """
        Enhanced tactical evaluation using modern pattern recognition.
        
        This replaces the existing _evaluate_tactical_factors method.
        """
        recognizer = TacticalPatternRecognizer()
        total_score = 0.0
        
        # Analyze each legal move for tactical opportunities
        for move in board.legal_moves:
            tactics = recognizer.analyze_move_tactics(board, move)
            
            # Sum up tactical values for this move
            move_tactical_value = sum(tactics.values())
            
            # Apply to score based on whose turn it is
            if board.turn == chess.WHITE:
                total_score += move_tactical_value * 0.1  # Scale factor
            else:
                total_score -= move_tactical_value * 0.1
        
        return total_score
    
    return _evaluate_tactical_factors_enhanced


# Test function to validate against README puzzle requirements
def test_against_readme_puzzles():
    """Test the tactical recognizer against the exact puzzles from README."""
    
    # Fork puzzle from README
    fork_fen = "5rk1/5ppp/4p3/4N3/8/1Pn5/5PPP/5RK1 w - - 0 28"
    
    print("Testing tactical recognition on README puzzles:")
    print(f"Fork puzzle: {fork_fen}")
    
    board = chess.Board(fork_fen)
    recognizer = TacticalPatternRecognizer()
    
    # Test the expected solution move
    solution_move = chess.Move.from_uci("f1c1")  # From README
    
    if solution_move in board.legal_moves:
        tactics = recognizer.analyze_move_tactics(board, solution_move)
        print(f"Solution move {solution_move} tactics found: {tactics}")
    else:
        print(f"Solution move {solution_move} not legal")
    
    # Test other moves for comparison
    for move in list(board.legal_moves)[:5]:  # First 5 moves
        tactics = recognizer.analyze_move_tactics(board, move)
        if tactics:
            print(f"Move {move}: {tactics}")


if __name__ == "__main__":
    test_against_readme_puzzles()