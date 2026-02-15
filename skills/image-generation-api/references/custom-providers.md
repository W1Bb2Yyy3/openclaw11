# Custom Providers Guide

## Overview
This guide explains how to add new image generation providers to the image-generation-api skill. The skill supports an extensible architecture that allows you to integrate any image generation API service.

## Architecture Overview

The image generation system uses a modular architecture:

```
ImageGenerator (main class)
├── BaseImageGenerator (abstract base class)
├── Existing Providers
│   ├── JimengGenerator
│   ├── OpenAIGenerator
│   └── StabilityAIGenerator
└── Custom Providers (user-defined)
```

## Creating a Custom Provider

### Step 1: Create the Provider Class

Create a new Python class that inherits from `BaseImageGenerator`:

```python
from scripts.image_generator import BaseImageGenerator

class CustomProvider(BaseImageGenerator):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.endpoint = "https://api.custom-provider.com/v1/generate"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def validate_params(self, **kwargs) -> bool:
        """Validate parameters for this provider."""
        required = ["prompt"]
        for param in required:
            if param not in kwargs:
                return False
        
        # Add custom validation logic
        if "size" in kwargs:
            valid_sizes = ["512x512", "1024x1024", "1536x1536"]
            if kwargs["size"] not in valid_sizes:
                return False
        
        return True
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate image using the provider's API."""
        if not self.validate_params(prompt=prompt, **kwargs):
            raise ValueError("Invalid parameters for CustomProvider")
        
        payload = {
            "prompt": prompt,
            "size": kwargs.get("size", "1024x1024"),
            "quality": kwargs.get("quality", "standard"),
            "style": kwargs.get("style", "default"),
            "n": kwargs.get("n", 1)
        }
        
        try:
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"CustomProvider API request failed: {str(e)}")
```

### Step 2: Register the Provider

Update the `ImageGenerator` class to include your custom provider:

```python
class ImageGenerator:
    def __init__(self):
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available providers based on API keys."""
        # Initialize existing providers
        jimeng_key = os.getenv("JIMENG_API_KEY")
        if jimeng_key:
            self.providers["jimeng"] = JimengGenerator(jimeng_key)
        
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.providers["openai"] = OpenAIGenerator(openai_key)
        
        # Initialize your custom provider
        custom_key = os.getenv("CUSTOM_API_KEY")
        if custom_key:
            self.providers["custom"] = CustomProvider(custom_key)
```

### Step 3: Update Configuration

Add your provider to the configuration file:

```yaml
providers:
  custom:
    name: "Custom Image Provider"
    endpoint: "https://api.custom-provider.com/v1/generate"
    required_params: ["prompt"]
    supported_sizes: ["512x512", "1024x1024", "1536x1536"]
    supported_qualities: ["standard", "hd"]
    supported_styles: ["default", "artistic", "realistic"]
    rate_limit:
      requests_per_minute: 30
      tokens_per_minute: 5000
```

## Provider Implementation Guide

### API Response Standardization

Different providers have different response formats. You should standardize the response to match the skill's expected format:

```python
def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
    """Generate image and standardize response."""
    raw_response = self._call_api(prompt, **kwargs)
    
    # Standardize the response format
    return {
        "provider": "custom",
        "success": True,
        "images": self._extract_images(raw_response),
        "metadata": {
            "raw_response": raw_response,
            "parameters": kwargs
        }
    }

def _extract_images(self, raw_response) -> List[Dict[str, Any]]:
    """Extract image URLs from provider response."""
    images = []
    
    # Handle different response formats
    if "images" in raw_response:
        for img in raw_response["images"]:
            images.append({
                "url": img.get("url"),
                "seed": img.get("seed")
            })
    elif "data" in raw_response:
        for img in raw_response["data"]:
            images.append({
                "url": img.get("url"),
                "revised_prompt": img.get("revised_prompt")
            })
    
    return images
```

### Authentication Handling

Support different authentication methods:

