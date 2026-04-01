from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# --- Models for incoming data ---

# Start options
class StartRequest(BaseModel):
    mode: str # e.g. "m_handoff", "direct_edi"

# End options
class EndRequest(BaseModel):
    reason: str # e.g. "end_edi", "back_to_m"

# The "Walkie-Talkie" - start_edi.py will fill this in automatically
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
def start_session(request: StartRequest):
    if shared_state is not None:
        shared_state["session_active"] = True
        shared_state["start_mode"] = request.mode
        
        if request.mode == "m_handoff":
            print("API: M has left. EDI is now active and taking over the tour.")
            shared_state["trigger_first_speech"] = True
            return {"message": "EDI Awakened via M Handoff"}
        
        elif request.mode == "direct_edi":
            print("API: User skipped M. Directly starting EDI.")
            shared_state["trigger_first_speech"] = True
            return {"message": "EDI Awakened Directly"}
            
        return {"message": f"Session started with mode: {request.mode}"}
            
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