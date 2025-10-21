#!/usr/bin/env python3
"""
Test script for Gotham Chess Engine.

This script tests all major components to ensure they work correctly together.
"""

import sys
import os
import traceback

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    print("🔧 Testing imports...")
    
    try:
        from src.engine import GothamChessEngine
        print("✓ Engine module imported")
        
        from src.openings.opening_book import GothamOpeningBook
        print("✓ Opening book module imported")
        
        from src.patterns.tactical_patterns import GothamTacticalAnalyzer
        print("✓ Tactical patterns module imported")
        
        from src.patterns.mate_detection import GothamMateDetector
        print("✓ Mate detection module imported")
        
        from src.patterns.historical_games import GothamHistoricalAnalyzer
        print("✓ Historical games module imported")
        
        from src.puzzles.puzzle_library import GothamPuzzleLibrary
        print("✓ Puzzle library module imported")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False

def test_engine_basic():
    """Test basic engine functionality."""
    print("\n🔧 Testing basic engine functionality...")
    
    try:
        from src.engine import GothamChessEngine
        
        engine = GothamChessEngine()
        print("✓ Engine created successfully")
        
        # Test getting a move
        move = engine.get_best_move()
        print(f"✓ Engine found move: {move}")
        
        # Test making a move
        if move and engine.make_move(move):
            print("✓ Move executed successfully")
        
        # Test position analysis
        analysis = engine.get_position_analysis()
        print(f"✓ Position analysis completed: {analysis['game_phase']}")
        
        return True
    except Exception as e:
        print(f"❌ Engine test failed: {e}")
        traceback.print_exc()
        return False

def test_opening_book():
    """Test opening book functionality."""
    print("\n🔧 Testing opening book...")
    
    try:
        from src.openings.opening_book import GothamOpeningBook
        from src.engine import GothamChessEngine
        
        engine = GothamChessEngine()
        opening_book = GothamOpeningBook()
        
        # Test getting opening move
        opening_move = opening_book.get_opening_move(engine.board, engine.board.turn)
        print(f"✓ Opening book suggests: {opening_move}")
        
        # Test opening recognition
        opening_name = opening_book.get_opening_name(engine.board)
        print(f"✓ Opening detection works: {opening_name}")
        
        return True
    except Exception as e:
        print(f"❌ Opening book test failed: {e}")
        traceback.print_exc()
        return False

def test_puzzle_library():
    """Test puzzle library functionality."""
    print("\n🔧 Testing puzzle library...")
    
    try:
        from src.puzzles.puzzle_library import GothamPuzzleLibrary, PuzzleCategory
        
        puzzle_lib = GothamPuzzleLibrary()
        print("✓ Puzzle library created")
        
        # Test getting random puzzle
        puzzle = puzzle_lib.get_random_puzzle()
        if puzzle:
            print(f"✓ Random puzzle: {puzzle.category.value}")
            print(f"  Description: {puzzle.description}")
        
        # Test statistics
        stats = puzzle_lib.get_puzzle_statistics()
        print(f"✓ Library contains {stats['total_puzzles']} puzzles")
        
        # Test each category has puzzles
        categories_with_puzzles = 0
        for category in PuzzleCategory:
            if puzzle_lib.puzzles[category]:
                categories_with_puzzles += 1
        
        print(f"✓ {categories_with_puzzles}/{len(PuzzleCategory)} categories have puzzles")
        
        return True
    except Exception as e:
        print(f"❌ Puzzle library test failed: {e}")
        traceback.print_exc()
        return False

def test_tactical_analysis():
    """Test tactical analysis functionality."""
    print("\n🔧 Testing tactical analysis...")
    
    try:
        from src.patterns.tactical_patterns import GothamTacticalAnalyzer
        from src.engine import GothamChessEngine
        
        engine = GothamChessEngine()
        analyzer = GothamTacticalAnalyzer()
        
        # Test tactical analysis
        results = analyzer.analyze_position(engine.board)
        print("✓ Tactical analysis completed")
        
        # Count total tactics found
        total_tactics = sum(len(tactics) for tactics in results.values())
        print(f"✓ Found {total_tactics} tactical opportunities")
        
        return True
    except Exception as e:
        print(f"❌ Tactical analysis test failed: {e}")
        traceback.print_exc()
        return False

def test_mate_detection():
    """Test mate detection functionality."""
    print("\n🔧 Testing mate detection...")
    
    try:
        from src.patterns.mate_detection import GothamMateDetector
        from src.engine import GothamChessEngine
        
        engine = GothamChessEngine()
        detector = GothamMateDetector()
        
        # Test mate detection
        mates = detector.find_mates(engine.board)
        print("✓ Mate detection completed")
        
        # Count total mates found
        total_mates = sum(len(mate_list) for mate_list in mates.values())
        print(f"✓ Found {total_mates} mate opportunities")
        
        return True
    except Exception as e:
        print(f"❌ Mate detection test failed: {e}")
        traceback.print_exc()
        return False

def test_historical_analysis():
    """Test historical game analysis."""
    print("\n🔧 Testing historical analysis...")
    
    try:
        from src.patterns.historical_games import GothamHistoricalAnalyzer
        from src.engine import GothamChessEngine
        
        engine = GothamChessEngine()
        analyzer = GothamHistoricalAnalyzer()
        
        # Test historical analysis
        analysis = analyzer.analyze_position_for_historical_patterns(engine.board)
        print("✓ Historical analysis completed")
        
        similar_games = len(analysis.get('similar_games', []))
        print(f"✓ Found {similar_games} similar historical patterns")
        
        return True
    except Exception as e:
        print(f"❌ Historical analysis test failed: {e}")
        traceback.print_exc()
        return False

def test_uci_interface():
    """Test UCI interface availability."""
    print("\n🔧 Testing UCI interface...")
    
    try:
        if os.path.exists('uci_engine.py'):
            print("✓ UCI engine file exists")
            
            # Try to import (without running)
            import uci_engine
            print("✓ UCI engine module can be imported")
            
            return True
        else:
            print("❌ UCI engine file not found")
            return False
    except Exception as e:
        print(f"❌ UCI interface test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🎯 GOTHAM CHESS ENGINE - COMPREHENSIVE TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Engine Basic", test_engine_basic),
        ("Opening Book", test_opening_book),
        ("Puzzle Library", test_puzzle_library),
        ("Tactical Analysis", test_tactical_analysis),
        ("Mate Detection", test_mate_detection),
        ("Historical Analysis", test_historical_analysis),
        ("UCI Interface", test_uci_interface)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n{'='*50}")
    print(f"🎯 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Engine is ready for use!")
        print("\n🚀 Next steps:")
        print("1. Run 'python uci_engine.py' to start UCI mode")
        print("2. Or run 'gotham_engine.bat' for the interactive menu")
        print("3. Connect to your favorite chess GUI for testing")
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)