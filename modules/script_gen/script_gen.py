# import json
# import os
# from typing import Dict, List, Optional
# import openai
# from pathlib import Path

# class ScriptGenerator:
#     def __init__(self, api_key: str, base_url: str):
#         self.api_key = api_key
#         self.base_url = base_url
#         openai.api_key = api_key
#         if base_url:
#             openai.api_base = base_url
    
#     def generate_script(self, paper_data: Dict, duration: int = 4) -> Dict:
#         """生成双人对话脚本"""
#         # 提取论文关键信息
#         title = paper_data['metadata'].get('title', '未知论文')
#         sections = paper_data.get('sections', [])
        
#         # 构建论文摘要
#         paper_summary = self._generate_paper_summary(paper_data)
        
#         # 生成对话脚本
#         script_prompt = f"""
# 你是一个专业的脚本作家，需要为一个3-5分钟的B站风格论文解读视频生成双人对话脚本。

# 论文信息：
# 标题：{title}
# 摘要：{paper_summary}

# 角色设定：
# - 主持人：引导对话，提出问题，确保内容易懂
# - 专家：详细解释论文内容，提供专业见解

# 脚本要求：
# 1. 总时长控制在{duration}分钟左右
# 2. 对话自然流畅，有互动感
# 3. 包含以下部分：
#    - 开场介绍（15-20秒）
#    - 论文背景和动机（30-40秒）
#    - 方法介绍（60-90秒）
#    - 实验结果（40-60秒）
#    - 结论和意义（30-40秒）
#    - 总结和结束（15-20秒）
# 4. 适当插入图片和文字展示的提示
# 5. 为每个对话部分添加镜头指示（单人镜头或双人镜头）
# 6. 对话要有剪辑感，避免单调

# 请按照以下格式输出脚本：

# [时间戳] 镜头类型: 角色: 对话内容
# [时间戳] 镜头类型: 角色: 对话内容
# [时间戳] 图片展示: 图片描述
# [时间戳] 文字展示: 文字内容
# ...
# """
        
#         response = openai.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "你是一个专业的脚本作家，擅长创作学术访谈视频脚本。"},
#                 {"role": "user", "content": script_prompt}
#             ],
#             temperature=0.7
#         )
        
#         script_content = response.choices[0].message.content
        
#         # 解析脚本
#         script_data = self._parse_script(script_content)
        
#         return {
#             "title": title,
#             "summary": paper_summary,
#             "script": script_data,
#             "duration": duration
#         }
    
#     def _generate_paper_summary(self, paper_data: Dict) -> str:
#         """生成论文摘要"""
#         sections = paper_data.get('sections', [])
#         text = paper_data.get('text', '')
        
#         # 如果有摘要部分，直接使用
#         for section in sections:
#             if '摘要' in section['title'] or 'abstract' in section['title'].lower():
#                 return ' '.join(section['content'][:10])  # 取前10句
        
#         # 否则生成摘要
#         prompt = f"""
# 请为以下论文内容生成一个简洁的摘要（100-150字）：

# {text[:2000]}  # 取前2000字
# """
        
#         response = openai.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "你是一个专业的学术摘要生成器。"},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.5
#         )
        
#         return response.choices[0].message.content
    
#     def _parse_script(self, script_content: str) -> List[Dict]:
#         """解析脚本内容"""
#         lines = script_content.strip().split('\n')
#         script_data = []
        
#         for line in lines:
#             line = line.strip()
#             if not line:
#                 continue
            
#             # 解析时间戳和内容
#             if ']' in line:
#                 parts = line.split('] ', 1)
#                 if len(parts) == 2:
#                     timestamp = parts[0].strip('[')
#                     content = parts[1]
                    
#                     # 解析内容部分
#                     if ': ' in content:
#                         content_parts = content.split(': ', 2)
#                         if len(content_parts) == 3:
#                             shot_type = content_parts[0]
#                             role = content_parts[1]
#                             dialogue = content_parts[2]
                            
#                             script_data.append({
#                                 "timestamp": timestamp,
#                                 "type": "dialogue",
#                                 "shot_type": shot_type,
#                                 "role": role,
#                                 "content": dialogue
#                             })
#                         elif len(content_parts) == 2:
#                             shot_type = content_parts[0]
#                             content = content_parts[1]
                            
#                             if '图片展示' in shot_type:
#                                 script_data.append({
#                                     "timestamp": timestamp,
#                                     "type": "image",
#                                     "shot_type": shot_type,
#                                     "content": content
#                                 })
#                             elif '文字展示' in shot_type:
#                                 script_data.append({
#                                     "timestamp": timestamp,
#                                     "type": "text",
#                                     "shot_type": shot_type,
#                                     "content": content
#                                 })
        
#         return script_data
    
#     def save_script(self, script_data: Dict, output_path: str):
#         """保存脚本到JSON文件"""
#         output_dir = os.path.dirname(output_path)
#         if output_dir:
#             os.makedirs(output_dir, exist_ok=True)
        
#         with open(output_path, "w", encoding="utf-8") as f:
#             json.dump(script_data, f, ensure_ascii=False, indent=2)
        
#         return script_data

# if __name__ == "__main__":
#     # 测试脚本生成
#     api_key = "sk-4loFmou3wa7YFgM1GZ6v3keYpPnVu6oPFhb8PuSMWWF5l3zD"
#     base_url = "https://api.openai.com/v1"
    
#     # 加载解析结果
#     parse_result_path = "../../../data/outputs/parse_result.json"
#     with open(parse_result_path, "r", encoding="utf-8") as f:
#         paper_data = json.load(f)
    
#     # 生成脚本
#     generator = ScriptGenerator(api_key, base_url)
#     script_data = generator.generate_script(paper_data, duration=4)
    
