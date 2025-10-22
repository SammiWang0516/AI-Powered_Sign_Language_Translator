# 🤟 AI-Powered Sign Language Translator

This project converts spoken or written English into **American Sign Language (ASL)** gloss or visual representations using deep-learning models.  
It combines audio transcription (speech-to-text) with text processing and optional gesture visualization.

---

## 🧰 Requirements

- **Python:** ≥ 3.9 and < 3.13  
  ⚠️ The `sign-language-translator` dependency is not compatible with Python 3.13+.  
- **Operating System:** macOS, Linux, or Windows  
- **Optional:** GPU support (for faster inference with PyTorch)

---

## 🚀 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/SammiWang0516/AI-Powered_Sign_Language_Translator.git
   cd AI-Powered_Sign_Language_Translator
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv slt_env
   source slt_env/bin/activate        # macOS / Linux
   # or
   slt_env\Scripts\activate         # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run a sample script**
   ```bash
   python test.py
   ```

---

## 🧩 Example Workflow

1. **Audio Input** → Speech recognition model (e.g., Whisper) → English text  
2. **Text Input** → NLP-based gloss converter → ASL-style gloss text  
3. **Gloss Output (optional)** → Visual sign representation using pose estimation

---

## 🧠 Troubleshooting

- **Error: NumPy version mismatch**  
  → Downgrade NumPy before installation:  
  ```bash
  pip install "numpy<2.0.0"
  ```

- **Error: Mediapipe build failure on macOS**  
  → Ensure you have the latest Xcode Command Line Tools installed:  
  ```bash
  xcode-select --install
  ```

- **Python version error**  
  → Use Python 3.9 – 3.12. The package currently does **not** support 3.13+.

---

## 🙌 Credits

This project builds upon open-source work from  
[sign-language-translator](https://github.com/sign-language-translator/sign-language-translator)  
and integrates additional preprocessing and visualization components for research and learning.
