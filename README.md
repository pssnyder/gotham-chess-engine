# Gotham Chess Engine
Gotham Chess Engine is a chess engine built from the cumulative chess knowledge of the chess Youtuber GothamChess (Levy Rozman). The engine is designed to provide strong chess play and analysis, leveraging modern algorithms and techniques. It aims be approachable to beginners by applying the same principles Levy teaches in his recently release hbook "How To Win At Chess" and his Chess Deck product.

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd gotham-chess-engine
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the demo:**
   ```bash
   python main.py
   ```

### Running Tests

```bash
pytest tests/ -v
```

## Features
- **Principled chess play** based on Gotham Chess teachings
- **Educational move explanations** with strategic insights
- **Approachable opening book** for black and white
- **Basic tactical heuristics** with pattern recognition
- **Key positional understanding** from critical games throughout history
- **Game phase awareness** (opening, middlegame, endgame)
- **Time management strategies** built into the search
- **Comprehensive position analysis** with educational feedback

---

## 🏗️ Project Structure

```
gotham-chess-engine/
├── src/
│   ├── core/
│   │   ├── board.py          # Enhanced chess board with educational features
│   │   └── pieces.py         # Piece evaluation and tactical patterns
│   ├── openings/
│   │   └── opening_book.py   # Opening repertoire based on Gotham teachings
│   ├── evaluation/           # Position evaluation heuristics (planned)
│   ├── patterns/             # Historical game patterns (planned)
│   ├── puzzles/              # Tactical puzzle library (planned)
│   └── engine.py             # Main engine with minimax search
├── tests/
│   └── test_gotham_engine.py # Comprehensive test suite
├── main.py                   # Demo application
├── requirements.txt          # Python dependencies
└── setup.py                  # Package configuration
```

## 🎓 Educational Features

### Opening Book
The engine includes Gotham Chess's recommended openings with educational explanations:

#### For White:
1. **London System** - Levy's #1 recommendation for beginners
2. **Vienna Gambit** - Aggressive opening for tactical players
3. **Ruy Lopez** - Classical opening for positional understanding

#### For Black:
1. **Scandinavian Defense** - Levy's top recommendation for Black
2. **Caro-Kann Defense** - Solid and reliable defense
3. **Queen's Gambit Declined** - Classical central control

### Position Analysis
The engine provides comprehensive position analysis including:
- **Material balance** with piece activity bonuses
- **King safety** evaluation using pawn shield and piece proximity
- **Development scores** tracking piece mobilization
- **Center control** measuring influence over key squares
- **Tactical motif detection** (forks, pins, skewers, etc.)

## Components

### Opening Book
1. **London System**: A solid and flexible opening for White, focusing on piece development and control of the center.
2. **Vienna Gambit**: An aggressive opening for White that aims to control the center and create attacking chances early in the game.
3. **Alapin Variant**: A popular response to the Sicilian Defense, focusing on quick development and central control.
4. **Ruy Lopez**: A classical opening for White that emphasizes piece activity and long-term positional pressure on Black.
5. **Danish Gambit**: An aggressive gambit for White that sacrifices material for rapid development and attacking chances.
6. **Scandinavian Defense**: A solid and straightforward opening for Black that aims to challenge White's control of the center early in the game.
7. **Queens Gambit Declined**: A classical opening for Black that focuses on solid development and control of the center.
8. **Nimzo-Indian Defense**: A flexible and dynamic opening for Black that aims to control the center and create counterplay opportunities.
9. **Caro-Kann Defense**: A solid and resilient opening for Black that emphasizes strong pawn structure and piece development.
10. **Pirc Defense**: A hypermodern opening for Black that allows White to occupy the center initially, with plans to undermine and counterattack later.

### Heuristics
1. **Material Balance**: Evaluates the material on the board using standard piece values.
2. **King Safety**: Assesses the safety of the king based on pawn structure, castling, and piece proximity.
3. **Tactical Motifs**: Identifies common tactical patterns: forks, discovered attacks, pins, skewers, removing the guard, deflections, sacrifices, and en passant captures.
4. **Development**: Rewards piece activity and control of the center, penalizes early repetition of moves and early queen development.
5. **Mate Patterns**: Recognizes common Mate in 1 and Mate in 2 patterns instantly. Identifies checkmate patterns such as back rank mates, smothered mates, and basic mating nets.

### Historical Game Knowledge
1. **The Immortal Game (Anderssen vs. Kieseritzky, 1851)**: Recognizes the key sacrifices and attacking themes from this famous game.
2. **Motzart Game (Carlsen vs. Ernst, 2004)**: Understands the positional imbalances despite the material deficit.
3. **Kasparov's Immortal (Kasparov vs. Topalov, 1999)**: Appreciates the deep sacrifices and long-term planning involved in one of the most memorable attacks in chess history.
4. **Short vs. Timman (1991)**: Recognizes the importance of piece activity and king safety (and king activity) in this dynamic game.
5. **The Opera Game (Morphy vs. Duke of Brunswick and Count Isouard, 1858)**: Understands the rapid development and open lines that led to Morphy's victory.

