#!/usr/bin/env python3
"""
Image Generation API Usage Examples

This script demonstrates how to use the image generation API skill
to generate images using different providers.
"""

import os
import sys
import json
from typing import Dict, Any, List

# Add the scripts directory to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from image_generator import ImageGenerator
from provider_configs import ProviderConfig
from utils import ParameterValidator, ImageUtils


def setup_environment():
    """Set up environment variables and configuration."""
    print("Setting up environment...")
    
    # Check required environment variables
    required_env_vars = {
        "JIMENG_API_KEY": "即梦AI API Key",
        "OPENAI_API_KEY": "OpenAI API Key", 
        "STABILITY_API_KEY": "Stability AI API Key"
    }
    
    missing_vars = []
    for var, description in required_env_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"{var}: {description}")
    
    if missing_vars:
        print("⚠️  Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these environment variables before running the examples.")
        return False
    
    return True


def demo_basic_generation():
    """Demonstrate basic image generation."""
    print("\n🎨 Basic Image Generation Demo")
    print("=" * 50)
    
    generator = ImageGenerator()
    available_providers = generator.get_available_providers()
    
    if not available_providers:
        print("❌ No available providers (check API keys)")
        return
    
    print(f"✅ Available providers: {', '.join(available_providers)}")
    
    # Generate images with each available provider
    for provider in available_providers:
        try:
            print(f"\n📸 Generating image with {provider}...")
            
            result = generator.generate(
                provider=provider,
                prompt="A beautiful sunset over mountains",
                size="1024x1024",
                quality="standard"
            )
            
            if result.get("success"):
                images = result.get("images", [])
                print(f"✅ Generated {len(images)} image(s)")
                
                for i, img in enumerate(images):
                    if "url" in img:
                        print(f"   Image {i+1}: {img['url']}")
                    else:
                        print(f"   Image {i+1}: Data embedded in response")
            else:
                print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error generating image: {str(e)}")


def demo_batch_generation():
    """Demonstrate batch image generation."""
    print("\n🔄 Batch Generation Demo")
    print("=" * 50)
    
    generator = ImageGenerator()
    available_providers = generator.get_available_providers()
    
    if not available_providers:
        print("❌ No available providers")
        return
    
    # Generate multiple images in batch
    prompts = [
        "A cute cat",
        "A beautiful dog", 
        "A colorful bird"
    ]
    
    provider = available_providers[0]  # Use first available provider
    print(f"Generating {len(prompts)} images with {provider}...")
    
    try:
        results = generator.batch_generate(
            provider=provider,
            prompts=prompts,
            size="512x512",
            quality="standard"
        )
        
        print(f"✅ Generated {len(results)} results")
        
        for i, result in enumerate(results):
            prompt = prompts[i]
            if result.get("success"):
                images = result.get("images", [])
                print(f"✅ '{prompt}': {len(images)} image(s)")
            else:
                print(f"❌ '{prompt}': {result.get('error', 'Unknown error')}")
                
    except Exception as e:
        print(f"❌ Batch generation failed: {str(e)}")


def demo_parameter_validation():
    """Demonstrate parameter validation."""
    print("\n🔍 Parameter Validation Demo")
    print("=" * 50)
    
    validator = ParameterValidator()
    
    # Test prompt validation
    test_prompts = [
        "A beautiful landscape",
        "",
        "A very long prompt that exceeds reasonable length " * 10,
        "violent content warning"
    ]
    
    print("Prompt validation results:")
    for prompt in test_prompts:
        result = validator.validate_prompt(prompt)
        status = "✅ Valid" if result["valid"] else "❌ Invalid"
        print(f"   '{prompt[:50]}...': {status}")
        if result["warnings"]:
            for warning in result["warnings"]:
                print(f"      ⚠️  {warning}")
    
    # Test size validation for each provider
    provider_config = ProviderConfig()
    for provider in provider_config.get_all_providers():
        size_result = validator.validate_size("1024x1024", provider)
        status = "✅ Valid" if size_result["valid"] else "❌ Invalid"
        print(f"   {provider} size 1024x1024: {status}")


