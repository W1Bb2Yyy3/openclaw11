#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
熊猫溜娃共享童车图片生成脚本
使用Python生成基础的图像素材
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# 创建输出目录
output_dir = "panda-share-stroller/images/generated"
os.makedirs(output_dir, exist_ok=True)

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_product_main_view():
    """创建产品主视图"""
    fig, ax = plt.subplots(figsize=(9, 5), dpi=100)
    
    # 背景
    ax.set_facecolor('#FFF4F0')
    fig.patch.set_facecolor('#FFF4F0')
    
    # 绘制童车主体框架
    # 车身
    body = patches.Rectangle((3, 1.5), 4, 3, linewidth=3, 
                           edgecolor='#FF6B35', facecolor='#FFFFFF', alpha=0.9)
    ax.add_patch(body)
    
    # 车轮
    wheel1 = patches.Circle((3.5, 1), 0.5, linewidth=2, 
                          edgecolor='#FF6B35', facecolor='#FF8C5A', alpha=0.8)
    wheel2 = patches.Circle((6.5, 1), 0.5, linewidth=2, 
                          edgecolor='#FF6B35', facecolor='#FF8C5A', alpha=0.8)
    ax.add_patch(wheel1)
    ax.add_patch(wheel2)
    
    # 座椅
    seat = patches.Rectangle((3.5, 2.5), 3, 1, linewidth=2, 
                           edgecolor='#FF6B35', facecolor='#FFE4B5', alpha=0.7)
    ax.add_patch(seat)
    
    # 靠背
    backrest = patches.Rectangle((3.5, 3.2), 3, 0.8, linewidth=2, 
                              edgecolor='#FF6B35', facecolor='#FFE4B5', alpha=0.7)
    ax.add_patch(backrest)
    
    # 把手
    handle = patches.Rectangle((3, 4), 4, 0.3, linewidth=2, 
                             edgecolor='#FF6B35', facecolor='#FFFFFF', alpha=0.9)
    ax.add_patch(handle)
    
    # 熊猫耳朵装饰
    ear1 = patches.Circle((3.2, 2.8), 0.3, linewidth=1, 
                        edgecolor='#FF6B35', facecolor='#FFFFFF', alpha=0.8)
    ear2 = patches.Circle((6.8, 2.8), 0.3, linewidth=1, 
                        edgecolor='#FF6B35', facecolor='#FFFFFF', alpha=0.8)
    ax.add_patch(ear1)
    ax.add_patch(ear2)
    
    # 熊猫脸部
    panda_face = patches.Circle((5, 2.5), 0.5, linewidth=1, 
                              edgecolor='#333333', facecolor='#FFFFFF', alpha=0.8)
    ax.add_patch(panda_face)
    
    # 熊猫眼睛
    eye1 = patches.Circle((4.8, 2.6), 0.08, facecolor='#333333')
    eye2 = patches.Circle((5.2, 2.6), 0.08, facecolor='#333333')
    ax.add_patch(eye1)
    ax.add_patch(eye2)
    
    # 熊猫鼻子
    nose = patches.Circle((5, 2.4), 0.06, facecolor='#333333')
    ax.add_patch(nose)
    
    # 添加文字
    ax.text(5, 0.3, '熊猫溜娃共享童车', fontsize=20, fontweight='bold', 
           ha='center', color='#FF6B35')
    ax.text(5, 0, '专业共享，轻松遛娃', fontsize=12, 
           ha='center', color='#666666')
    
    # 品牌LOGO
    ax.text(0.5, 4.5, '🐼', fontsize=16, ha='left', va='top')
    ax.text(0.5, 4.2, '熊猫溜娃', fontsize=10, fontweight='bold', 
           ha='left', va='top', color='#FF6B35')
    
    # 设置坐标轴
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # 保存图片
    filename = f"product_main_view_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(os.path.join(output_dir, filename), dpi=100, bbox_inches='tight', 
                facecolor='#FFF4F0', edgecolor='none')
    plt.close()
    
    print(f"✅ 生成产品主视图: {filename}")
    return filename

