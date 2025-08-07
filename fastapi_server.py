from fastapi import FastAPI
from pydantic import BaseModel
import io
from melo.api import TTS
from fastapi.responses import StreamingResponse
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

app = FastAPI()

# Initialize the TTS models as before
device = 'auto'
models = {
    'default': TTS(language='ZH_MIX_EN', device=device, config_path=config['config_path'], ckpt_path=config['ckpt_path']),
    'EN': TTS(language='EN', device=device),
    'ZH': TTS(language='ZH', device=device),
}

class SynthesizePayload(BaseModel):
    text: str = 'Ahoy there matey! There she blows!'
    language: str = 'EH'
    speaker: str = 'EN-US'
    speed: float = 1.0

@app.post("/stream")
async def synthesize_stream(payload: SynthesizePayload):
    language = payload.language
    text = payload.text
    speaker = payload.speaker or list(models[language].hps.data.spk2id.keys())[0]
    speed = payload.speed

    def audio_stream():
        bio = io.BytesIO()
        models[language].tts_to_file(text, models[language].hps.data.spk2id[speaker], bio, speed=speed, format='wav')
        audio_data = bio.getvalue()
        yield audio_data

    return StreamingResponse(audio_stream(), media_type="audio/wav")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
    
    