#     # 保存脚本
#     script_path = "../../../data/outputs/script.json"
#     generator.save_script(script_data, script_path)
    
#     print(f"脚本生成完成，结果保存到: {script_path}")
#     print(f"脚本包含 {len(script_data['script'])} 个片段")

import json
import os
from typing import Dict, List, Optional
from pathlib import Path

class ScriptGenerator:
    # ====================== 🔥 核心修改：只接收本地 LLM ======================
    def __init__(self, llm):
        self.llm = llm  # 本地 Qwen2.5 模型
    # ======================================================================

    def generate_script(self, paper_data: Dict, duration: int = 4) -> Dict:
        """生成双人对话脚本（本地LLM版，无API）"""
        # 提取论文关键信息
        title = paper_data['metadata'].get('title', '未知论文')
        sections = paper_data.get('sections', [])
        
        # 构建论文摘要
        paper_summary = self._generate_paper_summary(paper_data)
        
        # 生成对话脚本（Prompt 完全保持原版风格）
        script_prompt = f"""
你是一个专业的脚本作家，需要为一个3-5分钟的B站风格论文解读视频生成双人对话脚本。

论文信息：
标题：{title}
摘要：{paper_summary}

角色设定：
- 主持人：引导对话，提出问题，确保内容易懂
- 专家：详细解释论文内容，提供专业见解

脚本要求：
1. 总时长控制在{duration}分钟左右
2. 对话自然流畅，有互动感
3. 包含以下部分：
   - 开场介绍（15-20秒）
   - 论文背景和动机（30-40秒）
   - 方法介绍（60-90秒）
   - 实验结果（40-60秒）
   - 结论和意义（30-40秒）
   - 总结和结束（15-20秒）
4. 适当插入图片和文字展示的提示
5. 为每个对话部分添加镜头指示（单人镜头或双人镜头）
6. 对话要有剪辑感，避免单调

请按照以下格式输出脚本：

[时间戳] 镜头类型: 角色: 对话内容
[时间戳] 镜头类型: 角色: 对话内容
[时间戳] 图片展示: 图片描述
[时间戳] 文字展示: 文字内容
...
"""
        
        # ====================== 🔥 核心修改：本地LLM生成 ======================
        response = self.llm.generate(query=script_prompt)
        # ==================================================================
        
        script_content = response
        
        # 解析脚本（逻辑完全不变）
        script_data = self._parse_script(script_content)
        
        return {
            "title": title,
            "summary": paper_summary,
            "script": script_data,
            "duration": duration
        }
    
    def _generate_paper_summary(self, paper_data: Dict) -> str:
        """生成论文摘要（本地LLM版）"""
        sections = paper_data.get('sections', [])
        text = paper_data.get('text', '')
        
        # 如果有摘要部分，直接使用
        for section in sections:
            if '摘要' in section['title'] or 'abstract' in section['title'].lower():
                return ' '.join(section['content'][:10])  # 取前10句
        
        # 否则生成摘要
        prompt = f"""
请为以下论文内容生成一个简洁的摘要（100-150字）：

{text[:2000]}  # 取前2000字
"""
        
        # ====================== 🔥 核心修改：本地LLM生成 ======================
        response = self.llm.generate(query=prompt)
        # ==================================================================
        
        return response
    
    def _parse_script(self, script_content: str) -> List[Dict]:
        """解析脚本内容（完全不变，兼容原有格式）"""
        lines = script_content.strip().split('\n')
        script_data = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 解析时间戳和内容
            if ']' in line:
                parts = line.split('] ', 1)
                if len(parts) == 2:
                    timestamp = parts[0].strip('[')
                    content = parts[1]
                    
                    # 解析内容部分
                    if ': ' in content:
                        content_parts = content.split(': ', 2)
                        if len(content_parts) == 3:
                            shot_type = content_parts[0]
                            role = content_parts[1]
                            dialogue = content_parts[2]
                            
                            script_data.append({
                                "timestamp": timestamp,
                                "type": "dialogue",
                                "shot_type": shot_type,
                                "role": role,
                                "content": dialogue
                            })
                        elif len(content_parts) == 2:
                            shot_type = content_parts[0]
                            content = content_parts[1]
                            
                            if '图片展示' in shot_type:
                                script_data.append({
                                    "timestamp": timestamp,
                                    "type": "image",
                                    "shot_type": shot_type,
                                    "content": content
                                })
                            elif '文字展示' in shot_type:
                                script_data.append({
                                    "timestamp": timestamp,
                                    "type": "text",
                                    "shot_type": shot_type,
                                    "content": content
                                })
        
        return script_data
    
    def save_script(self, script_data: Dict, output_path: str):
        """保存脚本到JSON文件（完全不变）"""
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(script_data, f, ensure_ascii=False, indent=2)
        
        return script_data

if __name__ == "__main__":
    # 测试代码已适配本地模式
    from llm import LLM
    import yaml

    # 加载配置
    with open("../../../config/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # 初始化本地LLM
    llm = LLM(
        model_name=config["model"]["text_model"],
        model_path=config["model"]["qwen_model_path"]
    )

    # 加载解析结果
    parse_result_path = "../../../data/outputs/parse_result.json"
    with open(parse_result_path, "r", encoding="utf-8") as f:
        paper_data = json.load(f)
    
    # 生成脚本
    generator = ScriptGenerator(llm)
    script_data = generator.generate_script(paper_data, duration=4)
    
    # 保存脚本
    script_path = "../../../data/outputs/script.json"
    generator.save_script(script_data, script_path)
    
    print(f"脚本生成完成，结果保存到: {script_path}")
    print(f"脚本包含 {len(script_data['script'])} 个片段")