def create_shopping_mall_scene():
    """创建商场购物场景"""
    fig, ax = plt.subplots(figsize=(9, 5), dpi=100)
    
    # 背景 - 商场环境
    ax.set_facecolor('#F5F5F5')
    fig.patch.set_facecolor('#F5F5F5')
    
    # 绘制地面
    ground = patches.Rectangle((0, 0), 9, 1, facecolor='#E8E8E8', alpha=0.5)
    ax.add_patch(ground)
    
    # 绘制童车
    body = patches.Rectangle((3, 1.5), 4, 3, linewidth=3, 
                           edgecolor='#FF6B35', facecolor='#FFFFFF', alpha=0.9)
    ax.add_patch(body)
    
    # 车轮
    wheel1 = patches.Circle((3.5, 1), 0.5, linewidth=2, 
                          edgecolor='#FF6B35', facecolor='#FF8C5A', alpha=0.8)
    wheel2 = patches.Circle((6.5, 1), 0.5, linewidth=2, 
                          edgecolor='#FF6B35', facecolor='#FF8C5A', alpha=0.8)
    ax.add_patch(wheel1)
    ax.add_patch(wheel2)
    
    # 座椅上的孩子
    child_head = patches.Circle((5, 3.2), 0.2, facecolor='#FFDBAC', alpha=0.8)
    child_body = patches.Rectangle((4.7, 2.8), 0.6, 0.4, facecolor='#87CEEB', alpha=0.8)
    ax.add_patch(child_head)
    ax.add_patch(child_body)
    
    # 购物车篮子
    basket = patches.Rectangle((3, 2), 4, 0.5, linewidth=2, 
                            edgecolor='#FF6B35', facecolor='#FFB366', alpha=0.7)
    ax.add_patch(basket)
    
    # 商品（模拟）
    items = [
        patches.Circle((3.5, 2.2), 0.1, facecolor='#FF6347', alpha=0.8),
        patches.Circle((4.5, 2.2), 0.1, facecolor='#32CD32', alpha=0.8),
        patches.Circle((5.5, 2.2), 0.1, facecolor '#FFD700', alpha=0.8),
    ]
    for item in items:
        ax.add_patch(item)
    
    # 推车的妈妈
    mom_head = patches.Circle((6.5, 3.2), 0.2, facecolor='#FFDBAC', alpha=0.8)
    mom_body = patches.Rectangle((6.2, 2.8), 0.6, 0.5, facecolor='#FF69B4', alpha=0.8)
    mom_arm = patches.Rectangle((6.2, 3), 0.8, 0.15, facecolor='#FF69B4', alpha=0.8)
    ax.add_patch(mom_head)
    ax.add_patch(mom_body)
    ax.add_patch(mom_arm)
    
    # 商场环境装饰
    # 柱子
    pillar1 = patches.Rectangle((1, 0), 0.2, 4.5, facecolor='#D3D3D3', alpha=0.6)
    pillar2 = patches.Rectangle((7.8, 0), 0.2, 4.5, facecolor='#D3D3D3', alpha=0.6)
    ax.add_patch(pillar1)
    ax.add_patch(pillar2)
    
    # 灯光效果
    light1 = patches.Circle((1.5, 4.5), 0.5, facecolor='#FFFACD', alpha=0.3)
    light2 = patches.Circle((7.5, 4.5), 0.5, facecolor='#FFFACD', alpha=0.3)
    ax.add_patch(light1)
    ax.add_patch(light2)
    
    # 文字
    ax.text(5, 0.3, '商场购物场景', fontsize=18, fontweight='bold', 
           ha='center', color='#FF6B35')
    ax.text(5, 0, '轻松选购，遛娃无忧', fontsize=12, 
           ha='center', color='#666666')
    
    # 品牌LOGO
    ax.text(0.5, 4.5, '🐼', fontsize=16, ha='left', va='top')
    ax.text(0.5, 4.2, '熊猫溜娃', fontsize=10, fontweight='bold', 
           ha='left', va='top', color='#FF6B35')
    
    # 设置坐标轴
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # 保存图片
    filename = f"shopping_mall_scene_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(os.path.join(output_dir, filename), dpi=100, bbox_inches='tight', 
                facecolor='#F5F5F5', edgecolor='none')
    plt.close()
    
    print(f"✅ 生成商场购物场景: {filename}")
    return filename

