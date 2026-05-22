#!/usr/bin/env python3
import os
import json
import subprocess
import tempfile
from pathlib import Path


def transcribe_video(bv_id, output_file):
    """使用yt-dlp下载音频并用whisper转录"""
    url = f"https://www.bilibili.com/video/{bv_id}"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        audio_file = tmp_path / f"{bv_id}.m4a"
        
        try:
            # 下载音频
            print(f"  下载音频...")
            cmd = [
                'yt-dlp',
                '-x', '--audio-format', 'm4a',
                '-o', str(audio_file),
                '--no-playlist',
                url
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                return False, f"下载失败: {result.stderr}"
            
            # 检查文件
            actual_audio = None
            for f in tmp_path.iterdir():
                if f.suffix in ['.m4a', '.mp3', '.wav', '.webm']:
                    actual_audio = f
                    break
            
            if not actual_audio:
                return False, "未找到下载的音频文件"
            
            # 使用whisper转录
            print(f"  转录中...")
            cmd = [
                'whisper',
                str(actual_audio),
                '--language', 'Chinese',
                '--model', 'tiny',  # 使用最小模型
                '--output_format', 'txt',
                '--output_dir', str(tmp_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            # 查找输出文件
            transcript_file = None
            for f in tmp_path.iterdir():
                if f.name.endswith('.txt') and bv_id in f.name:
                    transcript_file = f
                    break
            
            if transcript_file and transcript_file.exists():
                import shutil
                shutil.move(str(transcript_file), str(output_file))
                return True, None
            else:
                return False, "转录文件未生成"
                
        except subprocess.TimeoutExpired:
            return False, "处理超时"
        except Exception as e:
            return False, str(e)


def main():
    base_dir = Path("/workspace/skills/xingyuexiezuo")
    json_file = base_dir / "videos_by_category.json"
    transcripts_dir = base_dir / "transcripts"
    
    # 加载分类信息
    with open(json_file, 'r', encoding='utf-8') as f:
        videos_by_category = json.load(f)
    
    # 只处理前5个视频作为测试
    limit = 5
    count = 0
    
    for category, videos in videos_by_category.items():
        cat_dir = transcripts_dir / category
        
        for video in videos:
            if count >= limit:
                break
                
            bv_id = video['bv_id']
            title = video['title']
            output_file = cat_dir / f"{bv_id}.txt"
            
            if output_file.exists():
                print(f"已存在,跳过: {bv_id}")
                count += 1
                continue
            
            print(f"\n[{count+1}/{limit}] 处理: {bv_id}")
            print(f"  标题: {title[:40]}...")
            
            success, error = transcribe_video(bv_id, output_file)
            
            if success:
                print(f"  ✓ 成功: {output_file}")
                # 添加标题信息
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"标题: {title}\n")
                    f.write(f"BV号: {bv_id}\n")
                    f.write(f"分类: {category}\n")
                    f.write("="*50 + "\n\n")
                    f.write(content)
            else:
                print(f"  ✗ 失败: {error}")
            
            count += 1
    
    print(f"\n测试完成,处理了 {count} 个视频")


if __name__ == "__main__":
    main()
