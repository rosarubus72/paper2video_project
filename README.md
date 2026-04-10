# Paper2Video Project

一个结合Paper2Video和MultiTalk的项目，用于生成3-5分钟的B站风格两人访谈论文解读视频。

## 项目结构

```
paper2video_project/
├── config/              # 配置文件
│   └── config.yaml      # 主配置文件
├── data/                # 数据目录
│   ├── pdfs/            # 论文PDF文件
│   ├── outputs/         # 输出目录
│   └── models/          # 模型目录
├── modules/             # 核心模块
│   ├── pdf_parser/      # PDF解析模块
│   ├── script_gen/      # 脚本生成模块
│   ├── audio_gen/       # 音频生成模块
│   ├── video_gen/       # 视频生成模块
│   └── editor/          # 剪辑拼接模块
├── scripts/             # 脚本文件
│   ├── pipeline.py      # 主pipeline脚本
│   ├── download_models.py  # 模型下载脚本
│   └── utils.py         # 工具函数
├── requirements.txt     # 依赖文件
└── README.md            # 项目说明
```

## 功能特点

- 论文PDF自动解析，提取关键内容
- 生成双人对话脚本，模拟访谈形式
- 自动生成音频，支持不同角色声音
- 生成两人访谈视频，支持镜头切换
- 自动剪辑和拼接，生成专业效果
- 支持3-5分钟长视频生成

## 依赖环境

- Python 3.10+
- PyTorch 2.0+
- FFmpeg
- 其他依赖详见requirements.txt

## 快速开始

1. 安装依赖
2. 下载模型
3. 配置API密钥
4. 运行pipeline脚本

## 示例用法

```bash
python scripts/pipeline.py \
    --pdf_path path/to/paper.pdf \
    --output_dir path/to/output \
    --duration 3-5  # 视频时长（分钟）
```