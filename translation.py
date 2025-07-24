"""
translator.py
Translate a predefined English-language JSON corpus into 40+ target languages
using Google Gemini.  For each language it creates:

    <lang_code>/translation.jsonThe resulting JSON file contains the same keys as the source, but with values
translated into the target language.

Prerequisites
-------------
1.  pip install google-generativeai
2.  Set the environment variable:
        export GEMINI_API_KEY="YOUR_API_KEY"
"""

import os
import json
import pathlib
import time
import google.generativeai as genai
import re

# ---------------------------------------------------------------------------
# 0.  List available models (for debugging)
# ---------------------------------------------------------------------------
def list_available_models():
    print("Available models:")
    try:
        models = genai.list_models()
        for m in models:
            print("-", m.name)
    except Exception as e:
        print("Could not list models:", e)

# Uncomment the following line to list models and exit
# list_available_models(); exit()

# ---------------------------------------------------------------------------
# 1.  Configuration
# ---------------------------------------------------------------------------

# 1-a.  Source corpus to translate
SOURCE_STRINGS = {
    "Go back to main menu": "Go back to main menu",
    "Clear History": "Clear History",
    "Please contact us.": "Please contact us.",
    "We will reply back.": "We will reply back.",
    "Documents": "Documents",
    "Important Links": "Important Links",
    "Leave your email": "Leave your email",
    "Cookie Consent": "We are tracking your Cookie. If you don't agree, please email us.",
    "Type your message": "Type your message here...",
    "Shopify placeholder": "Ask about orders, refunds, or discounts...",
    "Shopify greeting": "How can I help you today? Please select one of the following services:",
    "Order Status": "Order Status",
    "Refund": "Refund",
    "Discount": "Discount",
    "Name": "Name",
    "Email": "Email",
    "Note": "Note",
    "Send": "Send",
    "Message": "Message",
    "Phone Number": "Phone Number",
    "Phone": "Phone",
    "Send to WhatsApp": "Send to WhatsApp",
    "Sending...": "Sending...",
    "Submit": "Submit",
    "Write your note": "Write your note",
    "John Doe": "John Doe",
    "We have received your details.": "We have received your details.",
    "WhatsApp message sent successfully!": "WhatsApp message sent successfully!",
    "Sorry there is some problem. Please try again.": "Sorry there is some problem. Please try again."
}

# 1-b.  Language menu (Name ➜ code)
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Bengali": "bn",
    "Odia": "or",
    "Assamese": "as",
    "Urdu": "ur",
    "English (US)": "en-US",
    "English (UK)": "en-GB",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Chinese": "zh",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Turkish": "tr",
    "Polish": "pl",
    "Dutch": "nl",
    "Swedish": "sv",
    "Finnish": "fi",
    "Norwegian": "no",
    "Danish": "da",
    "Czech": "cs",
    "Greek": "el",
    "Hebrew": "he",
    "Indonesian": "id",
    "Thai": "th",
    "Vietnamese": "vi",
    "Ukrainian": "uk",
    "Hungarian": "hu",
    "Romanian": "ro",
    "Slovak": "sk",
    "Bulgarian": "bg",
    "Croatian": "hr",
    "Serbian": "sr",
    "Malay": "ms",
    "Tagalog": "tl",
    "Persian": "fa"
}

# ---------------------------------------------------------------------------
# 2.  Gemini setup
# ---------------------------------------------------------------------------

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

PROMPT_TEMPLATE = """You are a professional translator.
Translate the given JSON object's *values* (not keys) into {target_language}.
Return ONLY a valid JSON object with exactly the same keys.

JSON to translate:
{json_block}
"""

def extract_json(text):
    """Extract the first JSON object from a string."""
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    raise ValueError("No valid JSON object found in response.")

# ---------------------------------------------------------------------------
# 3.  Translation routine
# ---------------------------------------------------------------------------

def translate_to(language_name: str, lang_code: str, src_dict: dict):
    """Translate src_dict into the specified language and write translation.json."""
    # Build prompt
    prompt = PROMPT_TEMPLATE.format(
        target_language=language_name,
        json_block=json.dumps(src_dict, ensure_ascii=False, indent=2)
    )

    # Call Gemini
    response = model.generate_content(prompt)
    print(f"Raw response for {language_name} ({lang_code}):\n{response.text}\n")
    try:
        translated_json = extract_json(response.text)
    except Exception as e:
        print(f"✘ Failed to parse JSON for {language_name} ({lang_code}): {e}")
        print(f"Raw response was:\n{response.text}\n")
        return None

    # Write output
    out_dir = pathlib.Path(lang_code)
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "translation.json"
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(translated_json, f, ensure_ascii=False, indent=2)
    print(f"✔ {language_name:<15} → {out_file}")
    return out_file


def main():
    for name, code in LANGUAGES.items():
        # Skip source language (English) if desired
        if code.startswith("en"):
            continue
        try:
            translate_to(name, code, SOURCE_STRINGS)
            time.sleep(0.4)   # polite pacing to avoid rate limits
        except Exception as e:
            print(f"✘ Failed for {name} ({code}): {e}")


if __name__ == "__main__":
    main()
