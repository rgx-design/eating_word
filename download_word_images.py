import os
import re
import json
import asyncio
from playwright.async_api import async_playwright
from urllib.parse import quote

INDEX_HTML = 'index.html'
IMAGES_DIR = 'word_images'
PROGRESS_FILE = 'image_download_progress.json'

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

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

async def download_images_for_word(page, en, cn, progress, max_images=4):
    word_dir = os.path.join(IMAGES_DIR, en)
    os.makedirs(word_dir, exist_ok=True)
    
    existing = len([f for f in os.listdir(word_dir) if f.endswith('.png')])
    if existing >= max_images:
        print(f'  ✓ Already has {existing} images, skipping')
        progress[en] = {'status': 'done', 'count': existing}
        return
    
    search_query = f'{en} {cn} cartoon illustration clipart cute'
    encoded_query = quote(search_query)
    
    try:
        await page.goto(f'https://duckduckgo.com/?q={encoded_query}&iax=images&ia=images', timeout=30000)
        await page.wait_for_load_state('networkidle', timeout=20000)
        await page.wait_for_timeout(3000)
        
        img_elements = await page.query_selector_all('img')
        downloaded = 0
        seen_urls = set()
        
        for idx, img in enumerate(img_elements):
            if downloaded >= max_images:
                break
            
            try:
                src = await img.get_attribute('src')
                if not src or src.startswith('data:') or '.ico' in src.lower():
                    continue
                
                if src in seen_urls:
                    continue
                seen_urls.add(src)
                
                await img.scroll_into_view_if_needed()
                await page.wait_for_timeout(500)
                
                bbox = await img.bounding_box()
                if not bbox or bbox['width'] < 50 or bbox['height'] < 50:
                    continue
                
                clip = {
                    'x': bbox['x'],
                    'y': bbox['y'],
                    'width': bbox['width'],
                    'height': bbox['height']
                }
                
                filename = os.path.join(word_dir, f'{downloaded + 1}.png')
                await page.screenshot(path=filename, clip=clip)
                downloaded += 1
                print(f'    Downloaded: {filename}')
                
            except Exception as e:
                continue
        
        progress[en] = {'status': 'done', 'count': downloaded}
        print(f'  ✅ Downloaded {downloaded} images for {en}')
        
    except Exception as e:
        progress[en] = {'status': 'failed', 'error': str(e)}
        print(f'  ❌ Failed for {en}: {e}')
    
    await page.wait_for_timeout(800)

async def main():
    words = extract_words()
    progress = load_progress()
    
    print(f'Total words: {len(words)}')
    print(f'Already processed: {sum(1 for v in progress.values() if v.get("status") == "done")}')
    
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    p = None
    browser = None
    page = None
    
    for i, word in enumerate(words):
        en = word['en']
        cn = word['cn']
        
        if progress.get(en, {}).get('status') == 'done':
            continue
        
        if not browser or not page:
            print('\n🔄 Reconnecting browser...')
            try:
                if p:
                    await p.stop()
                p = await async_playwright().start()
                browser = await p.chromium.launch(headless=False, timeout=30000)
                page = await browser.new_page(viewport={'width': 1280, 'height': 800})
                print('✅ Browser connected')
            except Exception as e:
                print(f'❌ Failed to connect browser: {e}')
                await asyncio.sleep(10)
                continue
        
        print(f'\n[{i+1}/{len(words)}] Processing: {en} - {cn}')
        
        try:
            await download_images_for_word(page, en, cn, progress)
        except Exception as e:
            print(f'  ❌ Error: {e}')
            try:
                await browser.close()
            except:
                pass
            browser = None
            page = None
            await asyncio.sleep(5)
        
        save_progress(progress)
    
    if browser:
        try:
            await browser.close()
        except:
            pass
    if p:
        try:
            await p.stop()
        except:
            pass

if __name__ == '__main__':
    asyncio.run(main())