def demo_image_processing():
    """Demonstrate image processing utilities."""
    print("\n🖼️ Image Processing Demo")
    print("=" * 50)
    
    # Test image validation
    # Note: This is a demo - in real usage you'd have actual image data
    print("Image validation utilities:")
    print("   ✅ ImageUtils.validate_image_format() - Validates image format")
    print("   ✅ ImageUtils.get_image_info() - Gets image metadata")
    print("   ✅ ImageUtils.resize_image() - Resizes images")
    print("   ✅ ImageUtils.convert_to_base64() - Converts to base64")
    
    # Example of parameter validation
    validator = ParameterValidator()
    size_result = validator.validate_size("1024x1024", "jimeng")
    print(f"\nSize validation result: {size_result}")


def demo_configuration_management():
    """Demonstrate configuration management."""
    print("\n⚙️ Configuration Management Demo")
    print("=" * 50)
    
    config = ProviderConfig()
    
    print(f"Available providers: {list(config.get_all_providers().keys())}")
    print(f"Available providers with valid keys: {config.get_available_providers()}")
    
    # Show configuration for a provider
    if config.get_available_providers():
        provider = config.get_available_providers()[0]
        provider_config = config.get_provider_config(provider)
        print(f"\nConfiguration for {provider}:")
        print(f"   Name: {provider_config['name']}")
        print(f"   Endpoint: {provider_config['endpoint']}")
        print(f"   Supported sizes: {provider_config['supported_sizes']}")
        print(f"   Rate limit: {provider_config['rate_limit']}")


def demo_error_handling():
    """Demonstrate error handling."""
    print("\n❌ Error Handling Demo")
    print("=" * 50)
    
    generator = ImageGenerator()
    
    # Test with invalid provider
    try:
        result = generator.generate("invalid_provider", "test prompt")
        print(f"Result: {result}")
    except Exception as e:
        print(f"✅ Error caught: {str(e)}")
    
    # Test with invalid prompt
    try:
        result = generator.generate("jimeng", "")  # Empty prompt
        print(f"Result: {result}")
    except Exception as e:
        print(f"✅ Error caught: {str(e)}")


def demo_provider_comparison():
    """Compare different providers for the same prompt."""
    print("\n🔍 Provider Comparison Demo")
    print("=" * 50)
    
    generator = ImageGenerator()
    available_providers = generator.get_available_providers()
    
    if len(available_providers) < 2:
        print("❌ Need at least 2 providers for comparison")
        return
    
    prompt = "A beautiful sunset"
    
    print(f"Comparing providers for prompt: '{prompt}'")
    
    results = {}
    for provider in available_providers:
        try:
            print(f"\n📸 Testing {provider}...")
            result = generator.generate(
                provider=provider,
                prompt=prompt,
                size="512x512",
                quality="standard"
            )
            results[provider] = result
            
            if result.get("success"):
                images = result.get("images", [])
                print(f"   ✅ Generated {len(images)} image(s)")
            else:
                print(f"   ❌ Failed: {result.get('error')}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results[provider] = {"error": str(e)}
    
    # Summary
    print(f"\n📊 Summary:")
    successful = {p: r for p, r in results.items() if r.get("success")}
    failed = {p: r for p, r in results.items() if not r.get("success")}
    
    print(f"✅ Successful: {len(successful)} providers")
    print(f"❌ Failed: {len(failed)} providers")
    
    for provider, result in successful.items():
        images = result.get("images", [])
        print(f"   {provider}: {len(images)} image(s)")


def main():
    """Main function to run all demos."""
    print("🚀 Image Generation API Demo")
    print("=" * 50)
    
    # Check if we have the required environment setup
    if not setup_environment():
        print("\n💡 To set up environment variables:")
        print("   export JIMENG_API_KEY='your_jimeng_key'")
        print("   export OPENAI_API_KEY='your_openai_key'")
        print("   export STABILITY_API_KEY='your_stability_key'")
        return
    
    # Run all demos
    demo_basic_generation()
    demo_batch_generation()
    demo_parameter_validation()
    demo_image_processing()
    demo_configuration_management()
    demo_error_handling()
    demo_provider_comparison()
    
    print("\n🎉 Demo completed!")
    print("\n💡 Next steps:")
    print("   1. Set your API keys as environment variables")
    print("   2. Try generating images with your own prompts")
    print("   3. Experiment with different parameters")
    print("   4. Add your own custom providers")


if __name__ == "__main__":
    main()