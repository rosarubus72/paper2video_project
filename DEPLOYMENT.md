# Paper2Video 部署教程

本教程将指导您如何部署和运行 Paper2Video 项目，生成3-5分钟的B站风格两人访谈论文解读视频。

## 1. 环境准备

### 1.1 系统要求
- Linux/Unix 系统
- Python 3.10+
- CUDA 11.8+ (推荐，用于视频生成)
- 至少 16GB 内存
- 至少 50GB 磁盘空间（用于模型和输出文件）

### 1.2 安装依赖

#### 1.2.1 使用conda环境

```bash
# 创建并激活环境
conda create -n paper2video python=3.10
conda activate paper2video

# 安装PyTorch（带CUDA）
pip install torch==2.6.0+cu124 torchaudio==2.6.0+cu124 torchvision==0.21.0+cu124 --index-url https://download.pytorch.org/whl/cu124

# 安装项目依赖
cd paper2video_project
pip install -r requirements.txt

# 安装FFmpeg
conda install -c conda-forge ffmpeg
```

#### 1.2.2 使用现有的twitter环境

如果您已经有了 `twitter` 环境，并且里面已经安装了必要的依赖，可以直接使用：

```bash
source activate twitter

# 安装缺失的依赖
cd paper2video_project
pip install -r requirements.txt

# 安装FFmpeg（如果没有）
conda install -c conda-forge ffmpeg
```

## 2. 模型下载

### 2.1 下载MultiTalk模型

MultiTalk 是用于生成音频驱动的多人对话视频的模型：

```bash
# 运行模型下载脚本
cd paper2video_project
python scripts/download_models.py --multitalk
```

### 2.2 下载Paper2Video相关模型

Paper2Video 是用于从学术论文生成演讲视频的模型：

```bash
# 运行模型下载脚本
cd paper2video_project
python scripts/download_models.py --papertalk
```

### 2.3 下载所有模型

```bash
# 运行模型下载脚本
cd paper2video_project
python scripts/download_models.py --all
```

## 3. 配置设置

### 3.1 编辑配置文件

打开 `config/config.yaml` 文件，根据您的实际情况修改配置：

```yaml
# API配置
api:
  openai_api_key: "sk-4loFmou3wa7YFgM1GZ6v3keYpPnVu6oPFhb8PuSMWWF5l3zD"  # 替换为您的API密钥
  base_url: "https://api.openai.com/v1"

# 视频配置
video:
  duration: 4  # 视频时长（分钟）
  resolution: "1280x720"  # 视频分辨率
  fps: 30  # 帧率

# 人物配置
characters:
  host:
    name: "主持人"
    voice: "zh-CN-YunxiNeural"
    image: "data/models/host.jpg"  # 替换为您的主持人图片
  expert:
    name: "专家"
    voice: "zh-CN-YunyangNeural"
    image: "data/models/expert.jpg"  # 替换为您的专家图片
```

### 3.2 准备人物图片

在 `data/models/` 目录下准备主持人和专家的参考图片：
- `host.jpg`：主持人的参考图片
- `expert.jpg`：专家的参考图片

图片要求：
- 正方形图片
- 清晰的人物面部
- 建议尺寸：512x512 或更高

## 4. 运行流程

### 4.1 准备论文PDF

将您要解读的论文PDF文件放在 `data/pdfs/` 目录下。

### 4.2 运行Pipeline

```bash
# 激活环境
source activate paper2video  # 或 source activate twitter

# 运行pipeline
cd paper2video_project
python scripts/pipeline.py --pdf_path data/pdfs/test_paper.pdf --duration 3
```

参数说明：
- `--pdf_path`：论文PDF文件路径
- `--duration`：视频时长（分钟），默认4分钟
- `--config`：配置文件路径，默认 `config/config.yaml`

### 4.3 查看输出

运行完成后，输出文件会保存在 `data/outputs/` 目录下：
- `final_video.mp4`：最终生成的视频
- `parse_result.json`：PDF解析结果
- `script.json`：生成的对话脚本
- `audio/`：生成的音频片段
- `video/`：生成的视频片段

## 5. 常见问题解决

### 5.1 API密钥问题

如果遇到API密钥相关的错误，请检查：
- 确保API密钥正确无误
- 确保API密钥有足够的额度
- 确保网络连接正常

### 5.2 模型下载问题

如果模型下载失败：
- 检查网络连接
- 尝试使用代理
- 手动下载模型并放置到对应目录

### 5.3 视频生成失败

如果视频生成失败：
- 检查CUDA是否可用
- 确保内存足够
- 检查FFmpeg是否正确安装

### 5.4 音频生成失败

如果音频生成失败：
- 检查API密钥权限
- 确保文本长度在API限制范围内

## 6. 高级配置

### 6.1 自定义语音

在 `config/config.yaml` 中，您可以修改人物的语音：

```yaml
characters:
  host:
    voice: "zh-CN-YunxiNeural"  # 主持人语音
  expert:
    voice: "zh-CN-YunyangNeural"  # 专家语音
```

支持的语音列表可以参考OpenAI TTS文档。

### 6.2 调整视频参数

在 `config/config.yaml` 中，您可以调整视频参数：

```yaml
video:
  duration: 4  # 视频时长（分钟）
  resolution: "1920x1080"  # 更高的分辨率
  fps: 60  # 更高的帧率
```

### 6.3 调整剪辑参数

在 `config/config.yaml` 中，您可以调整剪辑参数：

```yaml
editing:
  single_shot_duration: 3-8  # 单人镜头时长（秒）
  double_shot_duration: 8-12  # 双人镜头时长（秒）
  image_duration: 6-10  # 图片展示时长（秒）
  text_duration: 4-8  # 文字展示时长（秒）
```

## 7. 项目结构

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
├── README.md            # 项目说明
└── DEPLOYMENT.md        # 部署教程
```

## 8. 性能优化

### 8.1 加速视频生成

- 使用GPU加速：确保CUDA可用
- 降低分辨率：对于快速预览，可以使用较低的分辨率
- 减少视频时长：对于测试，可以生成较短的视频

### 8.2 减少内存使用

- 清理临时文件：定期清理 `data/temp/` 目录
- 分批处理：对于大型PDF，可以考虑分批处理

## 9. 故障排除

如果遇到问题，请检查以下几点：

1. **依赖问题**：确保所有依赖都已正确安装
2. **API问题**：确保API密钥有效且有足够额度
3. **模型问题**：确保模型已正确下载
4. **权限问题**：确保有足够的文件系统权限
5. **资源问题**：确保有足够的内存和磁盘空间

如果问题仍然存在，请查看日志输出以获取更多信息。

## 10. 示例用法

### 10.1 基本用法

```bash
# 生成4分钟的视频
python scripts/pipeline.py --pdf_path data/pdfs/research_paper.pdf
```

### 10.2 自定义时长

```bash
# 生成5分钟的视频
python scripts/pipeline.py --pdf_path data/pdfs/research_paper.pdf --duration 5
```

### 10.3 使用自定义配置

```bash
# 使用自定义配置文件
python scripts/pipeline.py --pdf_path data/pdfs/research_paper.pdf --config config/custom_config.yaml
```

---

希望本教程能帮助您成功部署和运行 Paper2Video 项目。如果您有任何问题，请随时联系我们。