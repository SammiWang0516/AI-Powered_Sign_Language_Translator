# ==============================================
# Whisper Transcribe Utility (Record or Upload)
# ASL Gloss using sign-language-translator English Class
# ==============================================
# Author: Sammi Wang
# Description:
#   Step 1:
#   - Option 1: Record your own voice via microphone
#   - Option 2: Upload an existing audio file
#   Step 2:
#   - take the temporary text file (SLT/data/transcript/) as input
#   - implement the English class from languages/text/
#.  Step 3:
#.  - save the output gloss to temp folder (SLT/data/gloss/)
# ==============================================

import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
from pathlib import Path
import os
from importlib import reload
import custom_english
reload(custom_english)
from custom_english import EnglishCustom as English
from sign_language_translator.text.tagger import Tags
from pprint import pprint

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

def text_convert_gloss(obj, text):

    # step1: preprocess 
    cleaned = obj.preprocess(text)
    print('Preproessed Text:')
    print(cleaned)

    # step2: tokenize
    tokens = obj.tokenize(cleaned)
    print('\n Tokens:')
    pprint(tokens)

    # step3: tag tokens
    tagged = obj.tag(tokens)
    print('\n Tagged Tokens:')
    pprint(tagged)

    # step4: filter and only actual words left (no number or any punctuation)
    word_tokens = [token for token, tag in tagged if tag in (Tags.WORD, Tags.SUPPORTED_WORD)]
    print('\n Word Tokens (For Gloss):')
    pprint(word_tokens)

    # step5: convert to ASL-style gloss
    gloss = " ".join(t.upper() for t in word_tokens)
    print('\n ASL-style Gloss:')
    print(gloss)

    # step6: save gloss output
    gloss_dir = Path("data/gloss")
    gloss_dir.mkdir(parents=True, exist_ok=True)
    gloss_path = gloss_dir / "asl_output.txt"
    with open(gloss_path, "w", encoding="utf-8") as f:
        f.write(gloss)
    print(f"\n Gloss saved to: {gloss_path.resolve()}")

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

        # convert plain text to asl gloss
        with open(out_path, 'r', encoding='utf-8') as f:
            plain_text = f.read().strip()
        english = English()
        text_convert_gloss(english, plain_text)