def create_park_scene():
    """创建公园游玩场景"""
    fig, ax = plt.subplots(figsize=(9, 5), dpi=100)
    
    # 背景 - 公园环境
    ax.set_facecolor('#E8F5E8')
    fig.patch.set_facecolor('#E8F5E8')
    
    # 天空渐变效果
    sky_gradient = np.linspace([0.9, 1, 0.9], [0.6, 0.8, 0.6], 100).reshape(100, 1, 3)
    ax.imshow(sky_gradient, extent=[0, 9, 3, 5], aspect='auto')
    
    # 草地
    grass = patches.Rectangle((0, 0), 9, 3, facecolor='#90EE90', alpha=0.7)
    ax.add_patch(grass)
    
    # 童车
    body = patches.Rectangle((3, 1.5), 4, 3, linewidth=3, 
                           edgecolor='#FF6B35', facecolor='#FFFFFF', alpha=0.9)
    ax.add_patch(body)
    
    # 车轮
    wheel1 = patches.Circle((3.5, 1), 0.5, linewidth=2, 
                          edgecolor='#FF6B35', facecolor='#FF8C5A', alpha=0.8)
    wheel2 = patches.Circle((6.5, 1), 0.5, linewidth=2, 
                          edgecolor='#FF6B35', facecolor='#FF8C5A', alpha=0.8)
    ax.add_patch(wheel1)
    ax.add_patch(wheel2)
    
    # 座椅上的孩子
    child_head = patches.Circle((5, 3.2), 0.2, facecolor='#FFDBAC', alpha=0.8)
    child_body = patches.Rectangle((4.7, 2.8), 0.6, 0.4, facecolor='#87CEEB', alpha=0.8)
    ax.add_patch(child_head)
    ax.add_patch(child_body)
    
    # 树木装饰
    tree1 = patches.Circle((1, 2.5), 0.8, facecolor='#228B22', alpha=0.8)
    tree_trunk1 = patches.Rectangle((0.8, 0), 0.4, 2.5, facecolor='#8B4513', alpha=0.8)
    ax.add_patch(tree1)
    ax.add_patch(tree_trunk1)
    
    tree2 = patches.Circle((8, 2.8), 0.6, facecolor='#228B22', alpha=0.8)
    tree_trunk2 = patches.Rectangle((7.7, 0), 0.6, 2.8, facecolor='#8B4513', alpha=0.8)
    ax.add_patch(tree2)
    ax.add_patch(tree_trunk2)
    
    # 花朵
    for i, (x, y) in enumerate([(1.5, 0.2), (2, 0.3), (7, 0.2), (7.5, 0.3)]):
        flower = patches.Circle((x, y), 0.15, facecolor='#FF69B4', alpha=0.8)
        ax.add_patch(flower)
        center = patches.Circle((x, y), 0.05, facecolor='#FFD700', alpha=0.8)
        ax.add_patch(center)
    
    # 阳光效果
    sun = patches.Circle((7.5, 4.5), 0.4, facecolor='#FFD700', alpha=0.8)
    ax.add_patch(sun)
    
    # 云朵
    cloud1 = patches.Ellipse((2, 4.2), 1.2, 0.4, facecolor='#FFFFFF', alpha=0.8)
    cloud2 = patches.Ellipse((6, 4.5), 1.0, 0.35, facecolor='#FFFFFF', alpha=0.8)
    ax.add_patch(cloud1)
    ax.add_patch(cloud2)
    
    # 文字
    ax.text(5, 0.3, '公园游玩场景', fontsize=18, fontweight='bold', 
           ha='center', color='#FF6B35')
    ax.text(5, 0, '亲近自然，快乐遛娃', fontsize=12, 
           ha='center', color='#666666')
    
    # 品牌LOGO
    ax.text(0.5, 4.5, '🐼', fontsize=16, ha='left', va='top')
    ax.text(0.5, 4.2, '熊猫溜娃', fontsize=10, fontweight='bold', 
           ha='left', va='top', color='#FF6B35')
    
    # 设置坐标轴
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # 保存图片
    filename = f"park_scene_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(os.path.join(output_dir, filename), dpi=100, bbox_inches='tight', 
                facecolor='#E8F5E8', edgecolor='none')
    plt.close()
    
    print(f"✅ 生成公园游玩场景: {filename}")
    return filename

