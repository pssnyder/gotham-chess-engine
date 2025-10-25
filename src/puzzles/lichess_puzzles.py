"""
Real Lichess Puzzle Library for Gotham Chess Engine.

This module loads real tactical puzzles from the Lichess database
to replace the synthetic puzzles with authentic chess positions.
"""

import csv
import random
from typing import List, Dict, Optional, Tuple
from enum import Enum
import os


class LichessPuzzleCategory(Enum):
    """Lichess puzzle categories mapped to our themes."""
    FORK = "fork"
    DISCOVERED_ATTACK = "discoveredAttack"
    CHECKMATE_IN_ONE = "mateIn1"
    CHECKMATE_IN_TWO = "mateIn2"
    PIN = "pin"
    SKEWER = "skewer"
    REMOVE_GUARD = "deflection"  # Using deflection as closest match
    DEFLECTION = "deflection"
    SACRIFICE = "sacrifice"


class LichessPuzzle:
    """Represents a real Lichess tactical puzzle."""
    
    def __init__(self, puzzle_id: str, fen: str, solution: str, moves: List[str],
                 rating: int, themes: List[str], url: str, popularity: int = 0):
        """
        Initialize a Lichess puzzle.
        
        Args:
            puzzle_id: Lichess puzzle ID
            fen: Position in FEN notation
            solution: Solution move in UCI notation
            moves: All moves in the solution line
            rating: Puzzle rating (difficulty)
            themes: List of puzzle themes
            url: URL to the original game
            popularity: Puzzle popularity score
        """
        self.puzzle_id = puzzle_id
        self.fen = fen
        self.solution = solution
        self.moves = moves
        self.rating = rating
        self.themes = themes
        self.url = url
        self.popularity = popularity
        
        # Map rating to difficulty (1-3)
        if rating < 1200:
            self.difficulty = 1
        elif rating < 1800:
            self.difficulty = 2
        else:
            self.difficulty = 3
        
        # Get primary category
        self.category = self._determine_category()
        
        # Generate educational description
        self.description = self._generate_description()
        self.educational_note = self._generate_educational_note()
    
    def _determine_category(self) -> LichessPuzzleCategory:
        """Determine the primary puzzle category."""
        # Priority order for theme mapping
        theme_priority = [
            ('mateIn1', LichessPuzzleCategory.CHECKMATE_IN_ONE),
            ('mateIn2', LichessPuzzleCategory.CHECKMATE_IN_TWO),
            ('fork', LichessPuzzleCategory.FORK),
            ('pin', LichessPuzzleCategory.PIN),
            ('skewer', LichessPuzzleCategory.SKEWER),
            ('discoveredAttack', LichessPuzzleCategory.DISCOVERED_ATTACK),
            ('deflection', LichessPuzzleCategory.DEFLECTION),
            ('sacrifice', LichessPuzzleCategory.SACRIFICE)
        ]
        
        for theme, category in theme_priority:
            if theme in self.themes:
                return category
        
        # Default fallback
        return LichessPuzzleCategory.DEFLECTION
    
    def _generate_description(self) -> str:
        """Generate a description based on the puzzle category."""
        descriptions = {
            LichessPuzzleCategory.FORK: "Find the fork that attacks multiple pieces",
            LichessPuzzleCategory.PIN: "Use a pin to win material or gain advantage",
            LichessPuzzleCategory.SKEWER: "Force the enemy piece to move and capture what's behind",
            LichessPuzzleCategory.DISCOVERED_ATTACK: "Move a piece to reveal a powerful attack",
            LichessPuzzleCategory.CHECKMATE_IN_ONE: "Find the checkmate in one move",
            LichessPuzzleCategory.CHECKMATE_IN_TWO: "Find the forced checkmate in two moves",
            LichessPuzzleCategory.DEFLECTION: "Deflect the defending piece to win material",
            LichessPuzzleCategory.SACRIFICE: "Find the tactical sacrifice that wins material"
        }
        return descriptions.get(self.category, "Find the best tactical move")
    
    def _generate_educational_note(self) -> str:
        """Generate educational explanation."""
        notes = {
            LichessPuzzleCategory.FORK: f"This {self.solution} move creates a fork! Look for moves that attack two enemy pieces simultaneously - they're one of the most powerful tactical weapons.",
            LichessPuzzleCategory.PIN: f"The move {self.solution} creates a pin! The pinned piece cannot move without exposing a more valuable piece behind it.",
            LichessPuzzleCategory.SKEWER: f"After {self.solution}, the enemy must move their valuable piece, allowing you to capture what's behind it. Skewers are 'reverse pins'!",
            LichessPuzzleCategory.DISCOVERED_ATTACK: f"Moving with {self.solution} reveals an attack from another piece! Discovered attacks are often devastating because you get two attacks for one move.",
            LichessPuzzleCategory.CHECKMATE_IN_ONE: f"The move {self.solution} delivers immediate checkmate! Always look for checkmate first - it's the ultimate goal.",
            LichessPuzzleCategory.CHECKMATE_IN_TWO: f"Starting with {self.solution} forces checkmate in 2 moves! Look for forcing moves that give your opponent no good options.",
            LichessPuzzleCategory.DEFLECTION: f"The move {self.solution} deflects the defending piece from its duty! Once the defender is gone, you can capture the undefended piece.",
            LichessPuzzleCategory.SACRIFICE: f"The sacrifice {self.solution} leads to a winning advantage! Sometimes giving up material creates even bigger gains."
        }
        return notes.get(self.category, f"The move {self.solution} is the key tactical blow in this position!")


