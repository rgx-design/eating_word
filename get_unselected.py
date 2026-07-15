import os
import json

# Get all words from word_images directory
word_images_dir = "F:\\2fen\\eating_word\\word_images"
all_words = set()

if os.path.exists(word_images_dir):
    for item in os.listdir(word_images_dir):
        if os.path.isdir(os.path.join(word_images_dir, item)):
            all_words.add(item)

print(f"Total words in word_images: {len(all_words)}")

# Get selected words from JSON file
selected_file = "F:\\2fen\\eating_word\\selected_images.json"
selected_words = set()

if os.path.exists(selected_file):
    with open(selected_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            selected_words = set(data.keys())
            print(f"Selected words in JSON: {len(selected_words)}")
        except Exception as e:
            print(f"Error reading JSON: {e}")

# Find words not yet selected
unselected_words = all_words - selected_words

print(f"Unselected words: {len(unselected_words)}")

if unselected_words:
    print("\nFirst 20 unselected words:")
    for i, word in enumerate(sorted(list(unselected_words))[:20]):
        print(f"  {word}")
    
    # Write list of all unselected words to file
    with open("F:\\2fen\\eating_word\\unselected_words.txt", "w", encoding='utf-8') as f:
        for word in sorted(list(unselected_words)):
            f.write(word + "\n")
    
    print("\nList of all unselected words written to 'unselected_words.txt'")
else:
    print("All words have been selected!")

print(f"\nSummary:")
print(f"  Total words: {len(all_words)}")
print(f"  Selected: {len(selected_words)}")  
print(f"  Unselected: {len(unselected_words)}")