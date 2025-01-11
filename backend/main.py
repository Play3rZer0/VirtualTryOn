# main.py

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
import os
import uuid
from vton_pipeline import run_vton_pipeline  # Import your VTON pipeline
#from usage_db import SessionLocal, UsageRecord  # Import database-related modules
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create directories for temporary and output images
os.makedirs("temp_images", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

@app.post("/api/tryon")
async def try_on(
    #store_id: str,  # New parameter: store_id for usage tracking
    store_id: str = Form(...),  # Expect store_id as a form field
    user_photo: UploadFile = File(...),  # User photo upload
    cloth_photo: UploadFile = File(...)  # Clothing photo upload
):
    """
    Handles the try-on operation:
    1. Save uploaded files to disk.
    2. Run the VTON pipeline.
    3. Increment usage count in the database.
    4. Return the composited image.
    """
    try:
        # 1. Save user photo
        user_filename = f"temp_images/{uuid.uuid4()}.{user_photo.filename.split('.')[-1]}"
        with open(user_filename, "wb") as f:
            f.write(await user_photo.read())

        # 2. Save cloth photo
        cloth_filename = f"temp_images/{uuid.uuid4()}.{cloth_photo.filename.split('.')[-1]}"
        with open(cloth_filename, "wb") as f:
            f.write(await cloth_photo.read())

        # 3. Run the VTON pipeline
        output_path = run_vton_pipeline(user_filename, cloth_filename)

        # 4. Increment usage count in the database
        #session = SessionLocal()
        #record = session.query(UsageRecord).filter_by(store_id=store_id).first()
        #if not record:
        #    record = UsageRecord(store_id=store_id, usage_count=0)
        #record.usage_count += 1
        #session.add(record)
        #session.commit()
        #session.close()

        # 5. Return the final image as a file response
        return FileResponse(output_path, media_type="image/png")

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

