# Piper TTS Personalization Engine

This project extends the Piper TTS engine with a personalization layer that learns a user's speaking style (pacing, pauses, pitch variation, coarse emotion) from a sample recording and applies that style when generating speech.

Base engine: Piper TTS (piper.exe + ONNX model) running locally on Windows.

## 1. Requirements

- Windows 10/11 (64-bit)
- Python 3.10+ installed and `py` command available
- Git installed
- Piper for Windows downloaded and extracted
- Python packages from `requirements.txt`:

py -m pip install -r requirements.txt



## 2. Piper setup (one time, Windows)

1. **Download Piper Windows binary**

   - Go to the official releases page:  
     https://github.com/rhasspy/piper/releases  
   - Under the latest release, download the Windows ZIP:  
     `piper_windows_amd64.zip` (or similar name).  
   - Alternatively, you can use this mirror link for the Windows binary:  
     https://sourceforge.net/projects/piper-tts.mirror/files/2023.11.14-2/piper_windows_amd64.zip/download

2. **Download a voice model (example: en_US-kathleen-low)**

   - Go to the official Piper voices on Hugging Face:  
     https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0/en/en_US/kathleen/low  
   - Download both of these files from that page:
     - `en_US-kathleen-low.onnx`  
     - `en_US-kathleen-low.onnx.json`

3. **Place the files on Windows**

   - Extract `piper_windows_amd64.zip` into:

     `C:\piper\piper\`

   - Ensure this folder contains at least:
     - `C:\piper\piper\piper.exe`
     - `C:\piper\piper\en_US-kathleen-low.onnx`
     - `C:\piper\piper\en_US-kathleen-low.onnx.json`







## 3. Clone and install this project

git clone https://github.com/Bollavaramvasu/Piper_TTS_Personalization_Engine.git
cd Piper_TTS_Personalization_Engine
py -m pip install -r requirements.txt



All commands above are run in **PowerShell** on Windows.

## 4. Run the personalization flow 
1. **Record user audio**

Record around 1–2 minutes of your voice (Windows Voice Recorder is fine) and save it in the project folder as:

`user_raw.wav`

2. **Preprocess the audio**

py preprocess_audio.py



- Input: `user_raw.wav`
- Output: `user_clean.wav` (mono, 22050 Hz, 16-bit)

3. **Train / build personalized profile**

py main_cli.py --train-profile



- Input: `user_clean.wav`
- Output: `voice_profile.json` (prosody features, emotion, Piper params)

4. **Convert any text to personalized speech**

py main_cli.py --text "This is my personalized Piper voice." --output personalized.wav



- Input: text from `--text`
- Output: `personalized.wav` (Piper TTS using learned style)

You can change the text and output filename as needed.

## 5. Sample input/output

This repository contains example files:

- `sample_input/user_raw_sample.wav` – example user recording
- `sample_output/voice_profile_sample.json` – example generated profile
- `sample_output/personalized_sample.wav` – example personalized audio

## 6. Project files overview

- `preprocess_audio.py` – audio normalization (user_raw.wav → user_clean.wav)
- `prosody_profile.py` – extract duration, pitch, energy, pauses, speaking rate from user_clean.wav
- `emotion_model.py` – rule-based emotion classification (neutral / happy / sad / excited)
- `style_mapping.py` – map prosody + emotion to Piper parameters (length_scale, noise_scale, noise_w)
- `profile_builder.py` – build and save JSON voice profile
- `main_cli.py` – Windows CLI entrypoint for training profile and synthesizing text to speech
- `logger.py` – common logging configuration
- `requirements.txt` – Python dependencies
- `DATASET_ANALYSIS.md` – Task 1 dataset analysis
- `ARCHITECTURE.md` – Task 3 architecture and integration docs
- `LOGS.md` – sample logs from a full Windows run
