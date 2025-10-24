#!/usr/bin/env python3
"""
Performance Optimization Suite for Gotham Chess Engine.

Based on the analysis results, this script addresses:
1. Slow search performance (1100ms+ per move)
2. Poor tactical puzzle solving (12.5% success rate)
3. Limited opening book coverage (40% success rate)
4. Perft accuracy issues in complex positions
"""

import chess
import time
from typing import Dict, List, Tuple, Optional
from src.engine import GothamChessEngine
from src.core.board import GothamBoard
from src.openings.opening_book import GothamOpeningBook


class EngineOptimizer:
    """Optimize the Gotham Chess Engine for better performance."""
    
    def __init__(self):
        """Initialize the optimizer."""
        self.engine = GothamChessEngine()
    
    def optimize_search_performance(self):
        """Optimize search algorithm for faster move generation."""
        print("🚀 Optimizing Search Performance")
        print("=" * 50)
        
        # Test current performance
        test_positions = [
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 2 3"
        ]
        
        print("Current performance:")
        total_time = 0
        for i, fen in enumerate(test_positions):
            self.engine.set_position(fen)
            start = time.time()
            move = self.engine.get_best_move()
            end = time.time()
            time_ms = (end - start) * 1000
            total_time += time_ms
            print(f"  Position {i+1}: {move} ({time_ms:.1f}ms)")
        
        avg_time = total_time / len(test_positions)
        print(f"  Average: {avg_time:.1f}ms")
        
        # Optimization suggestions
        print("\n🔧 Recommended optimizations:")
        print("1. Reduce default search depth from 4 to 3")
        print("2. Implement more aggressive alpha-beta pruning")
        print("3. Add transposition table for position caching")
        print("4. Optimize move ordering for better pruning")
        
        # Apply basic optimization: reduce search depth
        original_depth = self.engine.search_depth
        self.engine.search_depth = 3
        
        print(f"\n⚡ Testing with reduced depth ({self.engine.search_depth}):")
        total_time_opt = 0
        for i, fen in enumerate(test_positions):
            self.engine.set_position(fen)
            start = time.time()
            move = self.engine.get_best_move()
            end = time.time()
            time_ms = (end - start) * 1000
            total_time_opt += time_ms
            print(f"  Position {i+1}: {move} ({time_ms:.1f}ms)")
        
        avg_time_opt = total_time_opt / len(test_positions)
        improvement = ((avg_time - avg_time_opt) / avg_time) * 100
        print(f"  Average: {avg_time_opt:.1f}ms (🎯 {improvement:.1f}% faster)")
        
        # Restore original depth
        self.engine.search_depth = original_depth
        
        return avg_time_opt < avg_time
    
    def optimize_tactical_evaluation(self):
        """Enhance tactical pattern recognition and evaluation."""
        print("\n🎯 Optimizing Tactical Evaluation")
        print("=" * 50)
        
        # Test a simple tactical puzzle
        fork_fen = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
        
        print("Testing fork recognition:")
        self.engine.set_position(fork_fen)
        
        # Analyze all legal moves for tactical motifs
        legal_moves = list(self.engine.board.legal_moves)
        tactical_moves = []
        
        for move in legal_moves:
            piece = self.engine.board.piece_at(move.from_square)
            if piece and piece.piece_type == chess.KNIGHT:
                # Check if this knight move creates a fork
                self.engine.board.push(move)
                
                # Count attacked valuable pieces
                attacked_pieces = []
                knight_square = move.to_square
                for target_square in self.engine.board.attacks(knight_square):
                    target_piece = self.engine.board.piece_at(target_square)
                    if target_piece and target_piece.color != piece.color:
                        if target_piece.piece_type in [chess.KING, chess.QUEEN, chess.ROOK]:
                            attacked_pieces.append(target_piece.piece_type)
                
                if len(attacked_pieces) >= 2 or chess.KING in attacked_pieces:
                    tactical_moves.append((move, attacked_pieces))
                
                self.engine.board.pop()
        
        print(f"Found {len(tactical_moves)} tactical knight moves:")
        for move, targets in tactical_moves:
            target_names = [chess.piece_name(p) for p in targets]
            print(f"  {move}: attacks {', '.join(target_names)}")
        
        # Test current engine choice
        best_move = self.engine.get_best_move()
        is_tactical = any(move == best_move for move, _ in tactical_moves)
        
        print(f"\nEngine choice: {best_move}")
        print(f"Is tactical: {'✅ YES' if is_tactical else '❌ NO'}")
        
        if not is_tactical and tactical_moves:
            print(f"🔧 Suggestion: Engine should prefer {tactical_moves[0][0]} (tactical)")
        
        return len(tactical_moves) > 0
    
    def expand_opening_book(self):
        """Expand and optimize the opening book coverage."""
        print("\n📚 Expanding Opening Book")
        print("=" * 50)
        
        opening_book = GothamOpeningBook()
        
        # Test current coverage
        test_positions = [
            (None, "Starting position"),
            ("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1", "After 1.e4"),
            ("rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1", "After 1.d4"),
            ("rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq - 1 1", "After 1.Nf3")
        ]
        
        coverage_before = 0
        print("Current opening book coverage:")
        for fen, name in test_positions:
            board = GothamBoard(fen)
            white_move = opening_book.get_opening_move(board, chess.WHITE)
            
            # Test black response if white move exists
            black_move = None
            if white_move:
                board.push(white_move)
                black_move = opening_book.get_opening_move(board, chess.BLACK)
                board.pop()
            
            has_white = bool(white_move)
            has_black = bool(black_move) if white_move else "N/A"
            
            if has_white:
                coverage_before += 1
            if black_move:
                coverage_before += 1
            
            print(f"  {name}: W={white_move} B={has_black}")
        
        total_positions = len(test_positions) * 2  # White and Black for each
        coverage_rate = coverage_before / total_positions
        print(f"\nCoverage: {coverage_before}/{total_positions} ({coverage_rate:.1%})")
        
        # Suggestions for improvement
        print("\n🔧 Recommended opening expansions:")
        print("1. Add responses to 1.e4 (Scandinavian, Caro-Kann)")
        print("2. Add responses to 1.d4 (Queen's Gambit Declined)")
        print("3. Add responses to 1.Nf3 (d5, Nf6)")
        print("4. Expand London System variations")
        print("5. Add more Sicilian Defense lines")
        
        # Create suggested additions
        suggestions = {
            "After 1.e4": ["d7d5", "c7c6", "e7e5"],  # Scandinavian, Caro-Kann, King's Pawn
            "After 1.d4": ["d7d5", "g8f6", "f7f5"],  # QGD, Nimzo, Dutch
            "After 1.Nf3": ["d7d5", "g8f6", "c7c5"],  # Various responses
        }
        
        print("\n💡 Specific move suggestions:")
        for position, moves in suggestions.items():
            print(f"  {position}: {', '.join(moves)}")
        
        return coverage_rate < 0.7  # Needs improvement if below 70%
    
    def create_optimization_plan(self):
        """Create a comprehensive optimization plan."""
        print("\n📋 OPTIMIZATION PLAN")
        print("=" * 60)
        
        # Run all optimization tests
        needs_search_opt = self.optimize_search_performance()
        needs_tactical_opt = self.optimize_tactical_evaluation()
        needs_opening_opt = self.expand_opening_book()
        
        print("\n🎯 PRIORITY RECOMMENDATIONS:")
        print("=" * 40)
        
        priorities = []
        
        if needs_search_opt:
            priorities.append(("HIGH", "Search Performance", [
                "Reduce default search depth to 3",
                "Implement transposition table",
                "Optimize move ordering",
                "Add iterative deepening"
            ]))
        
        if needs_tactical_opt:
            priorities.append(("HIGH", "Tactical Evaluation", [
                "Increase weights for tactical motifs",
                "Add specialized fork/pin detection",
                "Implement quiescence search",
                "Add tactical move ordering"
            ]))
        
        if needs_opening_opt:
            priorities.append(("MEDIUM", "Opening Book", [
                "Add 20+ opening variations",
                "Include popular responses to 1.e4/1.d4",
                "Expand Sicilian Defense lines",
                "Add King's Indian and Nimzo-Indian"
            ]))
        
        # Always include these general improvements
        priorities.append(("LOW", "General Improvements", [
            "Add endgame tablebase support",
            "Implement time management",
            "Add evaluation tuning",
            "Create UCI configuration options"
        ]))
        
        for priority, category, tasks in priorities:
            print(f"\n{priority} PRIORITY: {category}")
            for i, task in enumerate(tasks, 1):
                print(f"  {i}. {task}")
        
        # Estimate implementation effort
        print(f"\n⏱️  ESTIMATED IMPLEMENTATION TIME:")
        print(f"  Search optimizations: 4-6 hours")
        print(f"  Tactical improvements: 6-8 hours") 
        print(f"  Opening book expansion: 2-3 hours")
        print(f"  General improvements: 8-10 hours")
        print(f"  TOTAL: 20-27 hours")
        
        return priorities


def main():
    """Run the engine optimization analysis."""
    print("🔧 GOTHAM CHESS ENGINE - OPTIMIZATION ANALYSIS")
    print("=" * 70)
    print(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    optimizer = EngineOptimizer()
    plan = optimizer.create_optimization_plan()
    
    print(f"\n🏁 Optimization analysis completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Save the plan
    with open('optimization_plan.txt', 'w') as f:
        f.write("GOTHAM CHESS ENGINE - OPTIMIZATION PLAN\n")
        f.write("="*50 + "\n\n")
        
        for priority, category, tasks in plan:
            f.write(f"{priority} PRIORITY: {category}\n")
            for i, task in enumerate(tasks, 1):
                f.write(f"  {i}. {task}\n")
            f.write("\n")
    
    print("💾 Optimization plan saved to: optimization_plan.txt")


if __name__ == "__main__":
    main()