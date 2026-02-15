# Image Generation API Skill

这是一个用于集成外部API进行图像生成的技能，支持多种AI图像生成服务，包括即梦AI、OpenAI DALL-E和Stability AI。

## 功能特性

- 🎨 **多服务支持**: 集成即梦AI、OpenAI DALL-E、Stability AI等多种图像生成服务
- 🔑 **API密钥管理**: 安全的API密钥配置和管理
- 🔄 **统一接口**: 统一的接口和参数格式，简化使用
- ⚡ **批量生成**: 支持批量生成多个图像
- 🛡️ **错误处理**: 完善的错误处理和重试机制
- 🔍 **参数验证**: 参数验证和配置管理
- 📊 **性能优化**: 缓存机制和性能优化

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置API密钥

在环境变量中设置API密钥：

```bash
# 即梦AI
export JIMENG_API_KEY="your_jimeng_api_key"

# OpenAI DALL-E
export OPENAI_API_KEY="your_openai_api_key"

# Stability AI
export STABILITY_API_KEY="your_stability_api_key"
```

### 3. 基本使用

```python
from scripts.image_generator import ImageGenerator

# 初始化生成器
generator = ImageGenerator()

# 生成图像
result = generator.generate(
    provider="jimeng",
    prompt="一个可爱的卡通猫",
    size="1024x1024",
    style="natural"
)

print(result)
```

## 支持的提供商

### 即梦AI (Jimeng AI)
- **特点**: 中文AI图像生成，擅长动漫、卡通风格
- **API Key**: `JIMENG_API_KEY`
- **支持的尺寸**: 1024x1024, 512x512, 256x256
- **支持的风格**: natural, anime, realistic, cartoon

### OpenAI DALL-E
- **特点**: 通用图像生成，支持高质量输出
- **API Key**: `OPENAI_API_KEY`
- **支持的尺寸**: 1024x1024, 1024x1792, 1792x1024
- **支持的风格**: vivid, natural

### Stability AI
- **特点**: 基于Stable Diffusion，高质量写实图像
- **API Key**: `STABILITY_API_KEY`
- **支持的尺寸**: 1024x1024, 512x512, 768x768
- **支持的风格**: realistic, artistic, cartoon

## 使用示例

### 单个图像生成

```python
from scripts.image_generator import ImageGenerator

generator = ImageGenerator()

# 使用即梦AI
result = generator.generate(
    provider="jimeng",
    prompt="美丽的山水画，中国传统水墨风格",
    size="1024x1024",
    style="natural"
)

if result["success"]:
    for img in result["images"]:
        print(f"图像URL: {img['url']}")
else:
    print(f"生成失败: {result['error']}")
```

### 批量生成

```python
prompts = [
    "一只可爱的小猫",
    "一只忠诚的狗",
    "一只美丽的小鸟"
]

results = generator.batch_generate(
    provider="jimeng",
    prompts=prompts,
    size="512x512",
    style="cartoon"
)

for i, result in enumerate(results):
    prompt = prompts[i]
    if result["success"]:
        print(f"✅ '{prompt}': 成功生成 {len(result['images'])} 张图像")
    else:
        print(f"❌ '{prompt}': {result['error']}")
```

### 参数验证

```python
from scripts.utils import ParameterValidator

validator = ParameterValidator()

# 验证提示词
result = validator.validate_prompt("一个美丽的风景")
print(f"提示词有效: {result['valid']}")

# 验证尺寸
result = validator.validate_size("1024x1024", "jimeng")
print(f"尺寸有效: {result['valid']}")
```

## 配置管理

### 查看可用提供商

```python
from scripts.provider_configs import ProviderConfig

config = ProviderConfig()
available = config.get_available_providers()
print(f"可用的提供商: {available}")
```

### 查看提供商配置

```python
provider_config = config.get_provider_config("jimeng")
print(f"即梦AI配置: {provider_config}")
```

### 添加自定义提供商

```python
# 在 references/provider_configs.yaml 中添加新提供商
config = ProviderConfig()

new_provider = {
    "name": "New Provider",
    "endpoint": "https://api.new-provider.com/generate",
    "required_params": ["prompt"],
    "supported_sizes": ["1024x1024"],
    "rate_limit": {"requests_per_minute": 30}
}

config.add_provider("new_provider", new_provider)
```

## 运行演示

```bash
cd scripts
python demo.py
```

演示脚本将展示：
- 基本图像生成
- 批量生成
- 参数验证
- 图像处理
- 配置管理
- 错误处理
- 提供商对比

## 自定义提供商

要添加新的图像生成提供商，请参考 `references/custom-providers.md`。

### 基本步骤

1. 创建自定义提供商类
2. 继承 `BaseImageGenerator`
3. 实现 `generate()` 和 `validate_params()` 方法
4. 注册到 `ImageGenerator` 类
5. 更新配置文件

## 错误处理

```python
try:
    result = generator.generate("jimeng", prompt, **kwargs)
    if not result["success"]:
        print(f"生成失败: {result['error']}")
except Exception as e:
    print(f"发生错误: {str(e)}")
```

## 性能优化

### 缓存

```python
# 启用缓存
config = ProviderConfig()
config.config["global"]["cache_enabled"] = True
config.save_config()
```

### 批量处理

```python
# 使用批量生成减少API调用次数
prompts = [f"图像 {i}" for i in range(10)]
results = generator.batch_generate("jimeng", prompts)
```

## 监控和调试

### 启用调试模式

```python
import os
os.environ["IMAGE_GENERATION_DEBUG"] = "1"
```

### 日志记录

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 在自定义提供商中使用
logger.info("开始生成图像")
logger.error("生成失败", exc_info=True)
```

## 常见问题

### Q: 如何获取API密钥？

A: 
- 即梦AI: 注册即梦AI账号获取API密钥
- OpenAI: 注册OpenAI账号获取API密钥
- Stability AI: 注册Stability AI账号获取API密钥

### Q: 生成失败怎么办？

A: 
1. 检查API密钥是否正确
2. 验证网络连接
3. 检查参数格式
4. 查看错误信息
5. 尝试其他提供商

### Q: 如何添加新的提供商？

A: 参考 `references/custom-providers.md` 文件，按照指南添加新的提供商类。

## 技术支持

如果遇到问题，请检查：
1. 环境变量是否正确设置
2. API密钥是否有效
3. 网络连接是否正常
4. 依赖包是否正确安装

## 更新日志

### v1.0.0
- 初始版本发布
- 支持即梦AI、OpenAI DALL-E、Stability AI
- 基本的图像生成功能
- 批量生成支持
- 参数验证和错误处理