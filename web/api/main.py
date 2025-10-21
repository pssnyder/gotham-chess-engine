"""
FastAPI web server for the Gotham Chess Engine.

This module provides REST API endpoints for the chess engine,
enabling web-based interaction and real-time gameplay.
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import chess
import json
import uuid
import asyncio
from datetime import datetime

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.engine import GothamChessEngine
from src.core.board import GamePhase


# Pydantic models for API requests/responses
class GameCreateRequest(BaseModel):
    player_color: str = "white"  # "white", "black", or "random"
    time_control: Optional[str] = "10+0"  # Format: "minutes+increment"
    difficulty: str = "intermediate"  # "beginner", "intermediate", "advanced"


class MakeMoveRequest(BaseModel):
    game_id: str
    move: str  # Move in standard algebraic notation (SAN)


class GameStateResponse(BaseModel):
    game_id: str
    fen: str
    turn: str
    legal_moves: List[str]
    game_phase: str
    status: str  # "active", "checkmate", "stalemate", "draw"
    last_move: Optional[str]
    analysis: Optional[Dict[str, Any]]
    educational_notes: List[str]


class EngineAnalysisRequest(BaseModel):
    fen: str
    depth: Optional[int] = 4


class EngineAnalysisResponse(BaseModel):
    best_move: Optional[str]
    evaluation: float
    analysis: Dict[str, Any]
    move_explanation: Dict[str, Any]


# Game management
class GameManager:
    def __init__(self):
        self.games: Dict[str, Dict] = {}
        self.engines: Dict[str, GothamChessEngine] = {}
    
    def create_game(self, request: GameCreateRequest) -> str:
        game_id = str(uuid.uuid4())
        engine = GothamChessEngine()
        
        # Set difficulty
        if request.difficulty == "beginner":
            engine.search_depth = 2
            engine.time_limit = 0.5
        elif request.difficulty == "intermediate":
            engine.search_depth = 4
            engine.time_limit = 1.0
        elif request.difficulty == "advanced":
            engine.search_depth = 6
            engine.time_limit = 2.0
        
        # Determine colors
        if request.player_color == "random":
            import random
            player_color = "white" if random.choice([True, False]) else "black"
        else:
            player_color = request.player_color
        
        game_data = {
            "game_id": game_id,
            "player_color": player_color,
            "engine_color": "black" if player_color == "white" else "white",
            "time_control": request.time_control,
            "difficulty": request.difficulty,
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "moves": [],
            "last_move": None
        }
        
        self.games[game_id] = game_data
        self.engines[game_id] = engine
        
        return game_id
    
    def get_game_state(self, game_id: str) -> GameStateResponse:
        if game_id not in self.games:
            raise HTTPException(status_code=404, detail="Game not found")
        
        game = self.games[game_id]
        engine = self.engines[game_id]
        
        # Determine game status
        status = "active"
        if engine.board.is_checkmate():
            status = "checkmate"
        elif engine.board.is_stalemate():
            status = "stalemate"
        elif engine.board.is_insufficient_material() or engine.board.is_seventyfive_moves() or engine.board.is_fivefold_repetition():
            status = "draw"
        
        # Get analysis
        analysis = engine.get_position_analysis()
        
        return GameStateResponse(
            game_id=game_id,
            fen=engine.board.fen(),
            turn="white" if engine.board.turn else "black",
            legal_moves=[str(move) for move in engine.board.legal_moves],
            game_phase=engine.board.get_game_phase().value,
            status=status,
            last_move=game["last_move"],
            analysis=analysis,
            educational_notes=engine.board.get_educational_notes()
        )
    
    def make_move(self, game_id: str, move_san: str) -> GameStateResponse:
        if game_id not in self.games:
            raise HTTPException(status_code=404, detail="Game not found")
        
        game = self.games[game_id]
        engine = self.engines[game_id]
        
        try:
            # Parse and make the move
            move = engine.board.parse_san(move_san)
            if move not in engine.board.legal_moves:
                raise HTTPException(status_code=400, detail="Illegal move")
            
            engine.make_move(move)
            game["moves"].append(move_san)
            game["last_move"] = move_san
            
            return self.get_game_state(game_id)
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid move format: {str(e)}")
    
    def get_engine_move(self, game_id: str) -> Optional[str]:
        if game_id not in self.games:
            return None
        
        engine = self.engines[game_id]
        
        if engine.board.is_game_over():
            return None
        
        best_move = engine.get_best_move()
        if best_move:
            return engine.board.san(best_move)
        
        return None
    
    def make_engine_move(self, game_id: str) -> GameStateResponse:
        if game_id not in self.games:
            raise HTTPException(status_code=404, detail="Game not found")
        
        game = self.games[game_id]
        engine = self.engines[game_id]
        
        if engine.board.is_game_over():
            raise HTTPException(status_code=400, detail="Game is over")
        
        best_move = engine.get_best_move()
        if not best_move:
            raise HTTPException(status_code=500, detail="Engine could not find a move")
        
        move_san = engine.board.san(best_move)
        engine.make_move(best_move)
        game["moves"].append(move_san)
        game["last_move"] = move_san
        
        return self.get_game_state(game_id)


# Initialize FastAPI app
app = FastAPI(
    title="Gotham Chess Engine API",
    description="REST API for the Gotham Chess Engine with educational features",
    version="1.0.0"
)

# Enable CORS for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize game manager
game_manager = GameManager()

# WebSocket connection manager for real-time updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, game_id: str):
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        self.active_connections[game_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, game_id: str):
        if game_id in self.active_connections:
            self.active_connections[game_id].remove(websocket)
    
    async def send_game_update(self, game_id: str, data: dict):
        if game_id in self.active_connections:
            for connection in self.active_connections[game_id]:
                try:
                    await connection.send_text(json.dumps(data))
                except:
                    # Connection closed, remove it
                    self.active_connections[game_id].remove(connection)

manager = ConnectionManager()


# API Routes
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Gotham Chess Engine API! 🔥",
        "version": "1.0.0",
        "endpoints": {
            "create_game": "/api/games/create",
            "game_state": "/api/games/{game_id}",
            "make_move": "/api/games/{game_id}/move",
            "engine_move": "/api/games/{game_id}/engine-move",
            "analyze": "/api/analyze",
            "websocket": "/ws/{game_id}"
        }
    }


@app.post("/api/games/create", response_model=Dict[str, str])
async def create_game(request: GameCreateRequest):
    """Create a new game against the Gotham Chess Engine."""
    game_id = game_manager.create_game(request)
    return {"game_id": game_id, "status": "created"}


@app.get("/api/games/{game_id}", response_model=GameStateResponse)
async def get_game_state(game_id: str):
    """Get the current state of a game."""
    return game_manager.get_game_state(game_id)


@app.post("/api/games/{game_id}/move", response_model=GameStateResponse)
async def make_move(game_id: str, request: MakeMoveRequest):
    """Make a move in the game."""
    game_state = game_manager.make_move(game_id, request.move)
    
    # Send real-time update
    await manager.send_game_update(game_id, {
        "type": "move_made",
        "move": request.move,
        "game_state": game_state.dict()
    })
    
    return game_state


@app.post("/api/games/{game_id}/engine-move", response_model=GameStateResponse)
async def make_engine_move(game_id: str):
    """Make the engine's move."""
    game_state = game_manager.make_engine_move(game_id)
    
    # Send real-time update
    await manager.send_game_update(game_id, {
        "type": "engine_move",
        "move": game_state.last_move,
        "game_state": game_state.dict()
    })
    
    return game_state


