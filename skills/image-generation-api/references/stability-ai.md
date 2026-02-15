# Stability AI API Documentation

## Overview
Stability AI提供高质量的AI图像生成服务，基于Stable Diffusion模型，擅长生成写实、艺术和创意风格的图像。支持高分辨率图像和精细的参数控制。

## API Endpoints
- **Base URL**: `https://api.stability.ai/v1`
- **Text-to-Image**: `https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image`
- **Image-to-Image**: `https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image`

## Authentication
使用Bearer Token认证方式：
```
Authorization: Bearer YOUR_STABILITY_API_KEY
```

API密钥需要设置环境变量：
```bash
export STABILITY_API_KEY="your_stability_api_key_here"
```

## Text-to-Image Generation

### Request Format
```python
import requests

url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
headers = {
    "Authorization": f"Bearer {STABILITY_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

data = {
    "text_prompts": [
        {
            "text": "A beautiful sunset over the mountains",
            "weight": 1.0
        }
    ],
    "cfg_scale": 7,
    "height": 1024,
    "width": 1024,
    "samples": 1,
    "steps": 50
}

response = requests.post(url, headers=headers, json=data)
```

### Parameters

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `text_prompts` | array | Yes | 文本提示词数组 | - |
| `cfg_scale` | number | No | 引导缩放系数 | 7 |
| `height` | integer | No | 图像高度 | 1024 |
| `width` | integer | No | 图像宽度 | 1024 |
| `samples` | integer | No | 生成样本数量 | 1 |
| `steps` | integer | No | 生成步数 | 50 |
| `seed` | integer | No | 随机种子 | 随机 |

### Text Prompts Format
```python
"text_prompts": [
    {
        "text": "主要描述",
        "weight": 1.0
    },
    {
        "text": "负面描述 (可选)",
        "weight": -0.5
    }
]
```

#### Prompt Weights
- `weight > 0`: 正面引导（强度更高）
- `weight = 0`: 忽略此提示词
- `weight < 0`: 负面引导（避免某些元素）

### Response Format
```json
{
  "artifacts": [
    {
      "base64": "iVBORw0KGgoAAAANSUhEUgAA...",
      "seed": 1234567890
    }
  ]
}
```

## Image-to-Image Generation

### Request Format
```python
url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image"
headers = {
    "Authorization": f"Bearer {STABILITY_API_KEY}",
    "Accept": "application/json"
}

files = {
    "init_image": ("init_image.png", open("init_image.png", "rb"), "image/png"),
    "mask": ("mask.png", open("mask.png", "rb"), "image/png")  # 可选
}

data = {
    "text_prompts": [
        {
            "text": "Transform this into a fantasy landscape",
            "weight": 1.0
        }
    ],
    "cfg_scale": 7,
    "image_strength": 0.35,
    "samples": 1,
    "steps": 50
}

response = requests.post(url, headers=headers, files=files, data=data)
```

### Image-to-Image Parameters
| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `init_image` | file | Yes | 初始图像 | - |
| `mask` | file | No | 遮罩图像 | - |
| `image_strength` | number | No | 图像强度（0-1） | 0.35 |
| `text_prompts` | array | Yes | 文本提示词 | - |

## Advanced Parameters

### Sampling Methods
```python
data = {
    "text_prompts": [{"text": "..."}],
    "cfg_scale": 7,
    "height": 1024,
    "width": 1024,
    "samples": 1,
    "steps": 50,
    "sampler": "K_DPM_2_ANCESTRAL",  # 采样器
    "scheduler": "Karras"  # 调度器
}
```

#### Available Samplers
- `K_DPM_2_ANCESTRAL`
- `K_DPM_2`
- `EULER`
- `EULER_ANCESTRAL`
- `DDIM`
- `UNION`
- `K_DPMPP_2M`
- `K_DPMPP_2M_ANCESTRAL`
- `K_DPMPP_SDE`
- `K_LMS`

### Guidance Scale (CFG Scale)
- `0-1`: 创造性但可能偏离提示词
- `1-7`: 平衡创造性和准确性（推荐）
- `7-20`: 高度忠于提示词但可能僵硬

### Steps
- `10-25`: 快速生成，基本质量
- `25-50`: 平衡速度和质量（推荐）
- `50-100`: 最高质量，但耗时较长

## Available Models

| Model | Resolution | Use Case | Features |
|-------|-----------|----------|----------|
| `stable-diffusion-xl-1024-v1-0` | 1024x1024 | 通用图像生成 | 高质量，多功能 |
| `stable-diffusion-xl-1024-v0-9` | 1024x1024 | 稳定版本 | 更稳定，较少随机性 |
| `stable-diffusion-xl-refiner-v1-0` | 1024x1024 | 图像优化 | 用于改善生成结果 |
| `stable-diffusion-512-v2-1` | 512x512 | 快速生成 | 更快但分辨率较低 |

## Best Practices

### Prompt Engineering
1. **详细描述**：提供具体的视觉元素、颜色、构图
2. **使用权重**：通过权重控制提示词的重要性
3. **负面提示**：使用负权重排除不需要的元素
4. **迭代优化**：多次生成并调整参数

### Example Prompts

#### 写实风格
```python
"text_prompts": [
    {
        "text": "photorealistic portrait of a woman with freckles, natural lighting, detailed skin texture, 8k resolution",
        "weight": 1.0
    },
    {
        "text": "blurry, distorted, unrealistic",
        "weight": -0.5
    }
]
```

