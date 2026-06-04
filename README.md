# 🤟 SignSpeak AI

> **AI-Powered Sign Language Translator — Final Year Project**  
> Bridging the communication gap between the deaf/mute community and the world.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=for-the-badge&logo=streamlit)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Deployment](https://img.shields.io/badge/Deploy-Streamlit_Cloud-ff4b4b?style=for-the-badge)

---

## 📌 Project Overview

**SignSpeak AI** is a complete, production-ready sign language translation system that uses **computer vision** and **machine learning** to detect hand signs in real time and convert them into **text** and **speech**. Designed to help mute, deaf, and speech-impaired people communicate effortlessly.

### 🎯 Key Capabilities

| Feature | Description |
|---------|-------------|
| 📷 Live Detection | Real-time A–Z alphabet detection via webcam |
| 🤚 Gesture Recognition | 33 common gestures (Hello, Help, I Love You, etc.) |
| 🔤 Word Builder | Build words letter-by-letter → full sentences |
| 🖼️ Image Upload | Upload any sign photo for instant prediction |
| 🔊 Text-to-Speech | gTTS + pyttsx3 voice output |
| 🌐 Multi-Language | Translate to Hindi, Punjabi, French, Spanish, German, Arabic |
| 🆘 Emergency Mode | One-tap large-button emergency communication |
| 📊 Statistics | Usage analytics, confidence graphs, top signs |
| 🎓 Learning Mode | Visual alphabet & gesture reference guide |
| ⚙️ Accessibility | Large text, high contrast, voice feedback |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Webcam (for live detection)
- Internet (for gTTS voice)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/SignSpeakAI.git
cd SignSpeakAI

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your pre-trained model (optional)
# Place your model in the models/ folder:
# models/sign_model.pkl    → scikit-learn
# models/sign_model.h5     → Keras/TensorFlow
# models/sign_model.tflite → TFLite
# models/sign_model.pt     → PyTorch

# 5. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## 🧠 Using Your Pre-Trained Model

SignSpeak AI automatically detects and loads your model. No code changes needed.

### Supported Formats

| Format | Framework | File |
|--------|-----------|------|
| `.pkl` / `.pickle` | scikit-learn, any pickle | `models/sign_model.pkl` |
| `.h5` / `.keras` | TensorFlow / Keras | `models/sign_model.h5` |
| `.tflite` | TensorFlow Lite | `models/sign_model.tflite` |
| `.pt` / `.pth` | PyTorch | `models/sign_model.pt` |

### Expected Input
Your model should accept a **63-dimensional feature vector** (21 MediaPipe hand landmarks × 3 coordinates: x, y, z).

### Expected Output
- For **sklearn**: implements `predict_proba()`
- For **Keras/TFLite**: softmax output layer
- For **PyTorch**: returns logits (softmax applied automatically)

### Demo Mode
If no model is found, the app runs in **Demo Mode** with simulated predictions — perfect for UI testing and presentations.

---

## 📁 Project Structure

```
SignSpeakAI/
├── app.py                      # Main entry point
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python version for Streamlit Cloud
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml             # Streamlit theme configuration
│
├── models/                     # ← Place your pre-trained model here
│   └── sign_model.pkl          # (example)
│
├── pages/                      # UI pages (each is a Streamlit view)
│   ├── home.py
│   ├── live_detection.py
│   ├── gesture_recognition.py
│   ├── word_builder.py
│   ├── image_upload.py
│   ├── history_page.py
│   ├── statistics.py
│   ├── learning_mode.py
│   ├── emergency.py
│   ├── multi_language.py
│   └── settings.py
│
├── utils/                      # Core utilities
│   ├── model_loader.py         # Generic model loader (pkl/h5/tflite/pt)
│   ├── hand_extractor.py       # MediaPipe feature extraction
│   ├── tts.py                  # Text-to-speech (gTTS + pyttsx3)
│   ├── translator.py           # Multi-language translation
│   ├── history_utils.py        # Prediction history & statistics
│   ├── demo_predictor.py       # Demo mode fallback
│   ├── session.py              # Session state management
│   └── styles.py               # Global CSS (dark neon theme)
│
├── history/                    # Prediction logs (auto-created)
├── screenshots/                # Saved screenshots
├── assets/                     # Static assets (images, icons)
├── docs/                       # Documentation
└── tests/                      # Unit tests
```

---

## 🌐 Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app**
4. Select your repository
5. Set **Main file path**: `app.py`
6. Click **Deploy!**

> **Note:** For large model files (>25MB), use [Git LFS](https://git-lfs.github.com/) or host the model on Google Drive / Hugging Face Hub and load it at runtime.

---

## 🎨 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit 1.32+ with custom CSS |
| Computer Vision | MediaPipe Hands 0.10+ |
| ML Runtime | scikit-learn / TensorFlow / PyTorch |
| Image Processing | OpenCV, Pillow |
| Text-to-Speech | gTTS (cloud), pyttsx3 (offline) |
| Translation | deep-translator (Google Translate API) |
| Data | pandas, numpy |

---

## 🖼️ Screenshots

> Add screenshots of your running application here

| Home Page | Live Detection | Gesture Recognition |
|-----------|---------------|---------------------|
| ![home](docs/screenshots/home.png) | ![live](docs/screenshots/live.png) | ![gesture](docs/screenshots/gesture.png) |

| Word Builder | Emergency Mode | Statistics |
|-------------|---------------|------------|
| ![word](docs/screenshots/word.png) | ![emergency](docs/screenshots/emergency.png) | ![stats](docs/screenshots/stats.png) |

---

## 🏗️ System Architecture

```
User Input (Webcam / Image)
         │
         ▼
  MediaPipe Hands
  (21 Landmark Extraction → 63-dim features)
         │
         ▼
  Pre-Trained Model
  (sklearn / keras / tflite / pytorch)
         │
         ▼
  Prediction + Confidence
         │
    ┌────┴────┐
    │         │
  Text     Speech (gTTS/pyttsx3)
    │
    ├─ Word Builder
    ├─ Sentence Builder
    ├─ Multi-Language Translation
    └─ History & Statistics
```

---

## 📊 Feature Comparison

| Feature | Implementation |
|---------|---------------|
| A-Z Alphabet | MediaPipe + ML model, 26 classes |
| 33 Gestures | Same model, 33 gesture classes |
| TTS Language | 7 languages via gTTS |
| Translation | 7 languages via deep-translator |
| History | Session + JSON file persistence |
| Export | CSV, TXT download |
| Emergency | 12 pre-set messages with one-tap speak |

---

## 🔮 Future Scope

- [ ] Real-time video stream processing (OpenCV frame-by-frame)
- [ ] Support for ISL (Indian Sign Language)
- [ ] Mobile app (Flutter/React Native)
- [ ] Word-level gesture prediction
- [ ] Bidirectional communication (speech → signs)
- [ ] WebRTC for browser-based live video
- [ ] Fine-tuning interface for custom datasets
- [ ] PDF export with prediction report

---

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=utils --cov-report=html
```

---

## 👥 Contributors

| Role | Name |
|------|------|
| Lead Developer | *Your Name* |
| Project Guide | *Supervisor Name* |
| Institution | *Your College/University* |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [MediaPipe](https://mediapipe.dev/) — Google's hand landmark detection
- [Streamlit](https://streamlit.io/) — App framework
- [gTTS](https://gtts.readthedocs.io/) — Text-to-speech
- [deep-translator](https://github.com/nidhaloff/deep-translator) — Translation

---

<div align="center">

**Made with ❤️ for the deaf and mute community**

*Final Year AI Project — Sign Language Translator*

</div>
