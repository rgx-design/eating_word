import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        
        await page.goto('https://duckduckgo.com/?q=cat%20cartoon%20illustration&iax=images&ia=images', timeout=30000)
        await page.wait_for_load_state('networkidle', timeout=20000)
        await page.wait_for_timeout(3000)
        
        await page.keyboard.press('End')
        await page.wait_for_timeout(2000)
        
        img_elements = await page.query_selector_all('img')
        print(f'Total img elements: {len(img_elements)}')
        
        for i, img in enumerate(img_elements[:10]):
            try:
                src = await img.get_attribute('src')
                bbox = await img.bounding_box()
                
                if '.ico' in src.lower():
                    continue
                
                print(f'\n[{i}]')
                print(f'  src: {src[:150] if src else "None"}')
                print(f'  bbox: {bbox}')
                
                if bbox and bbox['width'] >= 50 and bbox['height'] >= 50:
                    clip = {
                        'x': bbox['x'],
                        'y': bbox['y'],
                        'width': bbox['width'],
                        'height': bbox['height']
                    }
                    filename = f'test_{i}.png'
                    print(f'  Trying to save: {filename}')
                    await img.screenshot(path=filename, clip=clip)
                    print(f'  ✅ Saved!')
                    
            except Exception as e:
                print(f'  ❌ Error: {e}')
        
        await page.wait_for_timeout(3000)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())