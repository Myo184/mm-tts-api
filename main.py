import os
import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ဘယ်ဝဘ်ဆိုဒ်ကမဆို လှမ်းသုံးလို့ရအောင် CORS ဖွင့်ပေးခြင်း
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    text: str
    voice: str
    rate: str
    pitch: str

@app.post("/api/tts")
async def text_to_speech(data: TTSRequest):
    try:
        # Voice Name ကို Microsoft Edge TTS Format ပြောင်းခြင်း
        voice_name = "my-MM-ThihaNeural" if data.voice == "th" else "my-MM-NadiNeural"
        
        communicate = edge_tts.Communicate(
            text=data.text, 
            voice=voice_name,
            rate=data.rate,
            pitch=data.pitch
        )
        
        # အသံဖိုင်ကို ယာယီသိမ်းဆည်းခြင်း
        output_filename = "output.mp3"
        await communicate.save(output_filename)
        
        # ဤနေရာတွင် တကယ့်စနစ်တွင် ဖိုင်ကို Cloud ပေါ်တင်၍ Link ပြန်ပေးရမည်။
        # လောလောဆယ် စမ်းသပ်ရန် အဆင်သင့် API Link ချိတ်ဆက်မှုပုံစံ ပြုလုပ်ထားသည်။
        return {
            "success": True,
            "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", # နမူနာ အသံဖိုင်လင့်ခ်
            "srtData": "1\n00:00:00,500 --> 00:00:04,000\n" + data.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
