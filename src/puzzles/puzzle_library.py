"""
Tactical puzzle library for Gotham Chess Engine.

This module contains a comprehensive puzzle database with 27 puzzles
across 9 tactical categories for educational training.
"""

import chess
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class PuzzleCategory(Enum):
    """Tactical puzzle categories."""
    FORK = "fork"
    DISCOVERED_ATTACK = "discovered_attack" 
    CHECKMATE_IN_ONE = "checkmate_in_one"
    CHECKMATE_IN_TWO = "checkmate_in_two"
    PIN = "pin"
    SKEWER = "skewer"
    REMOVE_GUARD = "remove_guard"
    DEFLECTION = "deflection"
    SACRIFICE = "sacrifice"


class TacticalPuzzle:
    """Represents a single tactical puzzle."""
    
    def __init__(self, fen: str, solution: str, category: PuzzleCategory, 
                 description: str, educational_note: str, difficulty: int = 1):
        """
        Initialize a tactical puzzle.
        
        Args:
            fen: Position in FEN notation
            solution: Solution move in algebraic notation
            category: Puzzle category
            description: Brief description of the tactic
            educational_note: Educational explanation
            difficulty: Difficulty level (1-3)
        """
        self.fen = fen
        self.solution = solution
        self.category = category
        self.description = description
        self.educational_note = educational_note
        self.difficulty = difficulty


