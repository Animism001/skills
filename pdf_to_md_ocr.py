#!/usr/bin/env python3
import os
from pathlib import Path
import pytesseract
from pdf2image import convert_from_path

INPUT_DIR = "/workspace/故事的织体"
OUTPUT_DIR = "/workspace/故事的织体_MD"

def pdf_to_markdown_with_ocr(pdf_path, md_path):
    """使用OCR将扫描件PDF转换为Markdown"""
    try:
        images = convert_from_path(pdf_path)
        text = ""
        
        for img in images:
            page_text = pytesseract.image_to_string(img, lang='chi_sim')
            text += page_text + "\n\n"
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        return True, len(text)
    except Exception as e:
        return False, str(e)

def main():
    print("开始使用OCR将扫描件PDF转换为MD文档...")
    print("=" * 60)
    
    total = 0
    success = 0
    failed = 0
    skipped = 0
    
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
            
            if md_file.exists() and md_file.stat().st_size > 100:
                print(f"  [跳过] {pdf_file.stem}.md")
                skipped += 1
                continue
            
            print(f"  [{total}] OCR识别: {pdf_file.stem}")
            
            success_flag, result = pdf_to_markdown_with_ocr(pdf_file, md_file)
            if success_flag:
                print(f"    ✓ 识别完成 ({result} 字符)")
                success += 1
            else:
                print(f"    ✗ 识别失败: {result}")
                failed += 1
    
    print("\n" + "=" * 60)
    print("统计结果:")
    print(f"  总计: {total}")
    print(f"  成功: {success}")
    print(f"  失败: {failed}")
    print(f"  跳过(已存在): {skipped}")
    print(f"\n所有MD文件已保存到: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
