# SignSpeak AI — Deployment Guide

## Table of Contents
1. [Local Development](#local-development)
2. [Streamlit Cloud](#streamlit-cloud)
3. [GitHub Setup](#github-setup)
4. [Using Your Pre-Trained Model](#using-your-pre-trained-model)
5. [Troubleshooting](#troubleshooting)

---

## 1. Local Development

### Requirements
- Python 3.10 or 3.11
- pip
- Webcam (for live detection)

### Steps

```bash
# Clone the project
git clone https://github.com/your-username/SignSpeakAI.git
cd SignSpeakAI

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

App opens at: `http://localhost:8501`

---

## 2. Streamlit Cloud

### Step-by-Step

1. **Push to GitHub** (see section 3 below)

2. **Go to** https://share.streamlit.io

3. **Sign in** with your GitHub account

4. **Click "New app"**

5. **Configure:**
   - Repository: `your-username/SignSpeakAI`
   - Branch: `main`
   - Main file path: `app.py`

6. **Click "Deploy!"**

7. Wait ~2–3 minutes. Your app will be live at:
   `https://your-username-signspeak-ai-app-xxxx.streamlit.app`

### Notes for Streamlit Cloud
- The app runs in **Demo Mode** if no model file is in `models/`
- For model files > 25MB, use Git LFS or load from URL (see below)
- `pyttsx3` will NOT work on Streamlit Cloud — use `gTTS` instead
- Camera input works via `st.camera_input()` in the browser

### Loading a Large Model from URL

If your model is too large for GitHub, host it on Google Drive or Hugging Face
and load it at startup. Add to `utils/model_loader.py`:

```python
import requests

def download_model_from_url(url: str, dest: str = "models/sign_model.pkl"):
    os.makedirs("models", exist_ok=True)
    if not os.path.exists(dest):
        r = requests.get(url, stream=True)
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return dest
```

Then call `download_model_from_url("YOUR_DIRECT_DOWNLOAD_LINK")` before `get_model()`.

---

## 3. GitHub Setup

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: SignSpeak AI Final Year Project"

# Create repo on github.com, then:
git remote add origin https://github.com/your-username/SignSpeakAI.git
git branch -M main
git push -u origin main
```

### For Large Model Files (Git LFS)

```bash
# Install Git LFS
git lfs install

# Track model files
git lfs track "models/*.pkl"
git lfs track "models/*.h5"
git lfs track "models/*.tflite"
git lfs track "models/*.pt"

git add .gitattributes
git commit -m "Add Git LFS tracking for model files"
git push
```

---

## 4. Using Your Pre-Trained Model

### Supported Formats

| File Extension | Framework | Notes |
|---|---|---|
| `.pkl` | scikit-learn (RandomForest, SVM, etc.) | Must implement `predict_proba()` |
| `.h5` / `.keras` | TensorFlow / Keras | Last layer must be softmax |
| `.tflite` | TensorFlow Lite | Optimized for mobile/cloud |
| `.pt` / `.pth` | PyTorch | Must be full model (not state_dict) |

### Required Model Interface

Your model must predict over these classes in order:

```python
# Alphabet classes (26)
['A','B','C','D','E','F','G','H','I','J','K','L','M',
 'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

# Gesture classes (33) — appended after alphabet
['Hello','Thank You','Yes','No','Good Morning','Good Night',
 'Please','Sorry','Help','I Love You','Welcome','Bye',
 'Nice To Meet You','How Are You','Fine','Hungry','Water',
 'Emergency','Doctor','Hospital','Police','Friend','Family',
 'Mother','Father','Brother','Sister','Food','Drink',
 'Stop','Go','Come','Wait']
```

If your model only predicts alphabets, that's fine — it will still work for
the Live Detection and Word Builder pages.

### Input Features

The app extracts **63 features** per hand using MediaPipe:
- 21 landmarks × (x, y, z) = 63 values
- Normalized relative to the wrist (landmark 0)

---

## 5. Troubleshooting

### "No module named mediapipe"
```bash
pip install mediapipe==0.10.9
```

### "No module named cv2"
```bash
pip install opencv-python-headless  # for cloud/server
# or
pip install opencv-python           # for local with GUI
```

### Camera not working on Streamlit Cloud
- Use `st.camera_input()` — it works in modern browsers
- Ensure your browser has camera permissions enabled
- Try Chrome or Edge (Safari may have issues)

### gTTS not working
- Check internet connection
- gTTS requires outbound HTTP to `translate.google.com`
- Streamlit Cloud allows outbound requests by default

### Model not loading
- Check file is in the `models/` directory
- Ensure the extension is one of: `.pkl`, `.h5`, `.keras`, `.tflite`, `.pt`, `.pth`
- Check the model was saved correctly (not a state_dict for PyTorch)

### Translation not working
- `deep-translator` requires internet access
- Falls back gracefully and returns original text if offline
- Check `pip install deep-translator` is in requirements.txt

### App is slow on first load
- MediaPipe initializes on first use — normal ~2–3s delay
- Model loading is cached with `@st.cache_resource`
- Subsequent predictions are fast

---

## Environment Variables (Optional)

Create `.streamlit/secrets.toml` for any API keys:

```toml
# .streamlit/secrets.toml (DO NOT commit to git)
[api]
some_key = "your-key-here"
```

Access in code: `st.secrets["api"]["some_key"]`
