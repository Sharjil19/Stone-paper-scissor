from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- Import this
from pydantic import BaseModel
import random

app = FastAPI(
    title="Rock Paper Scissors API",
    description="A simple backend API to play Rock, Paper, Scissors against the computer.",
    version="1.0.0"
)

# <-- Add CORS middleware here -->
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (good for local testing)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)

class GameRequest(BaseModel):
    choice: str

CHOICES = ["rock", "paper", "scissors"]

# (Keep the rest of your / and /play routes exactly the same)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Rock, Paper, Scissors API!",
        "instructions": "Send a POST request to /play with a JSON body: {\"choice\": \"rock\"}"
    }

@app.post("/play")
def play_game(request: GameRequest):
    player_choice = request.choice.lower().strip()
    
    # Validate player choice
    if player_choice not in CHOICES:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid choice '{request.choice}'. Choose from: {CHOICES}"
        )
        
    computer_choice = random.choice(CHOICES)
    
    # Determine winner
    if player_choice == computer_choice:
        winner = "tie"
    elif (
        (player_choice == "rock" and computer_choice == "scissors") or
        (player_choice == "paper" and computer_choice == "rock") or
        (player_choice == "scissors" and computer_choice == "paper")
    ):
        winner = "player"
    else:
        winner = "computer"
        
    return {
        "player_choice": player_choice,
        "computer_choice": computer_choice,
        "winner": winner
    }