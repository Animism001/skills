#!/usr/bin/env python3
"""
矩阵之网 SVG 卡片生成器（HTML 输出）— 自适应 + 导出

设计特色：
  - 支持 2×2 / 3×2 / 2×3 矩阵网格
  - 维度轴向指示 + 象限命名 + 关键特征
  - 径向渐变背景，双线边框 + 金色光晕
  - 半透明单元格 + hover 效果
  - 内容自适应高度
  - 导出工具栏（SVG / PNG / JPG / 自定义）

用法:
    1. 准备 JSON 数据文件:
    {
      "topic": "课题",
      "grid_type": "2x2",
      "dim1": {"name": "维度1", "low": "低", "high": "高", "mid": ""},
      "dim2": {"name": "维度2", "low": "低", "high": "高", "mid": ""},
      "cells": [
        {"name": "四字名", "features": ["特征1", "特征2", "特征3"]},
        ...
      ]
    }
    2. python3 generate_card.py --data data.json --output output.html

单元格顺序（行优先，从左到右，从上到下）：
    2×2: [TL, TR, BL, BR]
    3×2: [TL, TC, TR, BL, BC, BR]
    2×3: [TL, TR, ML, MR, BL, BR]
"""

import json
import argparse
import sys
import os


# ───────────────────────── 常量 ─────────────────────────

WIDTH = 720
MARGIN = 28
INNER_MARGIN = MARGIN + 14

# 颜色
BG_CENTER = "#0f0f23"
BG_EDGE = "#1a1a2e"
BORDER_GOLD = "#c9a961"
TITLE_COLOR = "#f0e6d3"
SUBTITLE_COLOR = "#c9a961"
TEXT_COLOR = "#e8dcc8"
DIM_COLOR = "#8a7d6b"
SEPARATOR_COLOR = "#4a4358"
CELL_BG = "rgba(201, 169, 97, 0.05)"
CELL_BORDER = "rgba(201, 169, 97, 0.15)"
AXIS_LINE_COLOR = "rgba(201, 169, 97, 0.25)"

FONT = "'KingHwa_OldSong', 'Noto Serif SC', 'SimSun', serif"


def _escape_xml(text: str) -> str:
    """转义 XML 特殊字符"""
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


# ───────────────────── SVG 定义区 ─────────────────────

def _svg_defs() -> list[str]:
    """生成 SVG <defs> 公共定义（渐变、滤镜、纹理、箭头标记）"""
    d = []
    d.append("  <defs>")

    # 径向渐变背景
    d.append('    <radialGradient id="bgGradient" cx="50%" cy="40%" r="70%" fx="50%" fy="40%">')
    d.append(f'      <stop offset="0%" stop-color="{BG_CENTER}"/>')
    d.append(f'      <stop offset="100%" stop-color="{BG_EDGE}"/>')
    d.append("    </radialGradient>")

    # 分隔线渐变
    d.append('    <linearGradient id="sepGradient" x1="0%" y1="0%" x2="100%" y2="0%">')
    d.append(f'      <stop offset="0%" stop-color="{SEPARATOR_COLOR}" stop-opacity="0"/>')
    d.append(f'      <stop offset="15%" stop-color="{SEPARATOR_COLOR}" stop-opacity="1"/>')
    d.append(f'      <stop offset="85%" stop-color="{SEPARATOR_COLOR}" stop-opacity="1"/>')
    d.append(f'      <stop offset="100%" stop-color="{SEPARATOR_COLOR}" stop-opacity="0"/>')
    d.append("    </linearGradient>")

    # 菱形渐变
    d.append('    <linearGradient id="diamondGradient" x1="0%" y1="0%" x2="100%" y2="100%">')
    d.append(f'      <stop offset="0%" stop-color="{BORDER_GOLD}" stop-opacity="0.9"/>')
    d.append(f'      <stop offset="100%" stop-color="{BORDER_GOLD}" stop-opacity="0.4"/>')
    d.append("    </linearGradient>")

    # 边框光晕
    d.append('    <filter id="borderGlow" x="-5%" y="-5%" width="110%" height="110%">')
    d.append('      <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur"/>')
    d.append('      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0.788  0 0 0 0 0.663  0 0 0 0 0.380  0 0 0 0.35 0" result="colorBlur"/>')
    d.append("      <feMerge>")
    d.append('        <feMergeNode in="colorBlur"/>')
    d.append('        <feMergeNode in="SourceGraphic"/>')
    d.append("      </feMerge>")
    d.append("    </filter>")

    # 网格纹理
    gs = 20
    d.append(f'    <pattern id="gridPattern" width="{gs}" height="{gs}" patternUnits="userSpaceOnUse">')
    d.append(f'      <path d="M {gs} 0 L 0 0 0 {gs}" fill="none" stroke="rgba(201,169,97,0.03)" stroke-width="0.5"/>')
    d.append("    </pattern>")

    # 噪点纹理
    d.append('    <filter id="noiseTexture" x="0%" y="0%" width="100%" height="100%">')
    d.append('      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" result="noise"/>')
    d.append('      <feColorMatrix type="saturate" values="0" in="noise" result="grayNoise"/>')
    d.append('      <feComponentTransfer in="grayNoise" result="faintNoise">')
    d.append('        <feFuncA type="linear" slope="0.03"/>')
    d.append("      </feComponentTransfer>")
    d.append('      <feBlend in="SourceGraphic" in2="faintNoise" mode="overlay"/>')
    d.append("    </filter>")

    d.append("  </defs>")
    return d


