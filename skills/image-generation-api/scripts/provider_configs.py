import os
import json
import yaml
from typing import Dict, Any, Optional


class ProviderConfig:
    """Configuration manager for image generation providers."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or os.path.join(os.path.dirname(__file__), "..", "references", "provider_configs.yaml")
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        default_config = {
            "providers": {
                "jimeng": {
                    "name": "即梦AI",
                    "endpoint": "https://api.jimeng.ai/v1/images/generations",
                    "required_params": ["prompt"],
                    "supported_sizes": ["1024x1024", "512x512", "256x256"],
                    "supported_qualities": ["standard", "hd"],
                    "supported_styles": ["natural", "anime", "realistic"],
                    "rate_limit": {
                        "requests_per_minute": 60,
                        "tokens_per_minute": 10000
                    }
                },
                "openai": {
                    "name": "OpenAI DALL-E",
                    "endpoint": "https://api.openai.com/v1/images/generations",
                    "required_params": ["prompt"],
                    "supported_sizes": ["1024x1024", "1024x1792", "1792x1024"],
                    "supported_qualities": ["standard", "hd"],
                    "supported_styles": ["vivid", "natural"],
                    "rate_limit": {
                        "requests_per_minute": 50,
                        "tokens_per_minute": 100000
                    }
                },
                "stability": {
                    "name": "Stability AI",
                    "endpoint": "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                    "required_params": ["prompt"],
                    "supported_sizes": ["1024x1024", "512x512", "768x768"],
                    "supported_qualities": ["standard", "high"],
                    "supported_styles": ["realistic", "artistic", "cartoon"],
                    "rate_limit": {
                        "requests_per_minute": 100,
                        "tokens_per_minute": 50000
                    }
                }
            },
            "global": {
                "timeout": 30,
                "max_retries": 3,
                "retry_delay": 1
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                    # Merge with default config
                    default_config.update(user_config)
            except Exception as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")
        
        return default_config
    
    def save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            raise Exception(f"Could not save config file: {e}")
    
    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """Get configuration for specific provider."""
        if provider not in self.config["providers"]:
            raise ValueError(f"Provider '{provider}' not found in configuration")
        return self.config["providers"][provider]
    
    def get_all_providers(self) -> Dict[str, Dict[str, Any]]:
        """Get all provider configurations."""
        return self.config["providers"]
    
    def get_available_providers(self) -> list:
        """Get list of providers with valid API keys."""
        available = []
        env_vars = {
            "jimeng": "JIMENG_API_KEY",
            "openai": "OPENAI_API_KEY",
            "stability": "STABILITY_API_KEY"
        }
        
        for provider, env_var in env_vars.items():
            if os.getenv(env_var):
                available.append(provider)
        
        return available
    
    def add_provider(self, provider_name: str, config: Dict[str, Any]):
        """Add new provider configuration."""
        self.config["providers"][provider_name] = config
        self.save_config()
    
    def remove_provider(self, provider_name: str):
        """Remove provider configuration."""
        if provider_name in self.config["providers"]:
            del self.config["providers"][provider_name]
            self.save_config()
    
    def update_provider(self, provider_name: str, updates: Dict[str, Any]):
        """Update provider configuration."""
        if provider_name not in self.config["providers"]:
            raise ValueError(f"Provider '{provider_name}' not found")
        
        self.config["providers"][provider_name].update(updates)
        self.save_config()
    
    def validate_api_key(self, provider: str) -> bool:
        """Validate that API key exists for provider."""
        env_vars = {
            "jimeng": "JIMENG_API_KEY",
            "openai": "OPENAI_API_KEY",
            "stability": "STABILITY_API_KEY"
        }
        
        if provider not in env_vars:
            return False
        
        api_key = os.getenv(env_vars[provider])
        return bool(api_key and api_key.strip())
    
    def get_rate_limit_info(self, provider: str) -> Dict[str, Any]:
        """Get rate limit information for provider."""
        config = self.get_provider_config(provider)
        return config.get("rate_limit", {})
    
    def get_supported_parameters(self, provider: str) -> Dict[str, Any]:
        """Get supported parameters for provider."""
        config = self.get_provider_config(provider)
        return {
            "required": config.get("required_params", []),
            "sizes": config.get("supported_sizes", []),
            "qualities": config.get("supported_qualities", []),
            "styles": config.get("supported_styles", [])
        }


# Global configuration instance
config = ProviderConfig()