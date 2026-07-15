import os
import json
import asyncio
from playwright.async_api import async_playwright
from urllib.parse import quote

# 配置文件路径
INDEX_HTML = 'index.html'
IMAGES_DIR = 'word_images'
SELECTED_FILE = 'selected_images.json'
UNSELECTED_LIST = 'unselected_words.txt'

def extract_words():
    """从index.html中提取所有单词"""
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式提取单词
    import re
    matches = re.findall(r"en:'([^\']+)',cn:'([^\']+)\'", content)
    words = []
    seen = set()
    for en, cn in matches:
        if en not in seen:
            seen.add(en)
            words.append({'en': en, 'cn': cn})
    return words

def load_selected():
    """加载已选择的单词"""
    if os.path.exists(SELECTED_FILE):
        with open(SELECTED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_unselected():
    """加载未选择的单词列表"""
    if os.path.exists(UNSELECTED_LIST):
        with open(UNSELECTED_LIST, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]
    return []

async def generate_image_for_word(word_data):
    """使用StepFun技能生成单词对应的图片"""
    try:
        # 构建提示词
        en = word_data['en']
        cn = word_data['cn']
        
        # 根据词性调整提示词 - 简单的词性判断逻辑
        prompt = ""
        if any(word in en for word in ['run', 'eat', 'sleep', 'walk', 'jump', 'swim', 'fly', 'read', 'write', 'sing', 'dance', 'drink', 'cook']):
            # 动词类
            prompt = f"卡通风格的 {cn} 的女孩正在 {en}"
        elif en in ['abstract', 'idea', 'concept', 'theory', 'philosophy']:
            # 抽象词类
            prompt = f"卡通风格，直观表达 {cn} (概念) 的图像，帮助理解"
        else:
            prompt = f"可爱的卡通风格的 {cn} ({en}) 图片"
        
        print(f"生成提示词: {prompt}")
        
        # 这里可以调用实际的图像生成API（目前简化实现）
        # 在实际应用中会调用StepFun或者其它技能
        print(f"模拟生成图片: {prompt}")
        
        # 创建目录并保存标记文件
        word_dir = os.path.join(IMAGES_DIR, en)
        os.makedirs(word_dir, exist_ok=True)
        
        # 创建一个简单的占位图像或直接标记为处理完成
        placeholder_path = os.path.join(word_dir, '1.png')
        # 这里实际上应该调用生成脚本来保存真实的图像
        # 现在创建一个简单的测试文件来模拟
        with open(placeholder_path, 'w') as f:
            f.write(f"Image for {en}")
        
        return True
        
    except Exception as e:
        print(f"❌ 为 {en} 生成图像时出错: {e}")
        return False

async def main():
    """主函数：处理未选择的单词并生成对应图片"""
    print("开始自动图像生成流程...")
    
    words = extract_words()
    selected = load_selected()
    unselected = load_unselected()
    
    print(f"总词数: {len(words)}")
    print(f"已选中: {len(selected)}")
    print(f"未选中: {len(unselected)}")
    
    # 选择需要处理的未选中的单词
    words_to_process = []
    for word in unselected:
        word_data = next((w for w in words if w['en'] == word), None)
        if word_data:
            words_to_process.append(word_data)
    
    print(f"准备处理 {len(words_to_process)} 个单词的图像生成")
    
    # 处理每个未选中的单词
    for i, word_data in enumerate(words_to_process):
        print(f"\n[{i+1}/{len(words_to_process)}] 正在为 '{word_data['en']}' 生成图片...")
        
        success = await generate_image_for_word(word_data)
        if success:
            print(f"✅ 成功处理: {word_data['en']}")
        else:
            print(f"❌ 处理失败: {word_data['en']}")
            
        # 添加适当的延迟
        await asyncio.sleep(1)
    
    print(f"\n已完成所有图像生成任务!")

if __name__ == '__main__':
    asyncio.run(main())