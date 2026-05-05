#!/usr/bin/env python3
import json
import os
import subprocess
import time
import random

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

# 转换单个视频为字幕
def convert_video_to_subtitle(video, output_dir):
    """转换单个视频为字幕"""
    url = video.get("url")
    title = video.get("title", "")
    bvid = video.get("bvid", "")
    
    if not url:
        print(f"视频 {title} 没有URL，跳过")
        return False
    
    print(f"\n处理视频: {title}")
    print(f"URL: {url}")
    
    # 构建命令
    script_path = "/workspace/skills/bilibili-transcript/scripts/bilibili_transcript.sh"
    command = ["bash", script_path, url, output_dir]
    
    try:
        # 执行命令
        result = subprocess.run(command, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ 字幕生成成功")
            # 输出文件路径
            if result.stdout:
                # 提取输出文件路径
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.startswith('📄 文件已保存: '):
                        output_file = line.replace('📄 文件已保存: ', '')
                        print(f"   字幕文件: {output_file}")
                        break
            return True
        else:
            print(f"❌ 字幕生成失败")
            print(f"   错误信息: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"❌ 处理超时")
        return False
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        return False

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
        
        # 随机延迟 3-5 秒，避免请求过于频繁
        delay = random.uniform(3, 5)
        print(f"等待 {delay:.2f} 秒...")
        time.sleep(delay)
        
        # 转换视频为字幕
        success = convert_video_to_subtitle(video, output_dir)
        
        if success:
            success_count += 1
        else:
            failure_count += 1
        
        # 每处理5个视频，休息更长时间
        if i % 5 == 0:
            long_delay = random.uniform(10, 15)
            print(f"\n--- 已处理 {i} 个视频，休息 {long_delay:.2f} 秒 ---\n")
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
