# import os
# import json
# from typing import Dict, List, Optional
# import openai
# from pydub import AudioSegment
# from pathlib import Path

# class AudioGenerator:
#     def __init__(self, api_key: str, base_url: str):
#         self.api_key = api_key
#         self.base_url = base_url
#         openai.api_key = api_key
#         if base_url:
#             openai.api_base = base_url
    
#     def generate_audio(self, script_data: Dict, output_dir: str) -> List[Dict]:
#         """为脚本生成音频"""
#         os.makedirs(output_dir, exist_ok=True)
#         audio_segments = []
        
#         for i, segment in enumerate(script_data['script']):
#             if segment['type'] == 'dialogue':
#                 # 生成对话音频
#                 audio_path = os.path.join(output_dir, f"audio_{i:04d}.mp3")
#                 voice = self._get_voice_for_role(segment['role'])
                
#                 # 生成音频
#                 self._generate_tts(segment['content'], voice, audio_path)
                
#                 # 获取音频时长
#                 duration = self._get_audio_duration(audio_path)
                
#                 audio_segments.append({
#                     "index": i,
#                     "type": "dialogue",
#                     "role": segment['role'],
#                     "audio_path": audio_path,
#                     "duration": duration
#                 })
#             elif segment['type'] in ['image', 'text']:
#                 # 为图片和文字展示生成背景音
#                 audio_path = os.path.join(output_dir, f"audio_{i:04d}.mp3")
#                 self._generate_background_music(audio_path, duration=8)  # 默认8秒
                
#                 audio_segments.append({
#                     "index": i,
#                     "type": segment['type'],
#                     "audio_path": audio_path,
#                     "duration": 8
#                 })
        
#         return audio_segments
    
#     def _get_voice_for_role(self, role: str) -> str:
#         """根据角色选择合适的语音"""
#         voice_map = {
#             "主持人": "zh-CN-YunxiNeural",
#             "专家": "zh-CN-YunyangNeural",
#             "host": "zh-CN-YunxiNeural",
#             "expert": "zh-CN-YunyangNeural"
#         }
#         return voice_map.get(role, "zh-CN-YunxiNeural")
    
#     def _generate_tts(self, text: str, voice: str, output_path: str):
#         """生成文字转语音"""
#         response = openai.audio.speech.create(
#             model="tts-1",
#             voice=voice,
#             input=text,
#             speed=1.0
#         )
        
#         with open(output_path, "wb") as f:
#             f.write(response.content)
    
#     def _generate_background_music(self, output_path: str, duration: int = 8):
#         """生成背景音乐"""
#         # 创建一个静音音频作为占位符
#         # 实际项目中可以使用真实的背景音乐
#         silence = AudioSegment.silent(duration=duration * 1000)  # 毫秒
#         silence.export(output_path, format="mp3")
    
#     def _get_audio_duration(self, audio_path: str) -> float:
#         """获取音频时长"""
#         audio = AudioSegment.from_mp3(audio_path)
#         return len(audio) / 1000.0  # 转换为秒
    
#     def concatenate_audio(self, audio_segments: List[Dict], output_path: str) -> str:
#         """拼接所有音频"""
#         combined = AudioSegment.empty()
        
#         for segment in audio_segments:
#             if os.path.exists(segment['audio_path']):
#                 audio = AudioSegment.from_mp3(segment['audio_path'])
#                 combined += audio
        
#         combined.export(output_path, format="mp3")
#         return output_path
    
#     def save_audio_data(self, audio_segments: List[Dict], output_path: str):
#         """保存音频数据到JSON文件"""
#         output_dir = os.path.dirname(output_path)
#         if output_dir:
#             os.makedirs(output_dir, exist_ok=True)
        
#         with open(output_path, "w", encoding="utf-8") as f:
#             json.dump(audio_segments, f, ensure_ascii=False, indent=2)
        
#         return audio_segments

# if __name__ == "__main__":
#     # 测试音频生成
#     api_key = "sk-4loFmou3wa7YFgM1GZ6v3keYpPnVu6oPFhb8PuSMWWF5l3zD"
#     base_url = "https://api.openai.com/v1"
    
#     # 加载脚本
#     script_path = "../../../data/outputs/script.json"
#     with open(script_path, "r", encoding="utf-8") as f:
#         script_data = json.load(f)
    
#     # 生成音频
#     generator = AudioGenerator(api_key, base_url)
#     audio_dir = "../../../data/outputs/audio"
#     audio_segments = generator.generate_audio(script_data, audio_dir)
    
