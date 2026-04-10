import os
import json
import yaml
import subprocess
from pathlib import Path

def load_config(config_path: str) -> dict:
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_json(data: dict, output_path: str):
    """保存数据到JSON文件"""
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(input_path: str) -> dict:
    """加载JSON文件"""
    with open(input_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_command(command: list, cwd: str = None) -> tuple:
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout, result.stderr, 0
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode

def check_ffmpeg() -> bool:
    """检查FFmpeg是否安装"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def get_video_duration(video_path: str) -> float:
    """获取视频时长"""
    command = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
        '-of', 'default=noprint_wrappers=1:nokey=1', video_path
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except (subprocess.SubprocessError, ValueError):
        return 0.0

def create_directory(path: str):
    """创建目录"""
    os.makedirs(path, exist_ok=True)

def get_file_size(path: str) -> int:
    """获取文件大小（字节）"""
    if os.path.exists(path):
        return os.path.getsize(path)
    return 0

def format_file_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"