@app.post("/api/analyze", response_model=EngineAnalysisResponse)
async def analyze_position(request: EngineAnalysisRequest):
    """Analyze a chess position."""
    engine = GothamChessEngine()
    engine.set_position(request.fen)
    engine.search_depth = request.depth or 4
    
    best_move = engine.get_best_move()
    evaluation = engine.evaluate_position(engine.board)
    analysis = engine.get_position_analysis()
    
    move_explanation = {}
    if best_move:
        move_explanation = engine.get_move_explanation(best_move)
        best_move_san = engine.board.san(best_move)
    else:
        best_move_san = None
    
    return EngineAnalysisResponse(
        best_move=best_move_san,
        evaluation=evaluation,
        analysis=analysis,
        move_explanation=move_explanation
    )


@app.get("/api/games/{game_id}/suggest-move")
async def suggest_move(game_id: str):
    """Get a move suggestion without making it."""
    engine_move = game_manager.get_engine_move(game_id)
    if not engine_move:
        raise HTTPException(status_code=400, detail="No move available")
    
    # Get explanation for the suggested move
    engine = game_manager.engines[game_id]
    move = engine.board.parse_san(engine_move)
    explanation = engine.get_move_explanation(move)
    
    return {
        "suggested_move": engine_move,
        "explanation": explanation
    }


@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    """WebSocket endpoint for real-time game updates."""
    await manager.connect(websocket, game_id)
    try:
        while True:
            # Keep connection alive and listen for client messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)


# Serve static files (for piece images, etc.)
app.mount("/static", StaticFiles(directory="images"), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)