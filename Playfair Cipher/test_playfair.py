
"""
Playfair Cipher Preparation, Encryption, Decryption + Test Suite (Single Module)

Usage:
  - Interactive mode (grid + pairs):
      python playfair_module.py

  - Run tests:
      python playfair_module.py --test
"""

from typing import List, Tuple

# =========================
# Core Playfair Functions
# =========================

def clean_keyword(keyword: str) -> str:
    """
    Uppercase, replace J->I, remove non-letters, and deduplicate while keeping order.
    """
    keyword = keyword.upper().replace('J', 'I')
    keyword = ''.join(ch for ch in keyword if ch.isalpha())
    seen = set()
    cleaned = []
    for ch in keyword:
        if ch not in seen:
            seen.add(ch)
            cleaned.append(ch)
    return ''.join(cleaned)

def build_grid(cleaned_keyword: str) -> List[List[str]]:
    """
    Build a 5×5 grid using the cleaned keyword, followed by remaining alphabet letters (no J).
    """
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # J excluded
    letters = list(cleaned_keyword)
    for ch in alphabet:
        if ch not in letters:
            letters.append(ch)
    return [letters[i:i+5] for i in range(0, 25, 5)]

def clean_message(message: str) -> str:
    """
    Uppercase, remove spaces and non-letters, replace J->I.
    """
    message = message.upper().replace(" ", "").replace("J", "I")
    return ''.join(ch for ch in message if ch.isalpha())

def separate_repeats(text: str) -> str:
    """
    When two identical letters are side-by-side, insert X unless the letter is X, then insert Z.
    Example: HELLO -> HELXLO ; XXY -> XZXZY
    """
    result = []
    for i in range(len(text)):
        result.append(text[i])
        if i < len(text) - 1 and text[i] == text[i + 1]:
            result.append('Z' if text[i] == 'X' else 'X')
    return ''.join(result)

def pad_message(text: str) -> str:
    """
    If final length is odd → add X unless final letter is X → then add Z.
    """
    if len(text) % 2 != 0:
        text += 'Z' if text[-1] == 'X' else 'X'
    return text

def split_pairs(text: str) -> List[str]:
    """
    Split final prepared text into digraphs (pairs).
    Example: HELXLO -> ["HE", "LX", "LO"]
    """
    return [text[i:i+2] for i in range(0, len(text), 2)]

def prepare_playfair(keyword: str, message: str) -> Tuple[str, List[List[str]], str, List[str]]:
    """
    Full preparation pipeline: clean keyword, grid, clean+separate+pad message, split pairs.
    """
    cleaned_kw = clean_keyword(keyword)
    grid = build_grid(cleaned_kw)
    cleaned_msg = clean_message(message)
    separated_msg = separate_repeats(cleaned_msg)
    padded_msg = pad_message(separated_msg)
    pairs = split_pairs(padded_msg)
    return cleaned_kw, grid, padded_msg, pairs

# =========================
# Encryption / Decryption
# =========================

def find_position(grid: List[List[str]], letter: str) -> Tuple[int, int]:
    for r, row in enumerate(grid):
        if letter in row:
            return r, row.index(letter)
    raise ValueError(f"Letter {letter} not found in grid.")

def encrypt_pair(pair: str, grid: List[List[str]]) -> str:
    r1, c1 = find_position(grid, pair[0])
    r2, c2 = find_position(grid, pair[1])
    if r1 == r2:  # same row
        return grid[r1][(c1 + 1) % 5] + grid[r2][(c2 + 1) % 5]
    if c1 == c2:  # same column
        return grid[(r1 + 1) % 5][c1] + grid[(r2 + 1) % 5][c2]
    # rectangle
    return grid[r1][c2] + grid[r2][c1]

def decrypt_pair(pair: str, grid: List[List[str]]) -> str:
    r1, c1 = find_position(grid, pair[0])
    r2, c2 = find_position(grid, pair[1])
    if r1 == r2:  # same row
        return grid[r1][(c1 - 1) % 5] + grid[r2][(c2 - 1) % 5]
    if c1 == c2:  # same column
        return grid[(r1 - 1) % 5][c1] + grid[(r2 - 1) % 5][c2]
    # rectangle
    return grid[r1][c2] + grid[r2][c1]

def playfair_encrypt(keyword: str, message: str) -> Tuple[str, List[List[str]], str, List[str], str]:
    """
    Return: cleaned_keyword, grid, prepared_msg, pairs, encrypted_text
    """
    cleaned_kw, grid, prepared_msg, pairs = prepare_playfair(keyword, message)
    encrypted = ''.join(encrypt_pair(pair, grid) for pair in pairs)
    return cleaned_kw, grid, prepared_msg, pairs, encrypted

def remove_fillers(text: str) -> str:
    """
    Remove filler X/Z inserted between duplicates and a trailing X (odd-length padding).
    Heuristic: drop X/Z that sit between identical letters (A X A → AA or A Z A → AA).
    Also remove a trailing X that was likely added for padding.
    """
    cleaned = []
    for i, ch in enumerate(text):
        if ch in ('X', 'Z'):
            if i > 0 and i < len(text) - 1 and text[i-1] == text[i+1]:
                continue
        cleaned.append(ch)
    # Drop terminal padding X (if present).
    if cleaned and cleaned[-1] == 'X':
        cleaned.pop()
    return ''.join(cleaned)

