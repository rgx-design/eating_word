import requests
import json
import os
from urllib.request import urlretrieve

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

# 创建下载目录
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)
print("Created/confirmed directory: " + download_dir)

# 发送 POST 请求到 StepFun 
try:
    response = requests.post(f"{api_base}/v1/images/generations", headers=headers, json=data, timeout=30)
    
    # 检查响应
    if response.status_code == 200:
        result = response.json()
        print("SUCCESS: StepFun 图像生成成功!")
        
        if 'data' in result and len(result['data']) > 0:
            urls = [item['url'] for item in result['data']]
            print("Got " + str(len(urls)) + " image links")
            
            # 下载所有图像
            for i, url in enumerate(urls):
                try:
                    filename = "downloaded_image_" + str(i+1) + ".png"
                    full_path = os.path.join(download_dir, filename)
                    print("Downloading: " + filename)
                    
                    # 使用urllib直接下载
                    urlretrieve(url, full_path)
                    print("Download complete: " + full_path)
                    
                except Exception as e:
                    print("Save failed " + filename + ": " + str(e))
                    
        else:
            print("No image links returned")
    else:
        print("Request failed, status code: " + str(response.status_code))
        print(response.text)
        
except requests.exceptions.RequestException as e:
    print("Network request exception: " + str(e))
except Exception as e:
    print("Execution exception: " + str(e))

print("\n--- Download task finished ---")