## 1. Dataset Pipeline

flowchart LR
    A[Raw Audio & Text Sources<br/>(Audiobooks, Scripts, Web Text)]
    B[Data Cleaning<br/>(remove noise, clipping, bad segments)]
    C[Segmentation<br/>(split into utterances)]
    D[Alignment<br/>(audio ↔ text)]
    E[Normalization<br/>(text, sampling rate, loudness)]
    F[Feature Extraction<br/>(mel-spectrograms, phonemes, prosody)]
    G[Training Dataset<br/>(ready for TTS models like Piper)]

    A --> B --> C --> D --> E --> F --> G


Feature Extraction Flow

flowchart LR
    A[Audio Waveform]
    B[Preprocessing<br/>(resample, trim, normalize)]

    C[Acoustic Features<br/>(mel-spectrogram, energy)]
    D[Prosodic Features<br/>(pitch F0, duration, pauses)]

    E[Text Transcripts]
    F[Text Normalization<br/>(expand numbers, abbreviations)]
    G[Phoneme / Character Sequences]

    H[TTS Model Input]

    A --> B
    B --> C
    B --> D

    E --> F --> G

    C --> H
    D --> H
    G --> H

Voice Characteristic Mapping

flowchart LR
    A[Dataset Properties]
    B[Learned Acoustic & Prosodic Space]
    C[Synthesized Voice Characteristics]

    A --> B --> C

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


## 2. Architecture

flowchart LR
    subgraph User_Side[User Side]
        U1[User Text Input]
        U2[User Audio Recording<br/>user_raw.wav]
    end

    subgraph Preprocessing
        P1[Audio Preprocess<br/>(preprocess_audio.py)]
        P2[user_clean.wav]
    end

    subgraph Analysis
        A1[Prosody Extraction<br/>(prosody_profile.py)]
        A2[Emotion Inference<br/>(emotion_model.py)]
        A3[Style Mapping<br/>(style_mapping.py)]
    end

    subgraph Profile
        J1[Profile Builder<br/>(profile_builder.py)]
        J2[voice_profile.json]
    end

    subgraph TTS_Engine[TTS Engine]
        T1[Piper CLI Wrapper<br/>(main_cli.py)]
        T2[Piper Binary<br/>(piper.exe + .onnx)]
        T3[personalized.wav]
    end

    U2 --> P1 --> P2
    P2 --> A1 --> A2 --> A3 --> J1 --> J2

    U1 --> T1
    J2 --> T1
    T1 --> T2 --> T3


## 3. Data Flow Diagram (DFD)

flowchart LR
    subgraph Level0[Level 0 DFD]
        U[(User)]

        D1[user_raw.wav]
        D2[user_clean.wav]
        D3[Prosody Features]
        D4[Emotion Label]
        D5[Piper Params]
        D6[voice_profile.json]
        D7[personalized.wav]

        P[Preprocess Audio]
        F[Feature Extractor]
        E[Emotion Classifier]
        S[Style Mapper]
        B[Profile Builder]
        T[CLI / API]
        C[Piper Engine]

        U -->|records voice| D1
        D1 --> P --> D2
        D2 --> F --> D3
        D3 --> E --> D4
        D3 --> S
        D4 --> S --> D5

        D3 --> B
        D4 --> B
        D5 --> B
        B --> D6

        U -->|types text| T
        D6 --> T --> C --> D7
        D7 --> U
    end

