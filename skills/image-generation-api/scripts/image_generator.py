import os
import json
import requests
import time
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod


class BaseImageGenerator(ABC):
    """Base class for image generation providers."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.timeout = 30
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate an image from a prompt."""
        pass
    
    @abstractmethod
    def validate_params(self, **kwargs) -> bool:
        """Validate parameters for image generation."""
        pass


class JimengGenerator(BaseImageGenerator):
    """即梦AI (Jimeng AI) image generation provider."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.endpoint = "https://api.jimeng.ai/v1/images/generations"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def validate_params(self, **kwargs) -> bool:
        """Validate 即梦AI specific parameters."""
        required = ["prompt"]
        for param in required:
            if param not in kwargs:
                return False
        
        # Validate size format
        if "size" in kwargs:
            valid_sizes = ["1024x1024", "512x512", "256x256"]
            if kwargs["size"] not in valid_sizes:
                return False
        
        return True
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate image using 即梦AI API."""
        if not self.validate_params(prompt=prompt, **kwargs):
            raise ValueError("Invalid parameters for 即梦AI")
        
        payload = {
            "prompt": prompt,
            "model": kwargs.get("model", "jimeng-v1"),
            "size": kwargs.get("size", "1024x1024"),
            "quality": kwargs.get("quality", "standard"),
            "n": kwargs.get("n", 1),
            "style": kwargs.get("style", "natural")
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
            raise Exception(f"即梦AI API request failed: {str(e)}")


class OpenAIGenerator(BaseImageGenerator):
    """OpenAI DALL-E image generation provider."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.endpoint = "https://api.openai.com/v1/images/generations"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def validate_params(self, **kwargs) -> bool:
        """Validate OpenAI DALL-E parameters."""
        required = ["prompt"]
        for param in required:
            if param not in kwargs:
                return False
        
        # Validate size format
        if "size" in kwargs:
            valid_sizes = ["1024x1024", "1024x1792", "1792x1024"]
            if kwargs["size"] not in valid_sizes:
                return False
        
        return True
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate image using OpenAI DALL-E API."""
        if not self.validate_params(prompt=prompt, **kwargs):
            raise ValueError("Invalid parameters for OpenAI DALL-E")
        
        payload = {
            "prompt": prompt,
            "n": kwargs.get("n", 1),
            "size": kwargs.get("size", "1024x1024"),
            "quality": kwargs.get("quality", "standard"),
            "style": kwargs.get("style", "vivid")
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
            raise Exception(f"OpenAI API request failed: {str(e)}")


class StabilityAIGenerator(BaseImageGenerator):
    """Stability AI image generation provider."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.endpoint = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def validate_params(self, **kwargs) -> bool:
        """Validate Stability AI parameters."""
        required = ["prompt"]
        for param in required:
            if param not in kwargs:
                return False
        
        return True
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate image using Stability AI API."""
        if not self.validate_params(prompt=prompt, **kwargs):
            raise ValueError("Invalid parameters for Stability AI")
        
        payload = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": kwargs.get("cfg_scale", 7),
            "height": kwargs.get("height", 1024),
            "width": kwargs.get("width", 1024),
            "samples": kwargs.get("n", 1),
            "steps": kwargs.get("steps", 50)
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
            raise Exception(f"Stability AI API request failed: {str(e)}")


class ImageGenerator:
    """Main image generator class with multi-provider support."""
    
    def __init__(self):
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available providers based on API keys."""
        # Initialize 即梦AI
        jimeng_key = os.getenv("JIMENG_API_KEY")
        if jimeng_key:
            self.providers["jimeng"] = JimengGenerator(jimeng_key)
        
        # Initialize OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.providers["openai"] = OpenAIGenerator(openai_key)
        
        # Initialize Stability AI
        stability_key = os.getenv("STABILITY_API_KEY")
        if stability_key:
            self.providers["stability"] = StabilityAIGenerator(stability_key)
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers."""
        return list(self.providers.keys())
    
    def generate(self, provider: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate image using specified provider."""
        if provider not in self.providers:
            raise ValueError(f"Provider '{provider}' not available. Available providers: {self.get_available_providers()}")
        
        generator = self.providers[provider]
        
        # Add retry logic
        max_retries = kwargs.get("max_retries", 3)
        for attempt in range(max_retries):
            try:
                return generator.generate(prompt, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
        
        raise Exception(f"Failed to generate image after {max_retries} attempts")
    
    def batch_generate(self, provider: str, prompts: List[str], **kwargs) -> List[Dict[str, Any]]:
        """Generate multiple images in batch."""
        results = []
        for prompt in prompts:
            try:
                result = self.generate(provider, prompt, **kwargs)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e), "prompt": prompt})
        
        return results