#     # 保存音频数据
#     audio_data_path = "../../../data/outputs/audio_data.json"
#     generator.save_audio_data(audio_segments, audio_data_path)
    
#     # 拼接音频
#     combined_audio_path = "../../../data/outputs/combined_audio.mp3"
#     generator.concatenate_audio(audio_segments, combined_audio_path)
    
#     print(f"音频生成完成，结果保存到: {audio_data_path}")
#     print(f"拼接后的音频: {combined_audio_path}")
#     print(f"生成了 {len(audio_segments)} 个音频片段")

import os
import json
import asyncio
from typing import Dict, List, Optional
from pydub import AudioSegment
from pathlib import Path

class AudioGenerator:
    def __init__(self):
        pass

    def generate_audio(self, script_data: Dict, output_dir: str) -> List[Dict]:
        os.makedirs(output_dir, exist_ok=True)
        audio_segments = []
        
        for i, segment in enumerate(script_data['script']):
            if segment['type'] == 'dialogue':
                audio_path = os.path.join(output_dir, f"audio_{i:04d}.mp3")
                voice = self._get_voice_for_role(segment['role'])
                
                self._generate_tts(segment['content'], voice, audio_path)
                
                duration = self._get_audio_duration(audio_path)
                
                audio_segments.append({
                    "index": i,
                    "type": "dialogue",
                    "role": segment['role'],
                    "audio_path": audio_path,
                    "duration": duration
                })
            elif segment['type'] in ['image', 'text']:
                audio_path = os.path.join(output_dir, f"audio_{i:04d}.mp3")
                self._generate_background_music(audio_path, duration=8)
                
                audio_segments.append({
                    "index": i,
                    "type": segment['type'],
                    "audio_path": audio_path,
                    "duration": 8
                })
        
        return audio_segments

    def _get_voice_for_role(self, role: str) -> str:
        """🔥 修复：使用 edge-tts 支持的原生中文音色"""
        voice_map = {
            "主持人": "zh-CN-XiaoxiaoNeural",   # ✅ 官方支持
            "专家": "zh-CN-YunyangNeural",     # ✅ 官方支持
            "host": "zh-CN-XiaoxiaoNeural",
            "expert": "zh-CN-YunyangNeural"
        }
        return voice_map.get(role, "zh-CN-XiaoxiaoNeural")

    def _generate_tts(self, text: str, voice: str, output_path: str):
        """🔥 修复：稳定版本地 TTS 生成"""
        try:
            asyncio.run(self._tts_async(text, voice, output_path))
        except Exception as e:
            print(f"⚠️ TTS 生成失败，使用备用方案: {e}")
            # 生成静音文件兜底
            silence = AudioSegment.silent(duration=2000)
            silence.export(output_path, format="mp3")

    async def _tts_async(self, text: str, voice: str, output_path: str):
        from edge_tts import Communicate
        communicate = Communicate(text, voice)
        await communicate.save(output_path)

    def _generate_background_music(self, output_path: str, duration: int = 8):
        silence = AudioSegment.silent(duration=duration * 1000)
        silence.export(output_path, format="mp3")

    def _get_audio_duration(self, audio_path: str) -> float:
        audio = AudioSegment.from_mp3(audio_path)
        return len(audio) / 1000.0

    def concatenate_audio(self, audio_segments: List[Dict], output_path: str) -> str:
        combined = AudioSegment.empty()
        for segment in audio_segments:
            if os.path.exists(segment['audio_path']):
                audio = AudioSegment.from_mp3(segment['audio_path'])
                combined += audio
        combined.export(output_path, format="mp3")
        return output_path

    def save_audio_data(self, audio_segments: List[Dict], output_path: str):
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(audio_segments, f, ensure_ascii=False, indent=2)
        return audio_segments

if __name__ == "__main__":
    script_path = "../../../data/outputs/script.json"
    with open(script_path, "r", encoding="utf-8") as f:
        script_data = json.load(f)

    generator = AudioGenerator()
    audio_dir = "../../../data/outputs/audio"
    audio_segments = generator.generate_audio(script_data, audio_dir)

    audio_data_path = "../../../data/outputs/audio_data.json"
    generator.save_audio_data(audio_segments, audio_data_path)

    combined_audio_path = "../../../data/outputs/combined_audio.mp3"
    generator.concatenate_audio(audio_segments, combined_audio_path)

    print(f"音频生成完成: {combined_audio_path}")