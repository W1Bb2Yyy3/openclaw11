# 即梦AI (Jimeng AI) API Documentation

## Overview
即梦AI是一个专注于中文AI图像生成的服务，支持多种艺术风格和高质量的图像生成。

## API Endpoints
- **Base URL**: `https://api.jimeng.ai/v1`
- **Image Generation**: `https://api.jimeng.ai/v1/images/generations`

## Authentication
使用Bearer Token认证方式：
```
Authorization: Bearer YOUR_JIMENG_API_KEY
```

API密钥需要设置环境变量：
```bash
export JIMENG_API_KEY="your_jimeng_api_key_here"
```

## Image Generation

### Request Format
```python
import requests

url = "https://api.jimeng.ai/v1/images/generations"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

data = {
    "prompt": "一个可爱的卡通猫",
    "model": "jimeng-v1",
    "size": "1024x1024",
    "quality": "standard",
    "n": 1,
    "style": "natural"
}

response = requests.post(url, headers=headers, json=data)
```

### Parameters

| Parameter | Type | Required | Description | Options |
|-----------|------|----------|-------------|---------|
| `prompt` | string | Yes | 图像生成提示词 | - |
| `model` | string | No | 使用的模型版本 | `jimeng-v1`, `jimeng-v2` |
| `size` | string | No | 图像尺寸 | `1024x1024`, `512x512`, `256x256` |
| `quality` | string | No | 图像质量 | `standard`, `hd` |
| `n` | integer | No | 生成图像数量 | `1-4` |
| `style` | string | No | 图像风格 | `natural`, `anime`, `realistic`, `cartoon` |

### Supported Styles

| Style | Description | Best For |
|-------|-------------|----------|
| `natural` | 自然风格 | 真实感图像，日常场景 |
| `anime` | 动漫风格 | 卡通人物，动漫场景 |
| `realistic` | 写实风格 | 照片级真实图像 |
| `cartoon` | 卡通风格 | 儿童插画，卡通艺术 |

### Response Format
```json
{
  "success": true,
  "data": [
    {
      "url": "https://api.jimeng.ai/images/abc123",
      "revised_prompt": "一个可爱的卡通猫，坐在花园里",
      "seed": 12345,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "metadata": {
    "model": "jimeng-v1",
    "size": "1024x1024",
    "quality": "standard"
  }
}
```

### Error Responses
```json
{
  "success": false,
  "error": {
    "code": "INVALID_API_KEY",
    "message": "Invalid API key provided"
  }
}
```

## Rate Limits

- **Requests per minute**: 60
- **Tokens per minute**: 10,000
- **Concurrent requests**: 5

### Rate Limit Headers
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 58
X-RateLimit-Reset: 1642339200
```

## Best Practices

### Prompt Engineering
1. **使用清晰的中文描述**：即梦AI对中文提示词理解更好
2. **包含具体细节**：描述颜色、材质、场景等细节
3. **指定艺术风格**：明确想要的风格类型
4. **避免敏感内容**：不要生成暴力、色情等不适宜内容

### Example Prompts

#### 卡通风格
```
一个可爱的卡通小猫，戴着红色帽子，坐在蓝色地毯上，动漫风格，明亮色彩
```

#### 写实风格
```
一只金毛犬在公园里奔跑，阳光明媚，写实摄影风格，高清细节
```

#### 艺术风格
```
山水画，青山绿水，云雾缭绕，中国传统水墨画风格
```

### Tips for Better Results
1. **长度适中**：提示词长度在50-200字符效果最佳
2. **正面描述**：描述想要的元素，而不是不要的元素
3. **迭代优化**：如果效果不满意，可以微调提示词重试
4. **批量生成**：可以使用`n`参数生成多个选择

## Integration Examples

### 基础生成
```python
from scripts.image_generator import ImageGenerator

generator = ImageGenerator()
result = generator.generate(
    provider="jimeng",
    prompt="一只可爱的柯基犬",
    size="1024x1024",
    style="natural"
)

print(result)
```

### 批量生成
```python
prompts = ["小猫", "小狗", "小鸟"]
results = generator.batch_generate(
    provider="jimeng",
    prompts=prompts,
    style="cartoon"
)

for result in results:
    print(f"Prompt: {result.get('prompt')}, URL: {result.get('url')}")
```

### 错误处理
```python
try:
    result = generator.generate("jimeng", prompt, **kwargs)
except Exception as e:
    print(f"Generation failed: {str(e)}")
    # 可以切换到其他重试逻辑
```

## Troubleshooting

### Common Issues

1. **API Key无效**
   - 检查环境变量`JIMENG_API_KEY`是否正确设置
   - 确认API密钥是否有效且未过期

2. **Rate Limit限制**
   - 监控`X-RateLimit-Remaining`头信息
   - 实现请求间隔和重试逻辑

3. **生成质量不满意**
   - 优化提示词
   - 尝试不同的`quality`和`style`参数
   - 增加图像尺寸获得更多细节

4. **网络连接问题**
   - 检查网络连接
   - 实现超时和重试机制

### Debug Mode
启用调试模式获取详细信息：
```python
import os
os.environ["JIMENG_DEBUG"] = "1"
```

这将输出详细的API请求和响应信息，便于调试。