# ───────────────────── 核心生成 ─────────────────────

def generate_matrix_svg(data: dict) -> str:
    """根据结构化数据生成矩阵 SVG"""

    grid_type = data.get("grid_type", "2x2")
    cols, rows = map(int, grid_type.split("x"))
    topic = data["topic"]
    dim1 = data["dim1"]
    dim2 = data["dim2"]
    cells = data["cells"]

    # 内容区
    L = INNER_MARGIN + 10
    R = WIDTH - INNER_MARGIN - 10
    W = R - L

    # ── 行标签左侧留白 ──
    ROW_LABEL_W = 46

    grid_left = L + ROW_LABEL_W
    grid_right = R
    grid_width = grid_right - grid_left

    # ── 单元格尺寸 ──
    cell_gap = 6
    cell_w = (grid_width - (cols - 1) * cell_gap) / cols
    max_feats = max((len(c.get("features", [])) for c in cells), default=0)
    cell_h = max(128, 42 + max_feats * 17 + 18)

    # ════════════════ 布局 Y 计算 ════════════════
    y = INNER_MARGIN

    # 标题区
    y += 8
    title_y = y + 22
    topic_y = y + 44
    y += 54

    # 分隔线 1
    sep1_y = y
    y += 16

    # dim2 名称 + 方向箭头（网格上方）
    dim2_name_y = y + 12
    y += 20

    # 列头（dim1 级别标签，网格上方）
    col_header_y = y + 10
    y += 18

    # ── 网格区 ──
    grid_top = y
    grid_height = cell_h * rows + cell_gap * (rows - 1)
    grid_bottom = grid_top + grid_height
    y = grid_bottom

    # dim1 名称 + 方向箭头（网格下方）
    dim1_labels_y = y + 14
    y += 20
    dim1_name_y = y + 10
    y += 22

    # 分隔线 2
    sep2_y = y
    y += 6

    # 总高度
    HEIGHT = y + INNER_MARGIN + 10
    HEIGHT = max(HEIGHT, 480)

    grid_center_x = grid_left + grid_width / 2

    # ════════════════ 构建 SVG ════════════════
    s = []

    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
             f'class="matrix-card-svg">')

    # defs
    s.extend(_svg_defs())

    # style
    s.append("  <style>")
    s.append("    .matrix-cell { transition: all 0.2s ease; }")
    s.append("    .matrix-cell:hover { filter: brightness(1.3); }")
    s.append("    .matrix-cell:hover .cell-bg { fill: rgba(201,169,97,0.12); stroke: rgba(201,169,97,0.35); stroke-width: 0.8; }")
    s.append("    .matrix-cell:hover .cell-name { fill: #f0e6d3; }")
    s.append("  </style>")

    # ── 背景层 ──
    s.append(f'  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bgGradient)" rx="6"/>')
    s.append(f'  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#gridPattern)" rx="6"/>')
    s.append(f'  <rect width="{WIDTH}" height="{HEIGHT}" fill="transparent" filter="url(#noiseTexture)" rx="6"/>')

    # ── 外边框 ──
    s.append(f'  <rect x="{MARGIN}" y="{MARGIN}" width="{WIDTH-2*MARGIN}" height="{HEIGHT-2*MARGIN}" '
             f'fill="none" stroke="{BORDER_GOLD}" stroke-width="1" rx="4" filter="url(#borderGlow)" opacity="0.7"/>')
    s.append(f'  <rect x="{INNER_MARGIN}" y="{INNER_MARGIN}" width="{WIDTH-2*INNER_MARGIN}" height="{HEIGHT-2*INNER_MARGIN}" '
             f'fill="none" stroke="{BORDER_GOLD}" stroke-width="0.5" rx="2" opacity="0.5"/>')

    # 四角装饰
    cs = 4
    for cx, cy in [(MARGIN+2, MARGIN+2), (WIDTH-MARGIN-2-cs, MARGIN+2),
                    (MARGIN+2, HEIGHT-MARGIN-2-cs), (WIDTH-MARGIN-2-cs, HEIGHT-MARGIN-2-cs)]:
        s.append(f'  <rect x="{cx}" y="{cy}" width="{cs}" height="{cs}" fill="{BORDER_GOLD}" opacity="0.6"/>')

    # ── 标题区 ──
    diamond_cx, diamond_cy, diamond_size = L, title_y - 6, 5
    s.append(f'  <polygon points="{diamond_cx},{diamond_cy-diamond_size} '
             f'{diamond_cx+diamond_size},{diamond_cy} '
             f'{diamond_cx},{diamond_cy+diamond_size} '
             f'{diamond_cx-diamond_size},{diamond_cy}" '
             f'fill="url(#diamondGradient)"/>')
    s.append(f'  <text x="{L+16}" y="{title_y}" font-family="{FONT}" font-size="22" '
             f'fill="{TITLE_COLOR}" font-weight="bold" letter-spacing="4">矩阵之网</text>')
    # 标题后装饰线
    title_end_x = L + 16 + 22 * 4
    s.append(f'  <line x1="{title_end_x+12}" y1="{title_y-6}" x2="{R}" y2="{title_y-6}" '
             f'stroke="{BORDER_GOLD}" stroke-width="0.5" opacity="0.3"/>')
    s.append(f'  <text x="{R}" y="{topic_y}" font-family="{FONT}" font-size="17" '
             f'fill="{SUBTITLE_COLOR}" text-anchor="end" font-weight="bold" letter-spacing="2">{_escape_xml(topic)}</text>')

    # ── 分隔线 1 ──
    s.append(f'  <line x1="{L}" y1="{sep1_y}" x2="{R}" y2="{sep1_y}" stroke="url(#sepGradient)" stroke-width="0.6"/>')

    # ── dim2 名称（网格上方居中）+ 方向箭头 ──
    s.append(f'  <text x="{grid_center_x}" y="{dim2_name_y}" font-family="{FONT}" font-size="12" '
             f'fill="{DIM_COLOR}" text-anchor="middle" letter-spacing="2">{_escape_xml(dim2["name"])}</text>')
    # 方向指示线（垂直小箭头，dim2 从低到高）
    arr_x = grid_center_x
    arr_top = dim2_name_y + 4
    arr_bot = col_header_y - 2
    s.append(f'  <line x1="{arr_x}" y1="{arr_bot}" x2="{arr_x}" y2="{arr_top}" '
             f'stroke="{BORDER_GOLD}" stroke-width="0.6" opacity="0.35"/>')
    # 箭头尖 ▲
    s.append(f'  <polygon points="{arr_x},{arr_top-3} {arr_x+3},{arr_top+3} {arr_x-3},{arr_top+3}" '
             f'fill="{BORDER_GOLD}" opacity="0.4"/>')

    # ── 列头：dim1 级别标签（网格上方，每列居中） ──
    for col in range(cols):
        cx = grid_left + col * (cell_w + cell_gap) + cell_w / 2
        if cols == 2:
            label = dim1["low"] if col == 0 else dim1["high"]
        else:
            label = [dim1["low"], dim1.get("mid", "中"), dim1["high"]][col]
        s.append(f'  <text x="{cx}" y="{col_header_y}" font-family="{FONT}" font-size="10" '
                 f'fill="{DIM_COLOR}" text-anchor="middle">{_escape_xml(label)}</text>')

    # ── 网格单元格 ──
    for row in range(rows):
        for col in range(cols):
            idx = row * cols + col
            if idx >= len(cells):
                break
            cell = cells[idx]
            cx = grid_left + col * (cell_w + cell_gap)
            cy = grid_top + row * (cell_h + cell_gap)

            s.append(f'  <g class="matrix-cell">')

            # 单元格背景
            s.append(f'    <rect class="cell-bg" x="{cx}" y="{cy}" width="{cell_w}" height="{cell_h}" '
                     f'fill="{CELL_BG}" stroke="{CELL_BORDER}" stroke-width="0.5" rx="4"/>')

            # 小菱形装饰
            dm_cx = cx + cell_w / 2
            dm_cy = cy + 18
            dm_s = 3.5
            s.append(f'    <polygon points="{dm_cx},{dm_cy-dm_s} {dm_cx+dm_s},{dm_cy} '
                     f'{dm_cx},{dm_cy+dm_s} {dm_cx-dm_s},{dm_cy}" '
                     f'fill="url(#diamondGradient)" opacity="0.6"/>')

            # 象限名称
            name_y = cy + 36
            s.append(f'    <text class="cell-name" x="{cx+cell_w/2}" y="{name_y}" font-family="{FONT}" '
                     f'font-size="15" fill="{SUBTITLE_COLOR}" text-anchor="middle" '
                     f'font-weight="bold" letter-spacing="3">{_escape_xml(cell["name"])}</text>')

            # 名称下分隔线
            sep_y = name_y + 8
            s.append(f'    <line x1="{cx+14}" y1="{sep_y}" x2="{cx+cell_w-14}" y2="{sep_y}" '
                     f'stroke="{BORDER_GOLD}" stroke-width="0.3" opacity="0.2"/>')

            # 特征列表
            for fi, feat in enumerate(cell.get("features", [])):
                feat_y = sep_y + 16 + fi * 17
                s.append(f'    <text x="{cx+16}" y="{feat_y}" font-family="{FONT}" font-size="11" '
                         f'fill="{TEXT_COLOR}">· {_escape_xml(feat)}</text>')

            s.append(f'  </g>')

    # ── 行标签：dim2 级别（网格左侧，每行居中） ──
    for row in range(rows):
        cy = grid_top + row * (cell_h + cell_gap) + cell_h / 2
        if rows == 2:
            label = dim2["high"] if row == 0 else dim2["low"]
        else:
            label = [dim2["high"], dim2.get("mid", "中"), dim2["low"]][row]
        s.append(f'  <text x="{grid_left - 8}" y="{cy + 4}" font-family="{FONT}" font-size="10" '
                 f'fill="{DIM_COLOR}" text-anchor="end">{_escape_xml(label)}</text>')

    # ── dim1 方向指示线（网格下方，水平） ──
    dim1_arr_y = dim1_labels_y - 4
    s.append(f'  <line x1="{grid_left}" y1="{dim1_arr_y}" x2="{grid_right}" y2="{dim1_arr_y}" '
             f'stroke="{BORDER_GOLD}" stroke-width="0.6" opacity="0.35"/>')
    # 箭头尖 ▶
    s.append(f'  <polygon points="{grid_right+3},{dim1_arr_y} {grid_right-3},{dim1_arr_y-3} {grid_right-3},{dim1_arr_y+3}" '
             f'fill="{BORDER_GOLD}" opacity="0.4"/>')

    # dim1 级别标签（下方两端）
    s.append(f'  <text x="{grid_left}" y="{dim1_labels_y+10}" font-family="{FONT}" font-size="10" '
             f'fill="{DIM_COLOR}" text-anchor="start">{_escape_xml(dim1["low"])}</text>')
    s.append(f'  <text x="{grid_right}" y="{dim1_labels_y+10}" font-family="{FONT}" font-size="10" '
             f'fill="{DIM_COLOR}" text-anchor="end">{_escape_xml(dim1["high"])}</text>')

    # dim1 名称（居中）
    s.append(f'  <text x="{grid_center_x}" y="{dim1_name_y}" font-family="{FONT}" font-size="12" '
             f'fill="{DIM_COLOR}" text-anchor="middle" letter-spacing="2">{_escape_xml(dim1["name"])}</text>')

    # ── 分隔线 2 ──
    s.append(f'  <line x1="{L}" y1="{sep2_y}" x2="{R}" y2="{sep2_y}" stroke="url(#sepGradient)" stroke-width="0.6"/>')

    s.append('</svg>')
    return "\n".join(s)


