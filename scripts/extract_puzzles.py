#!/usr/bin/env python3
"""
Lichess Puzzle Database Extractor for Gotham Chess Engine.

This script extracts puzzles from the Lichess puzzle database
and formats them for use in the Gotham Chess Engine.
"""

import csv
import random
from typing import List, Dict, Optional


def extract_puzzles_by_theme(csv_file_path: str, theme: str, count: int = 10) -> List[Dict]:
    """
    Extract puzzles from Lichess database by theme.
    
    Args:
        csv_file_path: Path to the Lichess puzzle CSV file
        theme: Theme to search for (e.g., 'fork', 'pin', 'mateIn1')
        count: Number of puzzles to extract
        
    Returns:
        List of puzzle dictionaries
    """
    puzzles = []
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                themes = row.get('Themes', '').split()
                if theme in themes:
                    # Parse the moves - first move is the solution
                    moves = row.get('Moves', '').split()
                    if moves:
                        solution = moves[0]  # First move is the solution
                        
                        puzzle = {
                            'id': row.get('PuzzleId', ''),
                            'fen': row.get('FEN', ''),
                            'solution': solution,
                            'all_moves': moves,
                            'rating': int(row.get('Rating', 0)) if row.get('Rating', '').isdigit() else 0,
                            'themes': themes,
                            'popularity': int(row.get('Popularity', 0)) if row.get('Popularity', '').isdigit() else 0,
                            'url': row.get('GameUrl', '')
                        }
                        puzzles.append(puzzle)
                        
                        if len(puzzles) >= count:
                            break
    
    except FileNotFoundError:
        print(f"Error: Could not find file {csv_file_path}")
        return []
    except Exception as e:
        print(f"Error reading puzzle database: {e}")
        return []
    
    return puzzles


def get_available_themes(csv_file_path: str, limit: int = 1000) -> Dict[str, int]:
    """
    Get all available themes and their counts.
    
    Args:
        csv_file_path: Path to the Lichess puzzle CSV file
        limit: Limit of rows to scan for performance
        
    Returns:
        Dictionary mapping themes to their counts
    """
    theme_counts = {}
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for i, row in enumerate(reader):
                if i >= limit:
                    break
                    
                themes = row.get('Themes', '').split()
                for theme in themes:
                    if theme:
                        theme_counts[theme] = theme_counts.get(theme, 0) + 1
    
    except Exception as e:
        print(f"Error scanning themes: {e}")
        return {}
    
    return theme_counts


def main():
    """Test the puzzle extraction."""
    csv_path = r"S:\Maker Stuff\Programming\Chess Engines\Chess Engine Playground\engine-tester\databases\lichess_db_puzzle.csv"
    
    print("🔍 Analyzing Lichess Puzzle Database...")
    
    # Get available themes
    print("📊 Scanning for available themes...")
    themes = get_available_themes(csv_path, limit=5000)
    
    # Print most common themes
    sorted_themes = sorted(themes.items(), key=lambda x: x[1], reverse=True)
    print(f"\n🎯 Top 20 most common themes:")
    for theme, count in sorted_themes[:20]:
        print(f"  {theme}: {count} puzzles")
    
    # Extract puzzles for our categories
    target_themes = ['fork', 'pin', 'skewer', 'discoveredAttack', 'mateIn1', 'mateIn2', 'deflection', 'sacrifice']
    
    print(f"\n🧩 Extracting puzzles for target themes...")
    
    for theme in target_themes:
        if theme in themes:
            print(f"\n--- {theme.upper()} PUZZLES ---")
            puzzles = extract_puzzles_by_theme(csv_path, theme, count=3)
            
            for i, puzzle in enumerate(puzzles, 1):
                print(f"\nPuzzle {i}:")
                print(f"  ID: {puzzle['id']}")
                print(f"  FEN: {puzzle['fen']}")
                print(f"  Solution: {puzzle['solution']}")
                print(f"  Rating: {puzzle['rating']}")
                print(f"  Themes: {', '.join(puzzle['themes'])}")
                print(f"  URL: {puzzle['url']}")
        else:
            print(f"\n❌ Theme '{theme}' not found in database")
    
    print(f"\n✅ Puzzle extraction complete!")


if __name__ == "__main__":
    main()