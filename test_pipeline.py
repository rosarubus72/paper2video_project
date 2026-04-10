#!/usr/bin/env python3
import os
import sys
import subprocess

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 测试函数
def test_pdf_parser():
    """测试PDF解析模块"""
    print("测试PDF解析模块...")
    # 复制测试PDF文件
    test_pdf = os.path.join(script_dir, "data", "pdfs", "test_paper.pdf")
    if not os.path.exists(test_pdf):
        # 创建一个简单的测试PDF
        print("创建测试PDF文件...")
        os.makedirs(os.path.dirname(test_pdf), exist_ok=True)
        # 使用echo创建一个简单的PDF（实际项目中应该使用真实的PDF）
        with open(test_pdf, "w") as f:
            f.write("%PDF-1.4\n1 0 obj<<>>endobj\nxref\ntrailer<<>>\n%%EOF")
    
    # 检查PDF解析模块文件是否存在
    parser_file = os.path.join(script_dir, "modules", "pdf_parser", "pdf_parser.py")
    if os.path.exists(parser_file):
        print("✅ PDF解析模块文件存在")
    else:
        print("❌ PDF解析模块文件不存在")

def test_script_gen():
    """测试脚本生成模块"""
    print("\n测试脚本生成模块...")
    # 检查API密钥是否配置
    config_path = os.path.join(script_dir, "config", "config.yaml")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            content = f.read()
        if "sk-" in content:
            print("✅ API密钥已配置")
        else:
            print("⚠️  API密钥未配置，请在config.yaml中设置")
    else:
        print("❌ 配置文件不存在")

def test_audio_gen():
    """测试音频生成模块"""
    print("\n测试音频生成模块...")
    # 检查FFmpeg是否安装
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ FFmpeg已安装")
    else:
        print("❌ FFmpeg未安装，请安装FFmpeg")

def test_video_gen():
    """测试视频生成模块"""
    print("\n测试视频生成模块...")
    # 检查模型目录是否存在
    model_dir = os.path.join(script_dir, "data", "models")
    if os.path.exists(model_dir):
        print("✅ 模型目录存在")
    else:
        print("⚠️  模型目录不存在，将在运行时创建")

def test_pipeline():
    """测试完整pipeline"""
    print("\n测试完整pipeline...")
    # 检查pipeline脚本是否存在
    pipeline_script = os.path.join(script_dir, "scripts", "pipeline.py")
    if os.path.exists(pipeline_script):
        print("✅ Pipeline脚本存在")
    else:
        print("❌ Pipeline脚本不存在")

def main():
    """运行所有测试"""
    print("=" * 60)
    print("Paper2Video 测试")
    print("=" * 60)
    
    test_pdf_parser()
    test_script_gen()
    test_audio_gen()
    test_video_gen()
    test_pipeline()
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()