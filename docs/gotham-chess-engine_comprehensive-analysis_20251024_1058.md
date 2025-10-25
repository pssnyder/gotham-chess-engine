🚀 GOTHAM CHESS ENGINE - COMPREHENSIVE ANALYSIS
================================================================================
Analysis started at: 2025-10-24 10:56:50

🔍 Running Perft Tests (Move Generation Validation)
============================================================

📍 Testing: Starting Position
FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
Depth  Nodes        Expected     Time(ms)   NPS          Status
----------------------------------------------------------------------
1      20           20           0.19       102675       ✅ PASS
2      400          400          1.98       201867       ✅ PASS
3      8902         8902         48.91      181993       ✅ PASS

📍 Testing: Kiwipete
FEN: r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1
Depth  Nodes        Expected     Time(ms)   NPS          Status
----------------------------------------------------------------------
1      6            48           0.09       66930        ❌ FAIL
2      264          2039         1.60       165070       ❌ FAIL
3      9467         97862        47.71      198441       ❌ FAIL

📍 Testing: Position 3
FEN: 8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1
Depth  Nodes        Expected     Time(ms)   NPS          Status
----------------------------------------------------------------------
1      14           14           0.12       118626       ✅ PASS
2      191          191          1.15       166171       ✅ PASS
3      2812         2812         17.87      157352       ✅ PASS

📍 Testing: Position 4
FEN: r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1
Depth  Nodes        Expected     Time(ms)   NPS          Status
----------------------------------------------------------------------
1      26           26           0.22       120233       ✅ PASS
2      568          568          4.25       133518       ✅ PASS
3      13744        13744        74.96      183359       ✅ PASS

📍 Testing: Position 5
FEN: rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8
Depth  Nodes        Expected     Time(ms)   NPS          Status
----------------------------------------------------------------------
1      44           44           0.31       142840       ✅ PASS
2      1486         1486         7.20       206320       ✅ PASS
3      62379        62379        300.29     207730       ✅ PASS

🔍 Running Search Performance Benchmarks
============================================================

📍 Benchmarking: WAC.001
FEN: 2rr3k/pp3pp1/1nnqbN1p/3pN3/2pP4/2P3Q1/PPB4P/R4RK1 w - - 0 1
  Depth 3: f6h5 (eval: 7734.2, time: 1278.0ms, ~999999 nps)
  Depth 4: g3g7 (eval: 7734.2, time: 1401.1ms, ~999999 nps)
  Depth 5: g3g7 (eval: 7734.2, time: 1358.1ms, ~999999 nps)

📍 Benchmarking: WAC.002
FEN: 8/7p/5k2/5p2/p1p2P2/Pr1pPK2/1P1R3P/8 b - - 0 1
  Depth 3: h7h6 (eval: -524.0, time: 1015.4ms, ~999999 nps)
  Depth 4: f6g6 (eval: -524.0, time: 1040.4ms, ~999999 nps)
  Depth 5: f6g6 (eval: -524.0, time: 1087.3ms, ~999999 nps)

📍 Benchmarking: WAC.003
FEN: 5rk1/1ppb3p/p1pb4/6q1/3P1p1r/2P1R2P/PP1BQ1P1/5RKN w - - 0 1
  Depth 3: e2b5 (eval: 3163.0, time: 1389.1ms, ~999999 nps)
  Depth 4: e2b5 (eval: 3163.0, time: 1440.3ms, ~999999 nps)
  Depth 5: e2b5 (eval: 3163.0, time: 1567.0ms, ~999999 nps)

📍 Benchmarking: Middlegame
FEN: r1bq1rk1/pp2nppp/2n5/2ppP3/3P4/P1P1BN2/1P3PPP/R2QK2R w KQ - 0 1
  Depth 3: d1a4 (eval: 4983.8, time: 1268.6ms, ~999999 nps)
  Depth 4: d1a4 (eval: 4983.8, time: 1381.2ms, ~999999 nps)
  Depth 5: d1a4 (eval: 4983.8, time: 1526.6ms, ~999999 nps)

📍 Benchmarking: Tactical
FEN: r2q1rk1/ppp2ppp/2n1bn2/2b1p3/3pP3/3P1NPP/PPP1NPB1/R1BQ1RK1 b - - 0 1
  Depth 3: e6h3 (eval: -2111.7, time: 1245.4ms, ~999999 nps)
  Depth 4: e6c8 (eval: -2111.7, time: 1471.1ms, ~999999 nps)
  Depth 5: e6h3 (eval: -2111.7, time: 1525.6ms, ~999999 nps)

