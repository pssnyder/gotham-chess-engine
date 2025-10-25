"""
Main Gotham Chess Engine implementation.

This module provides the core engine that coordinates all components
and provides both UCI interface and educational features.
"""

import chess
import chess.engine
from typing import Optional, Dict, List, Any
import time
import random

from .core.board import GothamBoard, GamePhase
from .core.pieces import GothamPieceEvaluator, GothamTacticalPatterns
from .openings.opening_book import GothamOpeningBook


class GothamChessEngine:
    """
    Main chess engine implementing Gotham Chess principles.
    
    This engine provides:
    - Educational move suggestions with explanations
    - Opening book based on Gotham Chess recommendations
    - Tactical pattern recognition
    - Principled position evaluation
    """
    
    def __init__(self, time_limit: float = 1.0):
        """
        Initialize the Gotham Chess Engine.
        
        Args:
            time_limit: Time limit for move calculation in seconds
        """
        self.board = GothamBoard()
        self.opening_book = GothamOpeningBook()
        self.piece_evaluator = GothamPieceEvaluator()
        self.tactical_patterns = GothamTacticalPatterns()
        
        # Initialize tactical recognizer for best practices evaluation
        from .core.tactical_recognizer import TacticalPatternRecognizer
        self._tactical_recognizer = TacticalPatternRecognizer()
        
        self.time_limit = time_limit
        self.search_depth = 4  # Default search depth
        self.educational_mode = True
        
    def set_position(self, fen: Optional[str] = None) -> None:
        """
        Set the board position.
        
        Args:
            fen: FEN string for the position (None for starting position)
        """
        self.board = GothamBoard(fen)
    
    def make_move(self, move: chess.Move) -> bool:
        """
        Make a move on the board.
        
        Args:
            move: Move to make
            
        Returns:
            bool: True if move was legal and made
        """
        if move in self.board.legal_moves:
            self.board.make_educational_move(move)
            return True
        return False
    
    def get_best_move(self) -> Optional[chess.Move]:
        """
        Get the best move for the current position.
        
        Returns:
            Optional[chess.Move]: Best move or None if no legal moves
        """
        if self.board.is_game_over():
            return None
        
        start_time = time.time()
        
        # Check opening book first
        opening_move = self.opening_book.get_opening_move(self.board, self.board.turn)
        if opening_move:
            return opening_move
        
        # Determine search depth based on tactical potential
        search_depth = self._get_adaptive_search_depth(self.board)
        
        # Use search algorithm for middle game and endgame
        best_move, _ = self._minimax(
            self.board, 
            search_depth, 
            -float('inf'), 
            float('inf'), 
            self.board.turn,
            start_time
        )
        
        return best_move
    
    def _minimax(self, board: GothamBoard, depth: int, alpha: float, beta: float, 
                maximizing_player: bool, start_time: float) -> tuple[Optional[chess.Move], float]:
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            board: Current board position
            depth: Search depth remaining
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing_player: Whether this is the maximizing player
            start_time: Start time for time management
            
        Returns:
            Tuple[Optional[chess.Move], float]: Best move and evaluation
        """
        # Time check
        if time.time() - start_time > self.time_limit:
            return None, self.evaluate_position(board)
        
        # Base case - use quiescence search for tactical positions
        if depth == 0 or board.is_game_over():
            if board.is_game_over():
                return None, self.evaluate_position(board)
            # Use quiescence search to handle tactical sequences
            return None, self._quiescence_search(board, alpha, beta, maximizing_player, start_time)
        
        best_move = None
        
        if maximizing_player:
            max_eval = -float('inf')
            for move in self._order_moves(board, list(board.legal_moves)):
                board.push(move)
                _, eval_score = self._minimax(board, depth - 1, alpha, beta, False, start_time)
                board.pop()
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            
            return best_move, max_eval
        else:
            min_eval = float('inf')
            for move in self._order_moves(board, list(board.legal_moves)):
                board.push(move)
                _, eval_score = self._minimax(board, depth - 1, alpha, beta, True, start_time)
                board.pop()
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            
            return best_move, min_eval
    
    def _quiescence_search(self, board: GothamBoard, alpha: float, beta: float, 
                          maximizing_player: bool, start_time: float, depth: int = 0) -> float:
        """
        Quiescence search for tactical sequences.
        
        Continues searching beyond normal depth for captures, checks, and promotions
        to avoid horizon effect in tactical positions.
        
        Args:
            board: Current board position
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing_player: Whether this is the maximizing player
            start_time: Start time for time management
            depth: Current quiescence depth (for limiting)
            
        Returns:
            float: Position evaluation
        """
        # Time check
        if time.time() - start_time > self.time_limit:
            return self.evaluate_position(board)
        
        # Limit quiescence depth to avoid infinite search
        if depth > 3:  # Reduced from 6 to 3 for efficiency
            return self.evaluate_position(board)
        
        # Stand pat evaluation - can we improve without making a move?
        stand_pat = self.evaluate_position(board)
        
        if maximizing_player:
            if stand_pat >= beta:
                return beta  # Beta cutoff
            alpha = max(alpha, stand_pat)
        else:
            if stand_pat <= alpha:
                return alpha  # Alpha cutoff
            beta = min(beta, stand_pat)
        
        # Generate only "noisy" moves (captures, checks, promotions)
        noisy_moves = self._get_noisy_moves(board)
        
        if not noisy_moves:
            return stand_pat  # No tactical moves, return stand pat
        
        # Order the noisy moves by tactical value
        ordered_moves = self._order_moves(board, noisy_moves)
        
        if maximizing_player:
            max_eval = stand_pat
            for move in ordered_moves:
                board.push(move)
                eval_score = self._quiescence_search(board, alpha, beta, False, start_time, depth + 1)
                board.pop()
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            
            return max_eval
        else:
            min_eval = stand_pat
            for move in ordered_moves:
                board.push(move)
                eval_score = self._quiescence_search(board, alpha, beta, True, start_time, depth + 1)
                board.pop()
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            
            return min_eval
    
    def _get_noisy_moves(self, board: GothamBoard) -> List[chess.Move]:
        """
        Get 'noisy' moves that should be searched in quiescence.
        
        Args:
            board: Current board position
            
        Returns:
            List[chess.Move]: List of tactical moves to search
        """
        noisy_moves = []
        
        for move in board.legal_moves:
            # Good captures only (winning material)
            if board.is_capture(move):
                captured_piece = board.piece_at(move.to_square)
                moving_piece = board.piece_at(move.from_square)
                if captured_piece and moving_piece:
                    captured_value = self.piece_evaluator.get_piece_value(captured_piece.piece_type)
                    moving_value = self.piece_evaluator.get_piece_value(moving_piece.piece_type)
                    # Only include captures that don't lose material or equal trades of valuable pieces
                    if captured_value >= moving_value or captured_value >= 300:
                        noisy_moves.append(move)
            # Checks that aren't just moving to safety
            elif self._gives_check(board, move):
                # Only include checks if the checking piece isn't hanging
                temp_board = board.copy()
                temp_board.push(move)
                if not temp_board.is_attacked_by(not board.turn, move.to_square):
                    noisy_moves.append(move)
            # Promotions (always tactical)
            elif move.promotion:
                noisy_moves.append(move)
            # High-value tactical moves only
            elif hasattr(self, '_tactical_recognizer'):
                tactics = self._tactical_recognizer.analyze_move_tactics(board, move)
                if tactics:
                    total_value = sum(tactics.values())
                    if total_value >= 200:  # Only high-value tactics
                        noisy_moves.append(move)
        
        # Limit the number of noisy moves to search (best 8 only)
        if len(noisy_moves) > 8:
            move_values = []
            for move in noisy_moves:
                value = 0
                if board.is_capture(move):
                    captured_piece = board.piece_at(move.to_square)
                    if captured_piece:
                        value = self.piece_evaluator.get_piece_value(captured_piece.piece_type)
                elif hasattr(self, '_tactical_recognizer'):
                    tactics = self._tactical_recognizer.analyze_move_tactics(board, move)
                    if tactics:
                        value = sum(tactics.values())
                move_values.append((move, value))
            
            # Sort by value and take top 8
            move_values.sort(key=lambda x: x[1], reverse=True)
            noisy_moves = [move for move, value in move_values[:8]]
        
        return noisy_moves
    
    def _gives_check(self, board: GothamBoard, move: chess.Move) -> bool:
        """Check if a move gives check."""
        board.push(move)
        is_check = board.is_check()
        board.pop()
        return is_check
    
    def _get_adaptive_search_depth(self, board: GothamBoard) -> int:
        """
        Determine search depth based on tactical potential.
        
        Args:
            board: Current board position
            
        Returns:
            int: Adaptive search depth
        """
        base_depth = self.search_depth
        
        # Count tactical potential in current position
        tactical_moves = 0
        high_value_tactics = 0
        
        if hasattr(self, '_tactical_recognizer'):
            for move in list(board.legal_moves)[:15]:  # Check top 15 moves
                tactics = self._tactical_recognizer.analyze_move_tactics(board, move)
                if tactics:
                    tactical_moves += 1
                    total_value = sum(tactics.values())
                    if total_value >= 500:  # High-value tactical motifs
                        high_value_tactics += 1
        
        # Check for forcing moves (captures, checks)
        forcing_moves = 0
        for move in board.legal_moves:
            if board.is_capture(move) or self._gives_check(board, move):
                forcing_moves += 1
        
        # Adaptive depth calculation
        depth_bonus = 0
        
        # Bonus for tactical richness (more conservative)
        if tactical_moves >= 4:  # Increased threshold
            depth_bonus += 1
        if high_value_tactics >= 2:  # Increased threshold
            depth_bonus += 1
        
        # Bonus for highly forcing positions only
        if forcing_moves >= 12:  # Increased threshold
            depth_bonus += 1
        
        # Limit the maximum depth increase (more conservative)
        adaptive_depth = min(base_depth + depth_bonus, base_depth + 1)  # Max +1 instead of +2
        
        return adaptive_depth

    def _order_moves(self, board: GothamBoard, moves: List[chess.Move]) -> List[chess.Move]:
        """
        Order moves for better alpha-beta pruning.
        
        Args:
            board: Current board position
            moves: List of legal moves
            
        Returns:
            List[chess.Move]: Ordered moves
        """
        def move_priority(move):
            score = 0
            
            # Tactical motifs get highest priority (new best practice)
            if hasattr(self, '_tactical_recognizer'):
                tactics = self._tactical_recognizer.analyze_move_tactics(board, move)
                if tactics:
                    tactical_value = sum(tactics.values())
                    score += tactical_value  # High priority for tactical moves
            
            # Captures second priority
            if board.is_capture(move):
                captured_piece = board.piece_at(move.to_square)
                if captured_piece:
                    score += self.piece_evaluator.get_piece_value(captured_piece.piece_type) * 10
            
            # Checks third priority
            board.push(move)
            if board.is_check():
                score += 50
            board.pop()
            
            # Promotions
            if move.promotion:
                score += 100
            
            # Castling
            if board.is_castling(move):
                score += 30
            
            return score
        
        return sorted(moves, key=move_priority, reverse=True)
    
    def evaluate_position(self, board: GothamBoard) -> float:
        """
        Evaluate the current position using Gotham Chess principles.
        
        Args:
            board: Board position to evaluate
            
        Returns:
            float: Position evaluation (positive favors White)
        """
        if board.is_checkmate():
            return -999999 if board.turn else 999999
        
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        
        score = 0.0
        game_phase = board.get_game_phase()
        is_endgame = game_phase == GamePhase.ENDGAME
        
        # Material evaluation
        material_score = self._evaluate_material(board, is_endgame)
        score += material_score
        
        # Positional evaluation
        positional_score = self._evaluate_position_factors(board, is_endgame)
        score += positional_score
        
        # Tactical evaluation
        tactical_score = self._evaluate_tactical_factors(board)
        score += tactical_score
        
        return score
    
    def _evaluate_material(self, board: GothamBoard, is_endgame: bool) -> float:
        """
        Evaluate material balance with positional bonuses.
        
        Args:
            board: Board position
            is_endgame: Whether we're in endgame
            
        Returns:
            float: Material evaluation
        """
        score = 0.0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Base material value
                piece_value = self.piece_evaluator.get_piece_value(piece.piece_type)
                
                # Positional bonus
                positional_bonus = self.piece_evaluator.get_piece_square_value(piece, square, is_endgame)
                
                # Activity bonus
                activity_bonus = self.piece_evaluator.evaluate_piece_activity(board, square)
                
                total_value = (piece_value * 100) + positional_bonus + (activity_bonus * 2)
                
                if piece.color == chess.WHITE:
                    score += total_value
                else:
                    score -= total_value
        
        return score
    
    def _evaluate_position_factors(self, board: GothamBoard, is_endgame: bool) -> float:
        """
        Evaluate positional factors using Gotham Chess principles.
        
        Args:
            board: Board position
            is_endgame: Whether we're in endgame
            
        Returns:
            float: Positional evaluation
        """
        score = 0.0
        
        # King safety
        white_king_safe = board.is_king_safe(chess.WHITE)
        black_king_safe = board.is_king_safe(chess.BLACK)
        
        if not is_endgame:  # King safety matters more in middlegame
            if white_king_safe:
                score += 50
            if black_king_safe:
                score -= 50
        
        # Development
        white_development = board.get_development_score(chess.WHITE)
        black_development = board.get_development_score(chess.BLACK)
        score += (white_development - black_development) * 10
        
        # Center control
        white_center = board.get_center_control(chess.WHITE)
        black_center = board.get_center_control(chess.BLACK)
        score += (white_center - black_center) * 5
        
        return score
    
    def _evaluate_tactical_factors(self, board: GothamBoard) -> float:
        """
        Evaluate tactical patterns and threats using best practices.
        
        Args:
            board: Board position
            
        Returns:
            float: Tactical evaluation (positive favors White)
        """
        from .core.tactical_recognizer import TacticalPatternRecognizer, TacticalMotif
        
        if not hasattr(self, '_tactical_recognizer'):
            self._tactical_recognizer = TacticalPatternRecognizer()
        
        # Evaluate tactical opportunities for both sides
        white_tactical_score = self._evaluate_side_tactics(board, chess.WHITE)
        black_tactical_score = self._evaluate_side_tactics(board, chess.BLACK)
        
        # Return net tactical advantage (positive favors White)
        return white_tactical_score - black_tactical_score
    
    def _evaluate_side_tactics(self, board: GothamBoard, color: chess.Color) -> float:
        """
        Evaluate tactical opportunities for one side.
        
        Args:
            board: Board position
            color: Color to evaluate tactics for
            
        Returns:
            float: Tactical score for this side
        """
        from .core.tactical_recognizer import TacticalMotif
        
        score = 0.0
        
        # NEVER mutate the original board during evaluation!
        # Create a copy and set the turn on the copy
        temp_board = board.copy()
        temp_board.turn = color
        
        # Analyze best tactical moves for this color
        best_moves = []
        for move in list(temp_board.legal_moves)[:15]:  # Top 15 moves for performance
            tactics = self._tactical_recognizer.analyze_move_tactics(temp_board, move)
            if tactics:
                move_value = sum(tactics.values())
                best_moves.append((move, move_value, tactics))
        
        # Sort by tactical value
        best_moves.sort(key=lambda x: x[1], reverse=True)
        
        # Apply tactical bonuses
        for move, total_value, tactics in best_moves[:3]:  # Top 3 tactical moves
            for motif, value in tactics.items():
                # Apply README-specified tactical motif weights
                if motif == TacticalMotif.MATE_IN_ONE:
                    score += 10000
                elif motif == TacticalMotif.MATE_IN_TWO:
                    score += 5000
                elif motif == TacticalMotif.BACK_RANK_MATE:
                    score += 800
                elif motif == TacticalMotif.SMOTHERED_MATE:
                    score += 1000
                elif motif == TacticalMotif.FORK:
                    score += min(value * 0.8, 600)
                elif motif == TacticalMotif.PIN:
                    score += min(value * 0.7, 400)
                elif motif == TacticalMotif.SKEWER:
                    score += min(value * 0.9, 500)
                elif motif == TacticalMotif.DISCOVERED_ATTACK:
                    score += min(value * 0.6, 350)
                elif motif == TacticalMotif.DEFLECTION:
                    score += min(value * 0.5, 300)
                elif motif == TacticalMotif.SACRIFICE:
                    score += min(value * 0.4, 250)
                elif motif == TacticalMotif.EN_PASSANT:
                    score += 120
                elif motif == TacticalMotif.REMOVE_GUARD:
                    score += min(value * 0.6, 350)
        
        return score
    
    def _evaluate_fork_potential(self, board: GothamBoard, move: chess.Move) -> float:
        """
        Evaluate if a move creates a fork (attacks multiple valuable pieces).
        
        Args:
            board: Board position after move
            move: The move that was made
            
        Returns:
            float: Fork evaluation bonus
        """
        attacking_piece = board.piece_at(move.to_square)
        if not attacking_piece:
            return 0.0
        
        attacked_squares = board.attacks(move.to_square)
        
        valuable_targets = []
        for square in attacked_squares:
            piece = board.piece_at(square)
            if piece and piece.color != attacking_piece.color:
                piece_value = self.piece_evaluator.get_piece_value(piece.piece_type)
                if piece_value >= 300:  # Rook or higher value
                    valuable_targets.append(piece_value)
        
        # If attacking 2+ valuable pieces, it's a fork
        if len(valuable_targets) >= 2:
            return sum(valuable_targets) * 0.5  # Fork bonus
        
        return 0.0
    
    def get_move_explanation(self, move: chess.Move) -> Dict[str, Any]:
        """
        Get educational explanation for a move.
        
        Args:
            move: Move to explain
            
        Returns:
            Dict: Move explanation with educational insights
        """
        explanation = {
            "move": str(move),
            "principles": [],
            "tactical_motifs": [],
            "strategic_goals": [],
            "educational_notes": []
        }
        
        piece = self.board.piece_at(move.from_square)
        if not piece:
            return explanation
        
        # Opening principles
        if len(self.board.move_stack) < 15:
            opening_name = self.opening_book.get_opening_name(self.board)
            if opening_name:
                opening_info = self.opening_book.get_opening_explanation(opening_name)
                explanation["strategic_goals"] = opening_info.get("typical_plans", [])
        
        # Piece-specific advice
        piece_tips = self.piece_evaluator.get_educational_piece_tips(piece.piece_type)
        explanation["educational_notes"].extend(piece_tips[:2])  # Limit to 2 tips
        
        # Tactical motifs
        if self.board.is_capture(move):
            explanation["tactical_motifs"].append("Capture - gaining material advantage")
        
        if self.board.is_castling(move):
            explanation["principles"].append("Castling - ensuring king safety")
        
        # Center control
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        if move.to_square in center_squares:
            explanation["principles"].append("Central control - dominating the center")
        
        return explanation
    
    def get_position_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive analysis of the current position.
        
        Returns:
            Dict: Position analysis with educational insights
        """
        analysis = {
            "game_phase": self.board.get_game_phase().value,
            "material_balance": self._get_material_balance(),
            "king_safety": {
                "white": self.board.is_king_safe(chess.WHITE),
                "black": self.board.is_king_safe(chess.BLACK)
            },
            "development_scores": {
                "white": self.board.get_development_score(chess.WHITE),
                "black": self.board.get_development_score(chess.BLACK)
            },
            "center_control": {
                "white": self.board.get_center_control(chess.WHITE),
                "black": self.board.get_center_control(chess.BLACK)
            },
            "tactical_motifs": self.board.is_tactical_motif_present(),
            "opening": self.opening_book.get_opening_name(self.board),
            "educational_notes": self.board.get_educational_notes()
        }
        
        return analysis
    
    def _get_material_balance(self) -> Dict[str, int]:
        """
        Calculate material balance for both sides.
        
        Returns:
            Dict: Material count for both colors
        """
        white_material = 0
        black_material = 0
        
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                value = self.piece_evaluator.get_piece_value(piece.piece_type)
                if piece.color == chess.WHITE:
                    white_material += value
                else:
                    black_material += value
        
        return {
            "white": white_material,
            "black": black_material,
            "difference": white_material - black_material
        }