import os
import json
import subprocess
from typing import Dict, List, Optional
from pathlib import Path

class VideoGenerator:
    def __init__(self, model_dir: str):
        self.model_dir = model_dir
        self.multitalk_path = os.path.join(model_dir, "multitalk")
    
    def generate_video(self, script_data: Dict, audio_segments: List[Dict], output_dir: str) -> List[Dict]:
        """生成视频片段"""
        os.makedirs(output_dir, exist_ok=True)
        video_segments = []
        
        for i, (script_segment, audio_segment) in enumerate(zip(script_data['script'], audio_segments)):
            if script_segment['type'] == 'dialogue':
                # 生成对话视频
                video_path = os.path.join(output_dir, f"video_{i:04d}.mp4")
                shot_type = script_segment['shot_type']
                role = script_segment['role']
                audio_path = audio_segment['audio_path']
                
                # 根据镜头类型生成视频
                if '单人' in shot_type or 'single' in shot_type.lower():
                    self._generate_single_shot_video(role, audio_path, video_path)
                else:
                    self._generate_double_shot_video(audio_path, video_path)
                
                video_segments.append({
                    "index": i,
                    "type": "dialogue",
                    "shot_type": shot_type,
                    "role": role,
                    "video_path": video_path,
                    "duration": audio_segment['duration']
                })
            elif script_segment['type'] == 'image':
                # 生成图片展示视频
                video_path = os.path.join(output_dir, f"video_{i:04d}.mp4")
                self._generate_image_video(script_segment['content'], audio_segment['audio_path'], video_path)
                
                video_segments.append({
                    "index": i,
                    "type": "image",
                    "video_path": video_path,
                    "duration": audio_segment['duration']
                })
            elif script_segment['type'] == 'text':
                # 生成文字展示视频
                video_path = os.path.join(output_dir, f"video_{i:04d}.mp4")
                self._generate_text_video(script_segment['content'], audio_segment['audio_path'], video_path)
                
                video_segments.append({
                    "index": i,
                    "type": "text",
                    "video_path": video_path,
                    "duration": audio_segment['duration']
                })
        
        return video_segments
    
    def _generate_single_shot_video(self, role: str, audio_path: str, output_path: str):
        """生成单人镜头视频"""
        # 这里是MultiTalk的调用逻辑
        # 实际项目中需要根据MultiTalk的API进行调整
        print(f"生成单人镜头视频: {role}")
        
        # 模拟生成视频
        # 实际项目中应该调用MultiTalk的推理脚本
        self._create_placeholder_video(output_path, duration=5)
    
    def _generate_double_shot_video(self, audio_path: str, output_path: str):
        """生成双人镜头视频"""
        # 这里是MultiTalk的调用逻辑
        print("生成双人镜头视频")
        
        # 模拟生成视频
        self._create_placeholder_video(output_path, duration=8)
    
    def _generate_image_video(self, image_desc: str, audio_path: str, output_path: str):
        """生成图片展示视频"""
        print(f"生成图片展示视频: {image_desc}")
        
        # 模拟生成视频
        self._create_placeholder_video(output_path, duration=8)
    
    def _generate_text_video(self, text: str, audio_path: str, output_path: str):
        """生成文字展示视频"""
        print(f"生成文字展示视频: {text[:20]}...")
        
        # 模拟生成视频
        self._create_placeholder_video(output_path, duration=6)
    
    def _create_placeholder_video(self, output_path: str, duration: int = 5):
        """创建占位视频"""
        # 使用FFmpeg创建一个简单的占位视频
        command = [
            'ffmpeg', '-y',
            '-f', 'lavfi', '-i', f'color=c=black:s=1280x720:d={duration}',
            '-f', 'lavfi', '-i', 'anullsrc',
            '-c:v', 'libx264', '-c:a', 'aac',
            '-shortest', output_path
        ]
        
        try:
            subprocess.run(command, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"创建占位视频失败: {e}")
    
    def concatenate_videos(self, video_segments: List[Dict], output_path: str) -> str:
        """拼接所有视频"""
        # 创建视频列表文件
        list_file = os.path.join(os.path.dirname(output_path), "video_list.txt")
        
        with open(list_file, "w") as f:
            for segment in video_segments:
                if os.path.exists(segment['video_path']):
                    f.write(f"file '{segment['video_path']}'\n")
        
        # 使用FFmpeg拼接视频
        command = [
            'ffmpeg', '-y',
            '-f', 'concat', '-safe', '0', '-i', list_file,
            '-c', 'copy', output_path
        ]
        
        try:
            subprocess.run(command, check=True, capture_output=True)
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"拼接视频失败: {e}")
            return None
    
    def save_video_data(self, video_segments: List[Dict], output_path: str):
        """保存视频数据到JSON文件"""
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(video_segments, f, ensure_ascii=False, indent=2)
        
        return video_segments

if __name__ == "__main__":
    # 测试视频生成
    model_dir = "../../../data/models"
    
    # 加载脚本和音频数据
    script_path = "../../../data/outputs/script.json"
    audio_data_path = "../../../data/outputs/audio_data.json"
    
    with open(script_path, "r", encoding="utf-8") as f:
        script_data = json.load(f)
    
    with open(audio_data_path, "r", encoding="utf-8") as f:
        audio_segments = json.load(f)
    
    # 生成视频
    generator = VideoGenerator(model_dir)
    video_dir = "../../../data/outputs/video"
    video_segments = generator.generate_video(script_data, audio_segments, video_dir)
    
    # 保存视频数据
    video_data_path = "../../../data/outputs/video_data.json"
    generator.save_video_data(video_segments, video_data_path)
    
    # 拼接视频
    combined_video_path = "../../../data/outputs/combined_video.mp4"
    generator.concatenate_videos(video_segments, combined_video_path)
    
    print(f"视频生成完成，结果保存到: {video_data_path}")
    print(f"拼接后的视频: {combined_video_path}")
    print(f"生成了 {len(video_segments)} 个视频片段")