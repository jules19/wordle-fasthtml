import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import main


def test_evaluate_guess_all_correct():
    target = "abcde"
    guess = "abcde"
    expected = ["green"] * main.WORD_LENGTH
    assert main.evaluate_guess(guess, target) == expected


def test_evaluate_guess_present_letters():
    target = "abcde"
    guess = "eabcd"
    expected = ["yellow"] * main.WORD_LENGTH
    assert main.evaluate_guess(guess, target) == expected


def test_evaluate_guess_absent_letters():
    target = "abcde"
    guess = "fghij"
    expected = ["gray"] * main.WORD_LENGTH
    assert main.evaluate_guess(guess, target) == expected


def test_reset_game_state_sets_new_word_and_clears_guesses():
    main.game_state['guesses'] = ['old']
    main.game_state['results'] = [['gray'] * main.WORD_LENGTH]
    with patch('main.random.choice', return_value='abcde'):
        main.reset_game_state()
    assert main.game_state['target_word'] == 'abcde'
    assert main.game_state['guesses'] == []
    assert main.game_state['results'] == []
