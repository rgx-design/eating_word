import requests
import json
import os
from urllib.parse import urlparse
import asyncio
from playwright.async_api import async_playwright

# StepFun API 配置
api_key = "a9okTRyAtAwCkFQP0lsI5J8HQpav2xEwKdLFAoVDo7ZxEqMPTnwj9YGog5oxYFmA"
api_base = "https://api.stepfun.com"

# 文生图请求参数 - 修改为新的提示词
prompt = "卡通风格 girl jumping"

# API 请求头
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# StepFun API 请求体
data = {
    "model": "step-image-edit-2",
    "prompt": prompt,
    "size": "1024x1024",
    "steps": 30,
    "cfg_scale": 1.0,
    "response_format": "url",
    "n": 4  # 生成4副图
}

async def download_image( playwright, url, filename ):
    """使用 Playwright 下载单个图片"""
    try:
        page = await playwright.context.new_page()
        await page.goto(url)
        # 等待页面加载
        await page.wait_for_timeout(2000)
        
        # 简单的保存逻辑：获取网页内容作为图片（如果是图片链接会自动下载）
        page_content = await page.content()
        
        # 如果直接是图片URL，可以尝试直接保存
        async with page.expect_download() as download_info:
            await page.goto(url)
        
        download = await download_info.value
        
        # 保存文件
        local_path = os.path.join("downloads", filename) 
        await download.save_as(local_path)
        print(f"✅ 图片已下载至: {local_path}")
        await page.close()
        return True
    except Exception as e:
        print(f"❌ 下载失败，错误：{e}")
        await playwright.context.close()
        return False

async def main():
    # 创建下载目录
    os.makedirs("downloads", exist_ok=True)
    
    # 发送 POST 请求到 StepFun 
    try:
        response = requests.post(f"{api_base}/v1/images/generations", headers=headers, json=data)
        
        # 检查响应
        if response.status_code == 200:
            result = response.json()
            print("🎉 StepFun 图像生成成功!")
            
            if 'data' in result and len(result['data']) > 0:
                urls = [item['url'] for item in result['data']]
                print(f"📋 已获取 {len(urls)} 张图片链接")
                
                # 使用 Playwright 下载所有图片
                async with async_playwright() as playwright:
                    tasks = []
                    for i, url in enumerate(urls):
                        filename = f"downloaded_image_{i+1}.png"
                        task = download_image(playwright, url, filename)
                        tasks.append(task)
                    
                    # 并发执行所有下载任务
                    await asyncio.gather(*tasks)
                    print("✅ 所有图片已下载完成!")
            else:
                print("❌ 未返回任何图像链接")
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求异常: {e}")
    except Exception as e:
        print(f"❌ 执行异常: {e}")

# 运行主程序
if __name__ == "__main__":
    # 这里使用 asyncio 来异步运行 main 函数
    import sys 
    if sys.version_info >= (3, 7):
        asyncio.run(main())
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())