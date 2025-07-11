from fasthtml.common import *
import asyncio
import sys
import random

if __name__ == "__main__": sys.exit("Run this app with `uvicorn main:app --reload`")

# Wordle Configuration
WORD_LENGTH = 5
MAX_GUESSES = 6

# A list of words for play.
# In a real app, you'd likely load these from a dictionary file.
WORDS = [
    "ABOUT", "ABOVE", "ADAPT", "AFTER", "AGAIN", "AGENT", "ALERT", "ALIVE",
    "ALONE", "ALONG", "AMONG", "ANGEL", "APPLE", "ARENA", "ARGUE", "ARISE",
    "ARRAY", "AWARD", "BADGE", "BASIC", "BATCH", "BEACH", "BEARD", "BEGIN",
    "BEING", "BERRY", "BLEND", "BLIND", "BLINK", "BLOCK", "BLOOM", "BOARD",
    "BONUS", "BRAIN", "BRAND", "BRAVE", "BRIEF", "BRING", "BROAD", "BROWN",
    "BRUSH", "BUILD", "BURST", "CABIN", "CABLE", "CAMEL", "CANAL", "CHAIN",
    "CHAIR", "CHAOS", "CHARM", "CHEER", "CHILD", "CIVIC", "CLEAN", "CLEAR",
    "CLERK", "CLICK", "CLIMB", "CLOUD", "CLOWN", "COACH", "COAST", "COLOR",
    "COUNT", "COURT", "CRAFT", "CRASH", "CRISP", "CROWD", "CROWN", "CRUEL",
    "DAILY", "DAIRY", "DANCE", "DEALT", "DEBIT", "DEFER", "DELAY", "DELTA",
    "DEPTH", "DEVIL", "DIGIT", "DIZZY", "DOUBT", "DRAFT", "DRAIN", "DREAM",
    "DRIVE", "EARLY", "EARTH", "EMBER", "ENJOY", "ENTER", "ENTRY", "EQUAL",
    "ERROR", "EVENT", "EVERY", "FAINT", "FAITH", "FALSE", "FAVOR", "FEAST",
    "FENCE", "FIELD", "FINAL", "FLAME", "FLOCK", "FLUTE", "FOCUS", "FOUND",
    "FRAME", "FRESH", "FRONT", "FROST", "FROWN", "FUNNY", "GHOST", "GIANT",
    "GLASS", "GLORY", "GRACE", "GRAND", "GRASS", "GREEN", "GROUP", "GUARD",
    "GUEST", "GUIDE", "HAPPY", "HAUNT", "HEART", "HEAVY", "HELLO", "HONEY",
    "HONOR", "HORSE", "HOTEL", "HOUSE", "HUMAN", "HUMOR", "IMAGE", "INDEX",
    "INPUT", "ISSUE", "JELLY", "JOINT", "JUDGE", "JUICE", "KNIFE", "KNOWN",
    "LARGE", "LASER", "LAUGH", "LAYER", "LEMON", "LEVEL", "LIGHT", "LIMIT",
    "LOCAL", "LOGIC", "LOYAL", "LUCKY", "MAGIC", "MAJOR", "MAPLE", "MARCH",
    "MERCY", "MERIT", "MINOR", "MODEL", "MONEY", "MONTH", "MOTOR", "MOUNT",
    "MOUSE", "MUSIC", "NERVE", "NIGHT", "NOBLE", "NOISE", "NORTH", "NOVEL",
    "NURSE", "OCEAN", "OFFER", "ONION", "OPERA", "ORBIT", "OTHER", "OUTER",
    "OZONE", "PAINT", "PANEL", "PAPER", "PARTY", "PASTA", "PENNY", "PHONE",
    "PHOTO", "PILOT", "PITCH", "PLANT", "PLATE", "POINT", "POLAR", "POWER",
    "PRESS", "PRICE", "PRIDE", "PRINT", "PUPPY", "QUEEN", "QUICK", "QUIET",
    "QUOTE", "RADIO", "RALLY", "RANGE", "RATIO", "REACH", "RIVER", "ROAST",
    "ROBOT", "ROUGH", "ROUND", "ROUTE", "ROYAL", "SALAD", "SCALE", "SCENE",
    "SCORE", "SCOUT", "SENSE", "SHADE", "SHAKE", "SHARE", "SHARP", "SHELF",
    "SHIFT", "SHINE", "SHIRT", "SHORT", "SHOWN", "SIGHT", "SKILL", "SKIRT",
    "SMILE", "SMOKE", "SOLID", "SOUND", "SPACE", "SPARE", "SPARK", "SPEED",
    "SPEND", "SPICY", "SPITE", "SPLIT", "SPOON", "SPRAY", "STACK", "STAGE",
    "STAIN", "STAND", "STARE", "START", "STATE", "STEEL", "STICK", "STOCK",
    "STONE", "STORE", "STORM", "STORY", "STOVE", "STRAP", "STUDY", "STUFF",
    "STYLE", "SUGAR", "SUNNY", "SWEET", "SWIFT", "TABLE", "TEACH", "TEETH",
    "TEMPO", "TENOR", "THANK", "THING", "THINK", "THORN", "THREE", "THUMB",
    "TIGHT", "TODAY", "TOUCH", "TOUGH", "TOWER", "TRACE", "TRACK", "TRADE",
    "TRAIN", "TREND", "TRIAL", "TRIBE", "TRICK", "TRUCK", "TRUST", "TRUTH",
    "TUTOR", "TWEET", "UNION", "UNITY", "UPPER", "URBAN", "USAGE", "VALID",
    "VALUE", "VENUE", "VERGE", "VIDEO", "VISIT", "VITAL", "VOCAL", "VOICE",
    "VOTER", "WAIST", "WASTE", "WATCH", "WATER", "WEARY", "WEIGH", "WHALE",
    "WHEAT", "WHEEL", "WHERE", "WHILE", "WHITE", "WHOLE", "WIDOW", "WOMAN",
    "WORLD", "WORRY", "WORTH", "WRITE", "WRONG", "YEAST", "YOUNG", "YOUTH",
    "ZEBRA", "ZESTY", "ZONED"
]
VALID_GUESSES = set(w.lower() for w in WORDS)  # Valid guesses come from the same list

