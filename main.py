# main.py

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import time
import random
import io
from PIL import Image

# 1. MOCK DATABASE AND LOGS (Simulating the Data Tier)
SIMULATED_DB = {
    # Pre-enrolled user: User ID and a simulated face encoding (a list of random floats)
    "1001": [0.12, 0.45, 0.78, 0.32],
}
ATTENDANCE_LOGS = []

# 2. FastAPI Application Instance
# main.py

# ... (baaki code)

# Note: '*' ko replace karke apne Render URL ko daalna hai
# Apne URL ko quotes ke andar aur list ke andar rakhiye.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://my-biometric-app.onrender.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... (baaki code)

# 4. MOCK BIOMETRIC FUNCTION (Simulating the Face Recognition Library)
def mock_get_face_encoding(image_data: bytes) -> list:
    """Simulates converting an image into a unique feature vector."""
    # In a real project, this calls dlib/face_recognition. Here, it returns a random vector of length 4.
    return [random.random() for _ in range(4)]

# 5. API ENDPOINTS (Implementation)

@app.post("/enroll")
async def enroll_user(user_id: str = Form(...), image: UploadFile = File(...)):
    """API endpoint for enrolling a new user."""
    
    # Read the uploaded image bytes
    image_bytes = await image.read()
    
    # Optional: Validate image format using Pillow (simulation of initial processing)
    try:
        Image.open(io.BytesIO(image_bytes))
    except Exception:
        return {"status": "error", "message": "Invalid image format received."}
    
    # 1. Simulate Feature Extraction
    new_encoding = mock_get_face_encoding(image_bytes)
    
    # 2. Store in Simulated DB
    SIMULATED_DB[user_id] = new_encoding
    
    return {"status": "success", "message": f"User {user_id} enrolled successfully. Total users: {len(SIMULATED_DB)}"}

@app.post("/clock-in")
async def clock_in(image: UploadFile = File(...)):
    """API endpoint for authentication and logging attendance."""
    
    # Read the uploaded image bytes
    image_bytes = await image.read()
    
    # 1. Simulate Feature Extraction for the incoming image
    live_encoding = mock_get_face_encoding(image_bytes)
    
    # 2. Simulate Authentication (Mock logic: 60% chance of matching a random user)
    
    matched_user_id = "N/A"
    match_status = "FAILED"
    
    if random.random() > 0.4:
        # 60% chance of success: select a random user to match
        matched_user_id = random.choice(list(SIMULATED_DB.keys()))
        match_status = "SUCCESS"
    
    # 3. Log Attendance
    if match_status == "SUCCESS":
        ATTENDANCE_LOGS.append({
            "user_id": matched_user_id,
            "timestamp": time.ctime(),
            "status": "CHECK-IN"
        })
    
    return {
        "status": match_status,
        "user_id": matched_user_id,
        "timestamp": time.ctime(),
        "log_count": len(ATTENDANCE_LOGS)
    }

# 6. Server Runner
if __name__ == "__main__":
    import uvicorn
    # This command is what you'll run in your terminal: uvicorn main:app --reload
    uvicorn.run(app, host="127.0.0.1", port=8000)