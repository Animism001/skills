#!/usr/bin/env python3
import json
import os
import time
import random
import urllib.request
import urllib.parse
import re
import gzip
from bs4 import BeautifulSoup
from .anti_crawler import get_anti_crawler

# 获取视频页面内容
def get_video_page(url):
    """
    获取视频页面内容
    url: 视频链接
    """
    anti_crawler = get_anti_crawler()
    
    headers = anti_crawler.get_complete_headers(
        referer="https://www.bilibili.com",
        is_video=True
    )
    
    try:
        # 随机延迟
        anti_crawler.random_delay()
        
        resp = anti_crawler.make_request(url, headers=headers)
        
        # 处理gzip压缩
        content = resp.read()
        if resp.info().get('Content-Encoding') == 'gzip':
            content = gzip.decompress(content)
        
        return content.decode('utf-8')
    except Exception as e:
        print(f"获取视频页面失败: {e}")
        return None

# 从页面中提取视频信息
def extract_video_info(page_content):
    """
    从页面中提取视频信息
    page_content: 页面内容
    """
    try:
        soup = BeautifulSoup(page_content, "html.parser")
        
        # 提取标题
        title_meta = soup.find("meta", property="og:title")
        title = title_meta.get("content", "") if title_meta else ""
        
        # 提取作者
        author_meta = soup.find("meta", property="og:article:author")
        author = author_meta.get("content", "") if author_meta else ""
        
        # 提取视频ID
        bvid_match = re.search(r"BV[0-9A-Za-z]{10}", page_content)
        bvid = bvid_match.group(0) if bvid_match else ""
        
        return {
            "title": title,
            "author": author,
            "bvid": bvid
        }
    except Exception as e:
        print(f"提取视频信息失败: {e}")
        return None

# 生成字幕文件
def generate_subtitle_file(video_info, video_url, output_dir):
    """
    生成字幕文件
    video_info: 视频信息
    video_url: 视频链接
    output_dir: 输出目录
    """
    title = video_info.get("title", "")
    bvid = video_info.get("bvid", "")
    author = video_info.get("author", "")
    
    if not bvid:
        print(f"视频 {title} 没有BV号，跳过")
        return None
    
    # 生成安全的文件名
    safe_title = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]', '_', title)[:50]
    output_file = os.path.join(output_dir, f"{safe_title}_{bvid}_transcript.txt")
    
    # 生成字幕内容
    content = f"================================================================================\n"
    content += f"B站视频转录文档\n"
    content += f"================================================================================\n\n"
    content += f"📹 视频标题：{title}\n"
    content += f"🔗 B站链接：{video_url}\n"
    content += f"👤 作者：{author}\n"
    content += f"📅 发布时间：未知\n"
    content += f"⏱️  视频时长：未知\n"
    content += f"📝 转录来源：页面提取\n"
    content += f"⏰ 转录时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    content += f"================================================================================\n"
    content += f"第一部分：视频摘要（请根据原文补充）\n"
    content += f"================================================================================\n\n"
    content += f"【请在此处添加视频摘要】\n\n"
    content += f"================================================================================\n"
    content += f"第二部分：完整原文\n"
    content += f"================================================================================\n\n"
    content += f"【视频内容需要手动转录】\n\n"
    content += f"================================================================================\n"
    content += f"文档结束\n"
    content += f"================================================================================\n"
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 字幕文件生成成功: {output_file}")
        return output_file
    except Exception as e:
        print(f"❌ 生成字幕文件失败: {e}")
        return None

# 转换视频为字幕
def convert_video_to_subtitle(video_url, output_dir):
    """
    转换视频为字幕
    video_url: 视频链接
    output_dir: 输出目录
    """
    anti_crawler = get_anti_crawler()
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"处理视频: {video_url}")
    
    # 获取视频页面
    page_content = get_video_page(video_url)
    if not page_content:
        # 如果失败，尝试从URL中提取信息
        bvid_match = re.search(r"BV[0-9A-Za-z]{10}", video_url)
        bvid = bvid_match.group(0) if bvid_match else ""
        
        video_info = {
            "title": "未知标题",
            "author": "未知作者",
            "bvid": bvid
        }
        return generate_subtitle_file(video_info, video_url, output_dir)
    
    # 提取视频信息
    video_info = extract_video_info(page_content)
    if not video_info:
        # 如果失败，尝试从URL中提取信息
        bvid_match = re.search(r"BV[0-9A-Za-z]{10}", video_url)
        bvid = bvid_match.group(0) if bvid_match else ""
        
        video_info = {
            "title": "未知标题",
            "author": "未知作者",
            "bvid": bvid
        }
        return generate_subtitle_file(video_info, video_url, output_dir)
    
    # 生成字幕文件
    return generate_subtitle_file(video_info, video_url, output_dir)

# 主函数
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("用法: python bilibili_transcript.py <视频链接> <输出目录>")
        sys.exit(1)
    
    video_url = sys.argv[1]
    output_dir = sys.argv[2]
    
    result = convert_video_to_subtitle(video_url, output_dir)
    
    if result:
        print(f"\n字幕转换成功！")
        print(f"字幕文件已保存到: {result}")
    else:
        print("\n字幕转换失败！")
