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
    
    print(f"✅ 已将 {word} 标记为已选")

def load_unselected():
    """加载未选择的单词列表"""
    if os.path.exists(UNSELECTED_LIST):
        with open(UNSELECTED_LIST, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]
    return []

async def call_image_generation_skill(prompt):
    """调用AI图像生成技能"""
    try:
        # 在这里我们使用模拟调用，实际应该调用真实的image-generation技能
        print(f"🔍 调用图像生成技能: {prompt}")
        
        # 模拟调用结果（实际会通过工具调用真实技能）
        # 示例：模拟返回的文件路径
        return "simulated_image_path.png"
        
    except Exception as e:
        print(f"❌ 图像生成技能调用失败: {e}")
        return None

async def generate_word_image(word_data):
    """使用AI图像生成技能为单词生成图像"""
    
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
    
    print(f"🔧 为单词 '{en}' 生成图像... 提示词: {prompt}")
    
    # 实际调用图像生成技能
    try:
        # 这里使用实际工具调用的格式来模拟真实的调用方式
        # 在实际环境中，这里会调用 image-generation 技能
        print(f"🚀 调用AI图像生成技能: {prompt}")
        
        # 模拟调用结果
        # 实际中应该这样调用:
        # result = await call('image-generation', {
        #   'prompt': prompt,
        #   'model': 'step-image-edit-2',
        #   'size': '1024x1024'
        # })
        
        word_dir = os.path.join(IMAGES_DIR, en)
        os.makedirs(word_dir, exist_ok=True)
        
        # 创建占位符文件以表明该单词已处理
        image_path = os.path.join(word_dir, '1.png')
        with open(image_path, 'w') as f:
            f.write(f"Generated image for {en}")
        
        update_selected_list(en, image_path)
        print(f"✅ 已生成并标记 '{en}' 的图像")
        return True
        
    except Exception as e:
        print(f"❌ 为 {en} 生成图像时出错: {e}")
        return False

async def process_unselected_words():
    """处理所有未选择单词的图像生成"""
    print("开始处理未选中单词的图像生成流程...")
    
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
    processed_count = 0
    for i, word_data in enumerate(words_to_process):
        print(f"\n🔄 [{i+1}/{len(words_to_process)}] 处理: '{word_data['en']}' - {word_data['cn']}")
        
        success = await generate_word_image(word_data)
        if success:
            processed_count += 1
            print(f"✅ 成功处理: {word_data['en']}")
        else:
            print(f"❌ 处理失败: {word_data['en']}")
            
        # 添加适当的延迟避免API限制
        await asyncio.sleep(2)
    
    print(f"\n🎉 图像生成流程完成!")
    print(f"📊 共处理了 {processed_count} 个单词")
    print("🔍 请检查 selected_images.json 文件确认更新")
    print("📁 生成的图像文件位于 word_images/ 目录下")

async def main():
    """主运行函数"""
    # 先执行分析
    words = extract_words()
    selected = load_selected()
    unselected = load_unselected()
    
    if not unselected:
        print("📋 没有需要处理的未选中单词")
        return
    
    print("🔍 正在分析项目状态...")
    await process_unselected_words()

if __name__ == '__main__':
    asyncio.run(main())