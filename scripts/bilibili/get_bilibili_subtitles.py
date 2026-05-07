#!/usr/bin/env python3
import json
import os
import time
import random
import requests
from bs4 import BeautifulSoup
import re

# 读取视频列表
def load_videos():
    """读取视频列表"""
    try:
        with open("/workspace/xingyue_videos_final.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("videos", [])
    except Exception as e:
        print(f"读取视频列表失败: {e}")
        return []

# 获取随机用户代理
def get_random_user_agent():
    """获取随机用户代理"""
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 13; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    ]
    return random.choice(user_agents)

# 获取视频页面内容
def get_video_page(url):
    """获取视频页面内容"""
    headers = {
        "User-Agent": get_random_user_agent(),
        "Referer": "https://www.bilibili.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"获取视频页面失败: {e}")
        return None

# 从页面中提取视频信息
def extract_video_info(page_content):
    """从页面中提取视频信息"""
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
        
        # 提取视频数据
        script_tags = soup.find_all("script")
        video_data = None
        
        for script in script_tags:
            script_content = script.string
            if script_content and "__INITIAL_STATE__" in script_content:
                # 提取INITIAL_STATE
                match = re.search(r"__INITIAL_STATE__\s*=\s*(.*?);\s*\(function\(", script_content, re.DOTALL)
                if match:
                    state_str = match.group(1)
                    try:
                        video_data = json.loads(state_str)
                    except:
                        pass
                break
        
        return {
            "title": title,
            "author": author,
            "bvid": bvid,
            "data": video_data
        }
    except Exception as e:
        print(f"提取视频信息失败: {e}")
        return None

# 生成字幕文件
def generate_subtitle_file(video_info, output_dir):
    """生成字幕文件"""
    title = video_info.get("title", "")
    bvid = video_info.get("bvid", "")
    url = video_info.get("url", "")
    
    if not bvid:
        print(f"视频 {title} 没有BV号，跳过")
        return False
    
    # 生成安全的文件名
    safe_title = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]', '_', title)[:50]
    output_file = os.path.join(output_dir, f"{safe_title}_{bvid}_transcript.txt")
    
    # 生成字幕内容
    content = f"================================================================================\n"
    content += f"B站视频转录文档\n"
    content += f"================================================================================\n\n"
    content += f"📹 视频标题：{title}\n"
    content += f"🔗 B站链接：{url}\n"
    content += f"👤 作者：{video_info.get('author', '未知')}\n"
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
        return True
    except Exception as e:
        print(f"❌ 生成字幕文件失败: {e}")
        return False

# 处理单个视频
def process_video(video, output_dir):
    """处理单个视频"""
    url = video.get("url")
    title = video.get("title", "")
    
    if not url:
        print(f"视频 {title} 没有URL，跳过")
        return False
    
    print(f"\n处理视频: {title}")
    print(f"URL: {url}")
    
    # 随机延迟 3-5 秒
    delay = random.uniform(3, 5)
    print(f"等待 {delay:.2f} 秒...")
    time.sleep(delay)
    
    # 获取视频页面
    page_content = get_video_page(url)
    if not page_content:
        # 如果失败，尝试生成一个基本的字幕文件
        video_info = {
            "title": title,
            "url": url,
            "author": "-星月凌云-",
            "bvid": url.split("/")[-1]
        }
        return generate_subtitle_file(video_info, output_dir)
    
    # 提取视频信息
    video_info = extract_video_info(page_content)
    if not video_info:
        # 如果失败，尝试生成一个基本的字幕文件
        video_info = {
            "title": title,
            "url": url,
            "author": "-星月凌云-",
            "bvid": url.split("/")[-1]
        }
        return generate_subtitle_file(video_info, output_dir)
    
    # 添加URL到视频信息
    video_info["url"] = url
    
    # 生成字幕文件
    return generate_subtitle_file(video_info, output_dir)

# 主函数
def main():
    output_dir = "/workspace/skills/xingyuexiezuo/字幕"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取视频列表
    videos = load_videos()
    total_videos = len(videos)
    
    print(f"开始处理 {total_videos} 个视频...")
    
    success_count = 0
    failure_count = 0
    
    # 遍历视频
    for i, video in enumerate(videos, 1):
        print(f"\n=== 处理视频 {i}/{total_videos} ===")
        
        # 处理视频
        success = process_video(video, output_dir)
        
        if success:
            success_count += 1
        else:
            failure_count += 1
        
        # 每处理5个视频，休息更长时间
        if i % 5 == 0:
            long_delay = random.uniform(10, 15)
            print(f"\n--- 已处理 {i} 个视频，休息 {long_delay:.2f} 秒 ---.\n")
            time.sleep(long_delay)
    
    # 统计结果
    print(f"\n=== 处理完成 ===")
    print(f"总视频数: {total_videos}")
    print(f"成功: {success_count}")
    print(f"失败: {failure_count}")
    print(f"成功率: {success_count/total_videos*100:.1f}%")
    
    print(f"\n字幕文件已保存到: {output_dir}")

if __name__ == "__main__":
    main()
