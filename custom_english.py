# custom_english.py
# ============================================
# Hard patch so "I" is always SUPPORTED_WORD
# ============================================

from sign_language_translator.languages.text.english import English
from sign_language_translator.text.tagger import Tags

class EnglishCustom(English):
    def __init__(self):
        super().__init__()

        # Wrap the original tag method
        orig_tag = self.tagger.tag

        def patched_tag(tokens):
            tagged = orig_tag(tokens)
            fixed = []
            for token, tag in tagged:
                if token == "I" or token.lower() == "i":
                    tag = Tags.SUPPORTED_WORD
                fixed.append((token, tag))
            return fixed

        # Replace the tagger’s tag method with our patched one
        self.tagger.tag = patched_tag