```python
class CustomProvider(BaseImageGenerator):
    def __init__(self, api_key: str, auth_type: str = "bearer"):
        super().__init__(api_key)
        self.auth_type = auth_type
        self._setup_auth()
    
    def _setup_auth(self):
        """Setup authentication headers based on type."""
        if self.auth_type == "bearer":
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        elif self.auth_type == "api_key":
            self.headers = {
                "X-API-Key": self.api_key,
                "Content-Type": "application/json"
            }
        elif self.auth_type == "basic":
            import base64
            credentials = base64.b64encode(f"{self.api_key}:".encode()).decode()
            self.headers = {
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/json"
            }
```

### Error Handling

Implement comprehensive error handling:

```python
def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
    """Generate image with error handling."""
    try:
        # Validate input
        if not self.validate_params(prompt=prompt, **kwargs):
            raise ValueError("Invalid parameters")
        
        # Make API call
        response = requests.post(
            self.endpoint,
            headers=self.headers,
            json=self._build_request(prompt, **kwargs),
            timeout=self.timeout
        )
        
        # Handle HTTP errors
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        
        # Validate response format
        if not self._validate_response(result):
            raise ValueError("Invalid response format")
        
        return result
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP Error {e.response.status_code}"
        if e.response.status_code == 401:
            error_msg = "Authentication failed"
        elif e.response.status_code == 429:
            error_msg = "Rate limit exceeded"
        
        return {
            "provider": "custom",
            "success": False,
            "error": error_msg,
            "retry_after": self._get_retry_after(e.response.headers)
        }
    
    except requests.exceptions.RequestException as e:
        return {
            "provider": "custom",
            "success": False,
            "error": f"Request failed: {str(e)}"
        }
    
    except Exception as e:
        return {
            "provider": "custom",
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }
```

## Implementation Examples

### Example 1: Midjourney API

```python
class MidjourneyProvider(BaseImageGenerator):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.endpoint = "https://api.midjourney.com/v1/imagine"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def validate_params(self, **kwargs) -> bool:
        required = ["prompt"]
        return all(param in kwargs for param in required)
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        payload = {
            "prompt": prompt,
            "model": kwargs.get("model", "latest"),
            "version": kwargs.get("version", "6.0"),
            "style": kwargs.get("style", "raw"),
            "chaos": kwargs.get("chaos", 0),
            "weird": kwargs.get("weird", 0)
        }
        
        response = requests.post(self.endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return {
            "provider": "midjourney",
            "success": True,
            "images": [
                {
                    "url": f"https://cdn.midjourney.com/{task_id}_0.png",
                    "task_id": task_id
                }
            ],
            "metadata": {
                "task_id": task_id,
                "raw_response": response.json()
            }
        }
```

### Example 2: Replicate API

```python
class ReplicateProvider(BaseImageGenerator):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.endpoint = "https://api.replicate.com/v1/predictions"
        self.headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json"
        }
    
    def validate_params(self, **kwargs) -> bool:
        required = ["prompt", "model"]
        return all(param in kwargs for param in required)
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        payload = {
            "input": {
                "prompt": prompt,
                "width": kwargs.get("width", 1024),
                "height": kwargs.get("height", 1024),
                "num_inference_steps": kwargs.get("steps", 50),
                "guidance_scale": kwargs.get("cfg_scale", 7)
            },
            "model": kwargs.get("model", "stability-ai/stable-diffusion")
        }
        
        response = requests.post(self.endpoint, headers=self.headers, json=payload)
        response.raise_for_status()
        
        prediction = response.json()
        prediction_id = prediction["id"]
        
        # Poll for completion
        while True:
            status_response = requests.get(
                f"https://api.replicate.com/v1/predictions/{prediction_id}",
                headers=self.headers
            )
            status_data = status_response.json()
            
            if status_data["status"] == "completed":
                return {
                    "provider": "replicate",
                    "success": True,
                    "images": [
                        {
                            "url": status_data["output"][0],
                            "prediction_id": prediction_id
                        }
                    ],
                    "metadata": {
                        "prediction_id": prediction_id,
                        "raw_response": status_data
                    }
                }
            elif status_data["status"] == "failed":
                raise Exception(f"Generation failed: {status_data.get('error', 'Unknown error')}")
            
            time.sleep(5)  # Wait before polling again
```

## Configuration Management

### Dynamic Provider Loading

