from gtts import gTTS
import os
from uuid import uuid4

def text_to_speech(text: str, lang: str = "hi", output_file: str = None) -> str:
    if output_file is None:
        output_file = f"{uuid4().hex}.mp3"
    
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_file)
    return output_file
