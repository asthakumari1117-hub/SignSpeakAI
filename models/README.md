# models/

Place your pre-trained sign language model file here.

## Supported Formats

| File | Framework |
|------|-----------|
| `sign_model.pkl` | scikit-learn (recommended) |
| `sign_model.h5` | TensorFlow / Keras |
| `sign_model.tflite` | TensorFlow Lite |
| `sign_model.pt` | PyTorch |

## Notes

- Only ONE model file is needed.
- The app auto-detects whichever file is present.
- If no model is found, the app runs in **Demo Mode**.
- For files > 25MB, use Git LFS or load from a URL at startup.

## Expected Input

- **Shape:** `(63,)` — 21 MediaPipe hand landmarks × (x, y, z)
- **Type:** `float32`
- **Normalization:** Wrist-relative (landmark 0 subtracted)

## Expected Output

- Probabilities for each class (softmax)
- Class order: A–Z (indices 0–25), then gestures (26–58)
