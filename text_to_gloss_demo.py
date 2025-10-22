# ============================================
# 🤟 English → ASL-style Gloss Demo (No normalize / lemmatize)
# ============================================
# Author: Sammi Wang
# ============================================

from importlib import reload
import custom_english
reload(custom_english)
from custom_english import EnglishCustom as English
from sign_language_translator.text.tagger import Tags
from pprint import pprint

# Initialize
english = English()

# Example Whisper transcript
text = "Hello, how are you doing today? I learn sign language!"

print("\n=======================================")
print("🎧 Original Text:")
print(text)

# Step 1 — Preprocess
cleaned = english.preprocess(text)
print("\n🧹 Preprocessed Text:")
print(cleaned)

# Step 2 — Tokenize
tokens = english.tokenize(cleaned)
print("\n🪞 Tokens:")
pprint(tokens)

# Step 3 — Tag tokens
tagged = english.tag(tokens)
print("\n🏷️ Tagged Tokens:")
pprint(tagged)

# Step 4 — Filter only actual words (skip punctuation / spaces)
word_tokens = [token for token, tag in tagged if tag in (Tags.WORD, Tags.SUPPORTED_WORD)]
print("\n📚 Word Tokens (for Gloss):")
pprint(word_tokens)

# Step 5 — Convert to ASL-style gloss (uppercase words)
gloss = " ".join(t.upper() for t in word_tokens)
print("\n🤟 ASL-style Gloss:")
print(gloss)

print("=======================================\n")

eng = English()
print("'I' in ambiguous_to_unambiguous:", "i" in eng.vocab.ambiguous_to_unambiguous)

if "I" in eng.vocab.ambiguous_to_unambiguous:
    print("Ambiguous meanings for 'I':", eng.vocab.ambiguous_to_unambiguous["I"])