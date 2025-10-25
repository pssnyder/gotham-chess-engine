"""
Comprehensive perspective consistency test for Gotham Chess Engine.

This test ensures that the engine always evaluates positions from the correct
perspective and doesn't accidentally help the opponent.
"""

import chess
from src.engine import GothamChessEngine
from src.core.board import GothamBoard

def test_perspective_consistency():
    """Test that evaluation perspective is consistent."""
    
    print("🔍 PERSPECTIVE CONSISTENCY TEST")
    print("=" * 60)
    
    # Test positions where one side has a clear advantage
    test_positions = [
        {
            "name": "White Material Advantage",
            "fen": "rnbqkb1r/pppppppp/5n2/8/8/8/PPPPPPPP/RNBQKB1R w KQkq - 0 1",  # White has extra rook
            "expected_white_advantage": True
        },
        {
            "name": "Black Material Advantage", 
            "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPP1P/RNBQKB1R b KQkq - 0 1",  # Black has extra knight
            "expected_white_advantage": False
        },
        {
            "name": "White Tactical Advantage (Fork)",
            "fen": "r3k3/8/8/3N4/8/8/8/4K3 w - - 0 1",  # White knight can fork
            "expected_white_advantage": True
        },
        {
            "name": "Black Tactical Advantage (Fork)",
            "fen": "4k3/8/8/3n4/8/8/8/R3K3 b - - 0 1",  # Black knight can fork
            "expected_white_advantage": False
        },
        {
            "name": "White Mate in 1",
            "fen": "6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1",  # White can mate with Ra8#
            "expected_white_advantage": True
        },
        {
            "name": "Black Mate in 1",
            "fen": "r5k1/5ppp/8/8/8/8/5PPP/6K1 b - - 0 1",  # Black can mate with Ra1#
            "expected_white_advantage": False
        }
    ]
    
    engine = GothamChessEngine()
    
    for test_pos in test_positions:
        print(f"\n📍 Testing: {test_pos['name']}")
        print(f"FEN: {test_pos['fen']}")
        
        # Set position
        engine.set_position(test_pos['fen'])
        board = engine.board
        
        print(f"Turn to move: {'White' if board.turn else 'Black'}")
        print("Board:")
        print(board)
        
        # Evaluate position
        eval_score = engine.evaluate_position(board)
        tactical_score = engine._evaluate_tactical_factors(board)
        
        print(f"Evaluation: {eval_score:.1f} (Tactical: {tactical_score:.1f})")
        
        # Check perspective consistency
        white_advantage = eval_score > 0
        expected = test_pos['expected_white_advantage']
        
        if white_advantage == expected:
            status = "✅ CORRECT"
        else:
            status = "❌ WRONG PERSPECTIVE"
        
        print(f"Expected White advantage: {expected}")
        print(f"Evaluation shows White advantage: {white_advantage}")
        print(f"Result: {status}")
        
        # Additional check: move selection should favor the side to move
        best_move = engine.get_best_move()
        if best_move:
            # Make the move and see if evaluation improves for the side that moved
            temp_board = board.copy()
            eval_before = engine.evaluate_position(temp_board)
            
            temp_board.push(best_move)
            eval_after = engine.evaluate_position(temp_board)
            
            # If White moved, eval should improve for White (increase)
            # If Black moved, eval should improve for Black (decrease)
            if board.turn == chess.WHITE:
                improvement = eval_after > eval_before
                expected_improvement = True
            else:
                improvement = eval_after < eval_before  
                expected_improvement = True
            
            move_status = "✅ GOOD" if improvement == expected_improvement else "❌ BAD"
            print(f"Best move: {best_move}")
            print(f"Eval before: {eval_before:.1f}, after: {eval_after:.1f}")
            print(f"Move improves position for {'White' if board.turn else 'Black'}: {improvement} {move_status}")
        
        print("-" * 40)


def test_tactical_perspective():
    """Test tactical evaluation perspective specifically."""
    
    print("\n🎯 TACTICAL PERSPECTIVE TEST")
    print("=" * 60)
    
    engine = GothamChessEngine()
    
    # Test the same tactical position from both perspectives
    print("\n📍 Testing: Royal Fork Position (White to move)")
    engine.set_position("r3k3/8/8/3N4/8/8/8/4K3 w - - 0 1")
    
    white_eval = engine._evaluate_tactical_factors(engine.board)
    white_total = engine.evaluate_position(engine.board)
    
    print(f"White tactical eval: {white_eval:.1f}")
    print(f"White total eval: {white_total:.1f}")
    
    # Flip the position (Black to move with same tactical opportunity)
    print("\n📍 Testing: Royal Fork Position (Black to move)")
    engine.set_position("4k3/8/8/3n4/8/8/8/R3K3 b - - 0 1")
    
    black_eval = engine._evaluate_tactical_factors(engine.board)  
    black_total = engine.evaluate_position(engine.board)
    
    print(f"Black tactical eval: {black_eval:.1f}")
    print(f"Black total eval: {black_total:.1f}")
    
    # Check symmetry: White advantage should be roughly opposite of Black advantage
    print(f"\nSymmetry check:")
    print(f"White total: {white_total:.1f}")
    print(f"Black total: {black_total:.1f}")
    print(f"Sum (should be ~0): {white_total + black_total:.1f}")
    
    if abs(white_total + black_total) < 100:  # Allow some asymmetry
        print("✅ Symmetric evaluation")
    else:
        print("❌ Asymmetric evaluation - perspective issue!")


def test_move_consistency():
    """Test that the engine chooses moves that benefit the correct side."""
    
    print("\n🎮 MOVE CONSISTENCY TEST")
    print("=" * 60)
    
    engine = GothamChessEngine()
    
    # Test in a position where there's a clear best move for each side
    test_cases = [
        {
            "name": "White Mate in 1",
            "fen": "6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1",
            "expected_move": "a1a8",  # Ra8# checkmate
            "side": "White"
        },
        {
            "name": "Black Mate in 1", 
            "fen": "r5k1/5ppp/8/8/8/8/5PPP/6K1 b - - 0 1",
            "expected_move": "a8a1",  # Ra1# checkmate
            "side": "Black"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📍 Testing: {test_case['name']}")
        engine.set_position(test_case['fen'])
        
        best_move = engine.get_best_move()
        expected = chess.Move.from_uci(test_case['expected_move'])
        
        print(f"{test_case['side']} to move")
        print(f"Expected: {expected}")
        print(f"Engine chose: {best_move}")
        
        if best_move == expected:
            print("✅ Correct move")
        else:
            print("❌ Wrong move - possible perspective issue!")
            
            # Analyze why it chose differently
            temp_board = engine.board.copy()
            if best_move:
                temp_board.push(best_move)
                eval_after_engine = engine.evaluate_position(temp_board)
                temp_board.pop()
            else:
                eval_after_engine = -999999
            
            temp_board.push(expected)
            eval_after_expected = engine.evaluate_position(temp_board)
            
            print(f"Eval after engine move: {eval_after_engine:.1f}")
            print(f"Eval after expected move: {eval_after_expected:.1f}")


if __name__ == "__main__":
    test_perspective_consistency()
    test_tactical_perspective()
    test_move_consistency()
    
    print("\n" + "=" * 60)
    print("🏁 PERSPECTIVE TEST COMPLETE")
    print("Check for any ❌ indicators above!")