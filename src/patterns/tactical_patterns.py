"""
Advanced tactical pattern recognition for Gotham Chess Engine.

This module implements detection of various tactical motifs that are
essential for strong chess play and educational value.
"""

import chess
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum


class TacticalMotif(Enum):
    """Types of tactical motifs."""
    FORK = "fork"
    PIN = "pin"
    SKEWER = "skewer"
    DISCOVERED_ATTACK = "discovered_attack"
    DEFLECTION = "deflection"
    REMOVING_GUARD = "removing_guard"
    SACRIFICE = "sacrifice"
    EN_PASSANT_TACTIC = "en_passant_tactic"
    BACK_RANK_MATE = "back_rank_mate"
    SMOTHERED_MATE = "smothered_mate"


class GothamTacticalAnalyzer:
    """
    Advanced tactical pattern analyzer for Gotham Chess Engine.
    
    Detects and evaluates tactical motifs in chess positions,
    providing educational insights and move suggestions.
    """
    
    def __init__(self):
        """Initialize the tactical analyzer."""
        self.motif_weights = {
            TacticalMotif.FORK: 50,
            TacticalMotif.PIN: 30,
            TacticalMotif.SKEWER: 40,
            TacticalMotif.DISCOVERED_ATTACK: 45,
            TacticalMotif.DEFLECTION: 35,
            TacticalMotif.REMOVING_GUARD: 35,
            TacticalMotif.SACRIFICE: 60,
            TacticalMotif.EN_PASSANT_TACTIC: 25,
            TacticalMotif.BACK_RANK_MATE: 100,
            TacticalMotif.SMOTHERED_MATE: 100
        }
    
    def analyze_position(self, board: chess.Board) -> Dict[TacticalMotif, List[Dict]]:
        """
        Analyze position for all tactical motifs.
        
        Args:
            board: Current chess position
            
        Returns:
            Dict mapping motifs to their instances
        """
        results = {}
        
        results[TacticalMotif.FORK] = self.find_forks(board)
        results[TacticalMotif.PIN] = self.find_pins(board)
        results[TacticalMotif.SKEWER] = self.find_skewers(board)
        results[TacticalMotif.DISCOVERED_ATTACK] = self.find_discovered_attacks(board)
        results[TacticalMotif.DEFLECTION] = self.find_deflections(board)
        results[TacticalMotif.REMOVING_GUARD] = self.find_removing_guard(board)
        results[TacticalMotif.SACRIFICE] = self.find_sacrifices(board)
        results[TacticalMotif.EN_PASSANT_TACTIC] = self.find_en_passant_tactics(board)
        results[TacticalMotif.BACK_RANK_MATE] = self.find_back_rank_mates(board)
        results[TacticalMotif.SMOTHERED_MATE] = self.find_smothered_mates(board)
        
        return results
    
    def find_forks(self, board: chess.Board) -> List[Dict]:
        """
        Find fork opportunities in the position.
        
        Args:
            board: Current chess position
            
        Returns:
            List of fork opportunities
        """
        forks = []
        
        for move in board.legal_moves:
            # Make the move temporarily
            board.push(move)
            
            piece = board.piece_at(move.to_square)
            if piece and piece.color == board.turn:
                # Count enemy pieces attacked from this square
                attacked_squares = board.attacks(move.to_square)
                enemy_pieces = []
                
                for square in attacked_squares:
                    attacked_piece = board.piece_at(square)
                    if attacked_piece and attacked_piece.color != piece.color:
                        enemy_pieces.append({
                            'square': square,
                            'piece_type': attacked_piece.piece_type,
                            'value': self._get_piece_value(attacked_piece.piece_type)
                        })
                
                # A fork needs at least 2 enemy pieces
                if len(enemy_pieces) >= 2:
                    # Calculate fork value
                    total_value = sum(p['value'] for p in enemy_pieces)
                    
                    forks.append({
                        'move': move,
                        'attacking_piece': piece.piece_type,
                        'forked_pieces': enemy_pieces,
                        'value': total_value,
                        'description': f"{piece.symbol().upper()} fork attacking {len(enemy_pieces)} pieces"
                    })
            
            board.pop()
        
        # Sort by value and return best forks
        forks.sort(key=lambda x: x['value'], reverse=True)
        return forks[:5]  # Return top 5 forks
    
    def find_pins(self, board: chess.Board) -> List[Dict]:
        """
        Find pin opportunities in the position.
        
        Args:
            board: Current chess position
            
        Returns:
            List of pin opportunities
        """
        pins = []
        
        for move in board.legal_moves:
            piece = board.piece_at(move.from_square)
            if not piece or piece.piece_type not in [chess.BISHOP, chess.ROOK, chess.QUEEN]:
                continue
            
            board.push(move)
            
            # Check if this move creates a pin
            pin_info = self._check_for_pin(board, move.to_square, piece.color)
            if pin_info:
                pins.append({
                    'move': move,
                    'attacking_piece': piece.piece_type,
                    'pinned_piece': pin_info['pinned_piece'],
                    'target_piece': pin_info['target_piece'],
                    'value': pin_info['value'],
                    'description': f"Pin {pin_info['pinned_piece'].symbol()} to {pin_info['target_piece'].symbol()}"
                })
            
            board.pop()
        
        pins.sort(key=lambda x: x['value'], reverse=True)
        return pins[:3]  # Return top 3 pins
    
    def find_skewers(self, board: chess.Board) -> List[Dict]:
        """
        Find skewer opportunities in the position.
        
        Args:
            board: Current chess position
            
        Returns:
            List of skewer opportunities
        """
        skewers = []
        
        for move in board.legal_moves:
            piece = board.piece_at(move.from_square)
            if not piece or piece.piece_type not in [chess.BISHOP, chess.ROOK, chess.QUEEN]:
                continue
            
            board.push(move)
            
            # Check if this move creates a skewer
            skewer_info = self._check_for_skewer(board, move.to_square, piece.color)
            if skewer_info:
                skewers.append({
                    'move': move,
                    'attacking_piece': piece.piece_type,
                    'front_piece': skewer_info['front_piece'],
                    'back_piece': skewer_info['back_piece'],
                    'value': skewer_info['value'],
                    'description': f"Skewer {skewer_info['front_piece'].symbol()} winning {skewer_info['back_piece'].symbol()}"
                })
            
            board.pop()
        
        skewers.sort(key=lambda x: x['value'], reverse=True)
        return skewers[:3]  # Return top 3 skewers
    
    def find_discovered_attacks(self, board: chess.Board) -> List[Dict]:
        """
        Find discovered attack opportunities.
        
        Args:
            board: Current chess position
            
        Returns:
            List of discovered attack opportunities
        """
        discovered_attacks = []
        
        for move in board.legal_moves:
            piece = board.piece_at(move.from_square)
            if not piece:
                continue
            
            board.push(move)
            
            # Check if moving this piece reveals an attack from another piece
            discovered_info = self._check_for_discovered_attack(board, move, piece.color)
            if discovered_info:
                discovered_attacks.append({
                    'move': move,
                    'moving_piece': piece.piece_type,
                    'discovering_piece': discovered_info['discovering_piece'],
                    'target': discovered_info['target'],
                    'value': discovered_info['value'],
                    'description': f"Discovered attack by {discovered_info['discovering_piece'].symbol()}"
                })
            
            board.pop()
        
        discovered_attacks.sort(key=lambda x: x['value'], reverse=True)
        return discovered_attacks[:3]
    
    def find_deflections(self, board: chess.Board) -> List[Dict]:
        """
        Find deflection opportunities.
        
        Args:
            board: Current chess position
            
        Returns:
            List of deflection opportunities
        """
        deflections = []
        
        for move in board.legal_moves:
            if not board.is_capture(move):
                continue
            
            captured_piece = board.piece_at(move.to_square)
            if not captured_piece:
                continue
            
            board.push(move)
            
            # Check if capturing this piece deflects it from defending something important
            deflection_info = self._check_for_deflection(board, move, captured_piece)
            if deflection_info:
                deflections.append({
                    'move': move,
                    'deflected_piece': captured_piece.piece_type,
                    'undefended_target': deflection_info['target'],
                    'value': deflection_info['value'],
                    'description': f"Deflection wins {deflection_info['target'].symbol()}"
                })
            
            board.pop()
        
        deflections.sort(key=lambda x: x['value'], reverse=True)
        return deflections[:3]
    
    def find_removing_guard(self, board: chess.Board) -> List[Dict]:
        """
        Find removing the guard opportunities.
        
        Args:
            board: Current chess position
            
        Returns:
            List of removing guard opportunities
        """
        removing_guard = []
        
        for move in board.legal_moves:
            if not board.is_capture(move):
                continue
            
            captured_piece = board.piece_at(move.to_square)
            if not captured_piece:
                continue
            
            board.push(move)
            
            # Check if removing this piece leaves something undefended
            guard_info = self._check_removing_guard(board, move.to_square, captured_piece.color)
            if guard_info:
                removing_guard.append({
                    'move': move,
                    'removed_guard': captured_piece.piece_type,
                    'undefended_piece': guard_info['undefended'],
                    'value': guard_info['value'],
                    'description': f"Remove guard, win {guard_info['undefended'].symbol()}"
                })
            
            board.pop()
        
        removing_guard.sort(key=lambda x: x['value'], reverse=True)
        return removing_guard[:3]
    
    def find_sacrifices(self, board: chess.Board) -> List[Dict]:
        """
        Find tactical sacrifice opportunities.
        
        Args:
            board: Current chess position
            
        Returns:
            List of sacrifice opportunities
        """
        sacrifices = []
        
        for move in board.legal_moves:
            piece = board.piece_at(move.from_square)
            if not piece:
                continue
            
            # Only consider captures and checks for sacrifices
            if not (board.is_capture(move) or board.gives_check(move)):
                continue
            
            board.push(move)
            
            # Check if this creates a winning tactical sequence
            sacrifice_info = self._evaluate_sacrifice(board, move, piece)
            if sacrifice_info and sacrifice_info['net_gain'] > 0:
                sacrifices.append({
                    'move': move,
                    'sacrificed_piece': piece.piece_type,
                    'net_gain': sacrifice_info['net_gain'],
                    'follow_up': sacrifice_info['follow_up'],
                    'description': f"Sacrifice {piece.symbol()} for {sacrifice_info['net_gain']} points"
                })
            
            board.pop()
        
        sacrifices.sort(key=lambda x: x['net_gain'], reverse=True)
        return sacrifices[:3]
    
    def find_en_passant_tactics(self, board: chess.Board) -> List[Dict]:
        """
        Find en passant tactical opportunities.
        
        Args:
            board: Current chess position
            
        Returns:
            List of en passant tactics
        """
        en_passant_tactics = []
        
        if not board.ep_square:
            return en_passant_tactics
        
        for move in board.legal_moves:
            if move.to_square == board.ep_square:
                board.push(move)
                
                # Evaluate the position after en passant
                tactic_value = self._evaluate_en_passant_tactic(board, move)
                if tactic_value > 0:
                    en_passant_tactics.append({
                        'move': move,
                        'value': tactic_value,
                        'description': "En passant wins material or position"
                    })
                
                board.pop()
        
        return en_passant_tactics
    
    def find_back_rank_mates(self, board: chess.Board) -> List[Dict]:
        """
        Find back rank mate opportunities.
        
        Args:
            board: Current chess position
            
        Returns:
            List of back rank mate opportunities
        """
        back_rank_mates = []
        
        for move in board.legal_moves:
            board.push(move)
            
            if board.is_checkmate():
                # Check if this is a back rank mate
                enemy_king = board.king(not board.turn)
                if enemy_king is not None:
                    king_rank = chess.square_rank(enemy_king)
                    expected_rank = 0 if not board.turn == chess.WHITE else 7
                    
                    if king_rank == expected_rank:
                        back_rank_mates.append({
                            'move': move,
                            'description': "Back rank mate",
                            'value': 1000  # Checkmate value
                        })
            
            board.pop()
        
        return back_rank_mates
    
    def find_smothered_mates(self, board: chess.Board) -> List[Dict]:
        """
        Find smothered mate opportunities.
        
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
                # Check if enemy king is surrounded by own pieces
                enemy_king = board.king(not board.turn)
                if enemy_king is not None and self._is_smothered_mate(board, enemy_king):
                    smothered_mates.append({
                        'move': move,
                        'description': "Smothered mate",
                        'value': 1000  # Checkmate value
                    })
            
            board.pop()
        
        return smothered_mates
    
    def _get_piece_value(self, piece_type: chess.PieceType) -> int:
        """Get the standard value of a piece."""
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        return values.get(piece_type, 0)
    
    def _check_for_pin(self, board: chess.Board, attacker_square: chess.Square, 
                      attacker_color: chess.Color) -> Optional[Dict]:
        """Check if a piece creates a pin from the given square."""
        # This is a simplified implementation
        # A full implementation would use ray-casting to detect pins
        return None
    
    def _check_for_skewer(self, board: chess.Board, attacker_square: chess.Square, 
                         attacker_color: chess.Color) -> Optional[Dict]:
        """Check if a piece creates a skewer from the given square."""
        # This is a simplified implementation
        # A full implementation would use ray-casting to detect skewers
        return None
    
    def _check_for_discovered_attack(self, board: chess.Board, move: chess.Move, 
                                   color: chess.Color) -> Optional[Dict]:
        """Check if a move creates a discovered attack."""
        # This is a simplified implementation
        return None
    
    def _check_for_deflection(self, board: chess.Board, move: chess.Move, 
                            captured_piece: chess.Piece) -> Optional[Dict]:
        """Check if capturing a piece deflects it from defending something."""
        # This is a simplified implementation
        return None
    
    def _check_removing_guard(self, board: chess.Board, square: chess.Square, 
                            color: chess.Color) -> Optional[Dict]:
        """Check if removing a piece leaves something undefended."""
        # This is a simplified implementation
        return None
    
    def _evaluate_sacrifice(self, board: chess.Board, move: chess.Move, 
                          piece: chess.Piece) -> Optional[Dict]:
        """Evaluate if a sacrifice is tactically sound."""
        # This is a simplified implementation
        return None
    
    def _evaluate_en_passant_tactic(self, board: chess.Board, move: chess.Move) -> int:
        """Evaluate the tactical value of an en passant capture."""
        # Basic implementation - en passant usually wins a pawn
        return 1
    
    def _is_smothered_mate(self, board: chess.Board, king_square: chess.Square) -> bool:
        """Check if a checkmate is a smothered mate."""
        king_piece = board.piece_at(king_square)
        if not king_piece:
            return False
        
        # Check if king is surrounded by own pieces
        adjacent_squares = chess.SquareSet(chess.BB_KING_ATTACKS[king_square])
        own_pieces_count = 0
        
        for square in adjacent_squares:
            piece = board.piece_at(square)
            if piece and piece.color == king_piece.color:
                own_pieces_count += 1
        
        # Smothered mate typically has king surrounded by own pieces
        return own_pieces_count >= 6


def get_tactical_advice(motifs: Dict[TacticalMotif, List[Dict]]) -> List[str]:
    """
    Generate educational advice based on detected tactical motifs.
    
    Args:
        motifs: Dictionary of detected tactical motifs
        
    Returns:
        List of educational advice strings
    """
    advice = []
    
    if motifs[TacticalMotif.FORK]:
        advice.append("Look for fork opportunities - knights are especially good at this!")
    
    if motifs[TacticalMotif.PIN]:
        advice.append("Pins can be very powerful - the pinned piece can't move!")
    
    if motifs[TacticalMotif.DISCOVERED_ATTACK]:
        advice.append("Discovered attacks often win material - move one piece to reveal another's attack!")
    
    if motifs[TacticalMotif.BACK_RANK_MATE]:
        advice.append("Back rank mates are deadly - always ensure your king has escape squares!")
    
    if motifs[TacticalMotif.SACRIFICE]:
        advice.append("Sometimes sacrificing material leads to bigger gains - calculate carefully!")
    
    return advice