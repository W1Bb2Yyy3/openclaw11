# OpenAI DALL-E API Documentation

## Overview
OpenAI DALL-E是一个强大的AI图像生成服务，能够根据文本提示词生成高质量、创意性的图像。支持多种尺寸、质量和风格选项。

## API Endpoints
- **Base URL**: `https://api.openai.com/v1`
- **Image Generation**: `https://api.openai.com/v1/images/generations`

## Authentication
使用Bearer Token认证方式：
```
Authorization: Bearer YOUR_OPENAI_API_KEY
```

API密钥需要设置环境变量：
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

## Image Generation

### Request Format
```python
import requests

url = "https://api.openai.com/v1/images/generations"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

data = {
    "prompt": "A cute cartoon cat",
    "n": 1,
    "size": "1024x1024",
    "quality": "standard",
    "style": "vivid"
}

response = requests.post(url, headers=headers, json=data)
```

### Parameters

| Parameter | Type | Required | Description | Options |
|-----------|------|----------|-------------|---------|
| `prompt` | string | Yes | 图像生成提示词 | - |
| `n` | integer | No | 生成图像数量 | `1-10` |
| `size` | string | No | 图像尺寸 | `1024x1024`, `1024x1792`, `1792x1024` |
| `quality` | string | No | 图像质量 | `standard`, `hd` |
| `style` | string | No | 图像风格 | `vivid`, `natural` |

### Supported Sizes

| Size | Aspect Ratio | Use Case |
|------|--------------|-----------|
| `1024x1024` | 1:1 | 正方形图像，通用场景 |
| `1024x1792` | 9:16 | 竖向图像，人物肖像 |
| `1792x1024` | 16:9 | 横向图像，风景画 |

### Quality Options

| Quality | Description | Use Case |
|---------|-------------|----------|
| `standard` | 标准质量 | 平衡质量和成本 |
| `hd` | 高清质量 | 更详细、更高质量的图像 |

### Style Options

| Style | Description | Characteristics |
|-------|-------------|-----------------|
| `vivid` | 生动的风格 | 更鲜艳、更戏剧化的色彩 |
| `natural` | 自然风格 | 更真实、更自然的图像 |

### Response Format
```json
{
  "created": 1642339200,
  "data": [
    {
      "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/...",
      "revised_prompt": "A cute cartoon cat sitting on a windowsill"
    }
  ]
}
```

## Variations (图像变体)

### Request Format
```python
url = "https://api.openai.com/v1/images/variations"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

files = {
    "image": open("original_image.png", "rb")
}

data = {
    "n": 3,
    "size": "1024x1024"
}

response = requests.post(url, headers=headers, files=files, data=data)
```

### Parameters
| Parameter | Type | Required | Description | Options |
|-----------|------|----------|-------------|---------|
| `image` | file | Yes | 原始图像文件 | PNG, JPG, JPEG |
| `n` | integer | No | 生成变体数量 | `1-10` |
| `size` | string | No | 变体尺寸 | `1024x1024` |

## Edits (图像编辑)

### Request Format
```python
url = "https://api.openai.com/v1/images/edits"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

files = {
    "image": open("original_image.png", "rb"),
    "mask": open("mask.png", "rb")  # 可选
}

data = {
    "prompt": "Add a hat to the cat",
    "n": 1,
    "size": "1024x1024"
}

response = requests.post(url, headers=headers, files=files, data=data)
```

### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | file | Yes | 原始图像文件 |
| `mask` | file | No | 遮罩文件，指定编辑区域 |
| `prompt` | string | Yes | 编辑描述 |
| `n` | integer | No | 生成图像数量 |
| `size` | string | No | 图像尺寸 |

## Rate Limits

- **Requests per minute**: 50
- **Tokens per minute**: 100,000
- **Image credits per month**: 取决于订阅计划

### Cost Estimates
| Quality | Size | Cost per Image |
|---------|------|----------------|
| Standard | 1024x1024 | $0.020 |
| HD | 1024x1024 | $0.040 |
| Standard | 1024x1792 | $0.040 |
| HD | 1024x1792 | $0.080 |

## Best Practices

### Prompt Engineering
1. **清晰具体的描述**：包含颜色、材质、构图等细节
2. **指定风格**：明确想要的视觉风格
3. **使用关键词**：包含重要的视觉元素
4. **避免模糊概念**：避免"美丽"、"很好"等主观词汇

### Example Prompts

#### 人物肖像
```
A professional headshot of a smiling businesswoman, studio lighting, clean background, realistic photography style
```

