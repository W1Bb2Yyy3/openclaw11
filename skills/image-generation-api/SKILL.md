---
name: image-generation-api
description: External API integration for image generation services including 即梦AI (Jimeng AI), OpenAI DALL-E, Stability AI, and other popular image generation APIs. Use this skill when Codex needs to: (1) Generate images through various AI image generation services, (2) Configure and manage API keys for different providers, (3) Handle different image generation parameters and styles, (4) Integrate image generation into larger workflows.
---

# Image Generation API Integration

## Overview

This skill provides comprehensive integration with external image generation APIs, allowing seamless connection to multiple AI-powered image creation services. The skill handles API authentication, parameter configuration, and standardized response processing across different providers.

## Core Capabilities

### 1. Multi-Service API Integration
Support for multiple image generation providers:
- **即梦AI (Jimeng AI)** - Chinese image generation service
- **OpenAI DALL-E** - Industry-standard image generation
- **Stability AI** - High-quality image synthesis
- **Midjourney API** - Artistic image generation
- **Custom endpoints** - Add new providers as needed

### 2. API Key Management
Secure configuration and management of API keys for different providers:
- Environment variable-based authentication
- Encrypted configuration files
- Multiple provider support with separate credentials
- Fallback mechanisms for service availability

### 3. Standardized Interface
Unified interface for image generation across all providers:
- Consistent parameter mapping (prompt, style, size, quality)
- Automatic format conversion and optimization
- Error handling and retry mechanisms
- Response standardization

## Quick Start

### Configuration
Configure API keys in your environment:

```bash
# For 即梦AI
export JIMENG_API_KEY="your_jimeng_api_key"

# For OpenAI DALL-E
export OPENAI_API_KEY="your_openai_api_key"

# For Stability AI
export STABILITY_API_KEY="your_stability_api_key"
```

### Basic Usage
Generate images using any supported service:

```python
from scripts.image_generator import ImageGenerator

# Initialize with multiple providers
generator = ImageGenerator()

# Generate with 即梦AI
image_data = generator.generate(
    provider="jimeng",
    prompt="一个可爱的卡通猫",
    style="anime",
    size="1024x1024"
)

# Generate with OpenAI DALL-E
image_data = generator.generate(
    provider="openai",
    prompt="A beautiful sunset over mountains",
    size="1024x1024",
    quality="hd"
)
```

## Provider Details

### 即梦AI (Jimeng AI)
- **Endpoint**: Chinese AI image generation service
- **Specialties**: Anime, cartoon, artistic styles
- **Parameters**: prompt, style, size, quality, seed
- **Reference**: [references/jimeng-api.md](references/jimeng-api.md)

### OpenAI DALL-E
- **Endpoint**: OpenAI's image generation API
- **Specialties**: Realistic images, creative concepts
- **Parameters**: prompt, size, quality, style
- **Reference**: [references/openai-dalle.md](references/openai-dalle.md)

### Stability AI
- **Endpoint**: Stability AI image synthesis
- **Specialties**: High-quality images, artistic styles
- **Parameters**: prompt, width, height, steps, guidance
- **Reference**: [references/stability-ai.md](references/stability-ai.md)

## Advanced Configuration

### Custom Providers
Add new image generation services by extending the base class:

```python
from scripts.image_generator import BaseImageGenerator

class CustomProvider(BaseImageGenerator):
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://api.custom-provider.com/v1/generate"
    
    def generate(self, prompt, **kwargs):
        # Implementation for custom provider
        pass
```

### Batch Generation
Generate multiple images efficiently:

```python
# Batch generation with different prompts
prompts = ["cat", "dog", "bird"]
images = generator.batch_generate(
    provider="jimeng",
    prompts=prompts,
    style="realistic"
)
```

## Error Handling

The skill includes comprehensive error handling:
- **API Rate Limits**: Automatic retry with exponential backoff
- **Authentication Failures**: Clear error messages and key validation
- **Service Outages**: Fallback to alternative providers
- **Invalid Parameters**: Parameter validation and helpful error messages

## Resources

### scripts/
- `image_generator.py` - Main image generation class with multi-provider support
- `provider_configs.py` - Configuration management for different providers
- `utils.py` - Utility functions for image processing and validation

### references/
- `jimeng-api.md` - 即梦AI API documentation and examples
- `openai-dalle.md` - OpenAI DALL-E API reference
- `stability-ai.md` - Stability AI API documentation
- `custom-providers.md` - Guide for adding new providers

### assets/
- `templates/` - Request templates for different providers
- `schemas/` - JSON schemas for API requests and responses