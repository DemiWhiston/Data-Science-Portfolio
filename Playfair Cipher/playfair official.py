
def clean_keyword(keyword: str) -> str:
    keyword = keyword.upper().replace('J', 'I')
    keyword = ''.join(ch for ch in keyword if ch.isalpha())
    seen = set()
    cleaned = []
    for ch in keyword:
        if ch not in seen:
            seen.add(ch)
            cleaned.append(ch)
    return ''.join(cleaned)

def build_grid(cleaned_keyword: str) -> list:
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # J excluded
    letters = list(cleaned_keyword)
    for ch in alphabet:
        if ch not in letters:
            letters.append(ch)
    grid = [letters[i:i+5] for i in range(0, 25, 5)]
    return grid

def clean_message(message: str) -> str:
    message = message.upper().replace(" ", "").replace("J", "I")
    message = ''.join(ch for ch in message if ch.isalpha())  # Remove non-letters
    return message

def separate_repeats(text: str) -> str:
    result = []
    for i in range(len(text)):
        result.append(text[i])
        if i < len(text) - 1 and text[i] == text[i + 1]:
            result.append('Z' if text[i] == 'X' else 'X')
    return ''.join(result)

def pad_message(text: str) -> str:
    if len(text) % 2 != 0:
        text += 'Z' if text[-1] == 'X' else 'X'
    return text

def split_pairs(text: str) -> list:
    return [text[i:i+2] for i in range(0, len(text), 2)]

def prepare_playfair(keyword: str, message: str):
    cleaned_kw = clean_keyword(keyword)
    grid = build_grid(cleaned_kw)
    cleaned_msg = clean_message(message)
    separated_msg = separate_repeats(cleaned_msg)
    padded_msg = pad_message(separated_msg)
    pairs = split_pairs(padded_msg)
    return cleaned_kw, grid, padded_msg, pairs

def main():
    # Ask user for keyword and message
    keyword = input("Enter keyword: ")
    message = input("Enter message: ")

    # Prepare Playfair components
    cleaned_kw, grid, final_msg, pairs = prepare_playfair(keyword, message)

    # Print results
    print("\nCleaned Keyword:", cleaned_kw)
    print("\n5x5 Grid:")
    for row in grid:
        print(" ".join(row))
    print("\nPrepared Message:", final_msg)
    print("Pairs:", pairs)

# Run main
if __name__ == "__main__":
    main()
# %%
