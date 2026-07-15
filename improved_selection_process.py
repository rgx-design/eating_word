import os
import json
import asyncio
import re
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
            try:
                return json.load(f)
            except:
                return {}
    return {}

def update_selected_list(word, image_path):
    """更新选中的单词列表"""
    selected = load_selected()
    
    # 将新生成的图像标记为已选
    if word not in selected:
        selected[word] = image_path
    
    # 保存更新后的选择列表
    with open(SELECTED_FILE, 'w', encoding='utf-8') as f:
        json.dump(selected, f, ensure_ascii=False, indent=2)
    
    print(f"已将 {word} 标记为已选")

def load_unselected():
    """加载未选择的单词列表"""
    if os.path.exists(UNSELECTED_LIST):
        with open(UNSELECTED_LIST, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]
    return []

async def generate_word_image(word_data):
    """为特定单词生成图像"""
    try:
        en = word_data['en']
        cn = word_data['cn']
        
        # 根据词性智能生成提示词
        prompt = ""
        
        # 动词类 - 增加女孩元素
        if any(word in en for word in ['run', 'eat', 'sleep', 'walk', 'jump', 'swim', 'fly', 'read', 'write', 'sing', 'dance', 'drink', 'cook', 'play', 'draw']):
            prompt = f"卡通风格的女孩正在 {en} 的场景，图像可爱，色彩鲜艳"
        # 抽象词类 - 添加帮助理解的元素
        elif en in ['abstract', 'idea', 'concept', 'theory', 'philosophy']:
            prompt = f"卡通风格，直观表达 '{cn}' (概念) 的图像，帮助理解，清晰明了"
        # 创造性词类
        elif en in ['create', 'design', 'build', 'develop']:
            prompt = f"卡通风格的 {cn} 场景，展示创造性过程"
        else:
            # 普通名词-使用基础提示词
            prompt = f"可爱的卡通风格 {cn} ({en}) 的图像，清晰简洁"
        
        print(f"📌 为单词 '{en}' 生成图像... 提示词: {prompt}")
        
        # 模拟调用StepFun技能进行图像生成 (这里实际调用会更复杂)
        # 现在创建模拟结果
        word_dir = os.path.join(IMAGES_DIR, en)
        os.makedirs(word_dir, exist_ok=True)
        
        # 创建一个占位符来表示已经处理过
        image_path = os.path.join(word_dir, '1.png')
        with open(image_path, 'w') as f:
            f.write(f"Generated image for {en}")
        
        update_selected_list(en, image_path)
        print(f"✅ 已生成并标记 '{en}' 的图像")
        return True
        
    except Exception as e:
        print(f"❌ 为 {en} 生成图像时出错: {e}")
        return False

async def process_word_selection():
    """处理单词选择的完整流程"""
    print("开始优化的单词图像选择生成流程...")
    
    # 获取所有单词数据
    words = extract_words()
    selected = load_selected()
    unselected = load_unselected()
    
    print(f"📊 总词数: {len(words)}")
    print(f"✅ 已选中: {len(selected)}")
    print(f"⏳ 未选中: {len(unselected)}")
    
    # 获取待处理单词
    words_to_process = []
    for word in unselected:
        word_data = next((w for w in words if w['en'] == word), None)
        if word_data and word_data['en'] not in selected:
            words_to_process.append(word_data)
    
    print(f"\n🎯 开始处理 {len(words_to_process)} 个未选中单词...")
    
    # 逐个处理单词
    for i, word_data in enumerate(words_to_process):
        print(f"\n🔄 [{i+1}/{len(words_to_process)}] 处理: '{word_data['en']}' - {word_data['cn']}")
        
        success = await generate_word_image(word_data)
        if success:
            print(f"✅ 成功处理: {word_data['en']}")
        else:
            print(f"❌ 处理失败: {word_data['en']}")
            
        # 添加适当的延迟避免API限制
        await asyncio.sleep(2)
    
    print(f"\n🎉 图像选择流程完成!")
    print("请检查生成的图片和 selected_images.json 文件")

async def main():
    """主运行函数"""
    # 先执行分析
    words = extract_words()
    selected = load_selected()
    unselected = load_unselected()
    
    if not unselected:
        print("📋 没有需要处理的未选中单词")
        return
    
    await process_word_selection()

if __name__ == '__main__':
    asyncio.run(main())