### Puzzle Library
- Find the fork (x3)
  1. `r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1`
  2. `rnbqkb1r/pppp1ppp/5n2/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 4 4`
  3. `r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 4 4`

- Find the discovered attack (x3)
  1. `rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1`
  2. `rnbqkb1r/pppppppp/5n2/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 2 2`
  3. `r1bqkbnr/pppp1ppp/2n5/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 2 3`

- Find checkmate in 1 (x3)
  1. `rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3`
  2. `rnbqkb1r/pppp1ppp/5n2/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 4 4`
  3. `r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/3P4/PPP2PPP/RNBQK1NR b KQkq - 0 5`

- Find checkmate in 2 (x3)
  1. `r1bqkbnr/pppp1ppp/2n5/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 2 3`
  2. `rnbqkb1r/pppppppp/5n2/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 2 2`
  3. `r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 4 4`

- Find the pin (x3)
  1. `rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 3`
  2. `r1bqkbnr/pppp1ppp/2n5/4p3/4P3/3P4/PPP2PPP/RNBQKBNR b KQkq - 0 4`
  3. `rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 3`

- Find the skewer (x3)
  1. `r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 6 5`
  2. `rnbqkb1r/ppp2ppp/3p1n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R b KQkq - 4 5`
  3. `r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 4 4`

- Remove the guard (x3)
  1. `rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 3`
  2. `r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 4 4`
  3. `rnbqkb1r/pppppppp/5n2/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 2 2`

- Deflect the defense (x3)
  1. `rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 3`
  2. `r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 4 4`
  3. `rnbqkb1r/pppppppp/5n2/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 2 2`

- Play a sacrifice (x3)
  1. `r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 6 5`
  2. `rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 3`
  3. `r1bqkbnr/pppp1ppp/2n5/4p3/4P3/3P4/PPP2PPP/RNBQKBNR b KQkq - 0 4`

## 🔧 Usage Examples

### Basic Engine Usage

```python
from src.engine import GothamChessEngine

# Initialize the engine
engine = GothamChessEngine()

# Get the best move for the current position
best_move = engine.get_best_move()
print(f"Recommended move: {best_move}")

# Get educational explanation
explanation = engine.get_move_explanation(best_move)
print(f"Why this move: {explanation['educational_notes'][0]}")

# Analyze the position
analysis = engine.get_position_analysis()
print(f"Game phase: {analysis['game_phase']}")
print(f"Material balance: {analysis['material_balance']}")
```

### Opening Book Usage

```python
from src.openings.opening_book import GothamOpeningBook
from src.core.board import GothamBoard

book = GothamOpeningBook()
board = GothamBoard()

# Get opening move suggestion
opening_move = book.get_opening_move(board, chess.WHITE)

# Get opening explanation
opening_name = book.get_opening_name(board)
if opening_name:
    explanation = book.get_opening_explanation(opening_name)
    print(f"Opening principles: {explanation['principles']}")
```

## 🎯 Development Status

### ✅ Completed
- [x] Core chess board representation with educational features
- [x] Piece evaluation with positional bonuses
- [x] Opening book with Gotham Chess recommendations
- [x] Main engine with minimax search and alpha-beta pruning
- [x] Educational move explanations
- [x] Comprehensive position analysis
- [x] Basic tactical pattern recognition
- [x] Test suite with comprehensive coverage

### 🚧 In Progress / Planned
- [ ] Enhanced evaluation heuristics module
- [ ] Historical game pattern recognition system
- [ ] Comprehensive puzzle library
- [ ] UCI protocol interface
- [ ] Advanced tactical pattern recognition
- [ ] Endgame tablebase integration
- [ ] Performance optimizations
- [ ] GUI interface

## 🤝 Contributing

This project is built to embody the chess teachings and philosophy of GothamChess (Levy Rozman). Contributions should focus on:

1. **Educational value** - Features should help players learn and improve
2. **Principled play** - Following fundamental chess principles
3. **Clarity over complexity** - Code and explanations should be clear and accessible
4. **Testing** - All new features should include comprehensive tests

## 📚 Educational Philosophy

The Gotham Chess Engine is designed around these core educational principles:

1. **Principles over Memorization** - Teach underlying concepts rather than rote learning
2. **Practical Application** - Focus on positions and patterns that occur in real games
3. **Progressive Learning** - Start with fundamentals and gradually introduce complexity
4. **Immediate Feedback** - Provide explanations and reasoning for all suggestions
5. **Pattern Recognition** - Help players recognize common tactical and positional themes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **GothamChess (Levy Rozman)** for the chess knowledge and educational approach
- **python-chess library** for the solid chess programming foundation
- **Chess community** for continuous learning and improvement

---

*"The most important thing is to not be afraid to take a chance. You have to risk it to get the biscuit."* - Levy Rozman