# --- Styles ---
css = Style(f'''
    body, html {{ height: 100%; margin: 0; font-family: Arial, sans-serif; }}
    body {{ display: flex; flex-direction: column; align-items: center; background-color: #f4f4f4; }}
    header {{ padding: 20px; text-align: center; background-color: #333; color: white; width:100%;}}
    main {{ flex: 1 0 auto; padding: 20px; width: 100%; max-width: 500px; box-sizing: border-box; }}
    footer {{ flex-shrink: 0; padding: 10px; text-align: center; background-color: #333; color: white; width:100%; }}
    footer a {{ color: #9cf; }}

    .wordle-container {{ display: flex; flex-direction: column; align-items: center; gap: 20px; }}
    .guess-grid {{ display: grid; grid-template-rows: repeat({MAX_GUESSES}, auto); gap: 5px; margin-bottom: 20px; }}
    .guess-row {{ display: grid; grid-template-columns: repeat({WORD_LENGTH}, 1fr); gap: 5px; }}
    .letter-box {{
        width: 50px; height: 50px;
        border: 2px solid #d3d6da;
        display: flex; justify-content: center; align-items: center;
        font-size: 2rem; font-weight: bold; text-transform: uppercase;
        color: black;
    }}
    .letter-box.empty {{ background-color: white; }}
    .letter-box.gray {{ background-color: #787c7e; border-color: #787c7e; color: white; }}
    .letter-box.yellow {{ background-color: #c9b458; border-color: #c9b458; color: white; }}
    .letter-box.green {{ background-color: #6aaa64; border-color: #6aaa64; color: white; }}
    .letter-box.small {{
        width: 30px; height: 30px;
        font-size: 1rem;
    }}
    .used-letters {{
        display: flex; flex-direction: column;
        gap: 4px; align-items: center;
    }}
    .keyboard-row {{
        display: flex; gap: 4px; justify-content: center;
    }}

    .input-area form {{ display: flex; gap: 10px; margin-bottom: 10px; }}
    .input-area input[type="text"] {{
        padding: 10px; font-size: 1rem; width: 200px; text-transform: uppercase;
        border: 1px solid #ccc; border-radius: 4px;
    }}
    .input-area button {{
        padding: 10px 15px; font-size: 1rem; cursor: pointer;
        border: none; border-radius: 4px; background-color: #5cb85c; color: white;
    }}
    .message-area {{ min-height: 24px; font-size: 1rem; color: red; text-align: center; }}
    .controls button {{
        padding: 10px 15px; font-size: 1rem; cursor: pointer;
        border: none; border-radius: 4px; background-color: #007bff; color: white;
    }}
''')

