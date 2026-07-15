# 文生图生成 Skill

## 概述
此技能提供文生图像生成功能，支持通过StepFun API进行图像创建。用户可以指定文本提示词来生成对应的图像内容。

## 功能特性
- 支持文本到图像的生成（Text-to-Image）
- 使用StepFun平台API
- 可自定义生成参数：模型、尺寸、步数、风格等
- 返回可访问的图像链接或直接下载

## 使用场景
- 应用界面设计中的图像素材生成
- 美食应用中各种菜品、界面元素的快速生成
- AI辅助创意设计流程
- 自动化图像内容生产

## 安装配置
### 1. 环境依赖
此技能需要以下依赖项：
```bash
pip3 install requests playwright
playwright install chromium
```

### 2. API配置
需要配置StepFun API密钥：
```python
# 配置文件位置 (可选)
api_key = "your_stepfun_api_key_here"
```
如未设置，将使用默认API密钥（可能需要修改）

## 调用示例
```python
from stepfun_image_skill import generate_image

# 基础调用
result = generate_image(
    prompt="卡通风格 girl jumping",
    model="step-image-edit-2",
    size="1024x1024"
)

# 获取图像链接
image_url = result["data"][0]["url"]
print(f"图像链接: {image_url}")
```

## 参数说明
### 必需参数
- `prompt` (字符串): 图像描述文本

### 可选参数
- `model` (字符串): 使用的模型名称（默认：step-image-edit-2）
- `size` (字符串): 图像大小格式 (默认："1024x1024")
- `steps` (整数): 生成步数（默认：30）
- `cfg_scale` (浮点数): 分类器自由引导比例（默认：1.0）

## 错误处理
技能会自动处理以下异常：
- API连接超时
- 模型参数错误
- 权限不足错误
- 网络中断问题

## 注意事项
1. 为确保正确使用，需要在StepFun平台上开通相关模型权限
2. 建议对提示词进行优化以获得更好的图像效果
3. API免费额度有限，长期使用建议升级订阅等级

## 使用许可
此技能基于StepFun官方API规范开发，仅限于合法用途。

## 作者信息
开发者：AI工程师
创建日期：2026-07-12