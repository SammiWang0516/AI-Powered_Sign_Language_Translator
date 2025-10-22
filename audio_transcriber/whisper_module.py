# ==============================================
# 🎙️ Whisper Transcribe Utility (Record or Upload)
# ==============================================
# Author: Sammi Wang
# Description:
#   - Option 1: Record your own voice via microphone
#   - Option 2: Upload an existing audio file
#   - Output: Transcribed text string (usable by SLT translator)
# ==============================================

import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
from pathlib import Path
import os


# ===========================
# 🧠 Load Whisper Model
# ===========================
def load_whisper(model_name="base"):
    """Load Whisper model (from local file if available)."""
    model_path = Path(__file__).parent / "models" / f"{model_name}.pt"
    if model_path.exists():
        print(f"🧠 Loading local Whisper model: {model_path}")
        return whisper.load_model(str(model_path))
    else:
        print(f"🌐 Loading Whisper model from OpenAI: {model_name}")
        return whisper.load_model(model_name)


# ===========================
# 🎙️ Record Audio Function
# ===========================
def record_audio(duration=5, samplerate=16000):
    """Record microphone input and save to temp WAV file."""
    print(f"🎤 Recording {duration} seconds of audio...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate,
                   channels=1, dtype='float32')
    sd.wait()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_path = tmp_file.name
    write(tmp_path, samplerate, audio)
    print(f"✅ Recording saved: {tmp_path}")
    return tmp_path


# ===========================
# 📂 Upload / Transcribe Function
# ===========================
def transcribe_audio(model_name="base"):
    """
    Ask user whether to record or upload, then transcribe audio.
    Returns the transcribed text.
    """
    model = load_whisper(model_name)

    print("\n============================")
    print("🎧 Whisper Transcription Mode")
    print("============================")
    print("1️⃣ Record new audio")
    print("2️⃣ Upload existing audio file")
    choice = input("Select option (1 or 2): ").strip()

    # --- Case 1: Record ---
    if choice == "1":
        try:
            duration = int(input("Enter recording duration (seconds): ").strip())
        except ValueError:
            duration = 5
            print("⚠️ Invalid input. Defaulting to 5 seconds.")
        audio_path = record_audio(duration=duration)

    # --- Case 2: Upload existing file ---
    elif choice == "2":
        audio_path = input("Enter full path of audio file: ").strip()
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"❌ File not found: {audio_path}")

    else:
        print("⚠️ Invalid selection. Exiting.")
        return ""

    print("\n🧠 Transcribing...")
    result = model.transcribe(audio_path)
    text = result["text"].strip()
    print(f"✅ Transcription complete:\n{text}\n")

    # Cleanup temp recording if recorded
    if choice == "1" and os.path.exists(audio_path):
        os.remove(audio_path)

    return text


# ===========================
# 🚀 Run Directly (Optional)
# ===========================
if __name__ == "__main__":
    text = transcribe_audio()
    if text:
        # Save transcription to a file
        save_dir = Path("data/transcripts")
        save_dir.mkdir(parents=True, exist_ok=True)
        out_path = save_dir / "whisper_output.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"💾 Transcript saved to: {out_path.resolve()}")
