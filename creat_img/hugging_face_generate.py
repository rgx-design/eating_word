import requests
import json
from PIL import Image
import io

# Hugging Face Inference API 配置
# 注意：需要申请免费的 API Token 用于访问
hf_api_token = "your-hf-api-token"  # 请替换为您的实际 token
api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

# 文生图请求参数
prompt = "一个可爱的卡通风格的美食应用界面，展示各种美食图片和分类菜单"

# API 请求头
headers = {
    "Authorization": f"Bearer {hf_api_token}",
    "Content-Type": "application/json"
}

# 请求体
data = {
    "inputs": prompt,
    "parameters": {
        "guidance_scale": 7.5,
        "num_inference_steps": 50
    }
}

# 发送 POST 请求
response = requests.post(api_url, headers=headers, json=data)

# 检查响应
if response.status_code == 200:
    # 如果返回的是图像数据（bytes）
    image_data = response.content
    
    # 尝试保存图像
    try:
        image = Image.open(io.BytesIO(image_data))
        image.save("generated_image_hf.png")
        print("图像已成功生成并保存为 generated_image_hf.png")
        print(f"图像尺寸: {image.size}")
    except Exception as e:
        print(f"保存图像时出错: {e}")
        # 如果无法识别为图像，显示原始内容
        print("响应内容:")
        print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
else:
    print(f"请求失败，状态码: {response.status_code}")
    print("错误详情:")
    print(response.text)