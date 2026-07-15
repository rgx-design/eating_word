import requests
import json

# Minimax API 配置
api_key = "sk-api-xtc0ZN6sr2Ht4GVyrv6_4C0dpRIxtW50sml2wBZsN9Yb056plgtIhFPAKmIUJCYavQVAECBlMtduyeN4hC5DuLZzSKajoZIM7mxj_Jsdl4hJq5ID6fjoRxw"
api_base = "https://api.minimaxi.com"

# 文生图请求参数
prompt = "一个可爱的卡通风格的美食应用界面，展示各种美食图片和分类菜单"

# API 请求头
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 使用正确的模型名称
data = {
    "model": "image-01",  # 正确的模型名称
    "prompt": prompt,
    "image_count": 1,
    "size": "1024x1024"
}

# 发送 POST 请求
response = requests.post(f"{api_base}/v1/image_generation", headers=headers, data=json.dumps(data))

# 检查响应
if response.status_code == 200:
    result = response.json()
    print("生成成功!")
    print(json.dumps(result, indent=2, ensure_ascii=False))
else:
    print(f"请求失败，状态码: {response.status_code}")
    print(response.text)