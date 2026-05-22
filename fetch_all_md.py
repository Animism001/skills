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
        "category": "",
        "items": [
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_8f1fe39f99f568502d6f111a991b945b7457252365583018", "title": "故事的织体_电影编剧的操作系统_宋传", "media_type": 1},
        ]
    },
    {
        "category": "故事的织体_电影编剧的操作系统_宋传",
        "items": [
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_8a165e41413937c47c8d740c2de87bbe7457252365583018", "title": "第三部分 笔记汇总", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_04cbd4a8aca5d04c3a83154f32f6226c7457252365583018", "title": "封面、书名、版权、前言、目录", "media_type": 1},
            {"media_id": "pdf_f1376fa77487efd02768360a1df87e12_85eda492756754543dc99d30d923f9517457252365583018", "title": "参考书目", "media_type": 1},
        ]
    },
    {
        "category": "第一部分_因为织体你才好编",
        "items": [
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_12bddb2e47bc302459d4e1f48bb60a117457252365583018", "title": "第一部分 因为织体，你才好编", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_fbcb380d72cc568cd05f01cfb25f94a57457252365583018", "title": "第1章 编故事，怎么学", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_da31d886c98a1b94c6aca584fef93b917457252365583018", "title": "第2章 艺术，怎么学", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_7b2f218378ee117b3003746a0ccd00507457252365583018", "title": "第3章 什么是故事的织体", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_a25f10497e5f5cbc37f66169fbb0d0557457252365583018", "title": "第4章 "直播"创作过程", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_544d55a08838022d96b2d3e92a5af4a67457252365583018", "title": "第5章 简化、分类、程序——操作", "media_type": 7},
        ]
    },
    {
        "category": "第二部分_编织你的故事",
        "items": [
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_f68476e753dae406a7f086dbb68a6f207457252365583018", "title": "第二部分 编织你的故事——织体：点、线、面，从想法到剧本的全过程", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_d85b60ef25f6c1e00204f6d80589d8107457252365583018", "title": "第10章 该写故事梗概了", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_3ca968644c992375a7878506b43ca6eb7457252365583018", "title": "第11章 幕的织体", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_22f926dc56d054e183833cba2189fffe7457252365583018", "title": "第12章 让人物关系一目了然", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_af4877f8d480796f60bc4207a0f5f3777457252365583018", "title": "第13章 走到幕里来", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_9fe2020f848daf04d2928747ea48a40b7457252365583018", "title": "第14章 高潮大纲", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_a1a270a83832153df8883f3f975a1c977457252365583018", "title": "第15章 故事路标", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_06dd51f1970cb2c2cc27eb33bde056947457252365583018", "title": "第16章 序列织体", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_956f58749a6586c61201f89aebec4b1e7457252365583018", "title": "第17章 序列人物", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_2460ca74f37680cba08b2bf00ad39c947457252365583018", "title": "第18章 故事大纲", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_dab85073184f3fc9ff1e62328f4416d67457252365583018", "title": "第19章 关注的点与线——创作的换位思考", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_4653c0b18879faf9039e5fb32755df947457252365583018", "title": "第20章 场景织体", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_7b46d858618c553ae091381d88eb8dc87457252365583018", "title": "第21章 环节", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_f92bffabfbbd1c4a6aa936826bef649d7457252365583018", "title": "第22章 人物图谱", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_690e751e70b247a57b2110e3167b7a557457252365583018", "title": "第23章 写剧本", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_6fcf423345e92ed6cf3b75645e87f7537457252365583018", "title": "第6章 你的灵感从哪里来，到哪里去", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_b5503947727da7e3c673467d12d9254a7457252365583018", "title": "第7章 写作的起点，三支柱与八要素", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_544d55a08838022d96b2d3e92a5af4a67457252365583018", "title": "第8章 故事的声部", "media_type": 7},
            {"media_id": "markdown_f1376fa77487efd02768360a1df87e12_fad5d1e3087e83876320ce86e595dda57457252365583018", "title": "第9章 关键事件与幕布局", "media_type": 7},
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

def download_content(url_info):
    url = url_info.get('url', '')
    headers = url_info.get('headers', {})
    if not url:
        return None, "URL为空"
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code != 200:
            return None, f"下载失败: HTTP {resp.status_code}"
        return resp.text, None
    except Exception as e:
        return None, str(e)

def main():
    total = 0
    success = 0
    failed = 0
    
    for group in ALL_MEDIA:
        category = group["category"]
        if category:
            output_dir = Path(OUTPUT_DIR) / category
        else:
            output_dir = Path(OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for item in group["items"]:
            media_id = item["media_id"]
            title = item["title"]
            media_type = item["media_type"]
            total += 1
            
            safe_title = title.replace('/', '_').replace('\\', '_').replace(':', '_')
            output_file = output_dir / f"{safe_title}.md"
            
            if output_file.exists():
                print(f"✓ 已存在,跳过: {safe_title}")
                success += 1
                continue
            
            print(f"\n[{total}] 获取: {title}")
            
            data, error = get_media_info(media_id)
            if error:
                print(f"  ✗ 获取媒体信息失败: {error}")
                failed += 1
                continue
            
            url_info = data.get('url_info', {})
            notebook_ext_info = data.get('notebook_ext_info')
            
            if media_type == 7 and url_info.get('url'):
                content, error = download_content(url_info)
                if error:
                    print(f"  ✗ 下载失败: {error}")
                    failed += 1
                    continue
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✓ 已保存: {output_file}")
                success += 1
                
            elif media_type == 1 and url_info.get('url'):
                download_url = url_info['url']
                download_url += f'&response-content-disposition=attachment;filename="{safe_title}.pdf"'
                headers = url_info.get('headers', {})
                
                pdf_file = output_dir / f"{safe_title}.pdf"
                try:
                    resp = requests.get(download_url, headers=headers, timeout=60)
                    if resp.status_code == 200:
                        with open(pdf_file, 'wb') as f:
                            f.write(resp.content)
                        print(f"  ✓ PDF已保存: {pdf_file}")
                        success += 1
                    else:
                        print(f"  ✗ PDF下载失败: HTTP {resp.status_code}")
                        failed += 1
                except Exception as e:
                    print(f"  ✗ PDF下载异常: {e}")
                    failed += 1
            else:
                print(f"  ✗ 无法获取内容 (media_type={media_type})")
                failed += 1
    
    print(f"\n=== 完成 ===")
    print(f"总计: {total}")
    print(f"成功: {success}")
    print(f"失败: {failed}")

if __name__ == "__main__":
    main()
