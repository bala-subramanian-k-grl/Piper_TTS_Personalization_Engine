# Piper TTS Personalization Engine

## Quickstart (Windows)

1. Install Piper and download a voice model.
2. Place `piper.exe` and the `.onnx` model in `C:\piper\piper`.
3. Clone this repo and go to the project folder.
4. Record `user_raw.wav` into the project folder.
5. Run:
   - `py preprocess_audio.py`
   - `py main_cli.py --train-profile`
   - `py main_cli.py --text "Hello" --output personalized.wav`
