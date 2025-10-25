#!/usr/bin/env python3
"""
Puzzle Solving Test for Gotham Chess Engine.

This script tests the engine's ability to solve tactical puzzles
from each category to ensure it meets minimum requirements.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.engine import GothamChessEngine
from src.puzzles.lichess_puzzles import LichessPuzzleLibrary, LichessPuzzleCategory
import chess


def test_single_puzzle(engine: GothamChessEngine, puzzle, timeout: float = 2.0) -> bool:
    """
    Test if the engine can solve a single puzzle.
    
    Args:
        engine: Chess engine instance
        puzzle: Puzzle to solve
        timeout: Time limit in seconds
        
    Returns:
        True if puzzle solved correctly
    """
    try:
        # Set up the position
        engine.set_position(puzzle.fen)
        
        # Temporarily reduce time limit for faster testing
        original_time_limit = engine.time_limit
        engine.time_limit = timeout
        
        # Get engine's move
        engine_move = engine.get_best_move()
        
        # Restore original time limit
        engine.time_limit = original_time_limit
        
        if engine_move:
            engine_move_str = str(engine_move)
            
            # Check if the move matches (UCI format)
            if engine_move_str == puzzle.solution:
                return True
            
            # Also check if it's the same move in different notation
            try:
                solution_move = chess.Move.from_uci(puzzle.solution)
                if engine_move == solution_move:
                    return True
            except:
                pass
        
        return False
    
    except Exception as e:
        print(f"Error testing puzzle {puzzle.puzzle_id}: {e}")
        return False


def comprehensive_puzzle_test():
    """Run comprehensive puzzle solving tests."""
    print("🧩 GOTHAM CHESS ENGINE - PUZZLE SOLVING TEST")
    print("=" * 55)
    
    # Initialize components
    print("🔧 Initializing engine and puzzle library...")
    engine = GothamChessEngine()
    puzzle_library = LichessPuzzleLibrary()
    
    if not puzzle_library.all_puzzles:
        print("❌ No puzzles loaded! Check the Lichess database path.")
        return False
    
    print(f"✅ Loaded {len(puzzle_library.all_puzzles)} puzzles")
    
    # Test requirements: at least 3 successful solves per category
    min_success_per_category = 3
    category_results = {}
    overall_success = True
    
    print(f"\n🎯 Testing puzzle solving (minimum {min_success_per_category} per category)...")
    print("-" * 55)
    
    for category in LichessPuzzleCategory:
        category_puzzles = puzzle_library.puzzles[category]
        
        if not category_puzzles:
            print(f"⚠️  {category.value}: No puzzles available")
            category_results[category.value] = False
            overall_success = False
            continue
        
        print(f"\n🔍 Testing {category.value} puzzles...")
        
        solved_count = 0
        total_tested = min(10, len(category_puzzles))  # Test up to 10 puzzles
        
        for i, puzzle in enumerate(category_puzzles[:total_tested]):
            print(f"  Puzzle {i+1}/{total_tested} (ID: {puzzle.puzzle_id}, Rating: {puzzle.rating})...", end="")
            
            success = test_single_puzzle(engine, puzzle)
            
            if success:
                solved_count += 1
                print(" ✅ SOLVED")
            else:
                print(" ❌ FAILED")
                
                # Show what the engine chose vs correct solution
                engine.set_position(puzzle.fen)
                engine_move = engine.get_best_move()
                print(f"    Expected: {puzzle.solution}, Engine chose: {engine_move}")
        
        success_rate = solved_count / total_tested if total_tested > 0 else 0
        category_passed = solved_count >= min_success_per_category
        
        status = "✅ PASS" if category_passed else "❌ FAIL"
        print(f"  {status} - {solved_count}/{total_tested} solved ({success_rate:.1%})")
        
        category_results[category.value] = category_passed
        if not category_passed:
            overall_success = False
    
    # Summary
    print("\n" + "=" * 55)
    print("📊 PUZZLE SOLVING TEST RESULTS")
    print("=" * 55)
    
    passed_categories = sum(1 for passed in category_results.values() if passed)
    total_categories = len(category_results)
    
    for category, passed in category_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {category}")
    
    print(f"\n🎯 OVERALL RESULT: {passed_categories}/{total_categories} categories passed")
    
    if overall_success:
        print("🎉 SUCCESS! Engine meets minimum puzzle solving requirements!")
        print("   Ready for deployment and external testing.")
    else:
        print("⚠️  PARTIAL SUCCESS: Some puzzle categories need improvement.")
        print("   Consider adjusting the engine's tactical evaluation.")
    
    return overall_success


def quick_puzzle_demo():
    """Quick demonstration of puzzle solving."""
    print("🧩 QUICK PUZZLE SOLVING DEMONSTRATION")
    print("=" * 40)
    
    engine = GothamChessEngine()
    puzzle_library = LichessPuzzleLibrary()
    
    if not puzzle_library.all_puzzles:
        print("❌ No puzzles available for demo")
        return
    
    # Get one puzzle from each available category
    demo_puzzles = []
    for category in LichessPuzzleCategory:
        puzzle = puzzle_library.get_puzzle_by_category(category)
        if puzzle:
            demo_puzzles.append(puzzle)
    
    print(f"Demonstrating with {len(demo_puzzles)} puzzles:\n")
    
    for i, puzzle in enumerate(demo_puzzles[:5], 1):  # Limit to 5 for demo
        print(f"🧩 Puzzle {i}: {puzzle.category.value.upper()}")
        print(f"   Rating: {puzzle.rating} | Themes: {', '.join(puzzle.themes)}")
        print(f"   Position: {puzzle.fen}")
        print(f"   Task: {puzzle.description}")
        
        # Test the engine
        engine.set_position(puzzle.fen)
        engine_move = engine.get_best_move()
        
        success = str(engine_move) == puzzle.solution if engine_move else False
        status = "✅ CORRECT" if success else "❌ INCORRECT"
        
        print(f"   Expected: {puzzle.solution}")
        print(f"   Engine:   {engine_move} {status}")
        print(f"   Learn: {puzzle.educational_note}")
        print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        quick_puzzle_demo()
    else:
        success = comprehensive_puzzle_test()
        sys.exit(0 if success else 1)