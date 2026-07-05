import os
import re
import json
from gtts import gTTS

INDEX_HTML = 'index.html'
AUDIO_DIR = 'audio'

os.makedirs(AUDIO_DIR, exist_ok=True)

with open(INDEX_HTML, 'r', encoding='utf-8') as f:
    content = f.read()

word_pattern = r'\{en:\'([^\']+)\',cn:\'([^\']+)\'\}'
matches = re.findall(word_pattern, content)

unique_words = {}
for en, cn in matches:
    if en not in unique_words:
        unique_words[en] = cn

print(f'Found {len(unique_words)} unique words')

generated_count = 0
skipped_count = 0

for i, (en, cn) in enumerate(sorted(unique_words.items()), 1):
    audio_path = os.path.join(AUDIO_DIR, f'{en}.mp3')
    
    if os.path.exists(audio_path):
        skipped_count += 1
        continue
    
    try:
        tts = gTTS(text=en, lang='en', tld='us')
        tts.save(audio_path)
        generated_count += 1
        print(f'[{i}/{len(unique_words)}] Generated: {en}.mp3')
    except Exception as e:
        print(f'[{i}/{len(unique_words)}] Failed: {en} - {e}')

print(f'\nDone! Generated: {generated_count}, Skipped: {skipped_count}')

words_list = [{'en': en, 'cn': cn, 'audio': f'audio/{en}.mp3'} for en, cn in sorted(unique_words.items())]

with open('words_with_audio.json', 'w', encoding='utf-8') as f:
    json.dump(words_list, f, ensure_ascii=False, indent=2)

print('Saved words_with_audio.json')
