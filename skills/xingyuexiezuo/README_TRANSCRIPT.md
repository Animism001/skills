# 星月凌云视频文字版提取说明

## 目录结构

```
/workspace/skills/xingyuexiezuo/
├── transcripts/              # 转录结果目录
│   ├── AI写作技巧/
│   ├── 使用教程/
│   ├── 收益与赚钱/
│   ├── 作者访谈/
│   ├── 创作素材/
│   ├── 榜单成绩/
│   ├── 其他/
│   ├── 新手入门/
│   ├── 励志故事/
│   ├── AI模型评测/
│   └── 短剧改编/
├── videos_by_category.json   # 视频分类信息
├── fetch_subtitles.py        # 获取B站字幕脚本
├── transcribe_all_videos.py  # 完整转录脚本(需要whisper)
└── test_parse.py             # 测试脚本
```

## 使用方法

### 1. 获取B站自带字幕(推荐)

首先尝试获取视频自带的字幕:

```bash
cd /workspace/skills/xingyuexiezuo
python fetch_subtitles.py
```

这个脚本会:
- 先检查视频是否有B站官方字幕
- 如果有,直接下载并保存
- 保存到对应分类目录

### 2. 使用yt-dlp + whisper完整转录

如果视频没有自带字幕,可以使用完整转录:

```bash
# 首先安装依赖
pip install yt-dlp openai-whisper

# 运行转录
python transcribe_all_videos.py
```

注意: whisper需要下载模型文件(约1GB左右),并且转录156个视频需要较长时间。

## 文件说明

- `videos_by_category.json`: 所有视频按分类整理的信息,包含BV号、标题、发布时间
- `transcripts/`: 按分类存放的文字版文件,文件名为BV号.txt
- `fetch_subtitles.py`: 优先获取B站官方字幕的脚本
- `transcribe_all_videos.py`: 使用yt-dlp下载音频 + whisper转录的完整脚本

## 视频分类统计

- AI写作技巧: 90个
- 使用教程: 35个
- 收益与赚钱: 10个
- 作者访谈: 5个
- 创作素材: 5个
- 榜单成绩: 4个
- 其他: 3个
- 新手入门: 1个
- 励志故事: 1个
- AI模型评测: 1个
- 短剧改编: 1个

总计: 156个视频
