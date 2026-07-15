import requests
import json

# StepFun API 配置
api_key = "a9okTRyAtAwCkFQP0lsI5J8HQpav2xEwKdLFAoVDo7ZxEqMPTnwj9YGog5oxYFmA"
api_base = "https://api.stepfun.com"

# 文生图请求参数
prompt = "一个可爱的卡通风格的美食应用界面，展示各种美食图片和分类菜单"

# API 请求头
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# StepFun API 请求体 (使用已开通的模型)
data = {
    "model": "step-image-edit-2",
    "prompt": prompt,
    "size": "1024x1024",
    "steps": 30,
    "cfg_scale": 1.0,
    "response_format": "url"
}

# 发送 POST 请求到 StepFun 
try:
    response = requests.post(f"{api_base}/v1/images/generations", headers=headers, json=data, timeout=30)
    
    # 检查响应
    if response.status_code == 200:
        result = response.json()
        print("SUCCESS: StepFun 图像生成成功!")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 提取图片链接
        if 'data' in result and len(result['data']) > 0:
            image_url = result['data'][0].get('url')
            if image_url:
                print(f"\nLINK: 图片可访问链接:")
                print(image_url)
    else:
        print(f"FAILED: 请求失败，状态码: {response.status_code}")
        print("错误详情:")
        print(response.text)
        
except requests.exceptions.RequestException as e:
    print(f"NETWORK ERROR: 网络请求异常: {e}")
except Exception as e:
    print(f"EXECUTION ERROR: 执行异常: {e}")

print("\n--- 测试完成 ---")