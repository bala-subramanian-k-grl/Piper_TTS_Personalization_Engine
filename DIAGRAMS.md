## 1. Dataset Pipeline

flowchart LR
A[Raw Audio & Text Sources\n(Audiobooks, Scripts, Web Text)] --> B[Data Cleaning\n(remove noise, clipping, bad segments)]
B --> C[Segmentation\n(split into utterances)]
C --> D[Alignment\n(audio ↔ text)]
D --> E[Normalization\n(text, sampling rate, loudness)]
E --> F[Feature Extraction\n(mel-spectrograms, phonemes, prosody)]
F --> G[Training Dataset\n(ready for TTS models like Piper)]


This diagram illustrates the typical pipeline from raw recordings and text sources to a training-ready dataset used by TTS models like Piper, similar to how LibriTTS and HUI corpora are prepared. [web:104][web:111]

Feature Extraction Flow

flowchart LR
A[Audio Waveform] --> B[Preprocessing\n(resample, trim, normalize)]
B --> C[Acoustic Features\n(mel-spectrogram, energy)]
B --> D[Prosodic Features\n(pitch F0, duration, pauses)]

E[Text Transcripts] --> F[Text Normalization\n(expand numbers, abbreviations)]
F --> G[Phoneme/Character Sequences]

C --> H[TTS Model Input]
D --> H
G --> H

This diagram shows how audio and text are converted into features such as mel-spectrograms, prosody signals, and phoneme sequences, which are then fed into the TTS model. [web:104][web:82]

Voice Characteristic Mapping

flowchart LR
A[Dataset Properties] --> B[Learned Acoustic & Prosodic Space]
B --> C[Synthesized Voice Characteristics]

A --> A1[Sampling Rate & Bit Depth]
A --> A2[Noise Level & Room Acoustics]
A --> A3[Speakers & Accents]
A --> A4[Text & Phoneme Coverage]
A --> A5[Prosody & Emotion Diversity]

C --> C1[Clarity]
C --> C2[Naturalness]
C --> C3[Accent & Pronunciation]
C --> C4[Pitch & Timbre]
C --> C5[Emotional Expressiveness]


This diagram conceptually links dataset design choices (left) to the latent representation learned by a TTS model and finally to perceived voice qualities (right). [web:104][web:110][web:111]

## 2. Architecture

flowchart LR
subgraph User Side
U1[User Text Input]
U2[User Audio Recording\nuser_raw.wav]
end


subgraph Preprocessing
    P1[Audio Preprocess\n(preprocess_audio.py)]
    P2[user_clean.wav]
end

subgraph Analysis
    A1[Prosody Extraction\n(prosody_profile.py)]
    A2[Emotion Inference\n(emotion_model.py)]
    A3[Style Mapping\n(style_mapping.py)]
end

subgraph Profile
    J1[Profile Builder\n(profile_builder.py)]
    J2[voice_profile.json]
end

subgraph TTS Engine
    T1[Piper CLI Wrapper\n(main_cli.py)]
    T2[Piper Binary\npiper.exe + .onnx]
    T3[personalized.wav]
end

U2 --> P1 --> P2
P2 --> A1 --> A2 --> A3 --> J1 --> J2
U1 --> T1
J2 --> T1
T1 --> T2 --> T3


This shows where personalization fits into the TTS pipeline: user audio is analyzed once to produce a reusable profile, which is then used at inference time along with text input.

---

## 3. Data Flow Diagram (DFD)

flowchart LR
subgraph Level0[Level 0 DFD]
U[(User)]
U -->|records voice| D1[user_raw.wav]


    D1 --> P[Preprocess Audio]
    P --> D2[user_clean.wav]

    D2 --> F[Feature Extractor]
    F --> D3[Prosody Features]

    D3 --> E[Emotion Classifier]
    E --> D4[Emotion Label]

    D3 --> S[Style Mapper]
    D4 --> S
    S --> D5[Piper Params]

    D3 --> B[Profile Builder]
    D4 --> B
    D5 --> B
    B --> D6[voice_profile.json]

    U -->|types text| T[CLI/API]
    D6 --> T
    T --> C[Piper Engine]
    C --> D7[personalized.wav]
    D7 --> U
end
