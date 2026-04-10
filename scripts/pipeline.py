# #!/usr/bin/env python3
# import os
# import json
# import argparse
# import yaml
# from pathlib import Path
# from tqdm import tqdm

# # 添加项目根目录到Python路径
# import sys
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from modules.pdf_parser.pdf_parser import PDFParser
# from modules.script_gen.script_gen import ScriptGenerator
# from modules.audio_gen.audio_gen import AudioGenerator
# from modules.video_gen.video_gen import VideoGenerator
# from modules.editor.editor import VideoEditor

# class Pipeline:
#     def __init__(self, config_path: str):
#         # 加载配置
#         with open(config_path, 'r', encoding='utf-8') as f:
#             self.config = yaml.safe_load(f)
        
#         # 初始化路径
#         self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         self.pdf_dir = os.path.join(self.base_dir, self.config['paths']['pdf_dir'])
#         self.output_dir = os.path.join(self.base_dir, self.config['paths']['output_dir'])
#         self.model_dir = os.path.join(self.base_dir, self.config['paths']['model_dir'])
#         self.temp_dir = os.path.join(self.base_dir, self.config['paths']['temp_dir'])
        
#         # 创建目录
#         os.makedirs(self.pdf_dir, exist_ok=True)
#         os.makedirs(self.output_dir, exist_ok=True)
#         os.makedirs(self.model_dir, exist_ok=True)
#         os.makedirs(self.temp_dir, exist_ok=True)
        
#         # 初始化模块
#         self.api_key = self.config['api']['openai_api_key']
#         self.base_url = self.config['api']['base_url']
        
#     def run(self, pdf_path: str, duration: int = None):
#         """运行完整流程"""
#         print("=" * 60)
#         print("Paper2Video Pipeline")
#         print("=" * 60)
        
#         # 1. PDF解析
#         print("\n1. 解析PDF文件...")
#         parser = PDFParser(pdf_path)
#         parse_result_path = os.path.join(self.output_dir, "parse_result.json")
#         paper_data = parser.save_parse_result(parse_result_path)
#         parser.close()
#         print(f"   ✅ PDF解析完成，结果保存到: {parse_result_path}")
#         print(f"   📄 论文标题: {paper_data['metadata'].get('title', '未知')}")
#         print(f"   📑 总页数: {paper_data['num_pages']}")
        
#         # 2. 脚本生成
#         print("\n2. 生成双人对话脚本...")
#         script_gen = ScriptGenerator(self.api_key, self.base_url)
#         script_path = os.path.join(self.output_dir, "script.json")
#         script_data = script_gen.generate_script(paper_data, duration or self.config['video']['duration'])
#         script_gen.save_script(script_data, script_path)
#         print(f"   ✅ 脚本生成完成，结果保存到: {script_path}")
#         print(f"   📝 脚本包含 {len(script_data['script'])} 个片段")
        
#         # 3. 音频生成
#         print("\n3. 生成音频...")
#         audio_gen = AudioGenerator(self.api_key, self.base_url)
#         audio_dir = os.path.join(self.output_dir, "audio")
#         audio_segments = audio_gen.generate_audio(script_data, audio_dir)
#         audio_data_path = os.path.join(self.output_dir, "audio_data.json")
#         audio_gen.save_audio_data(audio_segments, audio_data_path)
        
#         # 拼接音频
#         combined_audio_path = os.path.join(self.output_dir, "combined_audio.mp3")
#         audio_gen.concatenate_audio(audio_segments, combined_audio_path)
#         print(f"   ✅ 音频生成完成，结果保存到: {audio_data_path}")
#         print(f"   🔊 拼接后的音频: {combined_audio_path}")
        
#         # 4. 视频生成
#         print("\n4. 生成视频...")
#         video_gen = VideoGenerator(self.model_dir)
#         video_dir = os.path.join(self.output_dir, "video")
#         video_segments = video_gen.generate_video(script_data, audio_segments, video_dir)
#         video_data_path = os.path.join(self.output_dir, "video_data.json")
#         video_gen.save_video_data(video_segments, video_data_path)
        
#         # 拼接视频
#         combined_video_path = os.path.join(self.output_dir, "combined_video.mp4")
#         video_gen.concatenate_videos(video_segments, combined_video_path)
#         print(f"   ✅ 视频生成完成，结果保存到: {video_data_path}")
#         print(f"   🎬 拼接后的视频: {combined_video_path}")
        
#         # 5. 视频编辑
#         print("\n5. 编辑视频...")
#         editor = VideoEditor()
#         final_video_path = os.path.join(self.output_dir, "final_video.mp4")
#         final_video = editor.edit_video(script_data, video_segments, audio_segments, final_video_path)
#         print(f"   ✅ 视频编辑完成，最终视频: {final_video}")
        
#         print("\n" + "=" * 60)
#         print("🎉 流程完成！")
#         print(f"📁 输出目录: {self.output_dir}")
#         print(f"🎬 最终视频: {final_video}")
#         print("=" * 60)
        
#         return final_video

# def main():
#     parser = argparse.ArgumentParser(description='Paper2Video Pipeline')
#     parser.add_argument('--pdf_path', type=str, required=True, help='PDF文件路径')
#     parser.add_argument('--config', type=str, default='config/config.yaml', help='配置文件路径')
#     parser.add_argument('--duration', type=int, default=None, help='视频时长（分钟）')
    
#     args = parser.parse_args()
    
#     # 检查PDF文件是否存在
#     if not os.path.exists(args.pdf_path):
#         print(f"错误：PDF文件不存在: {args.pdf_path}")
#         sys.exit(1)
    
