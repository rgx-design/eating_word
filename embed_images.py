import os
import json
import base64

IMAGE_DIR = 'selected_images'
INDEX_FILE = os.path.join(IMAGE_DIR, 'index.json')
INDEX_HTML = 'index.html'

def main():
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        selected = json.load(f)
    
    print(f'Processing {len(selected)} words...')
    
    image_data = {}
    total_size = 0
    
    for word, _ in selected.items():
        img_path = os.path.join(IMAGE_DIR, word, '1.png')
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                img_bytes = f.read()
                total_size += len(img_bytes)
                img_b64 = base64.b64encode(img_bytes).decode('utf-8')
                image_data[word] = f'data:image/png;base64,{img_b64}'
            print(f'  {word}: {len(img_bytes)/1024:.1f} KB')
        else:
            print(f'  ⚠️ {word}: file not found')
    
    print(f'\nTotal embedded size: {total_size/1024/1024:.2f} MB')
    
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        html = f.read()
    
    old_map_start = '// ==================== WORD IMAGE MAP ===================='
    old_map_end = 'const IMAGE_BASE_URL'
    
    start_idx = html.find(old_map_start)
    end_idx = html.find(old_map_end, start_idx)
    
    if start_idx == -1 or end_idx == -1:
        print('Error: Could not find WORD_IMAGE_MAP section')
        return
    
    new_section = f'{old_map_start}\n// Embedded image data (base64)\nconst IMAGE_DATA = {json.dumps(image_data, ensure_ascii=False)};\n'
    
    html = html[:start_idx] + new_section + html[end_idx:]
    
    html = html.replace('const IMAGE_BASE_URL = \'https://raw.githubusercontent.com/wange2024/eating_word/master/selected_images/\';', '')
    
    with open(INDEX_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print('index.html updated successfully!')

if __name__ == '__main__':
    main()
