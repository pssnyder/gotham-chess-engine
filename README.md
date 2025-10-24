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
  1. fen: '5rk1/5ppp/4p3/4N3/8/1Pn5/5PPP/5RK1 w - - 0 28', moves: f1c1 c3e2 g1f1 e2c1, rating: 655, themes: crushing endgame fork short, link: https://lichess.org/2K7g2pDT#55
  2. fen: 'r3brk1/5pp1/p1nqpn1p/P2pN3/2pP4/2P1PN2/5PPP/RB1QK2R b KQ - 4 16', moves: c6e5 d4e5 d6e7 e5f6, rating: 1237, themes: advantage fork middlegame short, link: https://lichess.org/fDwvVUIp/black#32
  3. fen: '6k1/3bqr1p/2rpp1pR/p7/Pp1QP3/1B3P2/1PP3P1/2KR4 w - - 6 22', moves: d4a7 e7g5 c1b1 g5h6, rating: 993, themes: advantage fork master middlegame short, link: https://lichess.org/8RvK0idj#43

- Find the discovered attack (x3)
  1. fen: 'r5k1/1p1rqpp1/p3pnp1/2PN4/8/1Q5P/PP3PP1/3RR1K1 b - - 0 24', moves: e7c5 d5f6 g7f6 d1d7, rating: 1062, themes: advantage discoveredAttack kingsideAttack master middlegame short, link: https://lichess.org/jAILX5BH/black#48
  2. fen: '3r4/p1p2ppp/4k3/6Q1/5P2/4P3/Prqn2PP/3R1RK1 w - - 3 22', moves: g5d8 d2f3 g1h1 c2g2, rating: 1629, themes: discoveredAttack endgame mate mateIn2 short, link: https://lichess.org/SctCD3fJ#43
  3. fen: '5rk1/5ppp/1p6/1qp2P1Q/3p3P/6R1/6PK/8 b - - 0 30', moves: c5c4 g3g7 g8g7 f5f6 g7f6 h5b5, rating: 1746, themes: attraction crushing discoveredAttack endgame long sacrifice, link: https://lichess.org/2UeWcE4h/black#60

- Find checkmate in 1 (x3)
  1. fen: '8/6pp/4N1k1/5p2/5P2/5rPb/4R2P/6K1 w - - 0 35', moves: e6g5 f3f1, rating: 411, themes: endgame mate mateIn1 oneMove, link: https://lichess.org/jzHHsjDp#69
  2. fen: 'Q5k1/p1p3p1/5rP1/8/3P4/7P/q3r3/B4RK1 b - - 1 34', moves: f6f8 a8f8, rating: 471, themes: endgame mate mateIn1 oneMove, link: https://lichess.org/1k4lXfEi/black#68
  3. fen: '8/6kp/4b1q1/1p6/1PpPp2Q/2P1P3/r2N2P1/5RK1 w - - 7 34', moves: d2e4 g6g2, rating: 1126, themes: endgame master mate mateIn1 oneMove, link: https://lichess.org/ynNNLRgG#67

- Find checkmate in 2 (x3)
  1. fen: '3r2k1/1q3ppp/p2rp3/Qp1B4/7P/P4P2/1PP3P1/1K1R3R b - - 0 21', moves: d6d5 a5d8 d5d8 d1d8, rating: 1376, themes: backRankMate endgame mate mateIn2 short xRayAttack, link: https://lichess.org/6qWf8wOP/black#42
  2. fen: '8/2pR2kp/pb4p1/8/5p1P/B6K/P1r5/6r1 b - - 3 39', moves: g7h6 a3f8 h6h5 d7h7, rating: 1822, themes: deflection endgame mate mateIn2 short, link: https://lichess.org/8sbUxgqT/black#78
  3. fen: 'r5k1/pp3ppp/2p5/4pb2/2B2q2/P1P1nP2/1P1Q3P/3R1R1K b - - 1 22', moves: e3c4 d2d8 a8d8 d1d8, rating: 1574, themes: backRankMate master mate mateIn2 middlegame sacrifice short, link: https://lichess.org/I0tBjrDC/black#44

- Find the pin (x3)
  1. fen: '2rr2k1/5p2/4p2p/4N1pQ/1p3P2/4P3/np3P1P/2q2BRK b - - 1 32', moves: c8c7 h5h6 b2b1q h6g5, rating: 2465, themes: crushing kingsideAttack master middlegame pin short, link: https://lichess.org/Ri0duT8T/black#64
  2. fen: '2r3k1/2r1q1p1/p3p1Q1/1p1p4/nP1P4/2P4R/P4PPP/2R3K1 b - - 0 30', moves: e7f6 g6h7 g8f7 h3f3 f6f3 g2f3, rating: 1422, themes: advantage long middlegame pin, link: https://lichess.org/nsAQV9mj/black#60
  3. fen: '4r1k1/ppqb3p/6B1/3pb2Q/8/2P5/PP1B2PP/5RK1 b - - 0 20', moves: h7g6 h5g6 e5g7 f1f7 c7c5 g1h1 c5f8 f7f8, rating: 2008, themes: crushing middlegame pin veryLong, link: https://lichess.org/e986oDw6/black#40

