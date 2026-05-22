#!/usr/bin/env python3
import json
import subprocess
import os
import sys
import requests
from pathlib import Path

SKILL_DIR = "/data/user/skills/ima-skills-1.1.7"
OUTPUT_DIR = "/workspace/故事的织体"
KB_ID = "VgpR1jCnhtauRqSnhBWgi4pJ4G7Jml_1Tjb-Cpihi0g="

ALL_MEDIA = [
    {
        "category": "故事的织体_电影编剧的操作系统_宋传",
        "items": [
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_04cbd4a8aca5d04c3a83154f32f6226c7457252365583018", "title": "封面、书名、版权、前言、目录", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_8a165e41413937c47c8d740c2de87bbe7457252365583018", "title": "第三部分 笔记汇总", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_85eda492756754543dc99d30d923f9517457252365583018", "title": "参考书目", "media_type": 1},
        ]
    },
    {
        "category": "第一部分_因为织体你才好编",
        "items": [
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_6e105496f934f17658aab6377ea2dcca7457252365583018", "title": "第1章 编故事，怎么学", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_5792d70ba1e7d73eb6fdc95a4197a8cd7457252365583018", "title": "第2章 艺术，怎么学", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_421bcca96413856484ba72f7885c6a867457252365583018", "title": "第3章 什么是故事的织体", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_d90d27316897f8ec4cf48d9b76650ba97457252365583018", "title": "第4章 \"直播\"创作过程", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_0884c8497d6bdedbc4e53c3d29757bd67457252365583018", "title": "第5章 简化、分类、程序——操作", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_9d6e8e46eaf3a09c67bbf7efc9bf38ae7457252365583018", "title": "第一部分 因为织体，你才好编", "media_type": 1},
        ]
    },
    {
        "category": "第二部分_编织你的故事",
        "items": [
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_d0871ae2bc2cfc9468fbb13141f9a9707457252365583018", "title": "第6章 你的灵感从哪里来，到哪里去", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_c646e69e4f997e5d951298d9ff5871447457252365583018", "title": "第7章 写作的起点，三支柱与八要素", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_6a3e2ce7b8bef4e79a142c13164e3e7f7457252365583018", "title": "第8章 故事的声部", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_9f90f3335652ddb2a49a79983e7518547457252365583018", "title": "第9章 关键事件与幕布局", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_92f047f505d8088e3e1623c60effb4d37457252365583018", "title": "第10章 该写故事梗概了", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_dee8dec5c274eb174666e1cbe5c978ca7457252365583018", "title": "第11章 幕的织体", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_c81a64c182cca47068171175f05281227457252365583018", "title": "第12章 让人物关系一目了然", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_c6e62cb304aad06389a170e5626dc4aa7457252365583018", "title": "第13章 走到幕里来", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_3a7002d6737ce1fc85b10e9d3701b58f7457252365583018", "title": "第14章 高潮大纲", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_8bbf2025ad961eec567013f0868aebe07457252365583018", "title": "第15章 故事路标", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_e297d5ee49302192a38fb381feaeaa497457252365583018", "title": "第16章 序列织体", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_9fd1bc022242e8e50ec2121a976be03c7457252365583018", "title": "第17章 序列人物", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_0638abd085a26a962532d7438a9beef47457252365583018", "title": "第18章 故事大纲", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_c468b44af755d8fa0a9160f2b89f8b417457252365583018", "title": "第19章 关注的点与线——创作的换位思考", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_14db83a7c54f535e45d95e45870fea327457252365583018", "title": "第20章 场景织体", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_5cb3e00fe42d0d8d4d792f713b0c39d77457252365583018", "title": "第21章 环节", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_75972c635c45bb6dc7ec61319b2cbf357457252365583018", "title": "第22章 人物图谱", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_bb0fa3e472d388ee7cae6d192d6a1f297457252365583018", "title": "第23章 写剧本", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_c7b0552b5aaefcd73fb99dc54c1ab7cc7457252365583018", "title": "第二部分 编织你的故事——织体：点、线、面，从想法到剧本的全过程", "media_type": 1},
        ]
    }
]

def get_media_info(media_id):
    cmd = [
        'node', f'{SKILL_DIR}/ima_api.cjs',
        'openapi/wiki/v1/get_media_info',
        json.dumps({"media_id": media_id})
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=SKILL_DIR)
    if result.returncode != 0:
        return None, f"API调用失败: {result.stderr}"
    resp = json.loads(result.stdout)
    if resp.get('code') != 0:
        return None, f"API返回错误: {resp.get('msg')}"
    return resp.get('data'), None

def download_pdf(url_info, output_file):
    url = url_info.get('url', '')
    headers = url_info.get('headers', {})
    if not url:
        return False, "URL为空"
    
    try:
        resp = requests.get(url, headers=headers, timeout=60)
        if resp.status_code != 200:
            return False, f"下载失败: HTTP {resp.status_code}"
        
        with open(output_file, 'wb') as f:
            f.write(resp.content)
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    print("开始获取子目录中的PDF文档...")
    print("=" * 60)
    
    total = 0
    success = 0
    failed = 0
    skipped = 0
    
    for group in ALL_MEDIA:
        category = group["category"]
        output_dir = Path(OUTPUT_DIR) / category
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n📂 处理分类: {category}")
        
        for item in group["items"]:
            media_id = item["media_id"]
            title = item["title"]
            total += 1
            
            safe_title = title.replace('/', '_').replace('\\', '_').replace(':', '_').replace('"', '')
            output_file = output_dir / f"{safe_title}.pdf"
            
            if output_file.exists():
                print(f"  [跳过] {safe_title}.pdf")
                skipped += 1
                continue
            
            print(f"  [{total}] 获取: {safe_title}")
            
            data, error = get_media_info(media_id)
            if error:
                print(f"    ✗ 获取媒体信息失败: {error}")
                failed += 1
                continue
            
            url_info = data.get('url_info', {})
            if not url_info.get('url'):
                print(f"    ✗ 没有找到下载URL")
                failed += 1
                continue
            
            success_flag, error = download_pdf(url_info, output_file)
            if success_flag:
                print(f"    ✓ 已保存")
                success += 1
            else:
                print(f"    ✗ 下载失败: {error}")
                failed += 1
    
    print("\n" + "=" * 60)
    print("统计结果:")
    print(f"  总计: {total}")
    print(f"  成功: {success}")
    print(f"  失败: {failed}")
    print(f"  跳过(已存在): {skipped}")
    print(f"\n所有文件已保存到: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
