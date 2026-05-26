#!/usr/bin/env python3
import sys
import os

# 添加脚本所在目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from search_bilibili import search_bilibili_videos
from get_up_videos import get_all_up_videos
from bilibili_transcript import convert_video_to_subtitle

# 处理搜索请求
def handle_search(keyword):
    """
    处理搜索请求
    keyword: 搜索关键词
    """
    result = search_bilibili_videos(keyword)
    
    if "error" in result:
        print(f"错误: {result['error']}")
    else:
        print(f"搜索结果 ({result['total']}个视频):")
        for i, video in enumerate(result['videos'], 1):
            print(f"\n{i}. 标题：{video['title']}")
            print(f"   链接：{video['url']}")
            print(f"   UP主：{video['up']}")
            print(f"   播放量：{video['play']}")
            print(f"   发布时间：{video['pubdate']}")

# 处理UP主视频获取请求
def handle_get_up_videos(up_name, output_dir="."):
    """
    处理UP主视频获取请求
    up_name: UP主名称
    output_dir: 输出目录
    """
    result = get_all_up_videos(up_name, output_dir)
    
    if "error" in result:
        print(f"错误: {result['error']}")
    else:
        print(f"\n已获取UP主 \"{result['name']}\" 的 {result['total']} 个视频")
        print(f"视频链接已保存到:")
        print(f"- JSON文件: {result['json_path']}")
        print(f"- 文本文件: {result['txt_path']}")

# 处理字幕转换请求
def handle_convert_subtitle(video_url, output_dir="."):
    """
    处理字幕转换请求
    video_url: 视频链接
    output_dir: 输出目录
    """
    result = convert_video_to_subtitle(video_url, output_dir)
    
    if result:
        print(f"\n字幕转换成功！")
        print(f"字幕文件已保存到: {result}")
    else:
        print("\n字幕转换失败！")

# 主函数
def main():
    """
    主函数
    """
    if len(sys.argv) < 2:
        print("用法:")
        print("  python bilibili_main.py search <关键词>")
        print("  python bilibili_main.py get_up <UP主名称> [输出目录]")
        print("  python bilibili_main.py convert <视频链接> [输出目录]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "search":
        if len(sys.argv) < 3:
            print("用法: python bilibili_main.py search <关键词>")
            sys.exit(1)
        keyword = sys.argv[2]
        handle_search(keyword)
    
    elif command == "get_up":
        if len(sys.argv) < 3:
            print("用法: python bilibili_main.py get_up <UP主名称> [输出目录]")
            sys.exit(1)
        up_name = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "."
        handle_get_up_videos(up_name, output_dir)
    
    elif command == "convert":
        if len(sys.argv) < 3:
            print("用法: python bilibili_main.py convert <视频链接> [输出目录]")
            sys.exit(1)
        video_url = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "."
        handle_convert_subtitle(video_url, output_dir)
    
    else:
        print("未知命令。可用命令: search, get_up, convert")
        sys.exit(1)

if __name__ == "__main__":
    main()
