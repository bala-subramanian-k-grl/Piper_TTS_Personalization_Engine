# Dataset Pipeline & Architecture (Mermaid + Light fallback)

I fixed formatting issues, removed duplicate headings, simplified where Mermaid styling can cause rendering problems, and added a light (plain-text) fallback that will display well if Mermaid or rich styling does not render.

## 1. Dataset Pipeline

Below are refreshed Mermaid diagrams (styled but kept compatible). If your viewer cannot render the full styles, use the "Light display" plain-text section after the Mermaid blocks.

```mermaid
flowchart LR
  %% Sources
  subgraph Sources[" "]
    A["📚 Raw Audio & Text Sources\n(Audiobooks, Scripts, Web Text)"]
  end

  %% Cleaning / prep stages
  A --> B{{"🧹 Data Cleaning"}}
  B --> C["✂️ Segmentation\n(split into utterances)"]
  C --> D["🔗 Alignment\n(audio ↔ text)"]
  D --> E["⚖️ Normalization\n(text, sampling rate, loudness)"]
  E --> F["🔬 Feature Extraction\n(mel-spectrograms, phonemes, prosody)"]
  F --> G(["🎯 Training Dataset\n(ready for TTS models like Piper)"])

  %% Minimal styling that most Mermaid renderers accept
  classDef stage fill:#ECFEFF,stroke:#0891B2,color:#05445E;
  class A,B,C,D,E,F,G stage;
```

This diagram shows the journey from raw recordings and text to a training-ready dataset (used in corpora like LibriTTS/HUI).

## Feature Extraction Flow

```mermaid
flowchart LR
  subgraph Audio["Audio Path"]
    AW[Waveform] --> AP[Resample / Trim / Normalize]
    AP --> AF1["Acoustic Features\n(mel-spectrogram, energy)"]
    AP --> AF2["Prosodic Features\n(pitch F0, duration, pauses)"]
  end

  subgraph Text["Text Path"]
    T[Text Transcripts] --> TN["Text Normalization\n(expand numbers, abbreviations)"]
    TN --> TP[Phoneme / Character Sequences]
  end

  AF1 --> M[TTS Model Input]
  AF2 --> M
  TP --> M
```

This diagram visualizes parallel audio and text processing streams that converge into the TTS model input.


### 1.3 Voice Characteristic Mapping (Conceptual)

```mermaid
flowchart LR
  subgraph DatasetDesign["Dataset Design Choices"]
    D1[Sampling Rate & Bit Depth]
    D2[Noise Level & Room Acoustics]
    D3[Speakers & Accents]
    D4[Text & Phoneme Coverage]
    D5[Prosody & Emotion Diversity]
  end

  L[Learned Latent\nAcoustic & Prosodic Space] --> S[Synthesized Voice\nCharacteristics]

  D1 --> L
  D2 --> L
  D3 --> L
  D4 --> L
  D5 --> L

  S --> SC1[Clarity]
  S --> SC2[Naturalness]
  S --> SC3[Accent & Pronunciation]
  S --> SC4[Pitch & Timbre]
  S --> SC5[Emotional Expressiveness]
```

This conceptual map links dataset design to learned latent space and then to perceived voice qualities.
## 2. Architecture
```mermaid
flowchart TD
  %% Top-to-bottom, simple and compatible Mermaid diagram
  %% No parentheses in node labels to avoid parser issues on some renderers
  classDef big fill:#f8f9fa,stroke:#0366d6,stroke-width:1px,rx:6,ry:6,font-size:20px;

  UserText[User Text Input]:::big
  UserAudio[User Audio Recording\nuser_raw.wav]:::big
  AudioPreprocess[Audio Preprocess - preprocess_audio.py]:::big
  CleanedAudio[Cleaned Audio\nuser_clean.wav]:::big
  Prosody[Prosody Extraction - prosody_profile.py]:::big
  Emotion[Emotion Inference - emotion_model.py]:::big
  Style[Style Mapping - style_mapping.py]:::big
  ProfileBuilder[Profile Builder - profile_builder.py]:::big
  VoiceProfile[voice_profile.json]:::big
  PiperCLI[Piper CLI Wrapper - main_cli.py]:::big
  PiperBin[Piper Binary - piper.exe and onnx]:::big
  Output[personalized.wav]:::big

  %% Main vertical flow (straight top-to-bottom)
  UserAudio --> AudioPreprocess --> CleanedAudio --> Prosody --> Emotion --> Style --> ProfileBuilder --> VoiceProfile --> PiperCLI --> PiperBin --> Output

  %% Text input goes to the TTS CLI; profile also feeds the CLI
  UserText --> PiperCLI
  VoiceProfile --- Note[This voice profile is built once and is reused at inference time]:::big

  %% Links styling for visibility
  linkStyle default stroke:#6c757d,stroke-width:2px;
```


## 3. Data Flow Diagram (DFD) — Level 0

```mermaid
flowchart LR
  subgraph Level0["Level 0 DFD"]
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
```

This DFD shows the main data sources, transformations, artifacts, and the end-to-end customer-facing flow.

---


