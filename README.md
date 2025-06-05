# wordle-fasthtml

Simple Wordle clone built with FastHTML. The interface now displays a small
keyboard showing which letters you've already guessed.

## Development

1. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app**
   ```bash
   uvicorn main:app --reload
   ```
4. **Run tests**
   ```bash
   pytest
   ```
