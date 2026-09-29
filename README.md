# 招新报名数据清洗与统计工具

协会每年招新会收到几百份从问卷导出的 CSV 报名表。这个小工具用来做数据清洗与统计。

## 输入数据格式

CSV 应包含以下字段：姓名、学号、邮箱、志愿1、志愿2、推荐人。

仓库内的 `sample_data.csv` 是一份示例数据。

## 需求 1：读入与概览

```bash
python clean_recruit.py sample_data.csv overview
```

输出：总记录数、各列空值统计、完全重复行。
