
import json
from pathlib import Path
from logger import get_logger
from prosody_profile import extract_prosody
from emotion_model import infer_emotion
from style_mapping import prosody_to_piper_params

log = get_logger(__name__)

def build_profile(
    input_wav: str = "user_clean.wav",
    output_json: str = "voice_profile.json",
    user_id: str = "default_user",
):
    prosody = extract_prosody(input_wav)
    emotion = infer_emotion(prosody)
    style = prosody_to_piper_params(prosody, emotion)

    profile = {
        "version": "1.0",
        "user_id": user_id,
        "source_audio": input_wav,
        "prosody_features": prosody,
        "dominant_emotion": emotion,
        "piper_runtime_params": {
            "length_scale": style["length_scale"],
            "noise_scale": style["noise_scale"],
            "noise_w": style["noise_w"],
        },
    }

    Path(output_json).write_text(json.dumps(profile, indent=2), encoding="utf-8")
    log.info(f"Built profile for {user_id}: emotion={emotion}, params={style}")

    return profile

if __name__ == "__main__":
    p = build_profile()
    print("Saved profile:", p)

