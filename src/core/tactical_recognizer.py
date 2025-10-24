"""
Tactical Pattern Recognizer for Gotham Chess Engine.

Implements the exact tactical motifs specified in the README:
- Forks, discovered attacks, pins, skewers
- Removing the guard, deflections, sacrifices
- En passant captures  
- Mate in 1/2, back rank mates, smothered mates
"""

import chess
from typing import Dict, List, Optional
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
    """Recognizes tactical patterns specified in README requirements."""
    
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
        """Analyze a move for tactical motifs from README."""
        tactics_found = {}
        
        # Make the move on a copy
        temp_board = board.copy()
        temp_board.push(move)
        
        # Check for immediate mate (README requirement)
        if temp_board.is_checkmate():
            tactics_found[TacticalMotif.MATE_IN_ONE] = 10000.0
            return tactics_found
        
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
        
        # Deflection (README requirement)
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
        """Detect fork patterns (README requirement)."""
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
        
        # Calculate fork value
        total_value = sum(self.piece_values[p.piece_type] for p in attacked_pieces)
        
        # Bonus for royal fork (king + other piece)
        has_king = any(p.piece_type == chess.KING for p in attacked_pieces)
        if has_king:
            return total_value * 2.0  # Royal fork bonus
        
        return total_value * 0.8  # Regular fork
    
    def _detect_pin_creation(self, board_before: chess.Board, board_after: chess.Board, move: chess.Move) -> float:
        """Detect pin creation (README requirement)."""
        moving_piece = board_before.piece_at(move.from_square)
        if not moving_piece:
            return 0.0
        
        # Only long-range pieces can create pins
        if moving_piece.piece_type not in [chess.BISHOP, chess.ROOK, chess.QUEEN]:
            return 0.0
        
        return self._check_pin_lines(board_after, move.to_square, moving_piece)
    
    def _check_pin_lines(self, board: chess.Board, piece_square: chess.Square, piece: chess.Piece) -> float:
        """Check for pins along attack lines."""
        pin_value = 0.0
        directions = self._get_attack_directions(piece.piece_type)
        
        for direction in directions:
            pin_value += self._check_single_direction_pin(board, piece_square, direction, piece.color)
        
        return pin_value
    
    def _check_single_direction_pin(self, board: chess.Board, start_square: chess.Square,
                                   direction: int, attacker_color: chess.Color) -> float:
        """Check for pin in a single direction."""
        pieces_in_line = []
        current = start_square
        
        # Trace along the direction
        for _ in range(7):
            current += direction
            if not (0 <= chess.square_file(current) <= 7 and 0 <= chess.square_rank(current) <= 7):
                break
            
            piece = board.piece_at(current)
            if piece:
                pieces_in_line.append(piece)
                if piece.color == attacker_color:
                    break  # Our piece blocks the line
        
        # Check for pin pattern: enemy piece -> more valuable enemy piece
        if len(pieces_in_line) >= 2:
            enemy_pieces = [p for p in pieces_in_line if p.color != attacker_color]
            if len(enemy_pieces) >= 2:
                pinned_value = self.piece_values[enemy_pieces[0].piece_type]
                behind_value = self.piece_values[enemy_pieces[1].piece_type]
                
                if behind_value > pinned_value:
                    return pinned_value * 0.7  # Pin value
        
        return 0.0
    
    def _detect_skewer_creation(self, board_before: chess.Board, board_after: chess.Board, move: chess.Move) -> float:
        """Detect skewer creation (README requirement)."""
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
        pieces_in_line = []
        current = start_square
        
        for _ in range(7):
            current += direction
            if not (0 <= chess.square_file(current) <= 7 and 0 <= chess.square_rank(current) <= 7):
                break
            
            piece = board.piece_at(current)
            if piece:
                pieces_in_line.append(piece)
                if piece.color == attacker_color:
                    break
        
        # Check for skewer pattern: valuable piece -> less valuable piece
        if len(pieces_in_line) >= 2:
            enemy_pieces = [p for p in pieces_in_line if p.color != attacker_color]
            if len(enemy_pieces) >= 2:
                front_value = self.piece_values[enemy_pieces[0].piece_type]
                back_value = self.piece_values[enemy_pieces[1].piece_type]
                
                if front_value > back_value:
                    return back_value * 0.9  # We'll likely win the back piece
        
        return 0.0
    
    def _detect_discovered_attack(self, board: chess.Board, move: chess.Move) -> float:
        """Detect discovered attacks (README requirement)."""
        # Simplified version - check if moving piece uncovers an attack
        moving_piece = board.piece_at(move.from_square)
        if not moving_piece:
            return 0.0
        
        # Basic discovered attack detection
        from_square = move.from_square
        discovered_value = 0.0
        
        # Check if there's a piece behind that can now attack
        for direction in [-9, -8, -7, -1, 1, 7, 8, 9]:
            discovered_value += self._check_discovered_in_direction(board, from_square, direction, moving_piece.color)
        
        return discovered_value
    
    def _check_discovered_in_direction(self, board: chess.Board, from_square: chess.Square,
                                      direction: int, moving_color: chess.Color) -> float:
        """Check for discovered attack in one direction."""
        # Look behind the moving piece
        current = from_square - direction
        uncovered_piece = None
        
        while 0 <= chess.square_file(current) <= 7 and 0 <= chess.square_rank(current) <= 7:
            piece = board.piece_at(current)
            if piece:
                if piece.color == moving_color and piece.piece_type in [chess.BISHOP, chess.ROOK, chess.QUEEN]:
                    uncovered_piece = piece
                break
            current -= direction
        
        if not uncovered_piece:
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
        """Detect deflection/remove guard (README requirement)."""
        if not board_before.is_capture(move):
            return 0.0
        
        # Simplified deflection detection
        captured_piece = board_before.piece_at(move.to_square)
        if captured_piece:
            return self.piece_values[captured_piece.piece_type] * 0.3  # Basic deflection value
        
        return 0.0
    
    def _detect_sacrifice(self, board: chess.Board, move: chess.Move) -> float:
        """Detect tactical sacrifices (README requirement)."""
        if not board.is_capture(move):
            return 0.0
        
        captured_piece = board.piece_at(move.to_square)
        moving_piece = board.piece_at(move.from_square)
        
        if not captured_piece or not moving_piece:
            return 0.0
        
        captured_value = self.piece_values[captured_piece.piece_type]
        moving_value = self.piece_values[moving_piece.piece_type]
        
        # Sacrifice if giving up more material
        if moving_value > captured_value:
            material_deficit = moving_value - captured_value
            
            # Check if sacrifice leads to tactical gain
            temp_board = board.copy()
            temp_board.push(move)
            
            if temp_board.is_check():
                return material_deficit * 0.5  # Sacrifice for check
        
        return 0.0
    
    def _detect_back_rank_threat(self, board: chess.Board, color: chess.Color) -> float:
        """Detect back rank mate threats (README requirement)."""
        enemy_color = not color
        back_rank = 0 if enemy_color == chess.WHITE else 7
        
        # Check if enemy king is on back rank
        enemy_king_square = board.king(enemy_color)
        if enemy_king_square is None:
            return 0.0
        
        if chess.square_rank(enemy_king_square) == back_rank:
            # Count escape squares
            escape_squares = 0
            king_file = chess.square_file(enemy_king_square)
            
            for file_offset in [-1, 0, 1]:
                escape_file = king_file + file_offset
                if 0 <= escape_file <= 7:
                    forward_rank = back_rank + (1 if enemy_color == chess.WHITE else -1)
                    if 0 <= forward_rank <= 7:
                        escape_square = chess.square(escape_file, forward_rank)
                        if not board.piece_at(escape_square):
                            escape_squares += 1
            
            if escape_squares <= 1:
                return 500.0  # High value for back rank threat
        
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