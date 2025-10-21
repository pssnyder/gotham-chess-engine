#!/usr/bin/env python3
"""
Simple UCI Test Script for Gotham Chess Engine.

This script provides a minimal UCI interface that should work reliably
with Arena Chess GUI and other UCI-compatible interfaces.
"""

import sys
import chess
from src.engine import GothamChessEngine


class SimpleUCIEngine:
    """Simplified UCI engine for maximum Arena compatibility."""
    
    def __init__(self):
        """Initialize the simple UCI engine."""
        self.engine = GothamChessEngine()
        self.debug_mode = False
        
    def run(self):
        """Main UCI loop with simplified commands."""
        while True:
            try:
                line = input().strip()
                if not line:
                    continue
                
                parts = line.split()
                command = parts[0].lower()
                
                if command == "uci":
                    self.handle_uci()
                elif command == "isready":
                    print("readyok")
                    sys.stdout.flush()
                elif command == "ucinewgame":
                    self.engine = GothamChessEngine()
                elif command == "position":
                    self.handle_position(parts[1:])
                elif command == "go":
                    self.handle_go()
                elif command == "quit":
                    break
                elif command == "debug":
                    if len(parts) > 1 and parts[1] == "on":
                        self.debug_mode = True
                    else:
                        self.debug_mode = False
            
            except EOFError:
                break
            except Exception as e:
                if self.debug_mode:
                    print(f"info string Error: {e}")
                    sys.stdout.flush()
    
    def handle_uci(self):
        """Handle UCI identification."""
        print("id name Gotham Chess Engine v1.0")
        print("id author Gotham Chess Educational Project")
        print("option name Threads type spin default 1 min 1 max 1")
        print("option name Hash type spin default 64 min 1 max 1024")
        print("uciok")
        sys.stdout.flush()
    
    def handle_position(self, args):
        """Handle position setup."""
        if not args:
            return
        
        try:
            if args[0] == "startpos":
                self.engine.set_position(None)
                move_index = 2 if len(args) > 1 and args[1] == "moves" else -1
            elif args[0] == "fen":
                # Build FEN string
                fen_parts = []
                move_index = -1
                for i, arg in enumerate(args[1:], 1):
                    if arg == "moves":
                        move_index = i + 1
                        break
                    fen_parts.append(arg)
                
                if fen_parts:
                    fen = " ".join(fen_parts)
                    self.engine.set_position(fen)
            
            # Apply moves
            if move_index > 0 and move_index < len(args):
                for move_str in args[move_index:]:
                    try:
                        move = chess.Move.from_uci(move_str)
                        if move in self.engine.board.legal_moves:
                            self.engine.make_move(move)
                    except:
                        break
        
        except Exception as e:
            if self.debug_mode:
                print(f"info string Position error: {e}")
                sys.stdout.flush()
    
    def handle_go(self):
        """Handle go command with simple search."""
        try:
            best_move = self.engine.get_best_move()
            if best_move:
                print(f"bestmove {best_move}")
            else:
                print("bestmove (none)")
            sys.stdout.flush()
        
        except Exception as e:
            if self.debug_mode:
                print(f"info string Search error: {e}")
            print("bestmove (none)")
            sys.stdout.flush()


if __name__ == "__main__":
    engine = SimpleUCIEngine()
    engine.run()