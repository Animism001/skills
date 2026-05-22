#!/usr/bin/env python3
import os
from pathlib import Path
import fitz  # PyMuPDF

INPUT_DIR = "/workspace/故事的织体"
OUTPUT_DIR = "/workspace/故事的织体_MD"

def pdf_to_markdown(pdf_path, md_path):
    """将PDF文件转换为Markdown"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        
        for page in doc:
            text += page.get_text()
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    print("开始将PDF转换为MD文档...")
    print("=" * 60)
    
    total = 0
    success = 0
    failed = 0
    
    for category_dir in Path(INPUT_DIR).iterdir():
        if not category_dir.is_dir():
            continue
        
        output_category_dir = Path(OUTPUT_DIR) / category_dir.name
        output_category_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📂 处理分类: {category_dir.name}")
        
        pdf_files = sorted(category_dir.glob("*.pdf"))
        
        for pdf_file in pdf_files:
            total += 1
            md_file = output_category_dir / f"{pdf_file.stem}.md"
            
            if md_file.exists():
                print(f"  [跳过] {pdf_file.stem}.md")
                success += 1
                continue
            
            print(f"  [{total}] 转换: {pdf_file.stem}")
            
            success_flag, error = pdf_to_markdown(pdf_file, md_file)
            if success_flag:
                print(f"    ✓ 转换完成")
                success += 1
            else:
                print(f"    ✗ 转换失败: {error}")
                failed += 1
    
    print("\n" + "=" * 60)
    print("统计结果:")
    print(f"  总计: {total}")
    print(f"  成功: {success}")
    print(f"  失败: {failed}")
    print(f"\n所有MD文件已保存到: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
