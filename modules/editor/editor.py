import os
import json
import subprocess
from typing import Dict, List, Optional
from pathlib import Path

class VideoEditor:
    def __init__(self):
        pass
    
    def edit_video(self, script_data: Dict, video_segments: List[Dict], audio_segments: List[Dict], output_path: str) -> str:
        """编辑视频，添加转场效果和镜头切换"""
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # 创建编辑后的视频片段
        edited_segments = self._process_segments(video_segments, audio_segments)
        
        # 拼接视频
        final_video = self._concatenate_with_transitions(edited_segments, output_path)
        
        return final_video
    
    def _process_segments(self, video_segments: List[Dict], audio_segments: List[Dict]) -> List[Dict]:
        """处理视频片段，添加转场效果"""
        edited_segments = []
        
        for i, (video_segment, audio_segment) in enumerate(zip(video_segments, audio_segments)):
            if video_segment['type'] == 'dialogue':
                # 处理对话片段
                edited_segment = self._process_dialogue_segment(video_segment, audio_segment)
            elif video_segment['type'] == 'image':
                # 处理图片展示片段
                edited_segment = self._process_image_segment(video_segment, audio_segment)
            elif video_segment['type'] == 'text':
                # 处理文字展示片段
                edited_segment = self._process_text_segment(video_segment, audio_segment)
            else:
                edited_segment = video_segment
            
            edited_segments.append(edited_segment)
        
        return edited_segments
    
    def _process_dialogue_segment(self, video_segment: Dict, audio_segment: Dict) -> Dict:
        """处理对话片段"""
        # 这里可以添加对话片段的特殊处理
        # 例如调整音量、添加音效等
        return video_segment
    
    def _process_image_segment(self, video_segment: Dict, audio_segment: Dict) -> Dict:
        """处理图片展示片段"""
        # 这里可以添加图片展示的特殊处理
        # 例如添加文字说明、缩放效果等
        return video_segment
    
    def _process_text_segment(self, video_segment: Dict, audio_segment: Dict) -> Dict:
        """处理文字展示片段"""
        # 这里可以添加文字展示的特殊处理
        # 例如添加动画效果、背景等
        return video_segment
    
    def _concatenate_with_transitions(self, segments: List[Dict], output_path: str) -> str:
        """拼接视频并添加转场效果"""
        # 创建临时目录
        temp_dir = os.path.join(os.path.dirname(output_path), "temp")
        os.makedirs(temp_dir, exist_ok=True)
        
        # 处理每个片段并添加转场
        processed_files = []
        
        for i, segment in enumerate(segments):
            if os.path.exists(segment['video_path']):
                # 为每个片段添加转场效果
                processed_path = os.path.join(temp_dir, f"processed_{i:04d}.mp4")
                self._add_transition(segment['video_path'], processed_path, i)
                processed_files.append(processed_path)
        
        # 创建视频列表文件
        list_file = os.path.join(temp_dir, "video_list.txt")
        with open(list_file, "w") as f:
            for file in processed_files:
                f.write(f"file '{file}'\n")
        
        # 使用FFmpeg拼接视频
        command = [
            'ffmpeg', '-y',
            '-f', 'concat', '-safe', '0', '-i', list_file,
            '-c:v', 'libx264', '-c:a', 'aac',
            '-shortest', output_path
        ]
        
        try:
            subprocess.run(command, check=True, capture_output=True)
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"拼接视频失败: {e}")
            return None
    
    def _add_transition(self, input_path: str, output_path: str, index: int):
        """为视频添加转场效果"""
        # 简单的淡入淡出效果
        command = [
            'ffmpeg', '-y',
            '-i', input_path,
            '-vf', 'fade=t=in:st=0:d=0.5,fade=t=out:st=4.5:d=0.5',
            '-c:v', 'libx264', '-c:a', 'aac',
            output_path
        ]
        
        try:
            subprocess.run(command, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"添加转场效果失败: {e}")
            # 如果失败，直接复制原始文件
            subprocess.run(['cp', input_path, output_path], check=True)
    
    def add_bgm(self, video_path: str, bgm_path: str, output_path: str) -> str:
        """添加背景音乐"""
        command = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-i', bgm_path,
            '-filter_complex', '[1:a]volume=0.3[bgm];[0:a][bgm]amix=inputs=2:duration=first',
            '-c:v', 'copy', '-c:a', 'aac',
            output_path
        ]
        
        try:
            subprocess.run(command, check=True, capture_output=True)
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"添加背景音乐失败: {e}")
            return video_path
    
    def add_title(self, video_path: str, title: str, output_path: str) -> str:
        """添加标题"""
        command = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-vf', f"drawtext=text='{title}':fontcolor=white:fontsize=36:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=50",
            '-c:v', 'libx264', '-c:a', 'copy',
            output_path
        ]
        
        try:
            subprocess.run(command, check=True, capture_output=True)
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"添加标题失败: {e}")
            return video_path

if __name__ == "__main__":
    # 测试视频编辑
    editor = VideoEditor()
    
    # 加载视频和音频数据
    video_data_path = "../../../data/outputs/video_data.json"
    audio_data_path = "../../../data/outputs/audio_data.json"
    script_path = "../../../data/outputs/script.json"
    
    with open(video_data_path, "r", encoding="utf-8") as f:
        video_segments = json.load(f)
    
    with open(audio_data_path, "r", encoding="utf-8") as f:
        audio_segments = json.load(f)
    
    with open(script_path, "r", encoding="utf-8") as f:
        script_data = json.load(f)
    
    # 编辑视频
    output_path = "../../../data/outputs/final_video.mp4"
    final_video = editor.edit_video(script_data, video_segments, audio_segments, output_path)
    
    print(f"视频编辑完成，结果保存到: {final_video}")