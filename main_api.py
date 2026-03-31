from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# This is the "Walkie-Talkie" - start_edi.py will fill this in automatically
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

@app.post("/session/start")
def start_session():
    if shared_state is not None:
        shared_state["session_active"] = True
        print("API: Received Start Signal. M has left.")
        return {"message": "EDI Awakened"}
    return {"error": "Shared state not initialized"}

@app.get("/edi/status")
def get_status():
    if shared_state is not None:
        # Return the actual live data from the Brain
        return dict(shared_state) 
    return {"status": "offline"}