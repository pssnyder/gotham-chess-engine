# Gotham Chess Engine
Gotham Chess Engine is a chess engine built from the cumulative chess knowledge of the chess Youtuber GothamChess (Levy Rozman). The engine is designed to provide strong chess play and analysis, leveraging modern algorithms and techniques. It aims be approachable to beginners by applying the same principles Levy teaches in his recently release hbook "How To Win At Chess" and his Chess Deck product.

## Features
- Principled chess play
- Approachable opening book for black and white
- Basic tactical heuristics
- Key positional understanding of critical games throughout history
- Endgame mate pattern recognition
- Game continuation awareness (draw, stalemate, repetition)
- Time management strategies
- 100% solve rate for all Chess Deck puzzles

---

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
- Find the discovered attack (x3)
- Find checkmate in 1 (x3)
- Find checkmate in 2 (x3)
- Find the pin (x3)
- Find the skewer (x3)
- Remove the guard (x3)
- Deflect the defense (x3)
- Play a sacrifice (x3)
