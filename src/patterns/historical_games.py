"""
Historical game knowledge for Gotham Chess Engine.

This module contains pattern recognition for famous chess games
that Gotham Chess frequently references in educational content.
"""

import chess
import chess.pgn
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum


class HistoricalGame(Enum):
    """Famous chess games referenced by Gotham Chess."""
    IMMORTAL_GAME = "immortal_game"
    MOZART_GAME = "mozart_game"
    KASPAROV_IMMORTAL = "kasparov_immortal"
    SHORT_TIMMAN = "short_timman"
    OPERA_GAME = "opera_game"


class GothamHistoricalAnalyzer:
    """
    Historical game pattern analyzer for educational insights.
    
    Recognizes patterns and themes from famous games that Gotham
    Chess uses in educational content.
    """
    
    def __init__(self):
        """Initialize with historical game data."""
        self.historical_games = self._initialize_games()
        self.pattern_signatures = self._initialize_signatures()
    
    def _initialize_games(self) -> Dict[HistoricalGame, Dict]:
        """Initialize historical game database."""
        return {
            HistoricalGame.IMMORTAL_GAME: {
                "players": "Anderssen vs. Kieseritzky",
                "year": 1851,
                "opening": "King's Gambit Accepted",
                "key_themes": [
                    "Brilliant sacrifices",
                    "Attacking the king",
                    "Material sacrifice for attack",
                    "Open file domination"
                ],
                "famous_moves": [
                    "18.Bd6",  # Famous bishop sacrifice
                    "22.Be7",  # Another sacrifice
                    "23.Bxf7+"  # The final blow
                ],
                "educational_value": [
                    "Shows power of piece activity over material",
                    "Demonstrates importance of king safety",
                    "Example of brilliant tactical sacrifices",
                    "Classic attacking masterpiece"
                ],
                "position_features": {
                    "open_center": True,
                    "exposed_king": True,
                    "active_pieces": True,
                    "material_imbalance": True
                }
            },
            
            HistoricalGame.MOZART_GAME: {
                "players": "Carlsen vs. Ernst",
                "year": 2004,
                "opening": "Scandinavian Defense",
                "key_themes": [
                    "Positional sacrifices",
                    "Long-term compensation",
                    "Piece activity vs material",
                    "Endgame technique"
                ],
                "famous_moves": [
                    "7...Qd6",  # Ernst's creative queen move
                    "13.Bxf7+",  # Carlsen's positional sacrifice
                    "14.Ng5"    # Follow-up
                ],
                "educational_value": [
                    "Shows positional understanding over material",
                    "Demonstrates long-term thinking",
                    "Example of modern positional play",
                    "Piece activity compensation"
                ],
                "position_features": {
                    "pawn_structure_damage": True,
                    "piece_activity": True,
                    "king_safety": False,
                    "material_imbalance": True
                }
            },
            
            HistoricalGame.KASPAROV_IMMORTAL: {
                "players": "Kasparov vs. Topalov",
                "year": 1999,
                "opening": "Pirc Defense",
                "key_themes": [
                    "Deep positional sacrifices",
                    "Long-term planning",
                    "Tactical brilliance",
                    "King hunt"
                ],
                "famous_moves": [
                    "24.Rxd4",   # The exchange sacrifice
                    "25.Re4",    # Brilliant rook move
                    "26.Qg3"     # Queen enters the attack
                ],
                "educational_value": [
                    "Shows deep positional understanding",
                    "Demonstrates calculation depth",
                    "Example of modern attacking play",
                    "Combination of strategy and tactics"
                ],
                "position_features": {
                    "central_control": True,
                    "piece_coordination": True,
                    "tactical_complexity": True,
                    "king_hunt": True
                }
            },
            
            HistoricalGame.SHORT_TIMMAN: {
                "players": "Short vs. Timman",
                "year": 1991,
                "opening": "Sicilian Defense",
                "key_themes": [
                    "Piece activity",
                    "King in the center",
                    "Dynamic play",
                    "Tactical fireworks"
                ],
                "famous_moves": [
                    "18.Nd5",    # Knight sacrifice offer
                    "19.Kb1",    # King march
                    "20.Nf6+"    # Tactical blow
                ],
                "educational_value": [
                    "Shows importance of piece activity",
                    "Demonstrates king as fighting piece",
                    "Example of dynamic imbalances",
                    "Modern tactical play"
                ],
                "position_features": {
                    "active_king": True,
                    "piece_activity": True,
                    "tactical_themes": True,
                    "imbalanced_position": True
                }
            },
            
            HistoricalGame.OPERA_GAME: {
                "players": "Morphy vs. Duke & Count",
                "year": 1858,
                "opening": "Italian Game",
                "key_themes": [
                    "Rapid development",
                    "Open lines",
                    "Classic attack",
                    "Pure tactical beauty"
                ],
                "famous_moves": [
                    "10.Nxb5",   # Knight sacrifice
                    "11.Nxd7",   # Another sacrifice
                    "12.Qb3"     # Queen attack
                ],
                "educational_value": [
                    "Shows importance of development",
                    "Demonstrates open file power",
                    "Classic sacrificial attack",
                    "Perfect execution"
                ],
                "position_features": {
                    "rapid_development": True,
                    "open_files": True,
                    "tactical_themes": True,
                    "king_safety": False
                }
            }
        }
    
    def _initialize_signatures(self) -> Dict[HistoricalGame, List[str]]:
        """Initialize position signatures for game recognition."""
        return {
            HistoricalGame.IMMORTAL_GAME: [
                "f2f4",  # King's Gambit
                "exposed_black_king",
                "multiple_sacrifices",
                "open_center"
            ],
            HistoricalGame.MOZART_GAME: [
                "e4_d5",  # Scandinavian
                "positional_sacrifice",
                "piece_activity",
                "endgame_technique"
            ],
            HistoricalGame.KASPAROV_IMMORTAL: [
                "e4_d6_nf6_g6",  # Pirc setup
                "exchange_sacrifice",
                "king_hunt",
                "deep_calculation"
            ],
            HistoricalGame.SHORT_TIMMAN: [
                "sicilian_defense",
                "active_king",
                "piece_activity",
                "tactical_complexity"
            ],
            HistoricalGame.OPERA_GAME: [
                "e4_e5_nf3_d6",  # Italian Game setup
                "rapid_development",
                "multiple_sacrifices",
                "open_files"
            ]
        }
    
    def analyze_position_for_historical_patterns(self, board: chess.Board) -> Dict[str, Any]:
        """
        Analyze position for patterns from historical games.
        
        Args:
            board: Current chess position
            
        Returns:
            Dict with historical pattern analysis
        """
        analysis = {
            "historical_patterns": [],
            "educational_insights": [],
            "similar_games": [],
            "tactical_themes": [],
            "positional_themes": []
        }
        
        # Check for specific game patterns
        for game_type in HistoricalGame:
            similarity = self._calculate_similarity(board, game_type)
            if similarity > 0.3:  # Threshold for pattern recognition
                game_data = self.historical_games[game_type]
                analysis["similar_games"].append({
                    "game": game_type.value,
                    "similarity": similarity,
                    "players": game_data["players"],
                    "year": game_data["year"],
                    "themes": game_data["key_themes"]
                })
        
        # Extract educational insights
        analysis["educational_insights"] = self._get_educational_insights(board)
        
        # Identify tactical and positional themes
        analysis["tactical_themes"] = self._identify_tactical_themes(board)
        analysis["positional_themes"] = self._identify_positional_themes(board)
        
        return analysis
    
    def _calculate_similarity(self, board: chess.Board, game_type: HistoricalGame) -> float:
        """
        Calculate similarity to a historical game pattern.
        
        Args:
            board: Current position
            game_type: Historical game to compare with
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        game_data = self.historical_games[game_type]
        features = game_data["position_features"]
        score = 0.0
        total_features = len(features)
        
        # Check position features
        if features.get("open_center", False) and self._has_open_center(board):
            score += 1
        
        if features.get("exposed_king", False) and self._has_exposed_king(board):
            score += 1
        
        if features.get("active_pieces", False) and self._has_active_pieces(board):
            score += 1
        
        if features.get("material_imbalance", False) and self._has_material_imbalance(board):
            score += 1
        
        if features.get("tactical_complexity", False) and self._has_tactical_complexity(board):
            score += 1
        
        if features.get("piece_activity", False) and self._has_high_piece_activity(board):
            score += 1
        
        return min(score / max(total_features, 1), 1.0)
    
    def _has_open_center(self, board: chess.Board) -> bool:
        """Check if position has open center."""
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        pawns_in_center = 0
        
        for square in center_squares:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                pawns_in_center += 1
        
        return pawns_in_center <= 1
    
    def _has_exposed_king(self, board: chess.Board) -> bool:
        """Check if either king is exposed."""
        for color in [chess.WHITE, chess.BLACK]:
            king_square = board.king(color)
            if king_square is None:
                continue
            
            # Check if king is away from back rank or uncastled
            king_rank = chess.square_rank(king_square)
            back_rank = 0 if color == chess.WHITE else 7
            
            if king_rank != back_rank:
                return True
            
            # Check for missing pawn shield
            pawn_shield = 0
            king_file = chess.square_file(king_square)
            
            for file_offset in [-1, 0, 1]:
                shield_file = king_file + file_offset
                if 0 <= shield_file <= 7:
                    shield_rank = 1 if color == chess.WHITE else 6
                    shield_square = chess.square(shield_file, shield_rank)
                    piece = board.piece_at(shield_square)
                    if piece and piece.piece_type == chess.PAWN and piece.color == color:
                        pawn_shield += 1
            
            if pawn_shield < 2:
                return True
        
        return False
    
    def _has_active_pieces(self, board: chess.Board) -> bool:
        """Check if pieces are actively placed."""
        active_count = 0
        total_pieces = 0
        
        center_area = [
            chess.C3, chess.C4, chess.C5, chess.C6,
            chess.D3, chess.D4, chess.D5, chess.D6,
            chess.E3, chess.E4, chess.E5, chess.E6,
            chess.F3, chess.F4, chess.F5, chess.F6
        ]
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type != chess.PAWN:
                total_pieces += 1
                if square in center_area:
                    active_count += 1
        
        return total_pieces > 0 and (active_count / total_pieces) > 0.3
    
    def _has_material_imbalance(self, board: chess.Board) -> bool:
        """Check if there's significant material imbalance."""
        white_material = 0
        black_material = 0
        
        piece_values = {
            chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0
        }
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                if piece.color == chess.WHITE:
                    white_material += value
                else:
                    black_material += value
        
        return abs(white_material - black_material) >= 3
    
    def _has_tactical_complexity(self, board: chess.Board) -> bool:
        """Check if position has tactical complexity."""
        # Simple heuristic: multiple pieces attacking/defending
        attacking_moves = 0
        
        for move in board.legal_moves:
            if board.is_capture(move) or board.gives_check(move):
                attacking_moves += 1
        
        return attacking_moves > 5
    
    def _has_high_piece_activity(self, board: chess.Board) -> bool:
        """Check if pieces have high activity."""
        total_mobility = 0
        piece_count = 0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type != chess.PAWN:
                piece_count += 1
                # Count legal moves from this square
                moves_from_square = [m for m in board.legal_moves if m.from_square == square]
                total_mobility += len(moves_from_square)
        
        return piece_count > 0 and (total_mobility / piece_count) > 4
    
    def _get_educational_insights(self, board: chess.Board) -> List[str]:
        """Get educational insights based on position."""
        insights = []
        
        if self._has_open_center(board):
            insights.append("Open center allows for tactical possibilities - like the Immortal Game!")
        
        if self._has_exposed_king(board):
            insights.append("Exposed king creates attacking chances - remember Morphy's Opera Game!")
        
        if self._has_material_imbalance(board):
            insights.append("Material imbalance creates dynamic play - like Carlsen's Mozart Game!")
        
        if self._has_tactical_complexity(board):
            insights.append("Complex tactical position - calculate like Kasparov!")
        
        return insights
    
    def _identify_tactical_themes(self, board: chess.Board) -> List[str]:
        """Identify tactical themes in the position."""
        themes = []
        
        # Check for common tactical motifs
        for move in board.legal_moves:
            if board.is_capture(move):
                themes.append("Capturing")
            
            if board.gives_check(move):
                themes.append("Checking")
            
            board.push(move)
            if board.is_checkmate():
                themes.append("Checkmate threat")
            board.pop()
        
        return list(set(themes))  # Remove duplicates
    
    def _identify_positional_themes(self, board: chess.Board) -> List[str]:
        """Identify positional themes in the position."""
        themes = []
        
        if self._has_open_center(board):
            themes.append("Open center")
        
        if self._has_active_pieces(board):
            themes.append("Active pieces")
        
        if self._has_material_imbalance(board):
            themes.append("Material imbalance")
        
        return themes
    
    def get_historical_move_suggestion(self, board: chess.Board) -> Optional[Dict]:
        """
        Suggest a move based on historical game patterns.
        
        Args:
            board: Current position
            
        Returns:
            Move suggestion with historical context
        """
        # Find the most similar historical game
        best_similarity = 0
        best_game = None
        
        for game_type in HistoricalGame:
            similarity = self._calculate_similarity(board, game_type)
            if similarity > best_similarity:
                best_similarity = similarity
                best_game = game_type
        
        if best_game and best_similarity > 0.4:
            game_data = self.historical_games[best_game]
            return {
                "historical_reference": game_data["players"],
                "year": game_data["year"],
                "themes": game_data["key_themes"],
                "advice": f"This position resembles {game_data['players']} ({game_data['year']})",
                "educational_value": game_data["educational_value"]
            }
        
        return None


def get_historical_insights(position_analysis: Dict) -> List[str]:
    """
    Generate educational insights from historical analysis.
    
    Args:
        position_analysis: Analysis from historical analyzer
        
    Returns:
        List of educational insights
    """
    insights = []
    
    if position_analysis["similar_games"]:
        game = position_analysis["similar_games"][0]  # Most similar
        insights.append(f"This position reminds me of {game['players']} ({game['year']})!")
        insights.extend(game["themes"][:2])  # Add top 2 themes
    
    insights.extend(position_analysis["educational_insights"])
    
    return insights[:4]  # Limit to 4 insights