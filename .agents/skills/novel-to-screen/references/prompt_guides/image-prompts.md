# 图片生成提示词规范

## 基本结构

```
[主体描述], [风格], [光影], [构图], [细节], [负面提示词]
```

## 必须包含的要素

1. **主体描述** — 清晰描述画面主体
2. **风格** — 由分类参数决定（真人写实/2D动漫/3D渲染/水墨等）
3. **光影** — 光源方向、色温、阴影
4. **构图** — 景别、视角、画面比例
5. **负面提示词** — 排除不想要的元素

## 风格预设关键词

| 类型 | 风格关键词 |
|------|-----------|
| 真人 | photorealistic, cinematic lighting, 8K, DSLR |
| 动画(2D) | anime style, cel shading, vibrant colors |
| 动画(3D) | 3D render, Pixar style, volumetric lighting |
| 动画(水墨) | Chinese ink wash painting, traditional, minimalist |
| 动画(赛璐璐) | cel animation, hand-drawn, classic anime |
| 动画(像素) | pixel art, retro game, 16-bit |
| 动画(绘本) | picture book illustration, soft colors, whimsical |

## 画面比例

| 体裁 | 比例 |
|------|------|
| 短剧 | 9:16（竖屏） |
| 微电影 | 16:9 |
| 电影 | 2.39:1（宽银幕） |
| 电视剧 | 16:9 |

## 一致性要求

- 同一人物在不同提示词中外貌描述必须一致
- 同一场景在不同提示词中空间布局必须一致
- 风格关键词在所有提示词中必须统一