class GothamPuzzleLibrary:
    """
    Tactical puzzle library for Gotham Chess Engine.
    
    Contains 27 carefully selected puzzles across 9 categories
    to help players improve their tactical vision.
    """
    
    def __init__(self):
        """Initialize the puzzle library."""
        self.puzzles = self._initialize_puzzle_database()
        self.categories = list(PuzzleCategory)
    
    def _initialize_puzzle_database(self) -> Dict[PuzzleCategory, List[TacticalPuzzle]]:
        """Initialize the complete puzzle database."""
        puzzles = {category: [] for category in PuzzleCategory}
        
        # FORK PUZZLES (3)
        puzzles[PuzzleCategory.FORK].extend([
            TacticalPuzzle(
                fen="rnbqkb1r/pppp1ppp/5n2/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 2 3",
                solution="Qh5",
                category=PuzzleCategory.FORK,
                description="Queen fork on king and knight",
                educational_note="The queen attacks both the king and the knight on f6. This is a classic example of a royal fork!",
                difficulty=1
            ),
            TacticalPuzzle(
                fen="r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R b KQkq - 0 4",
                solution="Nd4",
                category=PuzzleCategory.FORK,
                description="Knight fork attacking king and bishop",
                educational_note="Knights are excellent forking pieces! Here Nd4 attacks both the king and the bishop on c4.",
                difficulty=2
            ),
            TacticalPuzzle(
                fen="rnbqk2r/pppp1ppp/5n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R b KQkq - 0 4",
                solution="Nd5",
                category=PuzzleCategory.FORK,
                description="Knight fork with check",
                educational_note="Nd5 gives check and also attacks the bishop. Always look for forks that give check - they're even more powerful!",
                difficulty=2
            )
        ])
        
        # DISCOVERED ATTACK PUZZLES (3)
        puzzles[PuzzleCategory.DISCOVERED_ATTACK].extend([
            TacticalPuzzle(
                fen="r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 b kq - 0 5",
                solution="Nd4",
                category=PuzzleCategory.DISCOVERED_ATTACK,
                description="Knight move discovers bishop attack",
                educational_note="Moving the knight discovers an attack from the bishop behind it. Discovered attacks can be devastating!",
                difficulty=2
            ),
            TacticalPuzzle(
                fen="r1bq1rk1/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 w - - 0 6",
                solution="Nh4",
                category=PuzzleCategory.DISCOVERED_ATTACK,
                description="Knight discovers queen attack on bishop",
                educational_note="The knight move uncovers the queen's attack on the bishop. Look for pieces that can move to reveal attacks!",
                difficulty=2
            ),
            TacticalPuzzle(
                fen="r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP1QPPP/RNB2RK1 b kq - 0 5",
                solution="Ng4",
                category=PuzzleCategory.DISCOVERED_ATTACK,
                description="Discovered check with knight",
                educational_note="Ng4 discovers check from the queen while attacking the queen! Discovered checks are extremely powerful.",
                difficulty=3
            )
        ])
        
        # CHECKMATE IN ONE PUZZLES (3)
        puzzles[PuzzleCategory.CHECKMATE_IN_ONE].extend([
            TacticalPuzzle(
                fen="6k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1",
                solution="Re8#",
                category=PuzzleCategory.CHECKMATE_IN_ONE,
                description="Back rank mate with rook",
                educational_note="The black king is trapped on the back rank by its own pawns. Re8# delivers checkmate!",
                difficulty=1
            ),
            TacticalPuzzle(
                fen="r3k2r/8/8/8/8/8/8/4K3 b kq - 0 1",
                solution="Ra1#",
                category=PuzzleCategory.CHECKMATE_IN_ONE,
                description="Rook delivers mate on first rank",
                educational_note="Ra1# is checkmate because the white king cannot escape and no piece can block or capture.",
                difficulty=1
            ),
            TacticalPuzzle(
                fen="5rk1/5ppp/8/8/8/8/5PPP/3Q2K1 w - - 0 1",
                solution="Qd8#",
                category=PuzzleCategory.CHECKMATE_IN_ONE,
                description="Queen delivers back rank mate",
                educational_note="Qd8# checkmates because the king is trapped by its own pawns and the rook cannot capture the queen.",
                difficulty=2
            )
        ])
        
        # CHECKMATE IN TWO PUZZLES (3)
        puzzles[PuzzleCategory.CHECKMATE_IN_TWO].extend([
            TacticalPuzzle(
                fen="6k1/5ppp/8/8/8/8/5PPP/4QK2 w - - 0 1",
                solution="Qe8+",
                category=PuzzleCategory.CHECKMATE_IN_TWO,
                description="Queen sacrifice leads to mate",
                educational_note="After 1.Qe8+ Kh7 (forced), then 2.Qh8# is checkmate. Sometimes sacrificing the queen wins the game!",
                difficulty=2
            ),
            TacticalPuzzle(
                fen="r3k3/8/8/8/8/8/8/4K2R w Kq - 0 1",
                solution="Rh8+",
                category=PuzzleCategory.CHECKMATE_IN_TWO,
                description="Rook check forces mate",
                educational_note="1.Rh8+ forces Kd7, then 2.Ra8# is mate. The rook controls the entire 8th rank!",
                difficulty=2
            ),
            TacticalPuzzle(
                fen="5k2/5ppp/8/8/8/8/5PPP/4QK2 w - - 0 1",
                solution="Qc8+",
                category=PuzzleCategory.CHECKMATE_IN_TWO,
                description="Queen forces king into mate net",
                educational_note="1.Qc8+ Ke7 2.Qe8# is forced mate. The queen controls all escape squares!",
                difficulty=3
            )
        ])
        
        # PIN PUZZLES (3)
        puzzles[PuzzleCategory.PIN].extend([
            TacticalPuzzle(
                fen="r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 4",
                solution="Bg5",
                category=PuzzleCategory.PIN,
                description="Bishop pins knight to queen",
                educational_note="Bg5 pins the knight to the queen - the knight cannot move without losing the queen!",
                difficulty=1
            ),
            TacticalPuzzle(
                fen="r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 5",
                solution="Bb5",
                category=PuzzleCategory.PIN,
                description="Bishop pins knight to king",
                educational_note="Bb5 pins the knight to the king. This is an absolute pin - the knight cannot move at all!",
                difficulty=2
            ),
            TacticalPuzzle(
                fen="r1bq1rk1/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 w - - 0 6",
                solution="Bxf7+",
                category=PuzzleCategory.PIN,
                description="Pin exploit with sacrifice",
                educational_note="After Bxf7+ the king must move, and then we can capture the pinned knight with Ng5!",
                difficulty=3
            )
        ])
        
        # SKEWER PUZZLES (3)
        puzzles[PuzzleCategory.SKEWER].extend([
            TacticalPuzzle(
                fen="r3k2r/8/8/8/8/8/8/4K3 w kq - 0 1",
                solution="Ra8+",
                category=PuzzleCategory.SKEWER,
                description="Rook skewers king and rook",
                educational_note="Ra8+ forces the king to move, and then we can capture the rook with Rxh8!",
                difficulty=1
            ),
            TacticalPuzzle(
                fen="r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 b kq - 0 5",
                solution="Bb4+",
                category=PuzzleCategory.SKEWER,
                description="Bishop skewer with check",
                educational_note="Bb4+ skewers the king and queen. The king must move and we win the queen!",
                difficulty=2
            ),
            TacticalPuzzle(
                fen="r1bq1rk1/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 w - - 0 6",
                solution="Bxf7+",
                category=PuzzleCategory.SKEWER,
                description="Discovered skewer attack",
                educational_note="Bxf7+ forces Kh8, and then Bb3+ skewers the king and the back rank rook!",
                difficulty=3
            )
        ])
        
        # REMOVE GUARD PUZZLES (3)
        puzzles[PuzzleCategory.REMOVE_GUARD].extend([
            TacticalPuzzle(
                fen="r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 w kq - 0 5",
                solution="Bxf7+",
                category=PuzzleCategory.REMOVE_GUARD,
                description="Remove the guard of the king",
                educational_note="Bxf7+ removes the pawn that guards the king, exposing it to further attack!",
                difficulty=2
            ),
            TacticalPuzzle(
                fen="r1bq1rk1/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 b - - 0 6",
                solution="Bxf2+",
                category=PuzzleCategory.REMOVE_GUARD,
                description="Remove guard with check",
                educational_note="Bxf2+ removes the pawn guard and gives check, winning material after the king moves!",
                difficulty=2
            ),
            TacticalPuzzle(
                fen="r1bqk2r/pppp1ppp/2n2n2/4p3/2B1P1b1/3P1N2/PPP2PPP/RNBQ1RK1 w kq - 0 5",
                solution="Nxe5",
                category=PuzzleCategory.REMOVE_GUARD,
                description="Remove guard of bishop",
                educational_note="Nxe5 removes the knight that was defending the bishop on g4, winning the bishop!",
                difficulty=3
            )
        ])
        
        # DEFLECTION PUZZLES (3)
        puzzles[PuzzleCategory.DEFLECTION].extend([
            TacticalPuzzle(
                fen="r1bq1rk1/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 w - - 0 6",
                solution="Nh4",
                category=PuzzleCategory.DEFLECTION,
                description="Deflect the defending knight",
                educational_note="Nh4 attacks the bishop, forcing it to move and deflecting it from defending the e5 pawn!",
                difficulty=2
            ),
            TacticalPuzzle(
                fen="r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 b kq - 0 5",
                solution="Nd4",
                category=PuzzleCategory.DEFLECTION,
                description="Deflect with knight attack",
                educational_note="Nd4 attacks the bishop and queen, deflecting one from defending the other!",
                difficulty=2
            ),
            TacticalPuzzle(
                fen="r1bq1rk1/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 w - - 0 6",
                solution="Qb3",
                category=PuzzleCategory.DEFLECTION,
                description="Queen deflection attack",
                educational_note="Qb3 attacks the bishop, deflecting it from its strong central position!",
                difficulty=3
            )
        ])
        
        # SACRIFICE PUZZLES (3)
        puzzles[PuzzleCategory.SACRIFICE].extend([
            TacticalPuzzle(
                fen="r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 w kq - 0 5",
                solution="Bxf7+",
                category=PuzzleCategory.SACRIFICE,
                description="Bishop sacrifice for attack",
                educational_note="Bxf7+ sacrifices the bishop to expose the king and gain a winning attack!",
                difficulty=2
            ),
            TacticalPuzzle(
                fen="r1bq1rk1/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQ1RK1 w - - 0 6",
                solution="Nxe5",
                category=PuzzleCategory.SACRIFICE,
                description="Knight sacrifice wins material",
                educational_note="Nxe5 sacrifices the knight but wins the bishop after Nxc6, gaining material advantage!",
                difficulty=2
            ),
            TacticalPuzzle(
                fen="r1bqk2r/pppp1ppp/2n2n2/4p3/2B1P1b1/3P1N2/PPP2PPP/RNBQ1RK1 w kq - 0 5",
                solution="Nxe5",
                category=PuzzleCategory.SACRIFICE,
                description="Exchange sacrifice for position",
                educational_note="Nxe5 sacrifices the knight to destroy Black's center and gain positional compensation!",
                difficulty=3
            )
        ])
        
        return puzzles
    
    def get_puzzle_by_category(self, category: PuzzleCategory) -> Optional[TacticalPuzzle]:
        """
        Get a random puzzle from a specific category.
        
        Args:
            category: Puzzle category
            
        Returns:
            Random puzzle from the category
        """
        if category in self.puzzles and self.puzzles[category]:
            return random.choice(self.puzzles[category])
        return None
    
    def get_puzzle_by_difficulty(self, difficulty: int) -> Optional[TacticalPuzzle]:
        """
        Get a random puzzle of specific difficulty.
        
        Args:
            difficulty: Difficulty level (1-3)
            
        Returns:
            Random puzzle of the specified difficulty
        """
        all_puzzles = []
        for category_puzzles in self.puzzles.values():
            all_puzzles.extend([p for p in category_puzzles if p.difficulty == difficulty])
        
        if all_puzzles:
            return random.choice(all_puzzles)
        return None
    
    def get_random_puzzle(self) -> Optional[TacticalPuzzle]:
        """
        Get a completely random puzzle.
        
        Returns:
            Random puzzle from any category
        """
        all_puzzles = []
        for category_puzzles in self.puzzles.values():
            all_puzzles.extend(category_puzzles)
        
        if all_puzzles:
            return random.choice(all_puzzles)
        return None
    
    def get_puzzle_set(self, count: int = 5) -> List[TacticalPuzzle]:
        """
        Get a set of diverse puzzles for training.
        
        Args:
            count: Number of puzzles to return
            
        Returns:
            List of diverse puzzles
        """
        puzzle_set = []
        categories_used = set()
        
        # Try to get one puzzle from each category first
        for category in self.categories:
            if len(puzzle_set) >= count:
                break
            puzzle = self.get_puzzle_by_category(category)
            if puzzle and category not in categories_used:
                puzzle_set.append(puzzle)
                categories_used.add(category)
        
        # Fill remaining slots with random puzzles
        while len(puzzle_set) < count:
            puzzle = self.get_random_puzzle()
            if puzzle and puzzle not in puzzle_set:
                puzzle_set.append(puzzle)
        
        return puzzle_set
    
    def check_solution(self, puzzle: TacticalPuzzle, player_move: str) -> bool:
        """
        Check if player's move matches the puzzle solution.
        
        Args:
            puzzle: The tactical puzzle
            player_move: Player's move in algebraic notation
            
        Returns:
            True if correct solution
        """
        return player_move.strip().lower() == puzzle.solution.strip().lower()
    
    def get_hint(self, puzzle: TacticalPuzzle) -> str:
        """
        Get a hint for the puzzle.
        
        Args:
            puzzle: The tactical puzzle
            
        Returns:
            Hint string
        """
        hints = {
            PuzzleCategory.FORK: "Look for a move that attacks two pieces at once!",
            PuzzleCategory.DISCOVERED_ATTACK: "Try moving a piece to reveal an attack from behind!",
            PuzzleCategory.CHECKMATE_IN_ONE: "Find the move that gives checkmate immediately!",
            PuzzleCategory.CHECKMATE_IN_TWO: "Look for a forcing move that leads to mate in two!",
            PuzzleCategory.PIN: "Pin an enemy piece to something more valuable!",
            PuzzleCategory.SKEWER: "Force a valuable piece to move and capture what's behind it!",
            PuzzleCategory.REMOVE_GUARD: "Remove the piece that's defending something important!",
            PuzzleCategory.DEFLECTION: "Force a defending piece away from its duty!",
            PuzzleCategory.SACRIFICE: "Sometimes giving up material leads to bigger gains!"
        }
        
        return hints.get(puzzle.category, "Look for the best tactical move!")
    
    def get_puzzle_statistics(self) -> Dict[str, int]:
        """
        Get statistics about the puzzle library.
        
        Returns:
            Dictionary with puzzle statistics
        """
        stats = {
            "total_puzzles": 0,
            "by_category": {},
            "by_difficulty": {1: 0, 2: 0, 3: 0}
        }
        
        for category, category_puzzles in self.puzzles.items():
            count = len(category_puzzles)
            stats["by_category"][category.value] = count
            stats["total_puzzles"] += count
            
            for puzzle in category_puzzles:
                stats["by_difficulty"][puzzle.difficulty] += 1
        
        return stats


def create_puzzle_training_session(puzzle_library: GothamPuzzleLibrary, 
                                 focus_category: Optional[PuzzleCategory] = None,
                                 difficulty: Optional[int] = None) -> List[TacticalPuzzle]:
    """
    Create a focused training session.
    
    Args:
        puzzle_library: The puzzle library
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
        training_puzzles = []
        for category_puzzles in puzzle_library.puzzles.values():
            training_puzzles.extend([p for p in category_puzzles if p.difficulty == difficulty])
    else:
        # Get a diverse set
        training_puzzles = puzzle_library.get_puzzle_set(count=10)
    
    # Shuffle for variety
    random.shuffle(training_puzzles)
    return training_puzzles[:5]  # Return 5 puzzles per session