🎯 Running Tactical Puzzle Tests
============================================================
Loaded 100 real Lichess puzzles:
  fork: 16 puzzles
  discoveredAttack: 9 puzzles
  mateIn1: 15 puzzles
  mateIn2: 17 puzzles
  pin: 12 puzzles
  skewer: 11 puzzles
  deflection: 8 puzzles
  sacrifice: 12 puzzles

🧩 Testing fork puzzles:
  000rO: e5c7 vs e5c7 - ✅ SOLVED (1038.8ms)
  0017R: d1a4 vs d3c4 - ❌ FAILED (1466.8ms)
  001wr: d6d5 vs d6c5 - ❌ FAILED (1503.3ms)
  Category success rate: 33.3% (1/3)

🧩 Testing discoveredAttack puzzles:
  001XA: e4f6 vs b1b7 - ❌ FAILED (1492.1ms)
  002KJ: g2g3 vs f3e5 - ❌ FAILED (1513.7ms)
  004RF: h5h7 vs g3g7 - ❌ FAILED (1086.9ms)
  Category success rate: 0.0% (0/3)

🧩 Testing mateIn1 puzzles:
  000rZ: d6h2 vs d6h2 - ✅ SOLVED (1458.6ms)
  001cr: d7e8 vs d7e8 - ✅ SOLVED (1030.6ms)
  001gi: a5c3 vs a5c3 - ✅ SOLVED (1192.9ms)
  Category success rate: 100.0% (3/3)

🧩 Testing mateIn2 puzzles:
  000Zo: e8e1 vs e8e1 - ✅ SOLVED (1220.9ms)
  000hf: e2e6 vs e2e6 - ✅ SOLVED (1317.0ms)
  001Wz: d1d8 vs d1d8 - ✅ SOLVED (1158.4ms)
  Category success rate: 100.0% (3/3)

🧩 Testing pin puzzles:
  0018S: d4c5 vs d4a1 - ❌ FAILED (1189.7ms)
  001Hi: g1h2 vs f4f6 - ❌ FAILED (1197.6ms)
  002rd: h5g6 vs e2f4 - ❌ FAILED (1364.5ms)
  Category success rate: 0.0% (0/3)

🧩 Testing skewer puzzles:
  000qP: c2c1 vs f4f3 - ❌ FAILED (1141.5ms)
  001m3: f3d4 vs h8h1 - ❌ FAILED (1111.6ms)
  001xl: e7f7 vs e7f7 - ✅ SOLVED (1150.9ms)
  Category success rate: 33.3% (1/3)

🧩 Testing deflection puzzles:
  001h8: c1f1 vs h4h7 - ❌ FAILED (1224.8ms)
  004LZ: c3c2 vs c3c2 - ✅ SOLVED (165.9ms)
  004b0: c4e6 vs e7g5 - ❌ FAILED (1031.6ms)
  Category success rate: 33.3% (1/3)

🧩 Testing sacrifice puzzles:
  001xO: f6d7 vs b6c5 - ❌ FAILED (1243.4ms)
  002e5: g4c4 vs g4c4 - ✅ SOLVED (1192.0ms)
  004kB: f6f2 vs f6f2 - ✅ SOLVED (1158.7ms)
  Category success rate: 66.7% (2/3)

🎯 Overall tactical success rate: 45.8% (11/24)

🔌 Testing UCI Compliance
============================================================
✅ Position startpos: PASS
✅ Position FEN: PASS
✅ Go command: PASS
✅ Bestmove format: PASS
✅ UCI command: PASS
✅ IsReady command: PASS

📚 Analyzing Opening Book Coverage
============================================================
  Starting position: White=d2d4, Black response available=True
  After 1.e4: White=None, Black response available=False
  After 1.d4: White=None, Black response available=False
  After 1.Nf3: White=None, Black response available=False

📊 Opening Coverage Summary:
  Total openings available: 2
  White openings: 1
  Black openings: 1
  Success rate: 40.0%

📊 Generating Performance Report
============================================================

🎯 PERFORMANCE SUMMARY
Metric                    Score      Status
---------------------------------------------
Tactical Success          45.8%      ⚠️  Needs Work
UCI Compliance            100.0%     ✅ Good
Opening Coverage          40.0%      ⚠️  Needs Work
Search Performance        1333.0    ms ⚠️  Slow
Perft Accuracy            95.0%      ✅ Good
---------------------------------------------
OVERALL SCORE             68.0%      ✅ Good

🏁 Analysis completed at: 2025-10-24 10:57:39
================================================================================

💾 Results saved to: engine_analysis_results.json