class LichessPuzzleLibrary:
    """
    Real puzzle library using Lichess database.
    
    Loads authentic tactical puzzles from the Lichess puzzle database
    for educational training.
    """
    
    def __init__(self, csv_file_path: Optional[str] = None):
        """
        Initialize the Lichess puzzle library.
        
        Args:
            csv_file_path: Path to Lichess puzzle CSV file
        """
        self.csv_file_path = csv_file_path or self._get_default_csv_path()
        self.puzzles = {category: [] for category in LichessPuzzleCategory}
        self.all_puzzles = []
        self._load_puzzles()
    
    def _get_default_csv_path(self) -> str:
        """Get the default path to the Lichess puzzle database."""
        return r"S:\Maker Stuff\Programming\Chess Engines\Chess Engine Playground\engine-tester\databases\lichess_db_puzzle.csv"
    
    def _load_puzzles(self):
        """Load puzzles from the Lichess database."""
        if not os.path.exists(self.csv_file_path):
            print(f"Warning: Lichess puzzle database not found at {self.csv_file_path}")
            print("Using fallback to empty puzzle set.")
            return
        
        # Target themes to extract
        target_themes = {
            'fork': 15,
            'pin': 15, 
            'skewer': 10,
            'discoveredAttack': 10,
            'mateIn1': 15,
            'mateIn2': 10,
            'deflection': 10,
            'sacrifice': 15
        }
        
        theme_counts = {theme: 0 for theme in target_themes.keys()}
        
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    # Check if we've collected enough puzzles
                    if all(count >= limit for count, limit in zip(theme_counts.values(), target_themes.values())):
                        break
                    
                    themes = row.get('Themes', '').split()
                    
                    # Check if this puzzle has a theme we want
                    for theme in target_themes:
                        if theme in themes and theme_counts[theme] < target_themes[theme]:
                            puzzle = self._create_puzzle_from_row(row)
                            if puzzle:
                                self.puzzles[puzzle.category].append(puzzle)
                                self.all_puzzles.append(puzzle)
                                theme_counts[theme] += 1
                                break
        
        except Exception as e:
            print(f"Error loading Lichess puzzles: {e}")
            print("Using fallback puzzle set.")
            self._load_fallback_puzzles()
        
        print(f"Loaded {len(self.all_puzzles)} real Lichess puzzles:")
        for category in LichessPuzzleCategory:
            count = len(self.puzzles[category])
            print(f"  {category.value}: {count} puzzles")
    
    def _create_puzzle_from_row(self, row: Dict[str, str]) -> Optional[LichessPuzzle]:
        """Create a LichessPuzzle from a CSV row."""
        try:
            puzzle_id = row.get('PuzzleId', '')
            fen = row.get('FEN', '')
            moves = row.get('Moves', '').split()
            
            if len(moves) < 2:  # Need at least opponent move + our response
                return None
            
            # In Lichess puzzles:
            # moves[0] = opponent's move (blunder/poor move)
            # moves[1] = our correct response (the actual solution)
            solution = moves[1] if len(moves) > 1 else moves[0]
            rating = int(row.get('Rating', 0)) if row.get('Rating', '').isdigit() else 1200
            themes = row.get('Themes', '').split()
            url = row.get('GameUrl', '')
            popularity = int(row.get('Popularity', 0)) if row.get('Popularity', '').isdigit() else 0
            
            return LichessPuzzle(
                puzzle_id=puzzle_id,
                fen=fen,
                solution=solution,
                moves=moves,
                rating=rating,
                themes=themes,
                url=url,
                popularity=popularity
            )
        
        except Exception as e:
            print(f"Error creating puzzle from row: {e}")
            return None
    
    def _load_fallback_puzzles(self):
        """Load a minimal set of fallback puzzles if the database isn't available."""
        # Create a few basic puzzles as fallback
        fallback_data = [
            {
                'id': 'fallback_001',
                'fen': 'rnbqkb1r/pppp1ppp/5n2/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 2 3',
                'solution': 'Qh5',
                'moves': ['Qh5'],
                'rating': 1000,
                'themes': ['fork'],
                'url': 'fallback://example',
                'popularity': 50
            }
        ]
        
        for data in fallback_data:
            puzzle = LichessPuzzle(**data)
            self.puzzles[puzzle.category].append(puzzle)
            self.all_puzzles.append(puzzle)
    
    def get_puzzle_by_category(self, category: LichessPuzzleCategory) -> Optional[LichessPuzzle]:
        """Get a random puzzle from a specific category."""
        if category in self.puzzles and self.puzzles[category]:
            return random.choice(self.puzzles[category])
        return None
    
    def get_puzzle_by_difficulty(self, difficulty: int) -> Optional[LichessPuzzle]:
        """Get a random puzzle of specific difficulty."""
        matching_puzzles = [p for p in self.all_puzzles if p.difficulty == difficulty]
        if matching_puzzles:
            return random.choice(matching_puzzles)
        return None
    
    def get_random_puzzle(self) -> Optional[LichessPuzzle]:
        """Get a completely random puzzle."""
        if self.all_puzzles:
            return random.choice(self.all_puzzles)
        return None
    
    def get_puzzle_set(self, count: int = 5) -> List[LichessPuzzle]:
        """Get a diverse set of puzzles for training."""
        puzzle_set = []
        categories_used = set()
        
        # Try to get one puzzle from each category first
        for category in LichessPuzzleCategory:
            if len(puzzle_set) >= count:
                break
            puzzle = self.get_puzzle_by_category(category)
            if puzzle and category not in categories_used:
                puzzle_set.append(puzzle)
                categories_used.add(category)
        
        # Fill remaining slots with random puzzles
        while len(puzzle_set) < count and len(puzzle_set) < len(self.all_puzzles):
            puzzle = self.get_random_puzzle()
            if puzzle and puzzle not in puzzle_set:
                puzzle_set.append(puzzle)
        
        return puzzle_set
    
    def check_solution(self, puzzle: LichessPuzzle, player_move: str) -> bool:
        """Check if player's move matches the puzzle solution."""
        # Normalize the moves for comparison
        return player_move.strip().lower() == puzzle.solution.strip().lower()
    
    def get_hint(self, puzzle: LichessPuzzle) -> str:
        """Get a hint for the puzzle."""
        hints = {
            LichessPuzzleCategory.FORK: "Look for a move that attacks two pieces at once!",
            LichessPuzzleCategory.DISCOVERED_ATTACK: "Try moving a piece to reveal an attack from behind!",
            LichessPuzzleCategory.CHECKMATE_IN_ONE: "Find the move that gives checkmate immediately!",
            LichessPuzzleCategory.CHECKMATE_IN_TWO: "Look for a forcing move that leads to mate in two!",
            LichessPuzzleCategory.PIN: "Pin an enemy piece to something more valuable!",
            LichessPuzzleCategory.SKEWER: "Force a valuable piece to move and capture what's behind it!",
            LichessPuzzleCategory.REMOVE_GUARD: "Remove the piece that's defending something important!",
            LichessPuzzleCategory.DEFLECTION: "Force a defending piece away from its duty!",
            LichessPuzzleCategory.SACRIFICE: "Sometimes giving up material leads to bigger gains!"
        }
        
        return hints.get(puzzle.category, "Look for the best tactical move!")
    
    def get_puzzle_statistics(self) -> Dict[str, int]:
        """Get statistics about the puzzle library."""
        stats = {
            "total_puzzles": len(self.all_puzzles),
            "by_category": {},
            "by_difficulty": {1: 0, 2: 0, 3: 0}
        }
        
        for category in LichessPuzzleCategory:
            count = len(self.puzzles[category])
            stats["by_category"][category.value] = count
        
        for puzzle in self.all_puzzles:
            stats["by_difficulty"][puzzle.difficulty] += 1
        
        return stats
    
    def test_engine_solving(self, engine, min_success_rate: float = 0.6) -> Dict[str, bool]:
        """
        Test if the engine can solve puzzles from each category.
        
        Args:
            engine: Chess engine instance
            min_success_rate: Minimum success rate required (0.0 to 1.0)
            
        Returns:
            Dict mapping categories to pass/fail status
        """
        results = {}
        
        for category in LichessPuzzleCategory:
            category_puzzles = self.puzzles[category]
            if not category_puzzles:
                results[category.value] = False
                continue
            
            # Test up to 5 puzzles from this category
            test_puzzles = category_puzzles[:min(5, len(category_puzzles))]
            solved = 0
            
            for puzzle in test_puzzles:
                try:
                    # Set up the position
                    engine.set_position(puzzle.fen)
                    
                    # Get engine's move
                    engine_move = engine.get_best_move()
                    
                    if engine_move and str(engine_move) == puzzle.solution:
                        solved += 1
                
                except Exception as e:
                    print(f"Error testing puzzle {puzzle.puzzle_id}: {e}")
            
            success_rate = solved / len(test_puzzles) if test_puzzles else 0
            results[category.value] = success_rate >= min_success_rate
            
            print(f"{category.value}: {solved}/{len(test_puzzles)} solved ({success_rate:.1%})")
        
        return results


def create_lichess_training_session(puzzle_library: LichessPuzzleLibrary, 
                                   focus_category: Optional[LichessPuzzleCategory] = None,
                                   difficulty: Optional[int] = None) -> List[LichessPuzzle]:
    """
    Create a focused training session with real Lichess puzzles.
    
    Args:
        puzzle_library: The Lichess puzzle library
        focus_category: Category to focus on (optional)
        difficulty: Difficulty level to focus on (optional)
        
    Returns:
        List of puzzles for training session
    """
    if focus_category:
        # Get all puzzles from the focus category
        training_puzzles = puzzle_library.puzzles[focus_category].copy()
        if difficulty:
            training_puzzles = [p for p in training_puzzles if p.difficulty == difficulty]
    elif difficulty:
        # Get puzzles of specific difficulty
        training_puzzles = [p for p in puzzle_library.all_puzzles if p.difficulty == difficulty]
    else:
        # Get a diverse set
        training_puzzles = puzzle_library.get_puzzle_set(count=10)
    
    # Shuffle for variety
    random.shuffle(training_puzzles)
    return training_puzzles[:5]  # Return 5 puzzles per session