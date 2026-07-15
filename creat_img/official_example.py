from openai import OpenAI

# StepFun API 配置 
STEPFUN_KEY = "a9okTRyAtAwCkFQP0lsI5J8HQpav2xEwKdLFAoVDo7ZxEqMPTnwj9YGog5oxYFmA"  # 替换为您的实际 API Key
STEPFUN_MODEL = "step-1x-medium"

def generate_image(prompt, model=STEPFUN_MODEL, n=1, response_format="url",
 size="1024x1024", steps=50, seed=11879934, cfg_scale=7.5):
    client = OpenAI(api_key=STEPFUN_KEY, base_url="https://api.stepfun.com/v1")
    image = client.images.generate(
        model=model,
        prompt=prompt,
        response_format=response_format,
        extra_body={
            "cfg_scale": cfg_scale,
            "seed": seed,
            "steps": steps
        },
        size=size,
        n=n,
    )
    return image.data

if __name__ == "__main__":
    prompt = "一个可爱的卡通风格的美食应用界面，展示各种美食图片和分类菜单"
    res = generate_image(prompt)
    print(res)