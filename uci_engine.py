"""
Universal Chess Interface (UCI) implementation for Gotham Chess Engine.

This module provides the UCI protocol implementation allowing the engine
to be used with standard chess GUIs and testing tools.
"""

import sys
import threading
import time
import chess
from typing import Optional, Dict, Any
from src.engine import GothamChessEngine


class UCIEngine:
    """
    UCI protocol implementation for Gotham Chess Engine.
    
    Handles all UCI commands and provides the interface between
    the engine logic and UCI-compatible chess GUIs.
    """
    
    def __init__(self):
        """Initialize the UCI engine."""
        self.engine = GothamChessEngine()
        self.engine_name = "Gotham Chess Engine"
        self.engine_author = "Gotham Chess Educational Project"
        self.engine_version = "1.0"
        
        # UCI state
        self.debug_mode = False
        self.search_thread = None
        self.searching = False
        self.stop_search = False
        
        # Engine options
        self.options = {
            "Hash": {
                "type": "spin",
                "default": 64,
                "min": 1,
                "max": 1024,
                "value": 64
            },
            "Threads": {
                "type": "spin", 
                "default": 1,
                "min": 1,
                "max": 8,
                "value": 1
            },
            "Educational_Mode": {
                "type": "check",
                "default": True,
                "value": True
            },
            "Search_Depth": {
                "type": "spin",
                "default": 4,
                "min": 1,
                "max": 10,
                "value": 4
            },
            "Time_Limit": {
                "type": "spin",
                "default": 1000,
                "min": 100,
                "max": 10000,
                "value": 1000
            }
        }
    
    def run(self):
        """Main UCI loop."""
        self.send_output("Gotham Chess Engine UCI Ready")
        
        while True:
            try:
                line = input().strip()
                if not line:
                    continue
                
                if self.debug_mode:
                    self.send_debug(f"Received: {line}")
                
                parts = line.split()
                command = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []
                
                if command == "uci":
                    self.handle_uci()
                elif command == "isready":
                    self.handle_isready()
                elif command == "ucinewgame":
                    self.handle_ucinewgame()
                elif command == "position":
                    self.handle_position(args)
                elif command == "go":
                    self.handle_go(args)
                elif command == "stop":
                    self.handle_stop()
                elif command == "quit":
                    self.handle_quit()
                    break
                elif command == "setoption":
                    self.handle_setoption(args)
                elif command == "debug":
                    self.handle_debug(args)
                else:
                    if self.debug_mode:
                        self.send_debug(f"Unknown command: {command}")
            
            except EOFError:
                break
            except Exception as e:
                if self.debug_mode:
                    self.send_debug(f"Error: {e}")
    
    def handle_uci(self):
        """Handle the 'uci' command."""
        self.send_output(f"id name {self.engine_name}")
        self.send_output(f"id author {self.engine_author}")
        
        # Send options
        for option_name, option_data in self.options.items():
            option_line = f"option name {option_name} type {option_data['type']}"
            
            if option_data["type"] == "spin":
                option_line += f" default {option_data['default']}"
                option_line += f" min {option_data['min']}"
                option_line += f" max {option_data['max']}"
            elif option_data["type"] == "check":
                option_line += f" default {str(option_data['default']).lower()}"
            
            self.send_output(option_line)
        
        self.send_output("uciok")
    
    def handle_isready(self):
        """Handle the 'isready' command."""
        self.send_output("readyok")
    
    def handle_ucinewgame(self):
        """Handle the 'ucinewgame' command."""
        self.engine = GothamChessEngine()
        if self.debug_mode:
            self.send_debug("New game started")
    
    def handle_position(self, args):
        """Handle the 'position' command."""
        if not args:
            return
        
        if args[0] == "startpos":
            self.engine.set_position(None)  # Starting position
            move_index = 2 if len(args) > 1 and args[1] == "moves" else -1
        elif args[0] == "fen":
            # Find where moves start
            move_index = -1
            fen_parts = []
            for i, arg in enumerate(args[1:], 1):
                if arg == "moves":
                    move_index = i + 1
                    break
                fen_parts.append(arg)
            
            if fen_parts:
                fen = " ".join(fen_parts)
                try:
                    self.engine.set_position(fen)
                except ValueError as e:
                    if self.debug_mode:
                        self.send_debug(f"Invalid FEN: {fen}")
                    return
        else:
            return
        
        # Apply moves if any
        if move_index > 0 and move_index < len(args):
            for move_str in args[move_index:]:
                try:
                    # Try UCI format first
                    move = chess.Move.from_uci(move_str)
                    if move in self.engine.board.legal_moves:
                        self.engine.make_move(move)
                    else:
                        if self.debug_mode:
                            self.send_debug(f"Illegal move: {move_str}")
                        break
                except ValueError:
                    try:
                        # Try SAN format as fallback
                        move = self.engine.board.parse_san(move_str)
                        self.engine.make_move(move)
                    except ValueError:
                        if self.debug_mode:
                            self.send_debug(f"Invalid move: {move_str}")
                        break
    
    def handle_go(self, args):
        """Handle the 'go' command."""
        if self.searching:
            return
        
        # Parse go command arguments
        search_params = self.parse_go_args(args)
        
        # Start search in separate thread
        self.searching = True
        self.stop_search = False
        self.search_thread = threading.Thread(
            target=self.search_position, 
            args=(search_params,)
        )
        self.search_thread.start()
    
    def parse_go_args(self, args) -> Dict[str, Any]:
        """Parse arguments from 'go' command."""
        params = {
            "wtime": None,
            "btime": None,
            "winc": None,
            "binc": None,
            "movestogo": None,
            "depth": None,
            "movetime": None,
            "infinite": False
        }
        
        i = 0
        while i < len(args):
            arg = args[i]
            if arg in params and i + 1 < len(args):
                try:
                    params[arg] = int(args[i + 1])
                    i += 2
                except ValueError:
                    i += 1
            elif arg == "infinite":
                params["infinite"] = True
                i += 1
            else:
                i += 1
        
        return params
    
    def search_position(self, search_params):
        """Search the current position."""
        try:
            # Set search parameters
            if search_params["depth"]:
                self.engine.search_depth = min(search_params["depth"], 10)
            else:
                self.engine.search_depth = self.options["Search_Depth"]["value"]
            
            if search_params["movetime"]:
                self.engine.time_limit = search_params["movetime"] / 1000.0
            else:
                # Calculate time based on remaining time
                if self.engine.board.turn == chess.WHITE and search_params["wtime"]:
                    self.engine.time_limit = min(search_params["wtime"] / 30000.0, 5.0)
                elif self.engine.board.turn == chess.BLACK and search_params["btime"]:
                    self.engine.time_limit = min(search_params["btime"] / 30000.0, 5.0)
                else:
                    self.engine.time_limit = self.options["Time_Limit"]["value"] / 1000.0
            
            # Search for best move
            start_time = time.time()
            best_move = self.engine.get_best_move()
            search_time = time.time() - start_time
            
            if best_move and not self.stop_search:
                # Send search info
                position_eval = self.engine.evaluate_position(self.engine.board)
                nodes = 1000  # Placeholder - would need actual node count
                
                info_line = f"info depth {self.engine.search_depth}"
                info_line += f" score cp {int(position_eval * 100)}"
                info_line += f" time {int(search_time * 1000)}"
                info_line += f" nodes {nodes}"
                info_line += f" pv {str(best_move)}"
                
                self.send_output(info_line)
                
                # Send best move
                best_move_uci = str(best_move)
                self.send_output(f"bestmove {best_move_uci}")
                
                # Educational output if enabled
                if self.options["Educational_Mode"]["value"] and self.debug_mode:
                    explanation = self.engine.get_move_explanation(best_move)
                    if explanation.get('educational_notes'):
                        self.send_debug(f"Move explanation: {explanation['educational_notes'][0]}")
            
            elif not self.stop_search:
                # No legal moves (game over)
                self.send_output("bestmove (none)")
        
        except Exception as e:
            if self.debug_mode:
                self.send_debug(f"Search error: {e}")
            self.send_output("bestmove (none)")
        
        finally:
            self.searching = False
    
    def handle_stop(self):
        """Handle the 'stop' command."""
        if self.searching:
            self.stop_search = True
            if self.search_thread and self.search_thread.is_alive():
                self.search_thread.join(timeout=1.0)
            self.searching = False
    
    def handle_quit(self):
        """Handle the 'quit' command."""
        if self.searching:
            self.handle_stop()
        if self.debug_mode:
            self.send_debug("Engine shutting down")
    
    def handle_setoption(self, args):
        """Handle the 'setoption' command."""
        if len(args) >= 4 and args[0] == "name" and args[2] == "value":
            option_name = args[1]
            option_value = args[3]
            
            if option_name in self.options:
                try:
                    if self.options[option_name]["type"] == "spin":
                        value = int(option_value)
                        min_val = self.options[option_name]["min"]
                        max_val = self.options[option_name]["max"]
                        self.options[option_name]["value"] = max(min_val, min(max_val, value))
                    elif self.options[option_name]["type"] == "check":
                        self.options[option_name]["value"] = option_value.lower() == "true"
                    
                    if self.debug_mode:
                        self.send_debug(f"Set {option_name} to {self.options[option_name]['value']}")
                
                except ValueError:
                    if self.debug_mode:
                        self.send_debug(f"Invalid value for {option_name}: {option_value}")
    
    def handle_debug(self, args):
        """Handle the 'debug' command."""
        if args and args[0] == "on":
            self.debug_mode = True
            self.send_debug("Debug mode enabled")
        elif args and args[0] == "off":
            self.debug_mode = False
    
    def send_output(self, message):
        """Send output to UCI interface."""
        print(message)
        sys.stdout.flush()
    
    def send_debug(self, message):
        """Send debug information."""
        if self.debug_mode:
            print(f"info string {message}")
            sys.stdout.flush()


def main():
    """Main entry point for UCI engine."""
    engine = UCIEngine()
    engine.run()


if __name__ == "__main__":
    main()