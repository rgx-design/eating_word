import os
import json
import shutil

SELECTED_FILE = 'selected_images.json'
IMAGES_DIR = 'word_images'
PUBLISH_DIR = 'selected_images'

def main():
    with open(SELECTED_FILE, 'r', encoding='utf-8') as f:
        selected = json.load(f)
    
    print(f'已选择 {len(selected)} 个单词')
    
    if os.path.exists(PUBLISH_DIR):
        shutil.rmtree(PUBLISH_DIR)
    os.makedirs(PUBLISH_DIR)
    
    total_size = 0
    for en, image_path in selected.items():
        src = image_path
        word_dir = os.path.join(PUBLISH_DIR, en)
        os.makedirs(word_dir, exist_ok=True)
        
        dst = os.path.join(word_dir, '1.png')
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            size = os.path.getsize(dst)
            total_size += size
            print(f'  {en}: {size/1024:.1f} KB')
        else:
            print(f'  ⚠️ {en}: 源文件不存在')
    
    print(f'\n总大小: {total_size/1024/1024:.2f} MB')
    print(f'发布目录: {PUBLISH_DIR}')
    
    with open(os.path.join(PUBLISH_DIR, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(selected, f, ensure_ascii=False, indent=2)
    
    print('已生成 index.json')

if __name__ == '__main__':
    main()