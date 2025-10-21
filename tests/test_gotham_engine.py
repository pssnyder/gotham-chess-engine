"""
Basic tests for the Gotham Chess Engine core components.
"""

import pytest
import chess
from src.core.board import GothamBoard, GamePhase
from src.core.pieces import GothamPieceEvaluator
from src.openings.opening_book import GothamOpeningBook
from src.engine import GothamChessEngine


class TestGothamBoard:
    """Test the enhanced board functionality."""
    
    def test_board_initialization(self):
        """Test board can be initialized."""
        board = GothamBoard()
        assert board.fen() == chess.STARTING_FEN
    
    def test_game_phase_detection(self):
        """Test game phase detection."""
        board = GothamBoard()
        assert board.get_game_phase() == GamePhase.OPENING
        
        # Test endgame detection with minimal pieces
        endgame_fen = "8/8/8/8/8/8/4K3/4k3 w - - 0 1"
        endgame_board = GothamBoard(endgame_fen)
        assert endgame_board.get_game_phase() == GamePhase.ENDGAME
    
    def test_king_safety_evaluation(self):
        """Test king safety evaluation."""
        board = GothamBoard()
        
        # Starting position should have relatively safe kings
        white_safe = board.is_king_safe(chess.WHITE)
        black_safe = board.is_king_safe(chess.BLACK)
        
        assert isinstance(white_safe, bool)
        assert isinstance(black_safe, bool)
    
    def test_development_score(self):
        """Test development scoring."""
        board = GothamBoard()
        
        white_dev = board.get_development_score(chess.WHITE)
        black_dev = board.get_development_score(chess.BLACK)
        
        assert isinstance(white_dev, int)
        assert isinstance(black_dev, int)
        assert white_dev >= 0
        assert black_dev >= 0
    
    def test_center_control(self):
        """Test center control evaluation."""
        board = GothamBoard()
        
        white_center = board.get_center_control(chess.WHITE)
        black_center = board.get_center_control(chess.BLACK)
        
        assert isinstance(white_center, int)
        assert isinstance(black_center, int)


class TestGothamPieceEvaluator:
    """Test piece evaluation functionality."""
    
    def test_piece_values(self):
        """Test basic piece values."""
        evaluator = GothamPieceEvaluator()
        
        assert evaluator.get_piece_value(chess.PAWN) == 1
        assert evaluator.get_piece_value(chess.KNIGHT) == 3
        assert evaluator.get_piece_value(chess.BISHOP) == 3
        assert evaluator.get_piece_value(chess.ROOK) == 5
        assert evaluator.get_piece_value(chess.QUEEN) == 9
        assert evaluator.get_piece_value(chess.KING) == 0
    
    def test_piece_square_values(self):
        """Test positional bonuses."""
        evaluator = GothamPieceEvaluator()
        
        white_pawn = chess.Piece(chess.PAWN, chess.WHITE)
        center_square = chess.E4
        
        bonus = evaluator.get_piece_square_value(white_pawn, center_square)
        assert isinstance(bonus, int)
    
    def test_educational_tips(self):
        """Test educational tips generation."""
        tips = GothamPieceEvaluator.get_educational_piece_tips(chess.KNIGHT)
        
        assert isinstance(tips, list)
        assert len(tips) > 0
        assert all(isinstance(tip, str) for tip in tips)


class TestGothamOpeningBook:
    """Test opening book functionality."""
    
    def test_opening_book_initialization(self):
        """Test opening book can be initialized."""
        book = GothamOpeningBook()
        assert hasattr(book, 'openings')
        assert len(book.openings) > 0
    
    def test_opening_move_suggestion(self):
        """Test opening move suggestions."""
        book = GothamOpeningBook()
        board = GothamBoard()
        
        move = book.get_opening_move(board, chess.WHITE)
        
        if move:  # Might be None if no book move available
            assert move in board.legal_moves
    
    def test_opening_name_detection(self):
        """Test opening name detection."""
        book = GothamOpeningBook()
        board = GothamBoard()
        
        # Play some London System moves
        board.push_san("d4")
        board.push_san("d5")
        board.push_san("Nf3")
        board.push_san("Nf6")
        board.push_san("Bf4")
        
        opening_name = book.get_opening_name(board)
        assert opening_name == "London System"


class TestGothamChessEngine:
    """Test the main engine functionality."""
    
    def test_engine_initialization(self):
        """Test engine can be initialized."""
        engine = GothamChessEngine()
        assert isinstance(engine.board, GothamBoard)
        assert isinstance(engine.opening_book, GothamOpeningBook)
    
    def test_best_move_generation(self):
        """Test best move generation."""
        engine = GothamChessEngine()
        
        best_move = engine.get_best_move()
        
        if best_move:  # Should have a move in starting position
            assert best_move in engine.board.legal_moves
    
    def test_position_evaluation(self):
        """Test position evaluation."""
        engine = GothamChessEngine()
        
        evaluation = engine.evaluate_position(engine.board)
        assert isinstance(evaluation, float)
        
        # Starting position should be roughly equal (close to 0)
        assert abs(evaluation) < 100  # Reasonable bound for starting position
    
    def test_move_explanation(self):
        """Test move explanation generation."""
        engine = GothamChessEngine()
        
        # Get a legal move
        legal_moves = list(engine.board.legal_moves)
        if legal_moves:
            move = legal_moves[0]
            explanation = engine.get_move_explanation(move)
            
            assert isinstance(explanation, dict)
            assert "move" in explanation
            assert "principles" in explanation
            assert "educational_notes" in explanation
    
    def test_position_analysis(self):
        """Test comprehensive position analysis."""
        engine = GothamChessEngine()
        
        analysis = engine.get_position_analysis()
        
        assert isinstance(analysis, dict)
        assert "game_phase" in analysis
        assert "material_balance" in analysis
        assert "king_safety" in analysis
        assert "development_scores" in analysis
        assert "center_control" in analysis
    
    def test_move_making(self):
        """Test making moves on the engine."""
        engine = GothamChessEngine()
        
        legal_moves = list(engine.board.legal_moves)
        if legal_moves:
            move = legal_moves[0]
            result = engine.make_move(move)
            
            assert result is True
            assert len(engine.board.move_stack) == 1