def playfair_decrypt(keyword: str, encrypted_text: str) -> str:
    """
    Decrypt and then post-process to remove likely filler characters (X/Z).
    """
    cleaned_kw = clean_keyword(keyword)
    grid = build_grid(cleaned_kw)
    pairs = split_pairs(encrypted_text)
    decrypted_raw = ''.join(decrypt_pair(pair, grid) for pair in pairs)
    return remove_fillers(decrypted_raw)

# =========================
# Optional Interactive Main
# =========================

def pretty_print_grid(grid: List[List[str]]) -> None:
    for row in grid:
        print(' '.join(row))

def main():
    keyword = input("Enter keyword: ")
    message = input("Enter message: ")
    cleaned_kw, grid, prepared_msg, pairs = prepare_playfair(keyword, message)
    print("\nCleaned Keyword:", cleaned_kw)
    print("\n5×5 Grid:")
    pretty_print_grid(grid)
    print("\nPrepared Message:", prepared_msg)
    print("Pairs:", pairs)

# =========================
# Test Suite (unittest)
# =========================

import unittest

class TestPlayfairModule(unittest.TestCase):

    # --- Grid and keyword cleaning ---
    def test_keyword_dedup_and_nonletters(self):
        kw = clean_keyword("K!E!Y!K")
        self.assertEqual(kw, "KEY")
        grid = build_grid(kw)
        self.assertEqual(len(grid), 5)
        self.assertTrue(all(len(row) == 5 for row in grid))
        # J must be excluded
        flat = ''.join(''.join(row) for row in grid)
        self.assertNotIn('J', flat)

    def test_j_to_i_in_message(self):
        msg = clean_message("JIG")
        self.assertEqual(msg, "IIG")  # J -> I, uppercase

    # --- Repeat handling and padding ---
    def test_separate_repeats_hello(self):
        prepared = separate_repeats("HELLO")
        self.assertEqual(prepared, "HELXLO")
        pairs = split_pairs(pad_message(prepared))
        self.assertEqual(pairs, ["HE", "LX", "LO"])

    def test_separate_repeats_x_to_z(self):
        # XXY -> XZXZY ; odd length -> pad with X (last char Y != X) => XZXZYX
        prepared = separate_repeats("XXY")
        self.assertEqual(prepared, "XZXZY")
        padded = pad_message(prepared)
        self.assertEqual(padded, "XZXZYX")
        pairs = split_pairs(padded)
        self.assertEqual(pairs, ["XZ", "XZ", "YX"])

    def test_padding_odd_length_not_x(self):
        # HEL (3) -> HELX
        padded = pad_message("HEL")
        self.assertEqual(padded, "HELX")

    def test_padding_odd_length_last_is_x(self):
        # ABX (3) -> ABXZ
        padded = pad_message("ABX")
        self.assertEqual(padded, "ABXZ")
        self.assertEqual(split_pairs(padded), ["AB", "XZ"])

    def test_no_padding_when_even(self):
        # Even length: none added even if ending with X
        padded = pad_message("ABCDX")  # length 5 → odd -> should pad
        self.assertEqual(padded, "ABCDXZ")  # last is X -> add Z
        padded_even = pad_message("ABCD")   # length 4 → even -> unchanged
        self.assertEqual(padded_even, "ABCD")

    def test_empty_message(self):
        _, _, prepared, pairs = prepare_playfair("KEY", "")
        self.assertEqual(prepared, "")
        self.assertEqual(pairs, [])

    def test_single_letter_message(self):
        _, _, prepared, pairs = prepare_playfair("KEY", "A")
        self.assertEqual(prepared, "AX")
        self.assertEqual(pairs, ["AX"])

    # --- Pairs correctness ---
    def test_exact_pairs_sequence(self):
        _, _, prepared, pairs = prepare_playfair("KEY", "HELLO")
        self.assertEqual(prepared, "HELXLO")
        self.assertEqual(pairs, ["HE", "LX", "LO"])

    # --- Encryption / Decryption round-trip ---
    def test_encrypt_decrypt_basic(self):
        keyword = "Jungle123!"
        message = "Just a simple message"
        cleaned_kw, grid, prepared, pairs, encrypted = playfair_encrypt(keyword, message)
        self.assertEqual(cleaned_kw, "UNGLEI")
        self.assertTrue(all(len(p) == 2 for p in pairs))
        decrypted = playfair_decrypt(keyword, encrypted)
        # After filler removal, should match the cleaned message (J->I, no spaces, letters only)
        self.assertEqual(decrypted, clean_message(message))

    def test_decrypt_removes_fillers_between_duplicates(self):
        # Construct a case with duplicate handling
        keyword = "KEYWORD"
        message = "BALLOON"
        _, _, prepared, _, encrypted = playfair_encrypt(keyword, message)
        decrypted = playfair_decrypt(keyword, encrypted)
        # After filler removal, expect original cleaned message (J->I is irrelevant here)
        self.assertEqual(decrypted, clean_message(message))

    def test_decrypt_trailing_padding_x_removed(self):
        keyword = "KEY"
        # Odd-length case without ending in X: should add X padding, later removed
        message = "ABC"
        _, _, prepared, _, encrypted = playfair_encrypt(keyword, message)
        decrypted = playfair_decrypt(keyword, encrypted)
        self.assertEqual(decrypted, clean_message(message))

# Entry point
if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        # Run the test suite
        unittest.main(argv=['first-arg-is-ignored'])
    else:
        # Interactive grid + pairs
        main()

