def prosody_to_piper_params(profile: dict, emotion: str) -> dict:
    speech_rate = profile["speech_event_rate"]
    std_f0 = profile["std_f0"]

    # Base defaults
    length_scale = 1.0
    noise_scale = 0.7
    noise_w = 0.8

    # Stronger mapping for speed
    if speech_rate > 5:
        length_scale = 0.8  # much faster
    elif speech_rate < 3:
        length_scale = 1.2  # much slower

    # Stronger mapping for expressiveness
    if std_f0 > 40:
        noise_scale = 1.0
        noise_w = 1.2
    else:
        noise_scale = 0.5
        noise_w = 0.6

    # Emotion tweaks
    if emotion == "excited":
        length_scale *= 0.9
        noise_scale *= 1.1
    elif emotion == "sad":
        length_scale *= 1.1
        noise_scale *= 0.9

    return {
        "length_scale": length_scale,
        "noise_scale": noise_scale,
        "noise_w": noise_w,
        "emotion": emotion,
    }
