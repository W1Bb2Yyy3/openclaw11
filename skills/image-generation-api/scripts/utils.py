import os
import json
import requests
from typing import Dict, Any, Optional, Union
from PIL import Image
import io
import base64
import hashlib
import logging


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageUtils:
    """Utility functions for image processing and validation."""
    
    @staticmethod
    def download_image(url: str, save_path: Optional[str] = None) -> bytes:
        """Download image from URL."""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            image_data = response.content
            
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(image_data)
                logger.info(f"Image saved to {save_path}")
            
            return image_data
        except Exception as e:
            raise Exception(f"Failed to download image: {str(e)}")
    
    @staticmethod
    def save_image(image_data: bytes, filename: str, directory: str = "output") -> str:
        """Save image data to file."""
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        
        try:
            with open(filepath, 'wb') as f:
                f.write(image_data)
            logger.info(f"Image saved to {filepath}")
            return filepath
        except Exception as e:
            raise Exception(f"Failed to save image: {str(e)}")
    
    @staticmethod
    def validate_image_format(image_data: bytes, allowed_formats: list = None) -> bool:
        """Validate image format."""
        if allowed_formats is None:
            allowed_formats = ['JPEG', 'PNG', 'GIF', 'WEBP']
        
        try:
            img = Image.open(io.BytesIO(image_data))
            return img.format in allowed_formats
        except Exception as e:
            logger.error(f"Image validation failed: {str(e)}")
            return False
    
    @staticmethod
    def resize_image(image_data: bytes, max_size: tuple = (1024, 1024)) -> bytes:
        """Resize image while maintaining aspect ratio."""
        try:
            img = Image.open(io.BytesIO(image_data))
            
            # Calculate new size maintaining aspect ratio
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save to bytes
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG', quality=85)
            img_buffer.seek(0)
            
            return img_buffer.getvalue()
        except Exception as e:
            raise Exception(f"Failed to resize image: {str(e)}")
    
    @staticmethod
    def get_image_info(image_data: bytes) -> Dict[str, Any]:
        """Get image metadata."""
        try:
            img = Image.open(io.BytesIO(image_data))
            return {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "width": img.width,
                "height": img.height,
                "has_transparency": img.mode in ('RGBA', 'LA') or 'transparency' in img.info
            }
        except Exception as e:
            raise Exception(f"Failed to get image info: {str(e)}")
    
    @staticmethod
    def convert_to_base64(image_data: bytes) -> str:
        """Convert image data to base64 string."""
        return base64.b64encode(image_data).decode('utf-8')
    
    @staticmethod
    def convert_to_bytes(base64_string: str) -> bytes:
        """Convert base64 string to bytes."""
        return base64.b64decode(base64_string)
    
    @staticmethod
    def calculate_hash(image_data: bytes) -> str:
        """Calculate MD5 hash of image data."""
        return hashlib.md5(image_data).hexdigest()


