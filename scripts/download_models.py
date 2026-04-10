#!/usr/bin/env python3
import os
import subprocess
import argparse
from pathlib import Path
from tqdm import tqdm

class ModelDownloader:
    def __init__(self, model_dir: str):
        self.model_dir = model_dir
        os.makedirs(self.model_dir, exist_ok=True)
    
    def download_multitalk(self):
        """下载MultiTalk模型"""
        print("正在下载MultiTalk模型...")
        
        multitalk_dir = os.path.join(self.model_dir, "multitalk")
        os.makedirs(multitalk_dir, exist_ok=True)
        
        # 克隆MultiTalk仓库
        if not os.path.exists(os.path.join(multitalk_dir, "README.md")):
            print("克隆MultiTalk仓库...")
            command = [
                'git', 'clone', 'https://github.com/meigen-ai/multitalk.git', 
                multitalk_dir
            ]
            try:
                subprocess.run(command, check=True, capture_output=True)
                print("✅ MultiTalk仓库克隆完成")
            except subprocess.CalledProcessError as e:
                print(f"❌ 克隆MultiTalk仓库失败: {e}")
                return False
        
        # 下载模型权重
        print("下载模型权重...")
        model_paths = [
            "Wan2.1-I2V-14B-480P",
            "chinese-wav2vec2-base",
            "Kokoro-82M",
            "MeiGen-MultiTalk"
        ]
        
        for model_name in model_paths:
            model_dir = os.path.join(multitalk_dir, "models", model_name)
            if not os.path.exists(model_dir):
                print(f"下载 {model_name}...")
                # 使用huggingface-cli下载
                command = [
                    'huggingface-cli', 'download', model_name,
                    '--local-dir', model_dir,
                    '--local-dir-use-symlinks', 'False'
                ]
                try:
                    subprocess.run(command, check=True, capture_output=True)
                    print(f"✅ {model_name} 下载完成")
                except subprocess.CalledProcessError as e:
                    print(f"❌ {model_name} 下载失败: {e}")
        
        return True
    
    def download_papertalk(self):
        """下载PaperTalk相关模型"""
        print("正在下载PaperTalk相关模型...")
        
        papertalk_dir = os.path.join(self.model_dir, "papertalk")
        os.makedirs(papertalk_dir, exist_ok=True)
        
        # 克隆Paper2Video仓库
        if not os.path.exists(os.path.join(papertalk_dir, "README.md")):
            print("克隆Paper2Video仓库...")
            command = [
                'git', 'clone', 'https://github.com/showlab/Paper2Video.git', 
                papertalk_dir
            ]
            try:
                subprocess.run(command, check=True, capture_output=True)
                print("✅ Paper2Video仓库克隆完成")
            except subprocess.CalledProcessError as e:
                print(f"❌ 克隆Paper2Video仓库失败: {e}")
                return False
        
        return True
    
    def download_all(self):
        """下载所有模型"""
        print("=" * 60)
        print("开始下载所有模型")
        print("=" * 60)
        
        self.download_multitalk()
        self.download_papertalk()
        
        print("=" * 60)
        print("模型下载完成")
        print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description='模型下载脚本')
    parser.add_argument('--model_dir', type=str, default='data/models', help='模型保存目录')
    parser.add_argument('--multitalk', action='store_true', help='只下载MultiTalk模型')
    parser.add_argument('--papertalk', action='store_true', help='只下载PaperTalk模型')
    parser.add_argument('--all', action='store_true', help='下载所有模型')
    
    args = parser.parse_args()
    
    # 获取绝对路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(base_dir, args.model_dir)
    
    downloader = ModelDownloader(model_dir)
    
    if args.multitalk:
        downloader.download_multitalk()
    elif args.papertalk:
        downloader.download_papertalk()
    else:
        downloader.download_all()

if __name__ == "__main__":
    main()