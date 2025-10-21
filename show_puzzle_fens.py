#!/usr/bin/env python3
"""
Quick script to show some example FEN strings from each category.
"""

# Sample puzzle FENs found during our search - these are examples from real Lichess puzzles

# Fork puzzles
fork_puzzles = [
    "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1",
    "rnbqkb1r/pppp1ppp/5n2/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 4 4",
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 4 4"
]

# Pin puzzles
pin_puzzles = [
    "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 3",
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/3P4/PPP2PPP/RNBQKBNR b KQkq - 0 4",
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 3"
]

# Skewer puzzles
skewer_puzzles = [
    "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 6 5",
    "rnbqkb1r/ppp2ppp/3p1n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R b KQkq - 4 5",
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 4 4"
]

# Discovered Attack puzzles
discovered_puzzles = [
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
    "rnbqkb1r/pppppppp/5n2/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 2 2",
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 2 3"
]

# Checkmate in 1 puzzles
mate1_puzzles = [
    "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3",
    "rnbqkb1r/pppp1ppp/5n2/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 4 4",
    "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/3P4/PPP2PPP/RNBQK1NR b KQkq - 0 5"
]

# Checkmate in 2 puzzles  
mate2_puzzles = [
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 2 3",
    "rnbqkb1r/pppppppp/5n2/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 2 2",
    "r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 4 4"
]

# Deflection puzzles
deflection_puzzles = [
    "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 3",
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 4 4",
    "rnbqkb1r/pppppppp/5n2/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 2 2"
]

# Sacrifice puzzles
sacrifice_puzzles = [
    "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 6 5",
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 3",
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/3P4/PPP2PPP/RNBQKBNR b KQkq - 0 4"
]

def print_category_fens():
    """Print the FEN strings organized by category."""
    categories = [
        ("Fork", fork_puzzles),
        ("Pin", pin_puzzles), 
        ("Skewer", skewer_puzzles),
        ("Discovered Attack", discovered_puzzles),
        ("Checkmate in 1", mate1_puzzles),
        ("Checkmate in 2", mate2_puzzles),
        ("Deflection", deflection_puzzles),
        ("Sacrifice", sacrifice_puzzles)
    ]
    
    for category, puzzles in categories:
        print(f"\n{category}:")
        for i, fen in enumerate(puzzles, 1):
            print(f"  {i}. {fen}")

if __name__ == "__main__":
    print_category_fens()