class ParameterValidator:
    """Parameter validation utilities."""
    
    @staticmethod
    def validate_prompt(prompt: str) -> Dict[str, Any]:
        """Validate prompt parameter."""
        errors = []
        warnings = []
        
        if not prompt or not prompt.strip():
            errors.append("Prompt cannot be empty")
        elif len(prompt) > 1000:
            warnings.append("Prompt is very long, consider making it more concise")
        
        # Check for potentially problematic content
        problematic_keywords = [
            "violence", "nudity", "explicit", "adult", "hate", "discrimination"
        ]
        lower_prompt = prompt.lower()
        for keyword in problematic_keywords:
            if keyword in lower_prompt:
                warnings.append(f"Prompt contains potentially sensitive content: {keyword}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    @staticmethod
    def validate_size(size: str, provider: str) -> Dict[str, Any]:
        """Validate size parameter."""
        from .provider_configs import config
        
        try:
            width, height = map(int, size.split('x'))
            if width <= 0 or height <= 0:
                return {"valid": False, "errors": ["Size must be positive"]}
            
            # Check provider-specific size limits
            provider_config = config.get_provider_config(provider)
            supported_sizes = provider_config.get("supported_sizes", [])
            
            if size not in supported_sizes:
                return {
                    "valid": False,
                    "errors": [f"Size {size} not supported by provider {provider}"],
                    "supported_sizes": supported_sizes
                }
            
            return {"valid": True}
            
        except ValueError:
            return {
                "valid": False,
                "errors": ["Size must be in format WIDTHxHEIGHT (e.g., 1024x1024)"]
            }
    
    @staticmethod
    def validate_quality(quality: str, provider: str) -> Dict[str, Any]:
        """Validate quality parameter."""
        from .provider_configs import config
        
        provider_config = config.get_provider_config(provider)
        supported_qualities = provider_config.get("supported_qualities", [])
        
        if quality not in supported_qualities:
            return {
                "valid": False,
                "errors": [f"Quality {quality} not supported by provider {provider}"],
                "supported_qualities": supported_qualities
            }
        
        return {"valid": True}
    
    @staticmethod
    def validate_style(style: str, provider: str) -> Dict[str, Any]:
        """Validate style parameter."""
        from .provider_configs import config
        
        provider_config = config.get_provider_config(provider)
        supported_styles = provider_config.get("supported_styles", [])
        
        if style not in supported_styles:
            return {
                "valid": False,
                "errors": [f"Style {style} not supported by provider {provider}"],
                "supported_styles": supported_styles
            }
        
        return {"valid": True}


class APIRateLimiter:
    """Rate limiting utilities for API calls."""
    
    def __init__(self, provider: str):
        from .provider_configs import config
        self.provider = provider
        self.config = config
        self.rate_limits = config.get_rate_limit_info(provider)
        self.requests = []
    
    def check_rate_limit(self) -> bool:
        """Check if API call is allowed based on rate limits."""
        import time
        
        now = time.time()
        requests_per_minute = self.rate_limits.get("requests_per_minute", 60)
        
        # Remove requests older than 1 minute
        self.requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        if len(self.requests) >= requests_per_minute:
            return False
        
        return True
    
    def record_request(self):
        """Record an API request."""
        import time
        self.requests.append(time.time())
    
    def get_wait_time(self) -> float:
        """Get required wait time before next request."""
        import time
        
        now = time.time()
        requests_per_minute = self.rate_limits.get("requests_per_minute", 60)
        
        if len(self.requests) < requests_per_minute:
            return 0
        
        oldest_request = min(self.requests)
        return max(0, 60 - (now - oldest_request))


class ResponseHandler:
    """Handle and standardize API responses."""
    
    @staticmethod
    def standardize_response(provider: str, raw_response: Dict[str, Any]) -> Dict[str, Any]:
        """Standardize response from different providers."""
        standardized = {
            "provider": provider,
            "success": True,
            "images": [],
            "metadata": {}
        }
        
        try:
            if provider == "jimeng":
                # Handle 即梦AI response format
                if "data" in raw_response:
                    for img_data in raw_response["data"]:
                        standardized["images"].append({
                            "url": img_data.get("url"),
                            "revised_prompt": img_data.get("revised_prompt"),
                            "seed": img_data.get("seed")
                        })
            
            elif provider == "openai":
                # Handle OpenAI response format
                if "data" in raw_response:
                    for img_data in raw_response["data"]:
                        standardized["images"].append({
                            "url": img_data.get("url"),
                            "revised_prompt": img_data.get("revised_prompt")
                        })
            
            elif provider == "stability":
                # Handle Stability AI response format
                if "artifacts" in raw_response:
                    for artifact in raw_response["artifacts"]:
                        standardized["images"].append({
                            "url": f"data:image/png;base64,{artifact.get('base64')}",
                            "seed": artifact.get("seed")
                        })
            
            standardized["metadata"] = {
                "raw_response": raw_response,
                "timestamp": standardized.get("timestamp")
            }
            
        except Exception as e:
            standardized["success"] = False
            standardized["error"] = str(e)
        
        return standardized
    
    @staticmethod
    def handle_error(provider: str, error: Exception) -> Dict[str, Any]:
        """Handle API errors."""
        error_info = {
            "provider": provider,
            "success": False,
            "error": str(error),
            "error_type": type(error).__name__
        }
        
        # Add provider-specific error handling
        if provider == "openai":
            if "rate limit" in str(error).lower():
                error_info["retry_after"] = 60
            elif "invalid api key" in str(error).lower():
                error_info["action"] = "check_api_key"
        
        return error_info