#### 风景画
```
A breathtaking mountain landscape at sunset, golden hour lighting, realistic style, 8k resolution
```

#### 艺术创作
```
A surreal painting of a floating city in the clouds, impressionist style, vibrant colors, dreamlike atmosphere
```

### Tips for Better Results
1. **使用质量参数**：重要图像使用`hd`质量
2. **调整尺寸**：根据用途选择合适的尺寸比例
3. **迭代生成**：生成多个选项选择最佳结果
4. **结合提示词优化**：使用`revised_prompt`作为改进基础

## Integration Examples

### 基础生成
```python
from scripts.image_generator import ImageGenerator

generator = ImageGenerator()
result = generator.generate(
    provider="openai",
    prompt="A cute cartoon cat sitting on a windowsill",
    size="1024x1024",
    quality="hd",
    style="vivid"
)

print(result)
```

### 批量生成
```python
prompts = [
    "A futuristic cityscape",
    "A underwater scene with fish",
    "A space exploration scene"
]
results = generator.batch_generate(
    provider="openai",
    prompts=prompts,
    size="1792x1024",
    quality="hd"
)
```

### 图像变体生成
```python
from scripts.utils import ImageUtils

# 下载原始图像
image_data = ImageUtils.download_image(original_image_url)
ImageUtils.save_image(image_data, "original.png")

# 生成变体
files = {"image": open("original.png", "rb")}
response = requests.post(
    "https://api.openai.com/v1/images/variations",
    headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
    files=files,
    data={"n": 3, "size": "1024x1024"}
)
```

## Troubleshooting

### Common Issues

1. **API Key无效**
   - 检查环境变量`OPENAI_API_KEY`是否正确设置
   - 确认API密钥是否有效且未过期

2. **配额用尽**
   - 检查API使用情况和配额限制
   - 升级到更高订阅计划

3. **内容过滤**
   - 提示词可能被内容过滤器拦截
   - 重新表述提示词避免敏感词汇

4. **生成质量不满意**
   - 使用`hd`质量获得更好效果
   - 优化提示词描述
   - 尝试不同的`style`参数

### Error Codes
```json
{
  "error": {
    "code": "invalid_api_key",
    "message": "Incorrect API key provided"
  }
}
```

### Advanced Usage

#### 使用自定义模型
```python
data = {
    "model": "dall-e-3",  # 使用最新模型
    "prompt": "A detailed description...",
    "n": 1,
    "quality": "hd",
    "style": "vivid"
}
```

#### 结合图像编辑
```python
# 创建遮罩文件
mask_data = create_mask_image()
ImageUtils.save_image(mask_data, "mask.png")

# 执行图像编辑
files = {
    "image": open("original.png", "rb"),
    "mask": open("mask.png", "rb")
}

data = {
    "prompt": "Make the cat wearing a hat",
    "n": 2
}

response = requests.post(
    "https://api.openai.com/v1/images/edits",
    headers=headers,
    files=files,
    data=data
)
```

## Performance Optimization

### 缓存策略
```python
import hashlib
import os

def get_cache_key(prompt, size, quality, style):
    key_string = f"{prompt}_{size}_{quality}_{style}"
    return hashlib.md5(key_string.encode()).hexdigest()

def cached_generate(prompt, **kwargs):
    cache_key = get_cache_key(prompt, 
                             kwargs.get('size', '1024x1024'),
                             kwargs.get('quality', 'standard'),
                             kwargs.get('style', 'vivid'))
    cache_file = f"cache/{cache_key}.json"
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    
    result = generator.generate(prompt, **kwargs)
    os.makedirs("cache", exist_ok=True)
    with open(cache_file, 'w') as f:
        json.dump(result, f)
    
    return result
```

### 异步处理
```python
import asyncio
import aiohttp

async def async_generate(prompt, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.openai.com/v1/images/generations",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={"prompt": prompt, **kwargs}
        ) as response:
            return await response.json()
```

## Monitoring and Analytics

### 使用统计
```python
import time
from collections import defaultdict

usage_stats = defaultdict(int)

def record_usage(provider, quality, size):
    usage_stats[f"{provider}_{quality}_{size}"] += 1

def get_usage_report():
    return dict(usage_stats)
```

### 成本估算
```python
def calculate_cost(prompt, quality, size):
    costs = {
        "standard_1024x1024": 0.020,
        "hd_1024x1024": 0.040,
        "standard_1792x1024": 0.040,
        "hd_1792x1024": 0.080
    }
    
    key = f"{quality}_{size}"
    return costs.get(key, 0.020)
```