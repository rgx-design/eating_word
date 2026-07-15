# 文生图应用开发

## 当前问题总结

使用 Minimax API 时遇到以下错误：
```
"status_code": 2013, "status_msg": "invalid params, unsupported model: <model_name>"
```

后续发现账户余额不足：
```
"status_code": 1008, "status_msg": "insuficient balance"
```

## 新增方案：StepFun API

通过查看文档并测试后，为 StepFun API 创建了专用生成脚本 (`stepfun_generate.py`)。

### 可用模型
根据官方文档支持的模型：
- `step-image-edit-2` (推荐)
- `step-2x-large`
- `step-1x-medium`

## 确认问题

执行过程中遇到：
```
{"error":{"message":"model step-1x-medium not supported","type":"request_params_invalid"}}
```

可能是:
1. 账户权限不足
2. 使用免费账户无法访问某些模型
3. 需要额外认证或订阅

## 推荐操作步骤

1. **检查 StepFun 订阅状态**
   - 登录控制台查看模型可用性
   - 确认账户是否已升级到支持所需模型的等级

2. **使用推荐模型**
   ```
   # 优先尝试 step-image-edit-2:
   model: "step-image-edit-2"
   ```

3. **测试替代方案**
   - 尝试本地图像生成
   - 部署 Stable Diffusion 等开源模型

## 文件列表

- `generate_image.py` - Minimax API 调用（正确配置后可用）
- `stepfun_generate.py` - StepFun API 调用脚本  
- `simple_image_gen.py` - 本地模拟演示程序
- `README.md` - 当前文件