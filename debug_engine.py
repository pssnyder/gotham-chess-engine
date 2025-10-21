#!/usr/bin/env python3
"""
Debug UCI to test engine functionality.
"""

import chess
from src.engine import GothamChessEngine


def test_engine():
    """Test the engine directly."""
    print("Creating engine...")
    engine = GothamChessEngine()
    
    print(f"Board position: {engine.board.fen()}")
    print(f"Legal moves count: {len(list(engine.board.legal_moves))}")
    print(f"First few legal moves: {list(engine.board.legal_moves)[:5]}")
    
    print("Getting best move...")
    try:
        best_move = engine.get_best_move()
        print(f"Best move: {best_move}")
        return best_move
    except Exception as e:
        print(f"Error getting best move: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    test_engine()