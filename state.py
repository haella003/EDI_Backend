session_active = False # The Master On/Off switch
# share whiteboard fo EDI's current vitals

# current phase (idle, listening, thinking, speaking, error)
status = "idle"

# current mood extracted from the AI response
emotion = "NEUTRAL"

# text EDI is currently saying (or just said)
message = ""

# How much EDI should vibrate in VR (1.0 = calm, 2.5 = intense)
wobble = 1.0

# ID of the current chat session for logging
session_id = ""