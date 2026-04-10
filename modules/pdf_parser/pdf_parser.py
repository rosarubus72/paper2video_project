import fitz
import json
import os
from pathlib import Path
from typing import Dict, List, Optional

class PDFParser:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.num_pages = self.doc.page_count
    
    def extract_text(self) -> str:
        """提取PDF中的所有文本"""
        text = ""
        for page_num in range(self.num_pages):
            page = self.doc[page_num]
            text += page.get_text()
        return text
    
    def extract_metadata(self) -> Dict:
        """提取PDF的元数据"""
        metadata = self.doc.metadata
        return {
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "subject": metadata.get("subject", ""),
            "keywords": metadata.get("keywords", ""),
            "creation_date": metadata.get("creationDate", ""),
            "mod_date": metadata.get("modDate", "")
        }
    
    def extract_sections(self) -> List[Dict]:
        """提取论文的章节结构"""
        sections = []
        current_section = None
        
        for page_num in range(self.num_pages):
            page = self.doc[page_num]
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            font_size = span["size"]
                            
                            # 检测标题
                            if font_size > 14 and text:
                                if current_section:
                                    sections.append(current_section)
                                current_section = {
                                    "title": text,
                                    "content": [],
                                    "page": page_num + 1
                                }
                            elif current_section and text:
                                current_section["content"].append(text)
        
        if current_section:
            sections.append(current_section)
        
        return sections
    
    def extract_figures(self, output_dir: Optional[str] = None) -> List[Dict]:
        """提取PDF中的图片"""
        figures = []
        
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        for page_num in range(self.num_pages):
            page = self.doc[page_num]
            images = page.get_images(full=True)
            
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = self.doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                figure_info = {
                    "page": page_num + 1,
                    "index": img_index,
                    "ext": image_ext,
                    "width": base_image.get("width", 0),
                    "height": base_image.get("height", 0)
                }
                
                if output_dir:
                    image_path = os.path.join(output_dir, f"figure_{page_num+1}_{img_index}.{image_ext}")
                    with open(image_path, "wb") as f:
                        f.write(image_bytes)
                    figure_info["path"] = image_path
                
                figures.append(figure_info)
        
        return figures
    
    def parse_paper(self, output_dir: Optional[str] = None) -> Dict:
        """解析整个论文，返回结构化数据"""
        paper_data = {
            "metadata": self.extract_metadata(),
            "sections": self.extract_sections(),
            "text": self.extract_text(),
            "num_pages": self.num_pages
        }
        
        if output_dir:
            paper_data["figures"] = self.extract_figures(output_dir)
        
        return paper_data
    
    def save_parse_result(self, output_path: str):
        """保存解析结果到JSON文件"""
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        figures_dir = os.path.join(os.path.dirname(output_path), "figures")
        paper_data = self.parse_paper(figures_dir)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(paper_data, f, ensure_ascii=False, indent=2)
        
        return paper_data
    
    def close(self):
        """关闭PDF文档"""
        if hasattr(self, "doc"):
            self.doc.close()

if __name__ == "__main__":
    # 测试PDF解析
    pdf_path = "../../../data/pdfs/sample.pdf"
    parser = PDFParser(pdf_path)
    
    # 解析论文
    output_path = "../../../data/outputs/parse_result.json"
    paper_data = parser.save_parse_result(output_path)
    
    print(f"PDF解析完成，结果保存到: {output_path}")
    print(f"论文标题: {paper_data['metadata'].get('title', '未知')}")
    print(f"总页数: {paper_data['num_pages']}")
    print(f"章节数: {len(paper_data['sections'])}")
    if 'figures' in paper_data:
        print(f"图片数: {len(paper_data['figures'])}")
    
    parser.close()