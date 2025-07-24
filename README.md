# Language Translation Script

This project provides a Python script (`translation.py`) to automatically translate a set of predefined English-language UI strings into 40+ target languages using Google Gemini. The script generates a `translation.json` file for each language, preserving the original keys and translating only the values.

## Features

- Translates a fixed set of UI strings into 40+ languages.
- Uses Google Gemini for high-quality, automated translations.
- Outputs a `translation.json` file for each language in its own directory.
- Easy to extend with more languages or strings.

## Directory Structure

```
LANGUAGE_TRANSLATION_SCRIPT/
  ├── translation.py
  ├── <lang_code>/
  │     └── translation.json
  └── ...
```

Each language (e.g., `hi` for Hindi, `fr` for French) gets its own folder containing a `translation.json` file.

## Prerequisites

- Python 3.7+
- Google Gemini API access

### Install Dependencies

```bash
pip install google-generativeai
```

### Set Up API Key

You must set your Gemini API key as an environment variable:

**Linux/macOS:**
```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=YOUR_API_KEY
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

## Usage

To generate translations for all supported languages, simply run:

```bash
python translation.py
```

- The script will skip English (source language) by default.
- Each target language will have its own `<lang_code>/translation.json` file created or updated.

## How It Works

- The script defines a dictionary of English UI strings (`SOURCE_STRINGS`).
- It iterates over a list of target languages (`LANGUAGES`).
- For each language, it sends the English strings to Google Gemini for translation.
- The translated strings are saved in a JSON file under the corresponding language directory.

## Customization

- To add or remove languages, edit the `LANGUAGES` dictionary in `translation.py`.
- To change the source strings, edit the `SOURCE_STRINGS` dictionary.

## Troubleshooting

- If you encounter API errors, ensure your `GEMINI_API_KEY` is set and valid.
- If translation fails for a language, check the console output for error details.

## License

MIT License 