- Find the skewer (x3)
  1. fen: 'r7/7R/P3k3/4p2p/3b2p1/3K4/8/5R2 b - - 7 55', moves: a8a6 h7h6 e6d5 h6a6, rating: 969, themes: crushing endgame short skewer, link: https://lichess.org/N9FWAV9a/black#110
  2. fen: '7k/Q1p3p1/5p1p/3q4/3Pr3/4P3/P4P1P/1R4K1 w - - 2 26', moves: a7c5 e4g4 g1f1 d5h1 f1e2 h1b1, rating: 1712, themes: crushing endgame long skewer, link: https://lichess.org/awh9vUFg#51
  3. fen: '8/8/2k3P1/R7/P2p2rp/3K4/8/8 b - - 0 45', moves: g4g6 a5a6 c6d7 a6g6, rating: 1224, themes: crushing endgame master rookEndgame short skewer, link: https://lichess.org/vMSyus5U/black#90

- Remove the guard (Interference/Attraction) (x3)
  1. fen: 'GUvYW,3r3r/1p2pkb1/p1q4p/2p2Qp1/2N2nP1/2P1N3/PP3P2/2KR3R b - - 9 31', moves: c6f6 c4e5 f7g8 d1d8, rating: 1586, themes: crushing interference middlegame short, link: https://lichess.org/ztfNEvxj/black#62
  2. fen: 'r1b1k3/ppp2p1p/8/3pb3/5qn1/5B2/PPP2PPP/RN1QR1K1 w q - 4 14', moves: f3g4 f4h2 g1f1 h2h1 f1e2 c8g4 e2d3 g4f5 d3d2 h1h6, rating: 2155, themes: crushing interference kingsideAttack middlegame veryLong, link: https://lichess.org/JAF55Fc9#27,Scotch_Game Scotch_Game_Classical_Variation
  3. fen: '2R5/8/8/4B1pP/5KP1/r7/p2k4/8 w - - 0 54', moves: f4e4 a3e3 e4f5 e3e5 f5e5 a2a1q, rating: 1486, themes: advancedPawn attraction crushing endgame long promotion, link: https://lichess.org/0Te97k1C#107

- Deflect the defense (x3)
  1. fen: '8/5ppk/1Q6/2pq3P/p7/3P2B1/2r2P1K/7R w - - 0 34', moves: b6d6 c2f2 g3f2 d5d6, rating: 1912, themes: advantage deflection endgame short, link: https://lichess.org/hM8N0iaZ#67
  2. fen: '3q4/1pp3pk/1b2p2p/4Pp2/PpQ5/1P3NP1/5PBP/6K1 w - - 0 25', moves: c4e6 d8d1 g2f1 d1f3 e6b6 c7b6, rating: 1176, themes: crushing deflection endgame long, link: https://lichess.org/dwz5An0G#49
  3. fen: 'Qn4k1/5p2/p2rp1p1/q3b1Np/6PP/2P5/1P1K4/3R3R w - - 0 27', moves: d2c2 a5a4 c2b1 d6d1 h1d1 a4d1, rating: 1189, themes: crushing deflection long middlegame, link: https://lichess.org/nrKVSPjP#53

- Play a sacrifice (x3)
  1. fen: 'r2q1rk1/p1p1nppp/2p3b1/4P3/Q1P2PP1/4P2P/PP6/RN2KB1R w KQ - 0 14', moves: f4f5 e7f5 g4f5 d8h4, rating: 1763, themes: clearance crushing middlegame sacrifice short, link: https://lichess.org/kVnHF6Eh#27,Queens_Gambit_Declined Queens_Gambit_Declined_Albin_Countergambit
  2. fen: 'r7/7R/2r1k3/3N4/p1P1K3/4P1P1/7P/8 w - - 2 33', moves: d5c7 c6c7 h7c7 a4a3, rating: 1352, themes: advantage endgame sacrifice short, link: https://lichess.org/8iPz7kFB#65
  3. fen: '1q5r/1p1n1kp1/2p3p1/3p4/3PBn2/PQ3P1P/1P4P1/R1R3K1 w - - 1 26', moves: e4d3 f4h3 g2h3 b8g3 g1f1 h8h3, rating: 2489, themes: advantage clearance intermezzo kingsideAttack long middlegame sacrifice, link: https://lichess.org/UZMmtXz8#51

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