Create a dynamic provider loader:

```python
class ProviderLoader:
    def __init__(self, config_file: str = "references/provider_configs.yaml"):
        self.config_file = config_file
        self.providers_config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load provider configuration from file."""
        try:
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {"providers": {}}
    
    def load_provider(self, provider_name: str, api_key: str) -> Optional[BaseImageGenerator]:
        """Dynamically load a provider based on configuration."""
        if provider_name not in self.providers_config["providers"]:
            return None
        
        config = self.providers_config["providers"][provider_name]
        provider_class = self._get_provider_class(provider_name)
        
        if provider_class:
            return provider_class(api_key)
        
        return None
    
    def _get_provider_class(self, provider_name: str) -> Optional[type]:
        """Get provider class by name."""
        provider_classes = {
            "jimeng": JimengGenerator,
            "openai": OpenAIGenerator,
            "stability": StabilityAIGenerator,
            "custom": CustomProvider
        }
        
        return provider_classes.get(provider_name)
```

## Testing Your Provider

### Unit Tests

```python
import unittest
from unittest.mock import Mock, patch

class TestCustomProvider(unittest.TestCase):
    def setUp(self):
        self.provider = CustomProvider("test_api_key")
    
    def test_validate_params(self):
        # Test valid parameters
        self.assertTrue(self.provider.validate_params(prompt="test"))
        self.assertTrue(self.provider.validate_params(prompt="test", size="1024x1024"))
        
        # Test invalid parameters
        self.assertFalse(self.provider.validate_params())
        self.assertFalse(self.provider.validate_params(prompt="test", size="invalid_size"))
    
    @patch('requests.post')
    def test_generate_success(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"images": [{"url": "https://example.com/test.jpg"}]}
        mock_post.return_value = mock_response
        
        result = self.provider.generate("test prompt")
        
        self.assertTrue(result["success"])
        self.assertEqual(len(result["images"]), 1)
    
    @patch('requests.post')
    def test_generate_error(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_post.return_value = mock_response
        
        result = self.provider.generate("test prompt")
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
```

### Integration Tests

```python
class TestProviderIntegration(unittest.TestCase):
    def setUp(self):
        self.generator = ImageGenerator()
    
    def test_custom_provider_integration(self):
        # Test with environment variable
        os.environ["CUSTOM_API_KEY"] = "test_key"
        
        # Reinitialize to load custom provider
        self.generator = ImageGenerator()
        
        self.assertIn("custom", self.generator.get_available_providers())
    
    def test_batch_generation(self):
        os.environ["CUSTOM_API_KEY"] = "test_key"
        self.generator = ImageGenerator()
        
        prompts = ["cat", "dog", "bird"]
        results = self.generator.batch_generate("custom", prompts)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertIn("success", result)
```

## Deployment Considerations

### Environment Variables

Set environment variables for your custom provider:
```bash
export CUSTOM_API_KEY="your_api_key_here"
export CUSTOM_PROVIDER_ENDPOINT="https://api.custom-provider.com"
export CUSTOM_AUTH_TYPE="bearer"
```

### Configuration Files

Create a provider configuration file:
```yaml
providers:
  custom:
    name: "Custom Image Provider"
    endpoint: "https://api.custom-provider.com/v1/generate"
    required_params: ["prompt"]
    supported_sizes: ["512x512", "1024x1024"]
    supported_qualities: ["standard", "hd"]
    supported_styles: ["default", "artistic"]
    rate_limit:
      requests_per_minute: 30
      tokens_per_minute: 5000
    auth_type: "bearer"
```

### Monitoring and Logging

Add monitoring for your custom provider:
```python
import logging

logger = logging.getLogger(__name__)

class CustomProvider(BaseImageGenerator):
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        start_time = time.time()
        
        try:
            result = super().generate(prompt, **kwargs)
            duration = time.time() - start_time
            
            logger.info(f"CustomProvider generation successful in {duration:.2f}s")
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"CustomProvider generation failed in {duration:.2f}s: {str(e)}")
            raise
```

By following this guide, you can easily integrate any image generation API into the image-generation-api skill and maintain consistent behavior across all providers.