app = FastHTML(hdrs=(picolink, css)) # Use picolink for icons and our CSS styles
rt = app.route

# --- Game State ---
game_state = {}

def choose_new_word():
    """Return a random word that matches the configured word length."""
    return random.choice(WORDS).lower()

def reset_game_state():
    global game_state
    game_state = {
        'target_word': choose_new_word(),
        'guesses': [], # list of strings
        'results': [], # list of lists of colors ('gray', 'yellow', 'green')
        'current_guess_str': "", # For direct input, not strictly necessary if form submits whole word
        'game_over': False,
        'win': False,
        'message': ""
    }
    print(f"New target word: {game_state['target_word']}") # For debugging

reset_game_state() # Initialize on load

# --- Game Logic ---
def evaluate_guess(guess: str, target: str) -> list[str]:
    if len(guess) != WORD_LENGTH or len(target) != WORD_LENGTH:
        return ["gray"] * WORD_LENGTH # Should not happen with validation

    result = [""] * WORD_LENGTH
    target_counts = {}
    for char in target:
        target_counts[char] = target_counts.get(char, 0) + 1

    # First pass: Green letters
    for i in range(WORD_LENGTH):
        if guess[i] == target[i]:
            result[i] = "green"
            target_counts[guess[i]] -= 1

    # Second pass: Yellow and Gray letters
    for i in range(WORD_LENGTH):
        if result[i] == "": # Not already green
            if guess[i] in target_counts and target_counts[guess[i]] > 0:
                result[i] = "yellow"
                target_counts[guess[i]] -= 1
            else:
                result[i] = "gray"
    return result

def get_used_letter_colors() -> dict[str, str]:
    """Return a mapping of guessed letters to their best achieved color."""
    priority = {"gray": 0, "yellow": 1, "green": 2}
    colors: dict[str, str] = {}
    for guess, result in zip(game_state['guesses'], game_state['results']):
        for ch, col in zip(guess, result):
            prev = colors.get(ch)
            if prev is None or priority[col] > priority[prev]:
                colors[ch] = col
    return colors

# --- UI Components ---
def UIGuessGrid():
    rows = []
    for i in range(MAX_GUESSES):
        letter_boxes = []
        if i < len(game_state['guesses']):
            guess_str = game_state['guesses'][i]
            guess_result = game_state['results'][i]
            for j in range(WORD_LENGTH):
                char = guess_str[j] if j < len(guess_str) else ""
                color_class = guess_result[j] if j < len(guess_result) else "empty"
                letter_boxes.append(Div(char, cls=f'letter-box {color_class}'))
        else:
            for _ in range(WORD_LENGTH):
                letter_boxes.append(Div(cls='letter-box empty'))
        rows.append(Div(*letter_boxes, cls='guess-row'))
    return Div(*rows, id='guess-grid', cls='guess-grid')

