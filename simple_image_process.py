import os
import json
import asyncio
import re

# 设置正确的项目路径
PROJECT_DIR = 'F:/2fen/eating_word'
INDEX_HTML = os.path.join(PROJECT_DIR, 'index.html')
IMAGES_DIR = os.path.join(PROJECT_DIR, 'word_images')
SELECTED_FILE = os.path.join(PROJECT_DIR, 'selected_images.json')
UNSELECTED_LIST = os.path.join(PROJECT_DIR, 'unselected_words.txt')

def extract_words():
    """从index.html中提取所有单词"""
    try:
        with open(INDEX_HTML, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则表达式提取单词
        matches = re.findall(r"en:'([^\']+)',cn:'([^\']+)\'", content)
        words = []
        seen = set()
        for en, cn in matches:
            if en not in seen:
                seen.add(en)
                words.append({'en': en, 'cn': cn})
        return words
    except Exception as e:
        print(f"Error reading index.html: {e}")
        return []

def load_selected():
    """加载已选择的单词"""
    try:
        if os.path.exists(SELECTED_FILE):
            with open(SELECTED_FILE, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except:
                    return {}
        return {}
    except Exception as e:
        print(f"Error loading selected_words.json: {e}")
        return {}

def update_selected_list(word, image_path):
    """更新选中的单词列表"""
    selected = load_selected()
    
    # 将新生成的图像标记为已选
    if word not in selected:
        selected[word] = image_path
    
    # 保存更新后的选择列表
    try:
        with open(SELECTED_FILE, 'w', encoding='utf-8') as f:
            json.dump(selected, f, ensure_ascii=False, indent=2)
        print(f"Updated {word} to selected list")
    except Exception as e:
        print(f"Error updating selected list: {e}")

def load_unselected():
    """加载未选择的单词列表"""
    try:
        if os.path.exists(UNSELECTED_LIST):
            with open(UNSELECTED_LIST, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f.readlines()]
        return []
    except Exception as e:
        print(f"Error loading unselected list: {e}")
        return []

async def generate_word_image(word_data):
    """模拟为单词生成图像"""
    
    en = word_data['en']
    cn = word_data['cn']
    
    # 根据词性智能生成提示词
    prompt = ""
    
    # 动词类 - 增加女孩元素
    if any(word in en for word in ['run', 'eat', 'sleep', 'walk', 'jump', 'swim', 'fly', 'read', 'write', 'sing', 'dance', 'drink', 'cook', 'play', 'draw']):
        prompt = f"卡通风格的可爱女孩正在 {en} 的场景，鲜艳色彩，清晰图像，适合儿童学习应用"
    # 抽象词类 - 添加帮助理解的元素
    elif en in ['abstract', 'idea', 'concept', 'theory', 'philosophy', 'knowledge', 'understanding']:
        prompt = f"卡通风格的动画概念图，直观表达 '{cn}' 的含义，视觉化抽象概念，适用于教育应用"
    # 创造性词类
    elif en in ['create', 'design', 'build', 'develop', 'innovate', 'imagine']:
        prompt = f"卡通风格的创造过程场景，展示 {cn} 的创造活动，积极向上的情感表达"
    # 普通名词类
    else:
        prompt = f"可爱的卡通风格 {cn} ({en}) 图片，清晰明了，适合儿童英语学习应用"
    
    print(f"Generating image for word '{en}' with prompt: {prompt}")
    
    # 模拟调用图像生成技能 (这里只是模拟)
    try:
        word_dir = os.path.join(IMAGES_DIR, en)
        os.makedirs(word_dir, exist_ok=True)
        
        # 创建占位符文件以表明该单词已处理
        image_path = os.path.join(word_dir, '1.png')
        with open(image_path, 'w') as f:
            f.write(f"Generated image for {en}")
        
        update_selected_list(en, image_path)
        print(f"Successfully generated and marked '{en}'")
        return True
        
    except Exception as e:
        print(f"Error generating image for {en}: {e}")
        return False

async def process_unselected_words():
    """处理所有未选择单词的图像生成"""
    print("Starting unselected words image generation...")
    
    # 获取所有单词数据
    words = extract_words()
    selected = load_selected()
    unselected = load_unselected()
    
    print(f"Total words: {len(words)}")
    print(f"Selected words: {len(selected)}")
    print(f"Unselected words: {len(unselected)}")
    
    # 获取待处理单词
    words_to_process = []
    for word in unselected:
        word_data = next((w for w in words if w['en'] == word), None)
        if word_data and word_data['en'] not in selected:
            words_to_process.append(word_data)
    
    print(f"Processing {len(words_to_process)} unselected words...")
    
    # 逐个处理单词
    processed_count = 0
    for i, word_data in enumerate(words_to_process):
        print(f"\nProcessing [{i+1}/{len(words_to_process)}]: '{word_data['en']}' - {word_data['cn']}")
        
        success = await generate_word_image(word_data)
        if success:
            processed_count += 1
            print(f"Successfully processed: {word_data['en']}")
        else:
            print(f"Failed processing: {word_data['en']}")
            
        # 添加适当的延迟避免API限制
        await asyncio.sleep(1)
    
    print(f"\nImage generation process complete!")
    print(f"Total processed: {processed_count} words")

async def main():
    """主运行函数"""
    # 先执行分析
    words = extract_words()
    selected = load_selected()
    unselected = load_unselected()
    
    if not unselected:
        print("No unselected words to process")
        return
    
    await process_unselected_words()

if __name__ == '__main__':
    asyncio.run(main())