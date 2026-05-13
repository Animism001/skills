#!/usr/bin/env python3
import json
import os
import time
import subprocess
from datetime import datetime

# 字幕文件目录
subtitle_dir = '/workspace/skills/xingyuexiezuo/字幕'

# 从字幕文件名中提取 BV 号
bv_list = []
for filename in os.listdir(subtitle_dir):
    if filename.endswith('_transcript.txt'):
        bv_match = None
        parts = filename.split('_BV')
        if len(parts) > 1:
            bv_part = parts[1].split('_')[0]
            bv = 'BV' + bv_part
            bv_list.append(bv)

print(f"找到 {len(bv_list)} 个 BV 号")

# 获取视频详情
video_data = []
script_path = '/workspace/skills/bilibili-search/scripts/bilibili.py'

for i, bv in enumerate(bv_list):
    print(f"[{i+1}/{len(bv_list)}] 获取 {bv}...")
    
    cmd = [
        'python3',
        script_path,
        json.dumps({"action": "video", "bvid": bv})
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if 'error' not in data:
                video_data.append(data)
                print(f"  成功: {data.get('title', '')}")
            else:
                print(f"  失败: {data.get('error')}")
        else:
            print(f"  错误: {result.stderr}")
            
    except Exception as e:
        print(f"  异常: {e}")
    
    # 控制请求频率，避免被限制
    time.sleep(1.5)

# 保存原始数据
output_dir = '/workspace/skills/xingyuexiezuo'
raw_file = os.path.join(output_dir, '视频数据_原始.json')
with open(raw_file, 'w', encoding='utf-8') as f:
    json.dump(video_data, f, ensure_ascii=False, indent=2)

print(f"\n原始数据已保存到: {raw_file}")
print(f"成功获取 {len(video_data)} 个视频信息")

# 生成 Markdown 文档
md_content = '''# 星月凌云 B站视频目录（含详细数据）

> 数据获取时间：{}
> UP主：-星月凌云-
> 视频总数：{}

---

## 视频列表（按发布时间排序）

| 序号 | 发布时间 | 视频标题 | 播放量 | 点赞 | 弹幕 | 收藏 | 硬币 | B站链接 |
|------|----------|----------|--------|------|------|------|------|----------|
'''.format(
    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    len(video_data)
)

# 按发布时间排序
video_data_sorted = sorted(video_data, key=lambda x: x.get('pubdate', 0), reverse=True)

for idx, video in enumerate(video_data_sorted, 1):
    # 格式化时间
    pubdate = video.get('pubdate')
    if pubdate:
        pubdate_str = datetime.fromtimestamp(pubdate).strftime('%Y-%m-%d')
    else:
        pubdate_str = '未知'
    
    title = video.get('title', '').replace('|', '&#124;')
    bvid = video.get('bvid', '')
    url = video.get('url', '')
    stat = video.get('stat', {})
    
    view = stat.get('view', 0)
    like = stat.get('like', 0)
    danmaku = stat.get('danmaku', 0)
    favorite = stat.get('favorite', 0)
    coin = stat.get('coin', 0)
    
    md_content += f'| {idx} | {pubdate_str} | {title} | {view} | {like} | {danmaku} | {favorite} | {coin} | [{bvid}]({url}) |\n'

# 添加统计信息
md_content += '''
---

## 📊 数据统计

| 指标 | 数值 |
|------|------|
| 视频总数 | {} |
| 总播放量 | {} |
| 总点赞 | {} |
| 总收藏 | {} |
| 总硬币 | {} |

---

## 📈 播放量 TOP10

'''.format(
    len(video_data),
    sum(v.get('stat', {}).get('view', 0) for v in video_data),
    sum(v.get('stat', {}).get('like', 0) for v in video_data),
    sum(v.get('stat', {}).get('favorite', 0) for v in video_data),
    sum(v.get('stat', {}).get('coin', 0) for v in video_data)
)

top10 = sorted(video_data, key=lambda x: x.get('stat', {}).get('view', 0), reverse=True)[:10]
md_content += '| 排名 | 播放量 | 标题 | 链接 |\n'
md_content += '|------|--------|------|------|\n'
for idx, v in enumerate(top10, 1):
    title = v.get('title', '').replace('|', '&#124;')
    bvid = v.get('bvid', '')
    url = v.get('url', '')
    view = v.get('stat', {}).get('view', 0)
    md_content += f'| {idx} | {view} | {title} | [{bvid}]({url}) |\n'

md_content += '''
---

> 🔗 UP主主页：https://space.bilibili.com/382179999
> 📝 数据来源：B站公开API
'''

# 保存 Markdown
md_file = os.path.join(output_dir, '星月凌云B站视频目录_详细数据.md')
with open(md_file, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"\nMarkdown文档已保存到: {md_file}")
print("完成！")