def create_hospital_scene():
    """创建医院就诊场景"""
    fig, ax = plt.subplots(figsize=(9, 5), dpi=100)
    
    # 背景 - 医院环境
    ax.set_facecolor('#F0F8FF')
    fig.patch.set_facecolor('#F0F8FF')
    
    # 地板
    floor = patches.Rectangle((0, 0), 9, 2, facecolor='#E6E6FA', alpha=0.5)
    ax.add_patch(floor)
    
    # 墙壁
    wall = patches.Rectangle((0, 2), 9, 3, facecolor='#F5F5F5', alpha=0.8)
    ax.add_patch(wall)
    
    # 童车
    body = patches.Rectangle((3, 1.5), 4, 3, linewidth=3, 
                           edgecolor='#FF6B35', facecolor='#FFFFFF', alpha=0.9)
    ax.add_patch(body)
    
    # 车轮
    wheel1 = patches.Circle((3.5, 1), 0.5, linewidth=2, 
                          edgecolor='#FF6B35', facecolor='#FF8C5A', alpha=0.8)
    wheel2 = patches.Circle((6.5, 1), 0.5, linewidth=2, 
                          edgecolor='#FF6B35', facecolor='#FF8C5A', alpha=0.8)
    ax.add_patch(wheel1)
    ax.add_patch(wheel2)
    
    # 座椅上的孩子
    child_head = patches.Circle((5, 3.2), 0.2, facecolor='#FFDBAC', alpha=0.8)
    child_body = patches.Rectangle((4.7, 2.8), 0.6, 0.4, facecolor='#87CEEB', alpha=0.8)
    ax.add_patch(child_head)
    ax.add_patch(child_body)
    
    # 医院装饰
    # 窗户
    window = patches.Rectangle((1, 2.8), 1.2, 1.2, facecolor='#87CEEB', alpha=0.6)
    ax.add_patch(window)
    window_frame = patches.Rectangle((1, 2.8), 1.2, 1.2, linewidth=2, 
                                   edgecolor='#4682B4', facecolor='none')
    ax.add_patch(window_frame)
    
    # 门
    door = patches.Rectangle((7, 2.5), 1, 1.8, facecolor='#DEB887', alpha=0.8)
    ax.add_patch(door)
    door_handle = patches.Circle((7.8, 2.9), 0.05, facecolor='#8B4513', alpha=0.8)
    ax.add_patch(door_handle)
    
    # 医疗符号（十字）
    cross = patches.Rectangle((4, 4.2), 0.2, 0.6, facecolor='#FF0000', alpha=0.8)
    cross2 = patches.Rectangle((3.7, 4.3), 0.8, 0.2, facecolor='#FF0000', alpha=0.8)
    ax.add_patch(cross)
    ax.add_patch(cross2)
    
    # 等候椅
    bench = patches.Rectangle((1.5, 0.8), 1.5, 0.3, facecolor='#8B4513', alpha=0.8)
    ax.add_patch(bench)
    
    # 文字
    ax.text(5, 0.3, '医院就诊场景', fontsize=18, fontweight='bold', 
           ha='center', color='#FF6B35')
    ax.text(5, 0, '舒适等候，减轻负担', fontsize=12, 
           ha='center', color='#666666')
    
    # 品牌LOGO
    ax.text(0.5, 4.5, '🐼', fontsize=16, ha='left', va='top')
    ax.text(0.5, 4.2, '熊猫溜娃', fontsize=10, fontweight='bold', 
           ha='left', va='top', color='#FF6B35')
    
    # 设置坐标轴
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # 保存图片
    filename = f"hospital_scene_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(os.path.join(output_dir, filename), dpi=100, bbox_inches='tight', 
                facecolor='#F0F8FF', edgecolor='none')
    plt.close()
    
    print(f"✅ 生成医院就诊场景: {filename}")
    return filename

