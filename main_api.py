from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Models for incoming data

# model for emotion definitions
class EmotionDef(BaseModel):
    name: str
    description: str
    
# main start request model
class StartRequest(BaseModel):
    initial_emotion: str = "NEUTRAL"
    available_emotions: List[EmotionDef] = []

# End options
class EndRequest(BaseModel):
    reason: str

# start_edi.py will set this to connect the API to the shared data
shared_state = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "EDI API is Active"}

# Start Options
@app.post("/session/start")
def start_session(request: StartRequest):
    if shared_state is not None:
        shared_state["session_active"] = True
        shared_state["trigger_first_speech"] = True
        
        # save list of emotions that the frontend sends
        shared_state["initial_emotion"] = request.initial_emotion
        shared_state["available_emotions"] = [{"name": e.name, "description": e.description} for e in request.available_emotions]
        
        print(f"API: Session started. Received {len(request.available_emotions)} emotions from frontend.")
        
        return {
            "status": "starting",
            "description": "Emotions loaded successfully. EDI is booting up."
        }
            
    return {"error": "Shared state not initialized"}
    
    
# End Options
@app.post("/session/end")
def end_session(request: EndRequest):
    if shared_state is not None:
        shared_state["session_active"] = False
        shared_state["end_reason"] = request.reason
        
        # tell start_edi.py to wipe the memory clean
        shared_state["reset_memory"] = True
        
        print(f"API: Session ended. Reason: {request.reason}")
        return {"message": f"EDI session closed successfully. Reason: {request.reason}"}
        
    return {"status": "error", "message": "Shared state not initialized"}
    
    
# --- Status ---
@app.get("/edi/status")
def get_status():
    if shared_state is not None:
        return dict(shared_state)
    return {"status": "offline"}