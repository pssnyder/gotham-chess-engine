#!/usr/bin/env python3
"""
Test tactical puzzle solving with enhanced evaluation.
"""

import chess
from src.engine import GothamChessEngine


def test_fork_puzzle():
    """Test the specific fork puzzle that failed before."""
    
    # Fork puzzle: White to move and fork the king and rook
    fen = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
    
    print(f"Testing fork puzzle:")
    print(f"FEN: {fen}")
    print()
    
    engine = GothamChessEngine()
    engine.set_position(fen)
    
    print(f"Board position:")
    print(engine.board)
    print()
    
    # Test specific moves
    test_moves = ["f1c1", "g1h1", "f3d4", "h6f7"]
    
    for move_str in test_moves:
        try:
            move = chess.Move.from_uci(move_str)
            if move in engine.board.legal_moves:
                # Make move and evaluate
                engine.board.push(move)
                score = engine.evaluate_position(engine.board)
                engine.board.pop()
                
                print(f"Move {move_str}: Score = {score}")
                
                # Check if this move creates a fork
                temp_board = engine.board.copy()
                temp_board.push(move)
                piece = temp_board.piece_at(move.to_square)
                if piece:
                    attacked_squares = temp_board.attacks(move.to_square)
                    targets = []
                    for sq in attacked_squares:
                        target = temp_board.piece_at(sq)
                        if target and target.color != piece.color:
                            targets.append(f"{chess.square_name(sq)}({target.symbol()})")
                    print(f"  Attacks: {', '.join(targets) if targets else 'none'}")
                
            else:
                print(f"Move {move_str}: ILLEGAL")
        
        except Exception as e:
            print(f"Move {move_str}: ERROR - {e}")
        
        print()
    
    # Get engine's best move
    print("Engine's choice:")
    best_move = engine.get_best_move()
    print(f"Best move: {best_move}")


if __name__ == "__main__":
    test_fork_puzzle()