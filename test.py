import sign_language_translator as slt

# Create a translator model (Concatenative Synthesis)
model = slt.models.ConcatenativeSynthesis(
    text_language="english",        # or "urdu"
    sign_language="pk-sl",          # or "us-asl", "bsl", etc.
    sign_format="video"             # or "landmarks"
)

# Translate a text sentence into a sign representation
sign = model.translate("this is an watermelon")

# Show or save the generated sign video
sign.show()             # open a viewer window
sign.save("sign_output.mp4", overwrite=True)