# ───────────────────── HTML 输出 ─────────────────────

def generate_html(data: dict, output_path: str) -> str:
    """生成包含矩阵 SVG 的 HTML 文件（响应式 + 导出工具栏）"""

    svg_content = generate_matrix_svg(data)
    topic_escaped = _escape_xml(data["topic"])

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>矩阵之网 — {topic_escaped}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap');

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    background: #0f0f23;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    font-family: 'Noto Serif SC', sans-serif;
    padding: 24px 16px 40px;
  }}

  .page-container {{
    width: 100%;
    max-width: 760px;
  }}

  .card-wrapper {{
    width: 100%;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 120px rgba(201,169,97,0.05);
  }}

  .matrix-card-svg {{
    display: block;
    width: 100%;
    height: auto;
    border-radius: 6px;
  }}

  /* ========== 导出工具栏 ========== */
  .export-bar {{
    width: 100%;
    margin-top: 16px;
    padding: 12px 18px;
    background: rgba(26,26,46,0.85);
    border: 1px solid rgba(201,169,97,0.12);
    border-radius: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    backdrop-filter: blur(8px);
  }}

  .export-bar .bar-label {{
    font-size: 12px; color: #6b6155;
    letter-spacing: 2px; margin-right: 2px;
    user-select: none; text-transform: uppercase;
  }}

  .export-btn {{
    display: inline-flex; align-items: center; justify-content: center; gap: 5px;
    padding: 7px 14px; font-family: 'Noto Serif SC', sans-serif; font-size: 13px;
    color: #c9a961; background: rgba(201,169,97,0.06);
    border: 1px solid rgba(201,169,97,0.18); border-radius: 6px;
    cursor: pointer; transition: all 0.2s ease; user-select: none; white-space: nowrap;
  }}
  .export-btn:hover {{
    background: rgba(201,169,97,0.16); border-color: rgba(201,169,97,0.4); color: #f0e6d3;
  }}
  .export-btn:active {{ transform: scale(0.97); background: rgba(201,169,97,0.22); }}
  .export-btn.active {{
    background: rgba(201,169,97,0.2); border-color: rgba(201,169,97,0.5); color: #f0e6d3;
  }}

  .export-btn .btn-icon svg {{
    width: 14px; height: 14px; fill: none; stroke: currentColor;
    stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;
  }}

  /* 展开面板 */
  .export-panel {{
    width: 100%; margin-top: 12px;
    background: rgba(26,26,46,0.92); border: 1px solid rgba(201,169,97,0.14);
    border-radius: 10px; padding: 20px 22px 18px; display: none;
  }}
  .export-panel.visible {{
    display: block; animation: panelIn 0.25s ease;
  }}
  @keyframes panelIn {{
    from {{ opacity: 0; transform: translateY(-8px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
  }}

  .panel-grid {{
    display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; align-items: end;
  }}

  .panel-field-label {{
    font-size: 11px; color: #6b6155; letter-spacing: 1px;
    margin-bottom: 7px; user-select: none;
  }}

  .panel-select {{
    width: 100%; padding: 8px 32px 8px 12px;
    font-family: 'Noto Serif SC', sans-serif; font-size: 13px; color: #e8dcc8;
    background: rgba(15,15,35,0.8); border: 1px solid rgba(201,169,97,0.2);
    border-radius: 6px; outline: none; cursor: pointer;
    appearance: none; -webkit-appearance: none; -moz-appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' fill='none'%3E%3Cpath d='M1 1l4 4 4-4' stroke='%236b6155' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
    background-repeat: no-repeat; background-position: right 10px center;
    transition: border-color 0.2s ease;
  }}
  .panel-select:hover {{ border-color: rgba(201,169,97,0.35); }}
  .panel-select:focus {{ border-color: rgba(201,169,97,0.55); box-shadow: 0 0 0 2px rgba(201,169,97,0.08); }}
  .panel-select option {{ background: #1a1a2e; color: #e8dcc8; }}

  .panel-action {{
    grid-column: 1 / -1; display: flex; justify-content: center; margin-top: 6px;
  }}

  .panel-export-btn {{
    padding: 9px 48px; font-family: 'Noto Serif SC', sans-serif; font-size: 13px;
    color: #0f0f23; background: linear-gradient(135deg, #c9a961 0%, #a88b3d 100%);
    border: none; border-radius: 6px; cursor: pointer;
    transition: all 0.2s ease; letter-spacing: 2px; font-weight: bold;
  }}
  .panel-export-btn:hover {{ filter: brightness(1.12); box-shadow: 0 2px 12px rgba(201,169,97,0.3); }}
  .panel-export-btn:active {{ transform: scale(0.98); }}

  /* Toast */
  .toast {{
    position: fixed; top: 24px; left: 50%;
    transform: translateX(-50%) translateY(-60px);
    padding: 10px 28px; background: rgba(201,169,97,0.92); color: #0f0f23;
    font-size: 13px; border-radius: 8px; opacity: 0;
    transition: all 0.3s ease; z-index: 9999; pointer-events: none;
    font-weight: bold; letter-spacing: 0.5px; box-shadow: 0 4px 20px rgba(0,0,0,0.4);
  }}
  .toast.show {{ opacity: 1; transform: translateX(-50%) translateY(0); }}

  @media (max-width: 480px) {{
    body {{ padding: 12px 8px 32px; }}
    .card-wrapper {{ padding: 10px; }}
    .export-bar {{ padding: 10px 12px; gap: 6px; }}
    .export-btn {{ padding: 6px 10px; font-size: 12px; }}
    .panel-grid {{ grid-template-columns: 1fr; gap: 10px; }}
  }}
</style>
</head>
<body>

<div class="page-container">
  <div class="card-wrapper">
    {svg_content}
  </div>

  <div class="export-bar">
    <span class="bar-label">导出</span>
    <button class="export-btn" onclick="exportSVG()">
      <span class="btn-icon"><svg viewBox="0 0 24 24"><path d="M12 3v12m0 0l-4-4m4 4l4-4M4 17v2a2 2 0 002 2h12a2 2 0 002-2v-2"/></svg></span>
      SVG
    </button>
    <button class="export-btn" onclick="exportPNG()">
      <span class="btn-icon"><svg viewBox="0 0 24 24"><path d="M12 3v12m0 0l-4-4m4 4l4-4M4 17v2a2 2 0 002 2h12a2 2 0 002-2v-2"/></svg></span>
      PNG
    </button>
    <button class="export-btn" onclick="exportJPG()">
      <span class="btn-icon"><svg viewBox="0 0 24 24"><path d="M12 3v12m0 0l-4-4m4 4l4-4M4 17v2a2 2 0 002 2h12a2 2 0 002-2v-2"/></svg></span>
      JPG
    </button>
    <button class="export-btn" id="otherBtn" onclick="togglePanel()">
      <span class="btn-icon"><svg viewBox="0 0 24 24"><circle cx="5" cy="12" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="19" cy="12" r="1.5"/></svg></span>
      其他
    </button>
  </div>

  <div class="export-panel" id="exportPanel">
    <div class="panel-grid">
      <div>
        <div class="panel-field-label">尺寸</div>
        <select class="panel-select" id="sizeSelect">
          <option value="1">原始 (720px)</option>
          <option value="1.5">1.5x (1080px)</option>
          <option value="2" selected>2x (1440px)</option>
          <option value="3">3x (2160px)</option>
          <option value="4">4x (2880px)</option>
        </select>
      </div>
      <div>
        <div class="panel-field-label">分辨率</div>
        <select class="panel-select" id="dpiSelect">
          <option value="72">72 DPI (屏幕)</option>
          <option value="150">150 DPI (打印)</option>
          <option value="300" selected>300 DPI (高清)</option>
        </select>
      </div>
      <div>
        <div class="panel-field-label">格式</div>
        <select class="panel-select" id="formatSelect">
          <option value="png">PNG (透明)</option>
          <option value="jpg">JPG (白底)</option>
          <option value="webp">WebP (透明)</option>
        </select>
      </div>
      <div class="panel-action">
        <button class="panel-export-btn" onclick="exportCustom()">导出</button>
      </div>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
(function() {{
  'use strict';
  var DOMAIN = '{topic_escaped}';
  var svgEl = document.querySelector('.matrix-card-svg');

  function showToast(msg) {{
    var t = document.getElementById('toast');
    t.textContent = msg; t.classList.add('show');
    clearTimeout(t._timer);
    t._timer = setTimeout(function() {{ t.classList.remove('show'); }}, 2200);
  }}

  function getSVGString() {{
    var clone = svgEl.cloneNode(true);
    clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    clone.removeAttribute('class');
    return new XMLSerializer().serializeToString(clone);
  }}

  function downloadBlob(blob, filename) {{
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    setTimeout(function() {{ URL.revokeObjectURL(url); }}, 5000);
  }}

  function svgToCanvas(scale) {{
    return new Promise(function(resolve, reject) {{
      var vb = svgEl.viewBox.baseVal;
      var w = vb.width * scale, h = vb.height * scale;
      var svgStr = getSVGString();
      var img = new Image();
      var blob = new Blob([svgStr], {{ type: 'image/svg+xml;charset=utf-8' }});
      var url = URL.createObjectURL(blob);
      img.onload = function() {{
        var canvas = document.createElement('canvas');
        canvas.width = w; canvas.height = h;
        canvas.getContext('2d').drawImage(img, 0, 0, w, h);
        URL.revokeObjectURL(url); resolve(canvas);
      }};
      img.onerror = function() {{ URL.revokeObjectURL(url); reject(new Error('SVG rendering failed')); }};
      img.src = url;
    }});
  }}

  function canvasToBlob(canvas, type, quality) {{
    return new Promise(function(resolve) {{ canvas.toBlob(resolve, type, quality); }});
  }}

  window.exportSVG = function() {{
    var blob = new Blob([getSVGString()], {{ type: 'image/svg+xml;charset=utf-8' }});
    downloadBlob(blob, '矩阵之网-' + DOMAIN + '.svg');
    showToast('SVG 已导出');
  }};

  window.exportPNG = function() {{
    svgToCanvas(2).then(function(c) {{ return canvasToBlob(c, 'image/png'); }})
    .then(function(b) {{ downloadBlob(b, '矩阵之网-' + DOMAIN + '.png'); showToast('PNG 已导出 (2x)'); }})
    .catch(function() {{ showToast('导出失败'); }});
  }};

  window.exportJPG = function() {{
    svgToCanvas(2).then(function(canvas) {{
      var w = canvas.width, h = canvas.height;
      var c2 = document.createElement('canvas'); c2.width = w; c2.height = h;
      var ctx = c2.getContext('2d'); ctx.fillStyle = '#ffffff'; ctx.fillRect(0,0,w,h);
      ctx.drawImage(canvas, 0, 0);
      return canvasToBlob(c2, 'image/jpeg', 0.92);
    }}).then(function(b) {{ downloadBlob(b, '矩阵之网-' + DOMAIN + '.jpg'); showToast('JPG 已导出 (2x)'); }})
    .catch(function() {{ showToast('导出失败'); }});
  }};

  window.togglePanel = function() {{
    var p = document.getElementById('exportPanel'), b = document.getElementById('otherBtn');
    var v = p.classList.contains('visible');
    p.classList.toggle('visible', !v); b.classList.toggle('active', !v);
  }};

  window.exportCustom = function() {{
    var scale = parseFloat(document.getElementById('sizeSelect').value);
    var dpi = parseInt(document.getElementById('dpiSelect').value, 10);
    var format = document.getElementById('formatSelect').value;
    var finalScale = scale * (dpi / 300);
    var mimeMap = {{ png:'image/png', jpg:'image/jpeg', webp:'image/webp' }};
    var extMap  = {{ png:'png', jpg:'jpg', webp:'webp' }};
    var mime = mimeMap[format], ext = extMap[format];
    var quality = format === 'jpg' ? 0.95 : undefined;

    svgToCanvas(finalScale).then(function(canvas) {{
      if (format === 'jpg') {{
        var w = canvas.width, h = canvas.height;
        var c2 = document.createElement('canvas'); c2.width = w; c2.height = h;
        var ctx = c2.getContext('2d'); ctx.fillStyle = '#ffffff'; ctx.fillRect(0,0,w,h);
        ctx.drawImage(canvas, 0, 0); return canvasToBlob(c2, mime, quality);
      }}
      return canvasToBlob(canvas, mime, quality);
    }}).then(function(b) {{
      downloadBlob(b, '矩阵之网-' + DOMAIN + '-' + scale + 'x-' + dpi + 'DPI.' + ext);
      showToast(ext.toUpperCase() + ' 已导出 (' + scale + 'x / ' + dpi + 'DPI)');
      document.getElementById('exportPanel').classList.remove('visible');
      document.getElementById('otherBtn').classList.remove('active');
    }}).catch(function() {{ showToast('导出失败'); }});
  }};
}})();
</script>

</body>
</html>"""

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path


# ───────────────────── 入口 ─────────────────────

def main():
    parser = argparse.ArgumentParser(description="矩阵之网 SVG 卡片生成器")
    parser.add_argument("--data", required=True, help="JSON 数据文件路径")
    parser.add_argument("--output", required=True, help="HTML 输出路径")
    args = parser.parse_args()

    with open(args.data, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 校验
    grid_type = data.get("grid_type", "2x2")
    cols, rows = map(int, grid_type.split("x"))
    expected = cols * rows
    actual = len(data.get("cells", []))
    if actual != expected:
        print(f"错误：grid_type={grid_type} 需要 {expected} 个单元格，当前 {actual} 个", file=sys.stderr)
        sys.exit(1)

    for field in ["topic", "dim1", "dim2", "cells"]:
        if field not in data:
            print(f"错误：缺少字段 '{field}'", file=sys.stderr)
            sys.exit(1)
    for sub in ["dim1", "dim2"]:
        for key in ["name", "low", "high"]:
            if key not in data[sub]:
                print(f"错误：{sub} 缺少字段 '{key}'", file=sys.stderr)
                sys.exit(1)

    output_path = generate_html(data, args.output)
    print(f"矩阵卡片已生成: {output_path}")


if __name__ == "__main__":
    main()
