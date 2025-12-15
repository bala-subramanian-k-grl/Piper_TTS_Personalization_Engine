import time
import parselmouth
import numpy as np
from logger import get_logger

log = get_logger(__name__)


def extract_prosody(wav_path: str):
    start = time.perf_counter()

    snd = parselmouth.Sound(wav_path)
    duration = snd.get_total_duration()

    pitch = snd.to_pitch()
    f0 = pitch.selected_array["frequency"]
    f0 = f0[f0 > 0]

    intensity = snd.to_intensity()
    energy = intensity.values[0]

    # ... your existing code to compute mean_f0, std_f0, mean_energy, std_energy,
    # num_pauses, pause_rate, speech_event_rate ...

    profile = {
        "duration": duration,
        "mean_f0": mean_f0,
        "std_f0": std_f0,
        "mean_energy": mean_energy,
        "std_energy": std_energy,
        "num_pauses": num_pauses,
        "pause_rate": pause_rate,
        "speech_event_rate": speech_event_rate,
    }

    elapsed = time.perf_counter() - start
    log.info(
        f"Prosody features extracted from {wav_path}: {profile} "
        f"(f0_len={len(f0)}, energy_len={len(energy)}, time={elapsed:.3f}s)"
    )
    return profile

if __name__ == "__main__":
    p = extract_prosody("user_clean.wav")
    print(p)
