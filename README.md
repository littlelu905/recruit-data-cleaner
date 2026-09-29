# 招新报名数据清洗与统计工具

协会每年招新会收到几百份从问卷导出的 CSV 报名表。这个小工具用来做**读入概览、校验清洗、统计导出**三件事。

## 快速开始

```bash
python clean_recruit.py sample_data.csv all        # 跑全部流程
python clean_recruit.py sample_data.csv overview   # 需求1：概览
python clean_recruit.py sample_data.csv clean      # 需求2：校验与清洗
python clean_recruit.py sample_data.csv stats      # 需求3：统计与导出
```

仅依赖 Python 标准库，Python 3.7+ 即可。

## 输入数据格式

| 字段 | 说明 |
|------|------|
| 姓名 | 报名人姓名 |
| 学号 | 报名人学号 |
| 邮箱 | 报名人邮箱 |
| 志愿1 | 第一志愿部门 |
| 志愿2 | 第二志愿部门（可选） |
| 推荐人 | 推荐人（可选） |

## 需求 1：读入与概览

```bash
python clean_recruit.py sample_data.csv overview
```

输出：总记录数、各列空值统计、完全重复行。

## 需求 2：校验与清洗

```bash
python clean_recruit.py sample_data.csv clean
```

校验规则：
1. 学号必须是纯数字
2. 邮箱必须是 `学号@smbu.edu.cn`
3. 同一学号出现两次及以上视为重复报名

导出 `*_问题清单.csv`，不修改原文件。

## 需求 3：统计与导出

```bash
python clean_recruit.py sample_data.csv stats
```

输出：按第一志愿分组统计、志愿填写情况、导出 `*_clean.csv`。

## 假设

- 学号位数不限，纯数字即可
- 邮箱域名固定 `smbu.edu.cn`
- CSV 使用 `utf-8-sig` 读取