#### 艺术风格
```python
"text_prompts": [
    {
        "text": "impressionist painting of a sunset, vibrant colors, loose brushstrokes, artistic style",
        "weight": 1.0
    },
    {
        "text": "photographic, realistic, detailed",
        "weight": -0.3
    }
]
```

#### 概念艺术
```python
"text_prompts": [
    {
        "text": "concept art of a futuristic city, cyberpunk style, neon lights, detailed architecture",
        "weight": 1.0
    },
    {
        "text": "medieval, ancient, historical",
        "weight": -0.4
    }
]
```

### Tips for Better Results
1. **使用适当的CFG Scale**：7通常是一个好的起点
2. **增加步数**：50-100步可获得更高质量
3. **尝试不同采样器**：不同采样器产生不同风格
4. **使用高质量初始化图像**：对于图像到图像转换

## Integration Examples

### 基础生成
```python
from scripts.image_generator import ImageGenerator

generator = ImageGenerator()
result = generator.generate(
    provider="stability",
    prompt="A beautiful landscape with mountains and lakes",
    cfg_scale=7,
    steps=50
)

print(result)
```

### 高级参数
```python
data = {
    "text_prompts": [
        {
            "text": "A magical forest with glowing plants, fantasy art style",
            "weight": 1.0
        }
    ],
    "cfg_scale": 9,
    "steps": 75,
    "sampler": "K_DPM_2_ANCESTRAL",
    "scheduler": "Karras",
    "height": 768,
    "width": 768,
    "samples": 3
}

response = requests.post(url, headers=headers, json=data)
```

### 图像到图像转换
```python
from scripts.utils import ImageUtils

# 准备初始图像
init_image_data = ImageUtils.download_image("https://example.com/init_image.png")
ImageUtils.save_image(init_image_data, "init_image.png")

# 图像到图像转换
files = {
    "init_image": ("init_image.png", open("init_image.png", "rb"), "image/png")
}

data = {
    "text_prompts": [
        {
            "text": "Transform this into a surreal dreamscape",
            "weight": 1.0
        }
    ],
    "cfg_scale": 7,
    "image_strength": 0.5,
    "samples": 2
}

response = requests.post(url, headers=headers, files=files, data=data)
```

## Performance Optimization

### 批量生成
```python
def batch_generate(prompts, **kwargs):
    """批量生成多个图像"""
    results = []
    for prompt in prompts:
        data = {
            "text_prompts": [{"text": prompt, "weight": 1.0}],
            "cfg_scale": 7,
            "steps": 50,
            "samples": 1,
            **kwargs
        }
        
        response = requests.post(url, headers=headers, json=data)
        results.append(response.json())
    
    return results
```

### 结果缓存
```python
import hashlib
import os

def generate_cached(prompt, **kwargs):
    """缓存生成结果以节省API调用"""
    cache_key = hashlib.md5(f"{prompt}_{json.dumps(kwargs)}".encode()).hexdigest()
    cache_file = f"cache/stability_{cache_key}.json"
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    
    result = generate_image(prompt, **kwargs)
    os.makedirs("cache", exist_ok=True)
    with open(cache_file, 'w') as f:
        json.dump(result, f)
    
    return result
```

## Troubleshooting

### Common Issues

1. **API Key无效**
   - 检查环境变量`STABILITY_API_KEY`设置
   - 确认密钥有效性

2. **配额限制**
   - 监控API使用配额
   - 实现请求限制和重试逻辑

3. **生成质量不满意**
   - 增加步数（50-100）
   - 调整CFG Scale（5-10）
   - 尝试不同的采样器

4. **图像尺寸问题**
   - 确保尺寸在模型支持范围内
   - 考虑使用更大的分辨率模型

### Error Handling
```python
def handle_stability_error(response):
    """处理Stability API错误"""
    try:
        error_data = response.json()
        error_msg = error_data.get("message", "Unknown error")
        
        if "quota exceeded" in error_msg.lower():
            return {"error": "API quota exceeded", "retry_after": 3600}
        elif "invalid key" in error_msg.lower():
            return {"error": "Invalid API key"}
        else:
            return {"error": error_msg}
    except:
        return {"error": "API request failed"}
```

## Cost Management

### 成本估算
Stability AI通常按成功生成的图像收费，一般$0.01-$0.05每张图像。

### 优化策略
1. **合理设置步数**：通常50步足够，质量提升不明显时减少步数
2. **批量生成**：使用`samples`参数一次性生成多张
3. **缓存结果**：避免重复生成相同提示词
4. **监控使用量**：记录API使用情况

## Advanced Features

### 图像微调
```python
# 使用refiner模型改善生成结果
def refine_image(base64_image):
    refiner_url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-refiner-v1-0/text-to-image"
    
    data = {
        "text_prompts": [{"text": "refine this image", "weight": 1.0}],
        "cfg_scale": 7,
        "steps": 25,
        "init_image": base64_image
    }
    
    return requests.post(refiner_url, headers=headers, json=data)
```

### 多重提示词组合
```python
# 结合多个提示词创建复杂图像
data = {
    "text_prompts": [
        {
            "text": "a beautiful woman",
            "weight": 0.8
        },
        {
            "text": "wearing a red dress",
            "weight": 0.6
        },
        {
            "text": "standing in a garden",
            "weight": 0.7
        },
        {
            "text": "sunset lighting",
            "weight": 0.5
        }
    ],
    "cfg_scale": 8,
    "steps": 60
}
```