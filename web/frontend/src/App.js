import React, { useState, useEffect, useCallback } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Card,
  CardContent,
  Chip,
  Alert,
  CircularProgress,
  Tabs,
  Tab
} from '@mui/material';
import { Chess } from 'chess.js';
import Chessboard from 'chessboard-jsx';
import './App.css';

// API configuration
const API_BASE = process.env.NODE_ENV === 'production' 
  ? 'https://your-firebase-function-url'  // Replace with your Firebase Functions URL
  : 'http://localhost:8000';

function App() {
  // Game state
  const [chess] = useState(new Chess());
  const [fen, setFen] = useState(chess.fen());
  const [gameId, setGameId] = useState(null);
  const [gameState, setGameState] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // UI state
  const [showNewGameDialog, setShowNewGameDialog] = useState(false);
  const [playerColor, setPlayerColor] = useState('white');
  const [difficulty, setDifficulty] = useState('intermediate');
  const [timeControl, setTimeControl] = useState('10+0');
  const [selectedSquare, setSelectedSquare] = useState(null);
  const [moveHistory, setMoveHistory] = useState([]);
  const [currentTab, setCurrentTab] = useState(0);
  
  // WebSocket connection for real-time updates
  const [ws, setWs] = useState(null);

  // Initialize WebSocket connection when game is created
  useEffect(() => {
    if (gameId && !ws) {
      const websocket = new WebSocket(`ws://localhost:8000/ws/${gameId}`);
      
      websocket.onopen = () => {
        console.log('WebSocket connected');
        setWs(websocket);
      };
      
      websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'move_made' || data.type === 'engine_move') {
          setGameState(data.game_state);
          setFen(data.game_state.fen);
          chess.load(data.game_state.fen);
          setMoveHistory(prev => [...prev, data.move]);
        }
      };
      
      websocket.onclose = () => {
        console.log('WebSocket disconnected');
        setWs(null);
      };
      
      return () => {
        websocket.close();
      };
    }
  }, [gameId, ws, chess]);

  // API call helper
  const apiCall = async (endpoint, options = {}) => {
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'API call failed');
      }
      
      return await response.json();
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  // Create new game
  const createNewGame = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await apiCall('/api/games/create', {
        method: 'POST',
        body: JSON.stringify({
          player_color: playerColor,
          time_control: timeControl,
          difficulty: difficulty
        })
      });
      
      setGameId(response.game_id);
      setShowNewGameDialog(false);
      
      // Reset board
      chess.reset();
      setFen(chess.fen());
      setMoveHistory([]);
      
      // Get initial game state
      await updateGameState(response.game_id);
      
    } catch (err) {
      console.error('Failed to create game:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Update game state from server
  const updateGameState = async (currentGameId = gameId) => {
    if (!currentGameId) return;
    
    try {
      const state = await apiCall(`/api/games/${currentGameId}`);
      setGameState(state);
      setFen(state.fen);
      chess.load(state.fen);
    } catch (err) {
      console.error('Failed to update game state:', err);
    }
  };

  // Make a move
  const makeMove = async (from, to, promotion = 'q') => {
    if (!gameId) return false;
    
    setIsLoading(true);
    
    try {
      // Validate move locally first
      const move = chess.move({
        from: from,
        to: to,
        promotion: promotion
      });
      
      if (!move) {
        setError('Illegal move');
        setIsLoading(false);
        return false;
      }
      
      // Send move to server
      await apiCall(`/api/games/${gameId}/move`, {
        method: 'POST',
        body: JSON.stringify({
          game_id: gameId,
          move: move.san
        })
      });
      
      // Update local state
      setFen(chess.fen());
      setMoveHistory(prev => [...prev, move.san]);
      setSelectedSquare(null);
      
      // If it's the engine's turn, request engine move
      if (gameState && gameState.turn !== (gameState.analysis?.player_color || 'white')) {
        setTimeout(() => makeEngineMove(), 1000); // Small delay for better UX
      }
      
      return true;
      
    } catch (err) {
      console.error('Failed to make move:', err);
      chess.undo(); // Undo the local move
      setFen(chess.fen());
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  // Request engine move
  const makeEngineMove = async () => {
    if (!gameId) return;
    
    setIsLoading(true);
    
    try {
      const response = await apiCall(`/api/games/${gameId}/engine-move`, {
        method: 'POST'
      });
      
      setGameState(response);
      setFen(response.fen);
      chess.load(response.fen);
      setMoveHistory(prev => [...prev, response.last_move]);
      
    } catch (err) {
      console.error('Failed to get engine move:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle square click
  const onSquareClick = (square) => {
    if (!gameId || isLoading) return;
    
    if (selectedSquare) {
      if (selectedSquare === square) {
        // Deselect
        setSelectedSquare(null);
      } else {
        // Try to make move
        makeMove(selectedSquare, square);
      }
    } else {
      // Select square if it has a piece of the current player
      const piece = chess.get(square);
      const isPlayerTurn = gameState && 
        ((gameState.turn === 'white' && gameState.analysis?.player_color === 'white') ||
         (gameState.turn === 'black' && gameState.analysis?.player_color === 'black'));
      
      if (piece && piece.color === chess.turn() && isPlayerTurn) {
        setSelectedSquare(square);
      }
    }
  };

  // Get move suggestions
  const getMoveHint = async () => {
    if (!gameId) return;
    
    try {
      const response = await apiCall(`/api/games/${gameId}/suggest-move`);
      alert(`Suggested move: ${response.suggested_move}\n\nExplanation: ${response.explanation.educational_notes?.[0] || 'Good move!'}`);
    } catch (err) {
      console.error('Failed to get move hint:', err);
    }
  };

  // Render analysis panel
  const renderAnalysis = () => {
    if (!gameState?.analysis) return null;
    
    const analysis = gameState.analysis;
    
    return (
      <Card sx={{ mt: 2 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            📊 Position Analysis
          </Typography>
          
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Game Phase: <Chip label={analysis.game_phase} size="small" />
            </Typography>
          </Box>
          
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Typography variant="body2">
                Material Balance
              </Typography>
              <Typography variant="caption">
                White: {analysis.material_balance?.white || 0}
                <br />
                Black: {analysis.material_balance?.black || 0}
              </Typography>
            </Grid>
            
            <Grid item xs={6}>
              <Typography variant="body2">
                King Safety
              </Typography>
              <Typography variant="caption">
                White: {analysis.king_safety?.white ? '✅' : '⚠️'}
                <br />
                Black: {analysis.king_safety?.black ? '✅' : '⚠️'}
              </Typography>
            </Grid>
          </Grid>
          
          {analysis.opening && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2">
                Opening: <Chip label={analysis.opening} size="small" color="primary" />
              </Typography>
            </Box>
          )}
          
          {gameState.educational_notes && gameState.educational_notes.length > 0 && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" gutterBottom>
                🎓 Educational Notes:
              </Typography>
              {gameState.educational_notes.map((note, index) => (
                <Alert key={index} severity="info" sx={{ mt: 1 }}>
                  {note}
                </Alert>
              ))}
            </Box>
          )}
        </CardContent>
      </Card>
    );
  };

  // Render move history
  const renderMoveHistory = () => {
    return (
      <Card sx={{ mt: 2 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            📝 Move History
          </Typography>
          <Box sx={{ maxHeight: 200, overflow: 'auto' }}>
            {moveHistory.map((move, index) => (
              <Chip
                key={index}
                label={`${Math.floor(index / 2) + 1}${index % 2 === 0 ? '.' : '...'} ${move}`}
                size="small"
                sx={{ m: 0.5 }}
              />
            ))}
          </Box>
        </CardContent>
      </Card>
    );
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <Typography variant="h3" component="h1" gutterBottom align="center">
        🔥 Gotham Chess Engine
      </Typography>
      <Typography variant="subtitle1" align="center" color="text.secondary" gutterBottom>
        Learn chess with GothamChess (Levy Rozman) principles
      </Typography>

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Main Game Interface */}
      <Grid container spacing={3}>
        {/* Chess Board */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            {/* Game Controls */}
            <Box sx={{ mb: 2, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Button
                variant="contained"
                color="primary"
                onClick={() => setShowNewGameDialog(true)}
                disabled={isLoading}
              >
                New Game
              </Button>
              
              {gameId && (
                <>
                  <Button
                    variant="outlined"
                    onClick={getMoveHint}
                    disabled={isLoading}
                  >
                    💡 Hint
                  </Button>
                  
                  <Button
                    variant="outlined"
                    onClick={() => updateGameState()}
                    disabled={isLoading}
                  >
                    🔄 Refresh
                  </Button>
                </>
              )}
              
              {isLoading && <CircularProgress size={24} />}
            </Box>

            {/* Game Status */}
            {gameState && (
              <Box sx={{ mb: 2 }}>
                <Typography variant="body1">
                  Turn: <Chip label={gameState.turn} size="small" color={gameState.turn === 'white' ? 'default' : 'secondary'} />
                  {gameState.status !== 'active' && (
                    <Chip label={gameState.status} size="small" color="error" sx={{ ml: 1 }} />
                  )}
                </Typography>
              </Box>
            )}

            {/* Chess Board */}
            <Box sx={{ 
              display: 'flex', 
              justifyContent: 'center',
              '& .chessboard': {
                border: '2px solid #333'
              }
            }}>
              <Chessboard
                position={fen}
                onSquareClick={onSquareClick}
                boardStyle={{
                  borderRadius: '5px',
                  boxShadow: '0 5px 15px rgba(0, 0, 0, 0.5)'
                }}
                squareStyles={{
                  [selectedSquare]: { backgroundColor: 'rgba(255, 255, 0, 0.4)' }
                }}
                orientation={playerColor}
                width={400}
              />
            </Box>
          </Paper>
        </Grid>

        {/* Side Panel */}
        <Grid item xs={12} md={4}>
          {/* Tabs for different panels */}
          <Paper sx={{ p: 2 }}>
            <Tabs value={currentTab} onChange={(e, newValue) => setCurrentTab(newValue)}>
              <Tab label="Analysis" />
              <Tab label="History" />
            </Tabs>
            
            {currentTab === 0 && renderAnalysis()}
            {currentTab === 1 && renderMoveHistory()}
          </Paper>
        </Grid>
      </Grid>

      {/* New Game Dialog */}
      <Dialog open={showNewGameDialog} onClose={() => setShowNewGameDialog(false)}>
        <DialogTitle>🔥 New Game vs Gotham Chess Engine</DialogTitle>
        <DialogContent>
          <Grid container spacing={3} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Your Color</InputLabel>
                <Select
                  value={playerColor}
                  label="Your Color"
                  onChange={(e) => setPlayerColor(e.target.value)}
                >
                  <MenuItem value="white">White</MenuItem>
                  <MenuItem value="black">Black</MenuItem>
                  <MenuItem value="random">Random</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Difficulty</InputLabel>
                <Select
                  value={difficulty}
                  label="Difficulty"
                  onChange={(e) => setDifficulty(e.target.value)}
                >
                  <MenuItem value="beginner">Beginner (Depth 2)</MenuItem>
                  <MenuItem value="intermediate">Intermediate (Depth 4)</MenuItem>
                  <MenuItem value="advanced">Advanced (Depth 6)</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Time Control</InputLabel>
                <Select
                  value={timeControl}
                  label="Time Control"
                  onChange={(e) => setTimeControl(e.target.value)}
                >
                  <MenuItem value="1+0">1 minute</MenuItem>
                  <MenuItem value="3+0">3 minutes</MenuItem>
                  <MenuItem value="5+0">5 minutes</MenuItem>
                  <MenuItem value="10+0">10 minutes</MenuItem>
                  <MenuItem value="15+10">15+10</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowNewGameDialog(false)}>Cancel</Button>
          <Button onClick={createNewGame} variant="contained" disabled={isLoading}>
            {isLoading ? <CircularProgress size={20} /> : 'Start Game'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default App;