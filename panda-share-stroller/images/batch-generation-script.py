#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
熊猫溜娃共享童车图片批量生成脚本
用于根据配置模板批量生成优化图片
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class ImageGenerator:
    """图片生成器类"""
    
    def __init__(self, config_file: str = "prompt-templates.json"):
        """初始化图片生成器"""
        self.config = self.load_config(config_file)
        self.output_dir = "generated_images"
        self.ensure_output_dir()
    
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"配置文件 {config_file} 未找到")
            return {}
        except json.JSONDecodeError as e:
            print(f"配置文件格式错误: {e}")
            return {}
    
    def ensure_output_dir(self):
        """确保输出目录存在"""
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_product_images(self) -> List[str]:
        """生成产品相关图片"""
        generated_files = []
        
        # 生成主视图
        main_view = self.config["image_generation_templates"]["product_main_view"]
        filename = self.generate_image(
            prompt=main_view["prompt"],
            negative_prompt=main_view["negative_prompt"],
            filename="product_main_view.jpg"
        )
        generated_files.append(filename)
        
        # 生成细节图
        for detail in self.config["image_generation_templates"]["product_detail_views"]:
            filename = self.generate_image(
                prompt=detail["prompt"],
                negative_prompt=detail["negative_prompt"],
                filename=f"product_detail_{detail['name']}.jpg"
            )
            generated_files.append(filename)
        
        return generated_files
    
    def generate_scenario_images(self) -> List[str]:
        """生成场景图片"""
        generated_files = []
        
        for scenario in self.config["image_generation_templates"]["usage_scenarios"]:
            filename = self.generate_image(
                prompt=scenario["prompt"],
                negative_prompt=scenario["negative_prompt"],
                filename=f"scenario_{scenario['name']}.jpg"
            )
            generated_files.append(filename)
        
        return generated_files
    
    def generate_brand_elements(self) -> List[str]:
        """生成品牌元素"""
        generated_files = []
        brand_elements = self.config["image_generation_templates"]["brand_elements"]
        
        # 生成LOGO
        logo_config = brand_elements["logo"]
        filename = self.generate_image(
            prompt=logo_config["prompt"],
            negative_prompt=logo_config["negative_prompt"],
            filename="brand_logo.png",
            format="png"
        )
        generated_files.append(filename)
        
        # 生成水印
        watermark_config = brand_elements["watermark"]
        filename = self.generate_image(
            prompt=watermark_config["prompt"],
            negative_prompt=watermark_config["negative_prompt"],
            filename="brand_watermark.png",
            format="png"
        )
        generated_files.append(filename)
        
        # 生成分享模板
        share_config = brand_elements["share_template"]
        filename = self.generate_image(
            prompt=share_config["prompt"],
            negative_prompt=share_config["negative_prompt"],
            filename="share_template.jpg"
        )
        generated_files.append(filename)
        
        return generated_files
    
    def generate_marketing_materials(self) -> List[str]:
        """生成营销材料"""
        generated_files = []
        
        for material in self.config["image_generation_templates"]["marketing_materials"]:
            filename = self.generate_image(
                prompt=material["prompt"],
                negative_prompt=material["negative_prompt"],
                filename=f"marketing_{material['name']}.jpg"
            )
            generated_files.append(filename)
        
        return generated_files
    
    def generate_image(self, prompt: str, negative_prompt: str, filename: str, format: str = "jpg") -> str:
        """
        生成单张图片
        
        Args:
            prompt: 正面提示词
            negative_prompt: 负面提示词
            filename: 文件名
            format: 文件格式
            
        Returns:
            生成的文件路径
        """
        # 这里可以集成不同的AI图片生成API
        # 目前返回模拟实现
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"{timestamp}_{filename}")
        
        # 模拟生成过程
        print(f"正在生成图片: {filename}")
        print(f"正面提示词: {prompt}")
        print(f"负面提示词: {negative_prompt}")
        
        # 实际使用时，这里应该调用相应的AI图片生成API
        # 例如：
        # if self.use_midjourney:
        #     return self.generate_with_midjourney(prompt, negative_prompt, output_path)
        # elif self.use_dalle:
        #     return self.generate_with_dalle(prompt, negative_prompt, output_path)
        
        # 模拟返回文件路径
        return output_path
    
    def generate_all_images(self) -> Dict[str, List[str]]:
        """生成所有配置的图片"""
        results = {
            "product_images": [],
            "scenario_images": [],
            "brand_elements": [],
            "marketing_materials": []
        }
        
        print("开始批量生成熊猫溜娃共享童车图片...")
        
        # 生成产品图片
        print("\n1. 生成产品展示图片...")
        results["product_images"] = self.generate_product_images()
        
        # 生成场景图片
        print("\n2. 生成使用场景图片...")
        results["scenario_images"] = self.generate_scenario_images()
        
        # 生成品牌元素
        print("\n3. 生成品牌元素...")
        results["brand_elements"] = self.generate_brand_elements()
        
        # 生成营销材料
        print("\n4. 生成营销材料...")
        results["marketing_materials"] = self.generate_marketing_materials()
        
        return results
    
    def create_image_manifest(self, results: Dict[str, List[str]]) -> str:
        """创建图片清单文件"""
        manifest = {
            "generation_date": datetime.now().isoformat(),
            "total_images": sum(len(files) for files in results.values()),
            "categories": results,
            "config_summary": {
                "product_views": len(results["product_images"]),
                "scenarios": len(results["scenario_images"]),
                "brand_elements": len(results["brand_elements"]),
                "marketing_materials": len(results["marketing_materials"])
            }
        }
        
        manifest_path = os.path.join(self.output_dir, "image_manifest.json")
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        return manifest_path

def main():
    """主函数"""
    print("=== 熊猫溜娃共享童车图片批量生成工具 ===")
    print("配置文件: prompt-templates.json")
    print("输出目录: generated_images/")
    print("=" * 50)
    
    # 创建生成器实例
    generator = ImageGenerator()
    
    # 生成所有图片
    results = generator.generate_all_images()
    
    # 创建图片清单
    manifest_path = generator.create_image_manifest(results)
    
    # 输出结果
    print("\n=== 生成完成 ===")
    print(f"总生成图片数: {sum(len(files) for files in results.values())}")
    
    for category, files in results.items():
        print(f"{category}: {len(files)} 个文件")
    
    print(f"\n图片清单: {manifest_path}")
    print("=" * 50)

if __name__ == "__main__":
    main()