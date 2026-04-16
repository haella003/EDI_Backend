from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Model for incoming data

# End options
class EndRequest(BaseModel):
    reason: str # e.g. "end_edi", "back_to_m"

# The "Walkie-Talkie"
# start_edi.py will fill this in automatically
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

# --- Start options ---
@app.post("/session/start")
def start_session():
    if shared_state is not None:
        shared_state["session_active"] = True
        shared_state["trigger_first_speech"] = True

        print("API: EDI awakened and listen.")
        
        return {
            "status": "starting",
            "emotion": "NEUTRAL",
            "description": "EDI is powering up and preparing to greet the user."
        }
            
    return {"error": "Shared state not initialized"}
    
    
# --- End options ---
@app.post("/session/end")
def end_session(request: EndRequest):
    if shared_state is not None:
        shared_state["session_active"] = False
        shared_state["end_reason"] = request.reason
        
        # tell start_edi.py to wipe the memory clean
        shared_state["reset_memory"] = True
        
        print(f"API: Session ended. Reason: {request.reason}")
        return {"message": f"EDI session closed successfully. Reason: {request.reason}"}
        
    return {"error": "Shared state not initialized"}
    
    
# --- Status ---
@app.get("/edi/status")
def get_status():
    if shared_state is not None:
        return dict(shared_state)
    return {"status": "offline"}