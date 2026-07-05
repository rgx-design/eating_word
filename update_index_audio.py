import re
import os

INDEX_HTML = 'index.html'
AUDIO_DIR = 'audio'

with open(INDEX_HTML, 'r', encoding='utf-8') as f:
    content = f.read()

audio_files = {f.replace('.mp3', '') for f in os.listdir(AUDIO_DIR) if f.endswith('.mp3')}

def add_audio_to_word(match):
    en = match.group(1)
    cn = match.group(2)
    if en in audio_files:
        return f"{{en:'{en}',cn:'{cn}',audio:'audio/{en}.mp3'}}"
    return match.group(0)

content = re.sub(r'\{en:\'([^\']+)\',cn:\'([^\']+)\'\}', add_audio_to_word, content)

with open(INDEX_HTML, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated index.html with audio paths')
