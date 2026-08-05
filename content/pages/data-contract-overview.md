---
title: M1 最小数据契约总览（预备草稿）
url: /data-contract-overview/
summary: 定义字段、来源、点时可得性、原始快照、转换版本和正式失败状态之间的最小契约。
status: published
draft: false
public: true
publication_status: public-review
methodology_maturity: m1-preparatory-draft
data_source_status: not-validated
implementation_status: not-implemented
---

> 前置状态：**M0 未关闭，M1 未正式开始。** 本页只冻结契约语言；没有创建数据库、采集任务、API、评分或生产数据。

## 契约要解决什么

任何进入系统的数值都必须回答四个问题：它是什么、来自哪里、在判断时点是否真的可见、能否用同一版本重新得到。最小链路是：

`字段登记 → 来源登记 → 不可变原始快照 → 有版本的转换 → 证据记录 → 六层系统`

来源网址或数值本身都不够。没有可得时间和原始快照，就不能声称完成了点时复现；没有转换版本，就不能解释数值为何变化。

## 最小字段模板

```yaml
field_id: ""
field_name: ""
module: ""
economic_meaning: ""

source_name: ""
source_type: ""
source_series: ""
source_url_or_identifier: ""
source_priority: ""

frequency: ""
unit: ""
currency: ""
seasonal_adjustment: ""
revision_policy: ""

data_as_of: ""
published_at: ""
available_at: ""
recorded_at: ""

raw_value: null
raw_snapshot_id: ""
transformation: ""
transformation_version: ""
transformed_value: null

data_quality: unknown
revision_status: unknown
missing_reason: ""
failure_reason: ""

source_version: ""
schema_version: ""
rule_version: ""
```

模板是单条观测的最小交接面。空值只有在状态明确为未知或失败时才合法，不能偷偷替换为零、中性分或上一期值。

## 字段组定义

### 身份与含义

- `field_id`：跨版本稳定的机器标识；改名不应改变其历史身份。
- `field_name`：面向人的名称。
- `module`：字段归属的证据模块，不代表它能直接产生资产或交易结论。
- `economic_meaning`：字段回答的经济问题，以及不能回答什么。

### 来源

- `source_name`、`source_type`、`source_series`：分别记录发布者、官方/供应商/计算值等类别和精确序列。
- `source_url_or_identifier`：可定位到具体发布页、序列代码或文件，而不是只有网站首页。
- `source_priority`：同一字段有多个来源时的使用顺序。切换来源必须留下版本和原因，不能把两个口径拼成一条无痕历史。

### 口径

- `frequency`、`unit`、`currency`、`seasonal_adjustment`：解释数值的时间频率和统计口径；不适用也要显式写明。
- `revision_policy`：说明初值、修订值和最终值怎样共存，以及是否存在基准、样本或成分调整。

### 四个时间

- `data_as_of`：数据描述的经济期或市场交易日。
- `published_at`：来源正式发布这条观测的时间。
- `available_at`：本系统通过所选来源实际可以读取它的最早时间。
- `recorded_at`：本系统将原始证据落盘的时间。

判断时点为 `T` 时，至少要求 `available_at <= T`；若声称复现当时系统真实状态，还必须有 `recorded_at <= T` 的原始快照。详细规则见[点时数据与修订]({{< relref "pages/point-in-time-data-and-revisions.md" >}})。

### 原始值与转换

- `raw_value` 和 `raw_snapshot_id` 保存来源当时返回的值与不可变证据身份。
- `transformation` 说明同比、环比、收益、币种转换等过程。
- `transformation_version` 标记转换实现；`transformed_value` 是其输出。
- 原始值被修订时新增观测和快照，不覆盖旧记录。

### 质量、失败与版本

- `data_quality` 表达可用性与质量：`available`、`delayed`、`missing`、`stale`、`source_failed`、`schema_changed`、`unknown`。
- `revision_status` 表达独立的修订阶段：`initial`、`revised`、`final`、`unknown`。修订值仍可能同时是 `available` 或 `stale`，两个维度不得合并成一个单值状态。
- `missing_reason` 解释为何没有观测；`failure_reason` 解释抓取、解析、校验或转换在哪里失败。
- `source_version`、`schema_version`、`rule_version` 分别锁定来源口径、数据结构和判定规则；三者不能互相替代。

## 准入规则

一条观测只有在身份、来源、口径、时间、快照、转换和版本都可解释时，才可作为正式证据。否则必须保留为未知或失败。尤其禁止：

- 把官方发布时间直接假定为供应商或本系统的实际可得时间；
- 用今天下载的最新修订值改写历史时点；
- 用 `0`、`0.5`、上一期值或人工猜测填补缺失；
- 只有转换结果，没有原始快照；
- 变更来源、成分、币种或算法但沿用旧版本号；
- 因单一来源失败就自动改用口径不同的备用来源。

## 与现有仓库材料的关系

现有宏观文章已使用 `data_as_of`、`available_at`、`recorded_at`、`decision_at`、`review_at`、`source_version`、`rule_version`、`data_quality`、`failure_reason` 和 `last_valid_state_at` 等候选语言，可以复用其语义。AlphaLab 中的 `data_available_at` 属于历史近义字段，未来若纳入本契约必须做显式映射，不能静默当作同一字段。

`tools/fund_bot` 是旧原型，不满足本契约所需的来源、可得时间、修订链和快照字段；其缺失值默认和硬编码结果不能升级为 M1 证据。本轮不修改或运行它。

## 本页的完成边界

本页只完成字段语言和准入门槛。来源是否稳定、采集是否成功、快照是否可复现、规则是否有效，仍全部未验证。
