

def infer_emotion(profile: dict) -> str:
    std_f0 = profile["std_f0"]
    std_energy = profile["std_energy"]
    speech_rate = profile["speech_event_rate"]
    pause_rate = profile["pause_rate"]

    high_pitch_var = std_f0 > 40
    high_energy_var = std_energy > 5
    fast = speech_rate > 4
    slow = speech_rate < 2
    many_pauses = pause_rate > 0.4

    if high_pitch_var and high_energy_var and fast and not many_pauses:
        return "excited"
    if slow and many_pauses and not high_pitch_var:
        return "sad"
    if not high_pitch_var and not high_energy_var and not fast:
        return "neutral"
    if high_pitch_var and not many_pauses:
        return "happy"

    return "neutral"

