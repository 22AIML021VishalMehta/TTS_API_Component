from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from tts import text_to_speech
import os

app = FastAPI()

def delete_file_after_response(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"✅ Deleted: {file_path}")
    except Exception as e:
        print(f"❌ Failed to delete {file_path}: {str(e)}")

@app.post("/tts/")
def generate_speech(
    text: str = Query(..., description="Text to convert to speech"),
    lang: str = Query("hi", description="Language code"),
    background_tasks: BackgroundTasks = None
):
    try:
        audio_file = text_to_speech(text=text, lang=lang)
        audio_stream = open(audio_file, "rb")
        
        # Schedule file deletion in the background
        background_tasks.add_task(delete_file_after_response, audio_file)
        
        return StreamingResponse(
            audio_stream,
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"inline; filename={audio_file}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