def UIInputArea():
    is_disabled = game_state['game_over']
    input_field = Input(
        type="text", name="guess_word", placeholder="Enter guess",
        maxlength=str(WORD_LENGTH), value="", # value is cleared by browser on successful htmx swap
        disabled=is_disabled,
        autofocus=True, # Add autofocus
        hx_on_input="this.value = this.value.toUpperCase()" # Force uppercase
    )
    submit_button = Button("Submit", type="submit", disabled=is_disabled)
    return Form(
        input_field, submit_button,
        hx_post="/guess", hx_target="#wordle-game-area", hx_swap="outerHTML",
        cls="input-area"
    )

def UIMessageArea():
    return Div(game_state['message'], id='message-area', cls='message-area')

def UIUsedLetters():
    colors = get_used_letter_colors()
    layout = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    rows = []
    for row_letters in layout:
        boxes = []
        for ch in row_letters:
            color = colors.get(ch, 'empty')
            boxes.append(Div(ch.upper(), cls=f'letter-box small {color}'))
        rows.append(Div(*boxes, cls='keyboard-row'))
    return Div(*rows, id='used-letters', cls='used-letters')

def UIControls():
    return Div(
        Form(
            Button("New Game", type="submit"),
            hx_post="/new_game", hx_target="#wordle-game-area", hx_swap="outerHTML"
        ),
        cls="controls"
    )

# This component will be the target for HTMX swaps to update the whole game area
def WordleGameArea():
    return Div(
        UIGuessGrid(),
        UIUsedLetters(),
        UIMessageArea(),
        UIInputArea(),
        UIControls(),
        id="wordle-game-area", # ID for HTMX targeting
        cls="wordle-container"
    )

# --- Main Page Structure ---
def HomePage():
    header = Header(H1("Wordle Clone"))
    main_content = Main(WordleGameArea()) # Initial render of the game area
    footer = Footer(P('Adapted from Game of Life example. Check out FastHTML ', AX('here', href='https://github.com/AnswerDotAI/fasthtml', target='_blank')))
    return Title('Wordle Clone'), header, main_content, footer

# --- Routes ---
@rt('/')
async def get_root():
    # `reset_game_state()` could be called here if you want a new word on every page refresh,
    # but typically Wordle games persist until explicitly reset or the session ends.
    # For simplicity, we only reset via the "New Game" button.
    return HomePage()

@rt('/guess', methods=['POST'])
async def post_guess(guess_word: str): # FastHTML automatically populates this from form data
    global game_state
    guess = guess_word.lower().strip()
    game_state['message'] = "" # Clear previous message

    if game_state['game_over']:
        game_state['message'] = "Game is over. Start a new game."
        return WordleGameArea()

    if len(guess) != WORD_LENGTH:
        game_state['message'] = f"Guess must be {WORD_LENGTH} letters long."
        return WordleGameArea()

    # For simplicity, we allow any 5-letter combination for now.
    # You could add validation against VALID_GUESSES here:
    # if guess not in VALID_GUESSES:
    #     game_state['message'] = "Not a valid word."
    #     return WordleGameArea()


    game_state['guesses'].append(guess)
    result = evaluate_guess(guess, game_state['target_word'])
    game_state['results'].append(result)

    if all(r == "green" for r in result):
        game_state['win'] = True
        game_state['game_over'] = True
        game_state['message'] = f"Congratulations! You guessed it: {game_state['target_word'].upper()}"
    elif len(game_state['guesses']) >= MAX_GUESSES:
        game_state['game_over'] = True
        game_state['message'] = f"Game Over. The word was: {game_state['target_word'].upper()}"

    return WordleGameArea() # Return the updated game area

@rt("/new_game", methods=['POST'])
async def post_new_game():
    reset_game_state()
    return WordleGameArea() # Return the fresh game area

# No background task or websockets needed for this version.
