# SignSpeak AI — Project Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│                    SignSpeak AI                          │
│           AI Sign Language Translator                    │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────┐
│   app.py            │  ← Entry point, router, sidebar
│   (Streamlit App)   │
└────────┬────────────┘
         │ routes to
    ┌────┴──────────────────────────────────────────┐
    │                   Pages                        │
    ├───────────────┬───────────────┬───────────────┤
    │ live_detection│  gesture_     │  word_builder  │
    │               │  recognition  │               │
    ├───────────────┼───────────────┼───────────────┤
    │ image_upload  │  history_page │  statistics    │
    ├───────────────┼───────────────┼───────────────┤
    │ learning_mode │  emergency    │  multi_language│
    ├───────────────┴───────────────┴───────────────┤
    │ settings      │  home                          │
    └───────────────┴───────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                     Utils Layer                          │
├──────────────┬──────────────┬──────────────────────────┤
│ model_loader │hand_extractor│         tts              │
│ (pkl/h5/     │(MediaPipe    │  (gTTS / pyttsx3)        │
│  tflite/pt)  │ landmarks)   │                          │
├──────────────┼──────────────┼──────────────────────────┤
│ translator   │history_utils │  demo_predictor          │
│(deep-        │(pandas,JSON) │  (fallback)              │
│ translator)  │              │                          │
├──────────────┴──────────────┴──────────────────────────┤
│       session.py  │  styles.py  │  __init__.py          │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                   Data Layer                             │
├──────────────────────┬──────────────────────────────────┤
│  models/             │  history/                        │
│  sign_model.pkl etc  │  predictions.json                │
└──────────────────────┴──────────────────────────────────┘
```

## Data Flow: Live Detection

```
Browser Webcam
     │
     ▼
st.camera_input()          ← Streamlit captures JPEG frame
     │
     ▼
cv2.imdecode()             ← Decode to numpy BGR array
     │
     ▼
HandExtractor.extract()    ← MediaPipe Hands
     │                        21 landmarks → 63-dim vector
     │                        Normalized to wrist origin
     ▼
SignModel.predict()        ← dispatch by model_type:
     │                        sklearn → predict_proba()
     │                        keras   → model.predict()
     │                        tflite  → interpreter.invoke()
     │                        torch   → model(inp)
     ▼
{ label, confidence }
     │
     ├─→ Display prediction box (HTML)
     ├─→ Confidence bar (HTML)
     ├─→ record_prediction() → session state + JSON
     ├─→ speak_text() → gTTS audio → HTML autoplay
     └─→ Word builder letters list
```

## Session State Architecture

```python
st.session_state = {
    # Navigation
    "current_page": str,           # active page key

    # Word/Sentence builder
    "current_letters": list[str],  # ['H','E','L','L','O']
    "current_word":    str,        # "HELLO"
    "sentence_words":  list[str],  # ['HELLO','HOW','ARE','YOU']
    "full_sentence":   str,        # "HELLO HOW ARE YOU"

    # Predictions
    "last_prediction": str,
    "last_confidence": float,
    "total_predictions": int,

    # History (list of dicts)
    "prediction_history": [
        {"time": str, "date": str, "sign": str,
         "confidence": float, "mode": str}
    ],

    # Analytics
    "sign_counts": dict,           # {"A": 5, "Hello": 3, ...}

    # Settings
    "tts_enabled":    bool,
    "tts_engine":     str,         # "gtts" | "pyttsx3"
    "output_language": str,        # "English" | "Hindi" | ...
    "large_text":     bool,
    "high_contrast":  bool,
}
```

## Model Loader Architecture

The `SignModel` class is a generic wrapper supporting 4 frameworks:

```
SignModel.__init__(path)
    │
    ├── .pkl / .pickle  → _load_sklearn()  → predict_proba()
    ├── .h5  / .keras   → _load_keras()    → model.predict()
    ├── .tflite         → _load_tflite()   → interpreter.invoke()
    └── .pt  / .pth     → _load_torch()    → model(inp) + softmax
```

All formats expose a unified `.predict(features, labels)` method returning:
```python
{"label": str, "confidence": float, "class_idx": int}
```

## Feature Extraction Pipeline

MediaPipe produces 21 hand landmarks. Each landmark has (x, y, z) normalized
to image dimensions [0,1]. We apply an additional wrist-relative normalization:

```python
# Subtract wrist (landmark 0) from all landmarks
for i in range(0, 63, 3):
    features[i]   -= wrist_x
    features[i+1] -= wrist_y
    features[i+2] -= wrist_z
# Result: 63-dim translation-invariant feature vector
```

This makes predictions robust to hand position in the frame.
