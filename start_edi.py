import multiprocessing
import uvicorn
import main_api
import main

def run_api(shared_data):
    # connecting the API to the shared data
    main_api.shared_state = shared_data
    uvicorn.run(main_api.app, host="127.0.0.1", port=8080) # adjust host/port as needed
    #uvicorn.run(main_api.app, host="0.0.0.0", port=8080)

def run_brain(shared_data):
    main.run_edi_loop(shared_data)

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    
    shared_data = manager.dict({
        "session_active": False,
        "status": "idle",
        "emotion": "NEUTRAL",
        "message": "",
        "trigger_first_speech": False,
        "reset_memory": False,
        "start_mode": "",
        "end_reason": ""
    })
    
    # start both processes
    api_p = multiprocessing.Process(target=run_api, args=(shared_data,))
    brain_p = multiprocessing.Process(target=run_brain, args=(shared_data,))

    api_p.start()
    brain_p.start()

    api_p.join()
    brain_p.join()