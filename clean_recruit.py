#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""招新报名数据清洗与统计工具。"""
import csv
import sys
import os
import argparse
from collections import Counter

FIELDS = ['姓名', '学号', '邮箱', '志愿1', '志愿2', '推荐人']


def read_csv(filepath):
    with open(filepath, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    return rows, fieldnames


def overview(filepath):
    rows, fieldnames = read_csv(filepath)
    print(f"总记录数: {len(rows)} 行")
    print(f"字段列表: {', '.join(fieldnames)}")
    print()
    print("各列空值统计:")
    for col in fieldnames:
        empty = sum(1 for r in rows if not r.get(col, '').strip())
        pct = (empty / len(rows) * 100) if rows else 0
        print(f"  {col:<8} {empty:>4} 个空值  ({pct:.1f}%)")
    print()
    seen = {}
    dup_groups = []
    for i, row in enumerate(rows, start=1):
        key = tuple((col, row.get(col, '').strip()) for col in fieldnames)
        if key in seen:
            dup_groups.append((seen[key], i))
        else:
            seen[key] = i
    if dup_groups:
        print(f"发现 {len(dup_groups)} 组完全重复的行:")
        for first, second in dup_groups:
            print(f"  第 {first} 行 与 第 {second} 行 完全重复")
    else:
        print("没有发现完全重复的行。")
    return rows, fieldnames

EMAIL_DOMAIN = 'smbu.edu.cn'


def validate_and_clean(filepath):
    rows, fieldnames = read_csv(filepath)
    sid_counter = Counter()
    for row in rows:
        sid = row.get('学号', '').strip()
        if sid:
            sid_counter[sid] += 1
    problem_rows = []
    clean_rows = []
    for i, row in enumerate(rows, start=1):
        reasons = []
        sid = row.get('学号', '').strip()
        email = row.get('邮箱', '').strip()
        if not sid.isdigit():
            reasons.append(f"学号 '{sid}' 不是纯数字")
        if sid.isdigit():
            expected = f"{sid}@{EMAIL_DOMAIN}"
            if email != expected:
                reasons.append(f"邮箱 '{email}' 不符合 '{expected}'")
        if sid and sid_counter[sid] > 1:
            reasons.append(f"学号 '{sid}' 重复报名（共出现 {sid_counter[sid]} 次）")
        if reasons:
            problem_rows.append((i, dict(row), reasons))
        else:
            clean_rows.append(dict(row))
    base = os.path.splitext(filepath)[0]
    problem_path = f"{base}_问题清单.csv"
    out_fields = ['行号'] + fieldnames + ['问题原因']
    with open(problem_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        for idx, row, reasons in problem_rows:
            out = {'行号': idx}
            for col in fieldnames:
                out[col] = row.get(col, '')
            out['问题原因'] = '; '.join(reasons)
            writer.writerow(out)
    print(f"问题清单已导出至: {problem_path}")
    print(f"共 {len(problem_rows)} 行存在问题，{len(clean_rows)} 行通过校验。")
    if problem_rows:
        print("问题明细:")
        for idx, _, reasons in problem_rows:
            print(f"  第 {idx:>3} 行: {'; '.join(reasons)}")
    return clean_rows, fieldnames, problem_rows

def stats_and_export(filepath):
    clean_rows, fieldnames, _ = validate_and_clean(filepath)
    v1_counter = Counter()
    both_filled = 0
    one_filled = 0
    for row in clean_rows:
        v1 = row.get('志愿1', '').strip()
        v2 = row.get('志愿2', '').strip()
        v1_counter[v1] += 1
        if v1 and v2:
            both_filled += 1
        elif v1 or v2:
            one_filled += 1
    print()
    print("=" * 50)
    print("按第一志愿分组统计:")
    print(f"  {'第一志愿':<12} {'人数':>6}  {'占比':>8}")
    print(f"  {'-'*12} {'-'*6}  {'-'*8}")
    total = sum(v1_counter.values())
    for v1, cnt in v1_counter.most_common():
        label = v1 if v1 else '(未填写)'
        pct = (cnt / total * 100) if total else 0
        print(f"  {label:<12} {cnt:>6}  {pct:>7.1f}%")
    print()
    print("志愿填写情况统计:")
    print(f"  两个志愿都填了 : {both_filled} 人")
    print(f"  只填了一个志愿 : {one_filled} 人")
    base = os.path.splitext(filepath)[0]
    clean_path = f"{base}_clean.csv"
    with open(clean_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(clean_rows)
    print()
    print(f"清洗后的干净数据已导出至: {clean_path}")
    return v1_counter, both_filled, one_filled


def main():
    parser = argparse.ArgumentParser(description='招新报名数据清洗与统计工具')
    parser.add_argument('csvfile', help='CSV 文件路径')
    parser.add_argument('action', choices=['overview', 'clean', 'stats', 'all'])
    args = parser.parse_args()
    if not os.path.exists(args.csvfile):
        print(f"错误: 文件不存在 -> {args.csvfile}", file=sys.stderr)
        sys.exit(1)
    if args.action == 'overview':
        overview(args.csvfile)
    elif args.action == 'clean':
        validate_and_clean(args.csvfile)
    elif args.action == 'stats':
        stats_and_export(args.csvfile)
    elif args.action == 'all':
        print("=" * 50)
        print("【需求 1】读入与概览")
        print("=" * 50)
        overview(args.csvfile)
        print()
        print("=" * 50)
        print("【需求 2】校验与清洗")
        print("=" * 50)
        validate_and_clean(args.csvfile)
        print()
        print("=" * 50)
        print("【需求 3】统计与导出")
        print("=" * 50)
        stats_and_export(args.csvfile)


if __name__ == '__main__':
    main()
