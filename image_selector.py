from flask import Flask, render_template, jsonify, request, send_from_directory
import os
import re
import json

app = Flask(__name__)

INDEX_HTML = 'index.html'
IMAGES_DIR = 'word_images'
SELECTED_FILE = 'selected_images.json'

def extract_words():
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'en:\'([^\']+)\',cn:\'([^\']+)\'', content)
    words = []
    seen = set()
    for en, cn in matches:
        if en not in seen:
            seen.add(en)
            words.append({'en': en, 'cn': cn})
    return words

def load_selected():
    if os.path.exists(SELECTED_FILE):
        with open(SELECTED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_selected(selected):
    with open(SELECTED_FILE, 'w', encoding='utf-8') as f:
        json.dump(selected, f, ensure_ascii=False, indent=2)

def get_word_images(en):
    word_dir = os.path.join(IMAGES_DIR, en)
    images = []
    if os.path.exists(word_dir):
        for f in sorted(os.listdir(word_dir)):
            if f.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                images.append(f'word_images/{en}/{f}')
    return images

@app.route('/')
def index():
    words = extract_words()
    selected = load_selected()
    return render_template('selector.html', words=words, selected=selected)

def is_new_download(en):
    return en not in load_selected()

@app.route('/api/words')
def api_words():
    words = extract_words()
    selected = load_selected()
    result = []
    for word in words:
        images = get_word_images(word['en'])
        result.append({
            'en': word['en'],
            'cn': word['cn'],
            'images': images,
            'selected': selected.get(word['en'], ''),
            'is_new': word['en'] not in selected and len(images) > 0
        })
    return jsonify(result)

@app.route('/api/select', methods=['POST'])
def api_select():
    data = request.get_json()
    en = data.get('en')
    image = data.get('image')
    
    selected = load_selected()
    selected[en] = image
    save_selected(selected)
    
    words = extract_words()
    current_idx = next((i for i, w in enumerate(words) if w['en'] == en), -1)
    next_word = None
    if current_idx < len(words) - 1:
        next_word = words[current_idx + 1]
        next_word['images'] = get_word_images(next_word['en'])
        next_word['selected'] = selected.get(next_word['en'], '')
    
    return jsonify({
        'success': True,
        'next_word': next_word
    })

@app.route('/api/skip', methods=['POST'])
def api_skip():
    data = request.get_json()
    en = data.get('en')
    
    words = extract_words()
    current_idx = next((i for i, w in enumerate(words) if w['en'] == en), -1)
    next_word = None
    if current_idx < len(words) - 1:
        next_word = words[current_idx + 1]
        selected = load_selected()
        next_word['images'] = get_word_images(next_word['en'])
        next_word['selected'] = selected.get(next_word['en'], '')
    
    return jsonify({
        'success': True,
        'next_word': next_word
    })

@app.route('/api/stats')
def api_stats():
    words = extract_words()
    selected = load_selected()
    total = len(words)
    completed = len([w for w in words if selected.get(w['en'])])
    return jsonify({'total': total, 'completed': completed})

@app.route('/word_images/<path:filename>')
def serve_word_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
