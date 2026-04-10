import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer
import warnings
warnings.filterwarnings("ignore")

class Qwen2_5_7B:
    def __init__(self, model_path):
        # 从 config 来的本地模型路径
        self.model_path = model_path
        self.device = "cuda:1"

        # 加载本地 Qwen2.5-7B-Instruct
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype="auto",
            device_map={"": self.device},
            trust_remote_code=True
        ).eval()

    def generate(self, query):
        # 纯文本生成（适合写论文脚本、对话）
        messages = [
            {"role": "system", "content": "你是B站知识区视频编剧，生成专业、易懂的双人访谈脚本。"},
            {"role": "user", "content": query}
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer([text], return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=8192,
                do_sample=True,
                temperature=0.3,
                top_p=0.85
            )

        response = self.tokenizer.decode(
            outputs[0][len(inputs.input_ids[0]):],
            skip_special_tokens=True
        )

        del inputs, outputs
        torch.cuda.empty_cache()
        return response


class LLM:
    def __init__(self, model_name, model_path):
        self.model_name = model_name
        self.model = Qwen2_5_7B(model_path)  # 纯本地

    def generate(self, **kwargs):
        query = kwargs.get('query', '')
        return self.model.generate(query)