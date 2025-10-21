#!/usr/bin/env python3
"""
Analyze the fork puzzle position more carefully.
"""

import chess
from src.engine import GothamChessEngine


def analyze_fork_puzzle():
    """Analyze the fork puzzle to understand the correct solution."""
    
    # Fork puzzle: White to move and fork the king and rook
    fen = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
    
    engine = GothamChessEngine()
    engine.set_position(fen)
    
    print(f"Testing fork puzzle:")
    print(f"FEN: {fen}")
    print()
    print(f"Board position:")
    print(engine.board)
    print()
    
    # List all legal moves
    legal_moves = list(engine.board.legal_moves)
    print(f"Legal moves ({len(legal_moves)}):")
    for i, move in enumerate(legal_moves):
        print(f"{i+1:2}. {move}")
    print()
    
    # Look for knight moves specifically (potential forks)
    knight_moves = []
    for move in legal_moves:
        piece = engine.board.piece_at(move.from_square)
        if piece and piece.piece_type == chess.KNIGHT:
            knight_moves.append(move)
    
    print(f"Knight moves:")
    for move in knight_moves:
        # Test the move
        engine.board.push(move)
        
        # Check what the knight attacks after the move
        knight_square = move.to_square
        attacked_squares = engine.board.attacks(knight_square)
        
        targets = []
        valuable_targets = []
        for sq in attacked_squares:
            target = engine.board.piece_at(sq)
            if target and target.color == chess.BLACK:
                targets.append(f"{chess.square_name(sq)}({target.symbol()})")
                if target.piece_type in [chess.KING, chess.QUEEN, chess.ROOK]:
                    valuable_targets.append(target.piece_type)
        
        is_fork = len(valuable_targets) >= 2 or (chess.KING in valuable_targets and len(valuable_targets) >= 1)
        
        print(f"  {move}: Attacks {', '.join(targets) if targets else 'none'}")
        if is_fork:
            print(f"    *** FORK! ***")
        
        # Evaluate the position
        score = engine.evaluate_position(engine.board)
        print(f"    Score after move: {score}")
        
        engine.board.pop()
    
    print()
    print("Engine's choice:")
    best_move = engine.get_best_move()
    print(f"Best move: {best_move}")


if __name__ == "__main__":
    analyze_fork_puzzle()