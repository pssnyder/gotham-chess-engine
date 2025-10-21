"""
Main entry point for the Gotham Chess Engine.

This module provides a simple command-line interface to interact with the engine
and demonstrate its educational features.
"""

import chess
import chess.pgn
from src.engine import GothamChessEngine


def main():
    """
    Main function to run the Gotham Chess Engine demo.
    """
    print("🔥 Welcome to the Gotham Chess Engine! 🔥")
    print("Built with the cumulative chess knowledge of GothamChess (Levy Rozman)")
    print("=" * 60)
    
    engine = GothamChessEngine()
    
    print(f"\nCurrent position: {engine.board.fen()}")
    print(f"Game phase: {engine.board.get_game_phase().value}")
    
    # Demo: Get opening move
    print("\n📚 Opening Book Analysis:")
    best_move = engine.get_best_move()
    if best_move:
        print(f"Recommended move: {best_move}")
        
        # Get move explanation
        explanation = engine.get_move_explanation(best_move)
        print(f"\n🎓 Educational Explanation:")
        
        if explanation["principles"]:
            print(f"Principles: {', '.join(explanation['principles'])}")
        
        if explanation["educational_notes"]:
            print(f"Tips: {explanation['educational_notes'][0]}")
        
        # Make the move
        engine.make_move(best_move)
        print(f"\nAfter {best_move}: {engine.board.fen()}")
    
    # Demo: Position analysis
    print("\n📊 Position Analysis:")
    analysis = engine.get_position_analysis()
    
    print(f"Material balance: White {analysis['material_balance']['white']} - Black {analysis['material_balance']['black']}")
    print(f"King safety: White {analysis['king_safety']['white']}, Black {analysis['king_safety']['black']}")
    print(f"Development: White {analysis['development_scores']['white']}, Black {analysis['development_scores']['black']}")
    print(f"Center control: White {analysis['center_control']['white']}, Black {analysis['center_control']['black']}")
    
    if analysis['opening']:
        print(f"Opening: {analysis['opening']}")
    
    if analysis['tactical_motifs']:
        active_motifs = [motif for motif, present in analysis['tactical_motifs'].items() if present]
        if active_motifs:
            print(f"Tactical motifs present: {', '.join(active_motifs)}")
    
    print("\n✅ Demo complete! The Gotham Chess Engine is ready to play.")
    print("Key features implemented:")
    print("  - Opening book with Gotham's recommendations")
    print("  - Educational move explanations")
    print("  - Position analysis with chess principles")
    print("  - Tactical pattern recognition")
    print("  - Material and positional evaluation")


if __name__ == "__main__":
    main()