#!/usr/bin/env python3
"""
SRT 分段翻译预处理脚本
解决长文本上下文丢失问题
"""

import json
import re
import sys
from pathlib import Path

# 默认术语文件路径
DEFAULT_REFERENCES_DIR = Path(__file__).parent.parent / "references"

def load_term_dict(filename: str) -> dict:
    """加载术语对照表，返回 en -> cn 映射"""
    filepath = DEFAULT_REFERENCES_DIR / filename
    if not filepath.exists():
        return {}

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    term_map = {}
    if isinstance(data, list):
        for item in data:
            if 'name_en' in item and 'name_cn' in item:
                term_map[item['name_en'].lower()] = item['name_cn']
    return term_map

def load_slang_dict() -> dict:
    """加载黑话对照表"""
    filepath = DEFAULT_REFERENCES_DIR / "wow_slang.json"
    if not filepath.exists():
        return {}

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    slang_map = {}
    if 'categories' in data:
        for category, items in data['categories'].items():
            for item in items:
                if 'abbr' in item and 'meaning' in item:
                    slang_map[item['abbr'].upper()] = item['meaning']
    return slang_map

def extract_srt_blocks(content: str) -> list:
    """解析 SRT 文件，返回字幕块列表"""
    pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?:\n\n|\n?$)'
    blocks = re.findall(pattern, content, re.DOTALL)
    return [(int(idx), time, text.strip()) for idx, time, text in blocks]

def chunk_blocks(blocks: list, chunk_size: int = 50) -> list:
    """将字幕块分段，每段指定条数"""
    chunks = []
    for i in range(0, len(blocks), chunk_size):
        chunks.append(blocks[i:i + chunk_size])
    return chunks

def scan_terms_in_chunk(texts: list, abilities: dict, trees: dict, slang: dict) -> dict:
    """扫描一段文本中出现的术语，返回术语摘要"""
    found_terms = {}
    found_slang = {}

    combined_text = ' '.join(texts).lower()

    for en, cn in abilities.items():
        if en.lower() in combined_text:
            found_terms[en] = cn

    for en, cn in trees.items():
        if en.lower() in combined_text:
            found_terms[en] = cn

    for abbr, meaning in slang.items():
        if abbr in combined_text.upper():
            found_slang[abbr] = meaning

    return {'terms': found_terms, 'slang': found_slang}

def format_chunk_for_translation(chunk: list, context_summary: dict) -> str:
    """格式化一个分段，附带术语摘要"""
    output = []

    # 术语摘要（供 LLM 参考）
    if context_summary['terms']:
        output.append("【本段术语对照】")
        for en, cn in context_summary['terms'].items():
            output.append(f"  {en} → {cn}")
        output.append("")

    if context_summary['slang']:
        output.append("【本段黑话对照】（保留原文+括号解释）")
        for abbr, meaning in context_summary['slang'].items():
            output.append(f"  {abbr} → {abbr}（{meaning}）")
        output.append("")

    # 字幕内容
    output.append("【字幕内容】")
    for idx, time, text in chunk:
        output.append(f"{idx}\n{time}\n{text}\n")

    return '\n'.join(output)

def main():
    """预处理 SRT 文件，分段输出"""
    if len(sys.argv) < 2:
        print("用法: python preprocess_srt.py <srt_file> [chunk_size]")
        print("输出分段后的字幕块，每段附带术语摘要")
        sys.exit(1)

    srt_path = Path(sys.argv[1])
    chunk_size = int(sys.argv[2]) if len(sys.argv) > 2 else 50

    if not srt_path.exists():
        print(f"文件不存在: {srt_path}")
        sys.exit(1)

    # 加载术语
    abilities = load_term_dict("abilities_translation.json")
    trees = load_term_dict("trees_translation.json")
    slang = load_slang_dict()

    # 解析 SRT
    content = srt_path.read_text(encoding='utf-8')
    blocks = extract_srt_blocks(content)

    print(f"总字幕条数: {len(blocks)}")
    print(f"分段大小: {chunk_size}")
    print(f"分段数量: {(len(blocks) + chunk_size - 1) // chunk_size}")
    print("=" * 50)

    # 分段处理
    chunks = chunk_blocks(blocks, chunk_size)
    for i, chunk in enumerate(chunks):
        texts = [b[2] for b in chunk]
        summary = scan_terms_in_chunk(texts, abilities, trees, slang)

        print(f"\n--- 分段 {i + 1}/{len(chunks)} ---")
        print(format_chunk_for_translation(chunk, summary))

if __name__ == "__main__":
    main()