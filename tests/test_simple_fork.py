#!/usr/bin/env python3
"""
Test a clear fork puzzle to validate tactical evaluation.
"""

import chess
from src.engine import GothamChessEngine


def test_simple_fork():
    """Test a simple knight fork puzzle."""
    
    # Simple fork: Knight on e4 can fork king on e8 and rook on a8
    # Position: black king on e8, black rook on a8, white knight can move to d6
    board = chess.Board()
    board.clear()
    
    # Set up a simple fork position
    board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
    board.set_piece_at(chess.A8, chess.Piece(chess.ROOK, chess.BLACK))
    board.set_piece_at(chess.E4, chess.Piece(chess.KNIGHT, chess.WHITE))
    board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
    
    fen = board.fen()
    print(f"Simple fork test:")
    print(f"FEN: {fen}")
    print()
    print("Board:")
    print(board)
    print()
    
    engine = GothamChessEngine()
    engine.set_position(fen)
    
    # Check knight moves
    legal_moves = list(engine.board.legal_moves)
    print(f"Legal moves: {[str(m) for m in legal_moves]}")
    
    for move in legal_moves:
        piece = engine.board.piece_at(move.from_square)
        if piece and piece.piece_type == chess.KNIGHT:
            print(f"\nKnight move: {move}")
            
            # Make the move and check attacks
            engine.board.push(move)
            
            knight_square = move.to_square
            attacked_squares = engine.board.attacks(knight_square)
            
            targets = []
            king_attacked = False
            rook_attacked = False
            
            for sq in attacked_squares:
                target = engine.board.piece_at(sq)
                if target and target.color == chess.BLACK:
                    targets.append(f"{chess.square_name(sq)}({target.symbol()})")
                    if target.piece_type == chess.KING:
                        king_attacked = True
                    elif target.piece_type == chess.ROOK:
                        rook_attacked = True
            
            print(f"  Attacks: {', '.join(targets)}")
            print(f"  Fork (King + Rook): {king_attacked and rook_attacked}")
            
            # Get evaluation
            score = engine.evaluate_position(engine.board)
            print(f"  Position score: {score}")
            
            engine.board.pop()
    
    print(f"\nEngine's best move: {engine.get_best_move()}")


def test_puzzle_from_csv():
    """Test one of the actual puzzles from our database."""
    from src.puzzles.lichess_puzzles import LichessPuzzles
    
    puzzles = LichessPuzzles()
    fork_puzzles = puzzles.get_puzzles_by_theme("fork")
    
    if fork_puzzles:
        puzzle = fork_puzzles[0]
        print(f"\nTesting real Lichess fork puzzle:")
        print(f"Puzzle ID: {puzzle.puzzle_id}")
        print(f"FEN: {puzzle.fen}")
        print(f"Solution: {puzzle.moves}")
        print(f"Themes: {puzzle.themes}")
        print()
        
        engine = GothamChessEngine()
        engine.set_position(puzzle.fen)
        
        print("Board:")
        print(engine.board)
        print()
        
        # Test the solution move
        if puzzle.moves:
            solution_move = puzzle.moves[0]
            try:
                move = chess.Move.from_uci(solution_move)
                print(f"Solution move: {solution_move}")
                
                if move in engine.board.legal_moves:
                    engine.board.push(move)
                    score = engine.evaluate_position(engine.board)
                    print(f"Score after solution: {score}")
                    engine.board.pop()
                else:
                    print("Solution move is not legal!")
            except:
                print(f"Invalid move format: {solution_move}")
        
        print(f"Engine's choice: {engine.get_best_move()}")


if __name__ == "__main__":
    test_simple_fork()
    test_puzzle_from_csv()