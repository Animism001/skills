#!/bin/bash

# PDF转MD脚本 - 使用tesseract OCR配合图像预处理
# 参数：--psm 6 --oem 3 -c preserve_interword_spaces=1

INPUT_DIR="/workspace/故事的织体"
OUTPUT_DIR="/workspace/故事的织体_OCR输出"
TMP_DIR="/tmp/pdf_ocr_temp"

# 创建临时目录和输出目录
mkdir -p "$TMP_DIR"
mkdir -p "$OUTPUT_DIR"

# 处理单个PDF文件的函数
process_pdf() {
    local pdf_path="$1"
    local relative_path="${pdf_path#$INPUT_DIR/}"
    local output_subdir="$OUTPUT_DIR/$(dirname "$relative_path")"
    local base_name=$(basename "$pdf_path" .pdf)
    local output_md="$output_subdir/${base_name}.md"
    
    # 创建输出子目录
    mkdir -p "$output_subdir"
    
    echo "正在处理: $pdf_path"
    
    # 创建临时工作目录
    local work_dir=$(mktemp -d -p "$TMP_DIR")
    
    # 将PDF转换为单页图像（每页一个文件）
    convert -density 300 "$pdf_path" "$work_dir/page_%04d.png"
    
    if [ $? -ne 0 ]; then
        echo "ERROR: PDF转换失败 - $pdf_path"
        rm -rf "$work_dir"
        return 1
    fi
    
    # 处理每个页面
    local page_count=$(ls "$work_dir/page_"*.png 2>/dev/null | wc -l)
    local md_content=""
    
    for page_file in "$work_dir/page_"*.png; do
        [ -f "$page_file" ] || continue
        
        # 图像预处理：
        # 1. 转换为灰度
        # 2. 调整对比度 (-contrast-stretch 用于增强对比度)
        # 3. 应用阈值进行二值化
        # 4. 使用中值滤波降噪
        convert "$page_file" \
            -colorspace Gray \
            -contrast-stretch 5%x5% \
            -threshold 50% \
            -median 1x1 \
            "$page_file_processed.png"
        
        # 使用tesseract进行OCR识别
        local txt_file="${page_file%.png}_ocr.txt"
        tesseract "$page_file_processed.png" "${txt_file%.txt}" \
            --psm 6 \
            --oem 3 \
            -c preserve_interword_spaces=1 \
            -l chi_sim+eng
        
        if [ -f "$txt_file" ]; then
            md_content+="$(cat "$txt_file")"
            md_content+="\n\n---\n\n"
        fi
        
        rm -f "$page_file_processed.png" "$txt_file"
    done
    
    # 保存MD文件
    echo "$md_content" > "$output_md"
    
    # 清理临时目录
    rm -rf "$work_dir"
    
    echo "完成: $output_md"
    echo "页数: $page_count"
}

export -f process_pdf
export INPUT_DIR
export OUTPUT_DIR
export TMP_DIR

# 查找所有PDF文件并并行处理
find "$INPUT_DIR" -type f -name "*.pdf" | while read -r pdf; do
    process_pdf "$pdf" &
    # 控制并发数
    while [ $(jobs -p | wc -l) -ge 4 ]; do
        sleep 1
    done
done

# 等待所有任务完成
wait

echo "所有PDF文件处理完成！"
echo "输出目录: $OUTPUT_DIR"