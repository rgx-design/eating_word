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

# 基于文档 - 先尝试支持的模型列表中的一个
models = ["step-image-edit-2", "step-2x-large", "step-1x-medium"]

success = False
for model in models:
    data = {
        "model": model,
        "prompt": prompt,
        "size": "1024x1024",
        "steps": 50,
        "cfg_scale": 7.5,
        "response_format": "url",
        "n": 1
    }
    
    print(f"尝试使用模型: {model}")
    response = requests.post(f"{api_base}/v1/images/generations", headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        print("图像生成成功!")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        success = True
        break
    else:
        print(f"使用模型 {model} 失败，状态码: {response.status_code}")

if not success:
    print("\n所有模型都尝试失败，请重新确认以下内容：")
    print("1. API Key 是否有效（确认是否为个人账号的密钥）")
    print("2. 需要访问权限的模型列表：") 
    print("   - step-image-edit-2")
    print("   - step-2x-large")
    print("   - step-1x-medium")
    print("3. 注意查看 API 文档，确认是否需要额外认证或额度")