---
title: 中国增长第一次点时回放（不可复现样例）
url: /first-growth-point-in-time-replay/
summary: 用 2024 年 4 月 16 日的官方发布演示点时准入，并记录为何当前不能声称还原了当时系统判断。
status: published
draft: false
public: true
publication_status: public-review
methodology_maturity: m1-preparatory-draft
data_source_status: source-publication-verified-system-availability-unknown
implementation_status: manual-negative-control
---

> 回放时点：`2024-04-16T10:05:00+08:00`；执行日期：`2026-08-05`；结论：`SNAPSHOT_NOT_REPRODUCIBLE`。这是一次数据规则负向测试，不是历史投资结论。

## 为什么选这个时点

国家统计局在 2024 年 3 月 31 日 09:30 发布 3 月制造业 PMI，在 2024 年 4 月 16 日 10:00 发布 3 月规模以上工业增加值和社会消费品零售总额。`10:05` 让四个候选字段在“官方已经发布”的层面同时存在，也能检验系统是否会把官方发布时间误当成自己的实际可得时间。

后来发布的[国家统计局 2025 年一季度数据表](https://www.stats.gov.cn/zwfwck/sjfb/202504/t20250416_1959321.html)对 2024 年 3 月的两个季调环比数值做了修订，因此这个日期也适合演示“修订值只能追加，不能覆盖初值”。这些环比数值不是本次四个正式同比/指数证据字段，只用于测试修订治理。

## 来源层能够核验的事实

| 字段 | `data_as_of` | 来源发布值 | `published_at` | 来源层结论 |
|---|---|---:|---|---|
| 官方制造业 PMI | 2024-03 | 50.8 | 2024-03-31 09:30 +08:00 | 在 `T` 前官方发布 |
| PMI 新订单指数 | 2024-03 | 53.0 | 2024-03-31 09:30 +08:00 | 在 `T` 前随 PMI 发布 |
| 规模以上工业增加值当月同比 | 2024-03 | 4.5% | 2024-04-16 10:00 +08:00 | 在 `T` 前官方发布 |
| 社会消费品零售总额当月同比 | 2024-03 | 3.1% | 2024-04-16 10:00 +08:00 | 在 `T` 前官方发布 |

本次手工核验使用国家统计局的[2024 年 3 月 PMI 发布](https://www.stats.gov.cn/sj/zxfb/202404/t20240411_1948446.html)、[工业增加值发布](https://www.stats.gov.cn/sj/zxfb/202404/t20240416_1948563.html)和[社会消费品零售总额发布](https://www.stats.gov.cn/sj/zxfb/202404/t20240416_1948573.html)。[2024 年发布日程](https://www.stats.gov.cn/xxgk/sjfb/fbrcb/202312/t20231229_1946090.html)只用于检查计划，不替代实际发布页。

## 系统层准入结果

本项目在 2024 年 4 月 16 日尚无 M1 采集系统、`available_at` 记录或不可变原始快照。当前文档是在 2026 年重建，因此四个字段均不满足“系统当时真实可见”的证据要求。

| 字段 | `available_at <= T` | `recorded_at <= T` | 正式处理 |
|---|---|---|---|
| 官方制造业 PMI | unknown | no | excluded |
| PMI 新订单指数 | unknown | no | excluded |
| 工业增加值同比 | unknown | no | excluded |
| 社会消费品零售总额同比 | unknown | no | excluded |

官方 `published_at` 不能代替系统 `available_at`。因此本页能证明“来源当时已发布”，不能证明“项目当时看到了这些值”。

## 当时还不能使用什么

- 2024 年 4 月 PMI 尚未发布；
- 2024 年 4 月工业增加值和社零尚未发布；
- `T` 之后出现的修订、样本范围调整或普查修订；
- 今天看到的最新历史序列、当前网页结构或后来补建的转换规则；
- 任何依据这些后见数据生成的分数、风险边界、资产选择或交易动作。

## 修订链示例

2024 年 4 月 16 日的原发布页记录：3 月规模以上工业增加值季调环比初值为 `-0.08%`，社零季调环比初值为 `0.26%`。国家统计局 2025 年 4 月 16 日发布的[工业历史表](https://www.stats.gov.cn/sj/zxfb/202504/t20250416_1959320.html)和[社零历史表](https://www.stats.gov.cn/sj/zxfb/202504/t20250416_1959317.html)中，相应数值为 `-0.05%` 和 `0.48%`。

正确保存方式是：

```text
2024-04-16 initial industrial_mom = -0.08
2025-04-16 revised industrial_mom = -0.05

2024-04-16 initial retail_mom = 0.26
2025-04-16 revised retail_mom = 0.48
```

两版都保留各自的发布时间、来源快照和版本。回放 `T` 时只能考虑初值；但由于本项目没有当时的 `available_at` 和 `recorded_at`，连初值也不能作为“系统原始快照”准入。

## 回放输出

```yaml
module: china_growth
snapshot_at: 2024-04-16T10:05:00+08:00
snapshot_type: reconstructed_snapshot
replay_status: SNAPSHOT_NOT_REPRODUCIBLE
status: unknown
direction: unknown
field_versions: []
supporting_evidence: []
contrary_evidence: []
conflicts: []
unknowns:
  - all_four_fields_available_at
  - immutable_raw_snapshots_recorded_before_T
  - source_and_schema_versions_at_T
confidence: unknown
invalidation_conditions:
  - discovering_timestamped_immutable_snapshots_recorded_before_T
next_review_at: unknown
```

## 能否形成判断

不能形成符合 M1 契约的正式增长判断。来源层的四个数值可以帮助人理解当时公开信息，但证据准入失败后，系统状态、方向和置信度必须保持未知。本回放没有进入资产层、产品风险预算层、执行层或交易层，也没有计算历史收益。

这次失败正是闭环的一部分：它证明规则会拒绝后见数据，而不是为了完成页面制造一个确定结论。未来第一个可成功复现的时点，必须从真实采集开始后选择，并保留 `available_at`、`recorded_at`、原始快照和全部版本。
