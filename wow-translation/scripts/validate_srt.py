#!/usr/bin/env python3
"""
SRT 格式验证与修复脚本
确保翻译后的 SRT 文件格式与原文件完全一致
"""

import re
import sys
from pathlib import Path

def parse_srt(content: str) -> list:
    """解析 SRT 文件，返回 (index, time, text) 列表"""
    # SRT 格式：序号 + 时间线 + 文本 + 空行
    pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?:\n\n|\n?$)'
    blocks = re.findall(pattern, content, re.DOTALL)
    return [(int(idx), time, text.strip()) for idx, time, text in blocks]

def validate_format(original: str, translated: str) -> dict:
    """验证翻译后的格式是否与原格式一致"""
    orig_blocks = parse_srt(original)
    trans_blocks = parse_srt(translated)

    issues = []

    # 1. 序号检查
    orig_indices = [b[0] for b in orig_blocks]
    trans_indices = [b[0] for b in trans_blocks]

    if orig_indices != trans_indices:
        missing = set(orig_indices) - set(trans_indices)
        extra = set(trans_indices) - set(orig_indices)
        if missing:
            issues.append(f"缺少序号: {sorted(missing)}")
        if extra:
            issues.append(f"多余序号: {sorted(extra)}")

    # 2. 时间线检查
    orig_times = [b[1] for b in orig_blocks]
    trans_times = [b[1] for b in trans_blocks]

    for i, (orig_t, trans_t) in enumerate(zip(orig_times, trans_times)):
        if orig_t != trans_t:
            issues.append(f"序号 {i+1}: 时间线不匹配\n  原版: {orig_t}\n  翻译: {trans_t}")

    # 3. 时间线格式检查
    time_pattern = r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$'
    for idx, time, _ in trans_blocks:
        if not re.match(time_pattern, time):
            issues.append(f"序号 {idx}: 时间线格式错误 '{time}'")

    # 4. 条数检查
    if len(orig_blocks) != len(trans_blocks):
        issues.append(f"条数不匹配: 原版 {len(orig_blocks)} 条, 翻译 {len(trans_blocks)} 条")

    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'orig_count': len(orig_blocks),
        'trans_count': len(trans_blocks)
    }

def repair_format(original: str, translated: str) -> str:
    """修复翻译后的格式，确保与原格式一致"""
    orig_blocks = parse_srt(original)
    trans_blocks = parse_srt(translated)

    # 构建翻译文本映射（按序号）
    trans_text_map = {idx: text for idx, time, text in trans_blocks}

    # 按原版顺序重建
    repaired = []
    for idx, time, _ in orig_blocks:
        # 使用原版时间线
        text = trans_text_map.get(idx, "【翻译缺失】")
        repaired.append(f"{idx}\n{time}\n{text}\n")

    return '\n'.join(repaired)

def check_encoding(content: str) -> dict:
    """检查是否有乱码或编码问题"""
    issues = []

    # 检查是否包含异常字符序列
    abnormal_patterns = [
        r'[\x00-\x08]',  # 控制字符
        r'�',       # 替换字符（乱码标志）
    ]

    for pattern in abnormal_patterns:
        if re.search(pattern, content):
            issues.append(f"包含异常字符: {pattern}")

    return {'valid': len(issues) == 0, 'issues': issues}

def main():
    """验证并修复 SRT 翻译格式"""
    if len(sys.argv) < 3:
        print("用法: python validate_srt.py <原版.srt> <翻译.srt> [--repair]")
        print("\n功能:")
        print("  1. 验证翻译格式是否与原版一致")
        print("  2. --repair 参数自动修复格式问题")
        sys.exit(1)

    orig_path = Path(sys.argv[1])
    trans_path = Path(sys.argv[2])
    repair_mode = '--repair' in sys.argv

    if not orig_path.exists():
        print(f"原版文件不存在: {orig_path}")
        sys.exit(1)

    if not trans_path.exists():
        print(f"翻译文件不存在: {trans_path}")
        sys.exit(1)

    # 读取文件
    orig_content = orig_path.read_text(encoding='utf-8')
    trans_content = trans_path.read_text(encoding='utf-8')

    print("=" * 60)
    print("SRT 格式验证报告")
    print("=" * 60)

    # 编码检查
    enc_check = check_encoding(trans_content)
    if not enc_check['valid']:
        print("\n❌ 编码问题:")
        for issue in enc_check['issues']:
            print(f"  {issue}")

    # 格式验证
    result = validate_format(orig_content, trans_content)

    print(f"\n原版条数: {result['orig_count']}")
    print(f"翻译条数: {result['trans_count']}")

    if result['valid']:
        print("\n✅ 格式验证通过")
        print("   - 序号一致")
        print("   - 时间线一致")
        print("   - 时间线格式正确")
    else:
        print("\n❌ 格式验证失败:")
        for issue in result['issues']:
            print(f"  {issue}")

        if repair_mode:
            print("\n🔧 正在修复...")
            repaired = repair_format(orig_content, trans_content)

            # 写入修复后的文件
            repair_path = trans_path.with_suffix('.repaired.srt')
            repair_path.write_text(repaired, encoding='utf-8')
            print(f"✅ 已修复并保存到: {repair_path}")

            # 重新验证
            print("\n重新验证修复后的文件:")
            repaired_check = validate_format(orig_content, repaired)
            if repaired_check['valid']:
                print("✅ 修复成功，格式验证通过")
            else:
                print("❌ 修复后仍有问题:")
                for issue in repaired_check['issues']:
                    print(f"  {issue}")
        else:
            print("\n💡 使用 --repair 参数自动修复格式问题")

    print("=" * 60)

if __name__ == "__main__":
    main()