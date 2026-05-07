# 项目结构说明

## 📂 目录结构

```
/workspace/
├── Library/                       # 图书存放目录
├── scripts/                       # 脚本目录
│   ├── bilibili/                 # B站相关脚本
│   │   ├── convert_videos_to_subtitles.py
│   │   ├── final_attempt_to_get_all_videos.py
│   │   ├── get_all_videos.py
│   │   ├── get_bilibili_subtitles.py
│   │   ├── get_complete_videos.py
│   │   ├── get_complete_videos_with_gzip.py
│   │   └── temp_research.py
│   └── utils/                    # 通用工具脚本（预留）
├── data/                         # 数据目录
│   ├── xingyue_videos/          # 星月视频数据
│   │   ├── xingyue_videos.json
│   │   ├── xingyue_videos_complete.json
│   │   ├── xingyue_videos_final.json
│   │   ├── xingyue_videos_links.txt
│   │   └── xingyue_videos_complete_links.txt
│   ├── star_river_videos/       # 星河视频数据
│   │   ├── all_videos.json
│   │   ├── subtitles/           # 字幕文件
│   │   ├── 工作成果总结.md
│   │   └── ...其他脚本文件
│   └── test_subtitles/          # 字幕测试数据
├── skills/                       # 技能目录
│   ├── bilibili/               # B站技能
│   ├── bilibili-search/        # B站搜索技能
│   ├── bilibili-transcript/    # B站字幕技能
│   ├── book-fetch/             # 图书获取技能
│   ├── cangjie-skill/          # 仓颉技能
│   ├── huashu-nuwa/           # 华树女娲技能
│   ├── ima-skill/              # IMA技能
│   ├── inkos/                  # InkOS技能
│   ├── literature-search/       # 文献搜索技能
│   ├── multi-search-engine/    # 多搜索引擎技能
│   ├── randy-ingermanson-perspective/
│   ├── robert-mckee-perspective/
│   ├── self-improving/         # 自我提升技能
│   ├── self-improving-agent/   # 自我提升代理技能
│   ├── skill-creator/          # 技能创建器
│   ├── thinking-model-enhancer/ # 思考模型增强
│   ├── web-researcher/         # 网页研究
│   ├── xingyuexiezuo/          # 星月写作
│   └── youtube-transcript/     # YouTube字幕
├── .clawhub/                    # Clawhub配置
├── .evals/                      # 评估目录
├── .gitignore                  # Git忽略文件
├── LICENSE                     # 许可证
└── README.md                  # 项目说明
```

## 📋 目录说明

### 📚 Library/
专门用于存放图书文件、PDF、电子书等文档资源。

### 🔧 scripts/
存放所有脚本文件，按功能分类：
- **bilibili/** - B站视频获取、字幕处理相关脚本
- **utils/** - 通用工具脚本（预留）

### 💾 data/
存放所有数据文件：
- **xingyue_videos/** - 星月视频相关数据
- **star_river_videos/** - 星河视频项目
- **test_subtitles/** - 字幕测试数据

### 🎯 skills/
存放所有技能，这是项目的核心部分。

## 🔄 文件位置对照表

| 旧位置 | 新位置 |
|--------|--------|
| /workspace/get_all_videos.py | /workspace/scripts/bilibili/get_all_videos.py |
| /workspace/xingyue_videos.json | /workspace/data/xingyue_videos/xingyue_videos.json |
| /workspace/star_river_videos/ | /workspace/data/star_river_videos/ |
| /workspace/test_subtitles/ | /workspace/data/test_subtitles/ |

## 📌 使用说明

1. **新增脚本** → 放入对应分类的 `scripts/` 子目录
2. **新增数据** → 放入 `data/` 对应子目录
3. **新增图书** → 放入 `Library/`
4. **技能管理** → 在 `skills/` 目录中维护

## 🎯 优化优势

✅ 逻辑清晰，易于维护
✅ 分类明确，查找方便
✅ 避免根目录杂乱
✅ 便于后续扩展