#     # 检查配置文件是否存在
#     config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), args.config)
#     if not os.path.exists(config_path):
#         print(f"错误：配置文件不存在: {config_path}")
#         sys.exit(1)
    
#     # 运行pipeline
#     pipeline = Pipeline(config_path)
#     pipeline.run(args.pdf_path, args.duration)

# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3
import os
import json
import argparse
import yaml
from pathlib import Path
from tqdm import tqdm

# 添加项目根目录到Python路径
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm import LLM
from modules.pdf_parser.pdf_parser import PDFParser
from modules.script_gen.script_gen import ScriptGenerator
from modules.audio_gen.audio_gen import AudioGenerator
from modules.video_gen.video_gen import VideoGenerator
from modules.editor.editor import VideoEditor

class Pipeline:
    def __init__(self, config_path: str):
        # 加载配置
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 初始化路径
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.pdf_dir = os.path.join(self.base_dir, self.config['paths']['pdf_dir'])
        self.output_dir = os.path.join(self.base_dir, self.config['paths']['output_dir'])
        self.model_dir = os.path.join(self.base_dir, self.config['paths']['model_dir'])
        self.temp_dir = os.path.join(self.base_dir, self.config['paths']['temp_dir'])
        
        # 初始化本地LLM（Qwen2.5，无API）
        self.llm = LLM(
            model_name=self.config['model']['text_model'],
            model_path=self.config['model']['qwen_model_path']
        )
        
        # 创建目录
        os.makedirs(self.pdf_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # 初始化模块（删除所有API参数）
        self.script_generator = ScriptGenerator(self.llm)
        self.audio_generator = AudioGenerator()
        
    def run(self, pdf_path: str, duration: int = None):
        """运行完整流程"""
        print("=" * 60)
        print("Paper2Video Pipeline")
        print("=" * 60)
        
        # 1. PDF解析
        print("\n1. 解析PDF文件...")
        parser = PDFParser(pdf_path)
        parse_result_path = os.path.join(self.output_dir, "parse_result.json")
        paper_data = parser.save_parse_result(parse_result_path)
        parser.close()
        print(f"   ✅ PDF解析完成，结果保存到: {parse_result_path}")
        print(f"   📄 论文标题: {paper_data['metadata'].get('title', '未知')}")
        print(f"   📑 总页数: {paper_data['num_pages']}")
        
        # 2. 脚本生成（本地LLM，无API）
        print("\n2. 生成双人对话脚本...")
        script_path = os.path.join(self.output_dir, "script.json")
        script_data = self.script_generator.generate_script(paper_data, duration or self.config['video']['duration'])
        self.script_generator.save_script(script_data, script_path)
        print(f"   ✅ 脚本生成完成，结果保存到: {script_path}")
        print(f"   📝 脚本包含 {len(script_data['script'])} 个片段")
        
        # 3. 音频生成（本地TTS，无API）
        print("\n3. 生成音频...")
        audio_dir = os.path.join(self.output_dir, "audio")
        audio_segments = self.audio_generator.generate_audio(script_data, audio_dir)
        audio_data_path = os.path.join(self.output_dir, "audio_data.json")
        self.audio_generator.save_audio_data(audio_segments, audio_data_path)
        
        # 拼接音频
        combined_audio_path = os.path.join(self.output_dir, "combined_audio.mp3")
        self.audio_generator.concatenate_audio(audio_segments, combined_audio_path)
        print(f"   ✅ 音频生成完成，结果保存到: {audio_data_path}")
        print(f"   🔊 拼接后的音频: {combined_audio_path}")
        
        # 4. 视频生成
        print("\n4. 生成视频...")
        video_gen = VideoGenerator(self.model_dir)
        video_dir = os.path.join(self.output_dir, "video")
        video_segments = video_gen.generate_video(script_data, audio_segments, video_dir)
        video_data_path = os.path.join(self.output_dir, "video_data.json")
        video_gen.save_video_data(video_segments, video_data_path)
        
        # 拼接视频
        combined_video_path = os.path.join(self.output_dir, "combined_video.mp4")
        video_gen.concatenate_videos(video_segments, combined_video_path)
        print(f"   ✅ 视频生成完成，结果保存到: {video_data_path}")
        print(f"   🎬 拼接后的视频: {combined_video_path}")
        
        # 5. 视频编辑
        print("\n5. 编辑视频...")
        editor = VideoEditor()
        final_video_path = os.path.join(self.output_dir, "final_video.mp4")
        final_video = editor.edit_video(script_data, video_segments, audio_segments, final_video_path)
        print(f"   ✅ 视频编辑完成，最终视频: {final_video}")
        
        print("\n" + "=" * 60)
        print("🎉 流程完成！")
        print(f"📁 输出目录: {self.output_dir}")
        print(f"🎬 最终视频: {final_video}")
        print("=" * 60)
        
        return final_video

def main():
    parser = argparse.ArgumentParser(description='Paper2Video Pipeline')
    parser.add_argument('--pdf_path', type=str, required=True, help='PDF文件路径')
    parser.add_argument('--config', type=str, default='config/config.yaml', help='配置文件路径')
    parser.add_argument('--duration', type=int, default=None, help='视频时长（分钟）')
    
    args = parser.parse_args()
    
    # 检查PDF文件是否存在
    if not os.path.exists(args.pdf_path):
        print(f"错误：PDF文件不存在: {args.pdf_path}")
        sys.exit(1)
    
    # 检查配置文件是否存在
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), args.config)
    if not os.path.exists(config_path):
        print(f"错误：配置文件不存在: {config_path}")
        sys.exit(1)
    
    # 运行pipeline
    pipeline = Pipeline(config_path)
    pipeline.run(args.pdf_path, args.duration)

if __name__ == "__main__":
    main()