def create_comparison_chart():
    """创建对比图表"""
    fig, ax = plt.subplots(figsize=(9, 5), dpi=100)
    
    # 背景
    ax.set_facecolor('#FFF4F0')
    fig.patch.set_facecolor('#FFF4F0')
    
    # 对比项目
    categories = ['购买成本', '携带便利', '卫生安全', '使用灵活性', '存储空间']
    traditional_scores = [9, 3, 7, 4, 2]  # 传统童车（分数越低越好）
    shared_scores = [2, 9, 8, 9, 9]      # 共享童车（分数越低越好）
    
    x = np.arange(len(categories))
    width = 0.35
    
    # 绘制柱状图
    bars1 = ax.bar(x - width/2, traditional_scores, width, 
                   label='传统童车', color='#FF9999', alpha=0.8)
    bars2 = ax.bar(x + width/2, shared_scores, width, 
                   label='共享童车', color='#FF6B35', alpha=0.8)
    
    # 添加数值标签
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height}', ha='center', va='bottom', fontsize=10)
    
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height}', ha='center', va='bottom', fontsize=10)
    
    # 设置图表
    ax.set_ylabel('评分（分数越低越好）', fontsize=12)
    ax.set_title('传统童车 vs 共享童车 对比', fontsize=16, fontweight='bold', 
                color='#FF6B35')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.legend(loc='upper right', fontsize=10)
    
    # 添加优势说明
    ax.text(0.02, 0.98, '共享童车优势：', transform=ax.transAxes, 
           fontsize=12, fontweight='bold', va='top', color='#FF6B35')
    advantages = [
        '✓ 经济实惠，按需付费',
        '✓ 轻便便携，随时随地',
        '✓ 专业消毒，卫生保障',
        '✓ 使用灵活，扫码即用',
        '✓ 无需存储，节省空间'
    ]
    
    for i, advantage in enumerate(advantages):
        ax.text(0.02, 0.93 - i*0.05, advantage, transform=ax.transAxes, 
               fontsize=10, va='top', color='#666666')
    
    # 品牌LOGO
    ax.text(0.85, 0.95, '🐼', fontsize=16, transform=ax.transAxes, 
           ha='left', va='top')
    ax.text(0.85, 0.90, '熊猫溜娃', fontsize=10, fontweight='bold', 
           transform=ax.transAxes, ha='left', va='top', color='#FF6B35')
    
    # 网格线
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_ylim(0, 10)
    
    # 保存图片
    filename = f"comparison_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(os.path.join(output_dir, filename), dpi=100, bbox_inches='tight', 
                facecolor='#FFF4F0', edgecolor='none')
    plt.close()
    
    print(f"✅ 生成对比图表: {filename}")
    return filename

def main():
    """主函数"""
    print("=== 开始生成熊猫溜娃共享童车图片 ===")
    
    # 生成所有图片
    generated_files = []
    
    generated_files.append(create_product_main_view())
    generated_files.append(create_shopping_mall_scene())
    generated_files.append(create_park_scene())
    generated_files.append(create_hospital_scene())
    generated_files.append(create_comparison_chart())
    
    # 输出结果
    print("\n=== 生成完成 ===")
    print(f"总共生成 {len(generated_files)} 张图片")
    print(f"保存目录: {output_dir}")
    
    for filename in generated_files:
        print(f"✓ {filename}")
    
    # 创建清单文件
    manifest_file = os.path.join(output_dir, "generated_manifest.txt")
    with open(manifest_file, 'w', encoding='utf-8') as f:
        f.write("熊猫溜娃共享童车 - 图片生成清单\n")
        f.write("=" * 50 + "\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"生成数量: {len(generated_files)}\n")
        f.write(f"保存目录: {output_dir}\n")
        f.write("\n生成的图片文件:\n")
        
        for filename in generated_files:
            f.write(f"• {filename}\n")
        
        f.write("\n图片用途:\n")
        f.write("• product_main_view.png: 产品主视图，适合公众号封面\n")
        f.write("• shopping_mall_scene.png: 商场购物场景\n")
        f.write("• park_scene.png: 公园游玩场景\n")
        f.write("• hospital_scene.png: 医院就诊场景\n")
        f.write("• comparison_chart.png: 对比图表，突出优势\n")
    
    print(f"📋 清单文件: {manifest_file}")

if __name__ == "__main__":
    main()