---
title: 点时数据与修订规则（预备草稿）
url: /point-in-time-data-and-revisions/
summary: 规定历史判断时哪些数据可进入证据集，以及初值、修订值、来源差异和失败状态怎样保留。
status: published
draft: false
public: true
publication_status: public-review
methodology_maturity: m1-preparatory-draft
data_source_status: not-validated
implementation_status: not-implemented
---

> 前置状态：**M0 未关闭，M1 未正式开始。** 本页是规则草稿，不证明仓库已有点时数据库。

## 一个历史时点只能看到当时可得的证据

设判断时点为 `T`。某条观测只有满足 `available_at <= T`，才可以进入当时的候选证据集。若要声称还原的是“当时系统实际看到的状态”，必须同时存在 `recorded_at <= T` 的不可变原始快照。

```text
source published
      ↓
system actually available  ── available_at <= T ? ── no → excluded
      ↓ yes
immutable snapshot recorded ── recorded_at <= T ? ── no → reconstructed only
      ↓ yes
original system snapshot at T
```

`published_at <= T` 只证明发布者已经发布，不证明所选供应商、网络或采集任务当时已经把数据交给系统。

## 四个时间不能混用

| 字段 | 回答的问题 | 例子 |
|---|---|---|
| `data_as_of` | 这条数据描述哪个经济期或交易日？ | 2024 年 3 月 |
| `published_at` | 发布者何时正式发布？ | 2024-04-16 10:00 +08:00 |
| `available_at` | 本系统通过指定来源何时首次读到？ | 采集成功并可解析的时间 |
| `recorded_at` | 何时把原始证据写入不可变存储？ | 快照落盘时间 |

只有日期、没有时分或时区时，必须保存原始精度并采用保守边界；不得擅自补成当天 00:00。页面更新时间、文件修改时间和搜索引擎收录时间都不能自动替代以上字段。

## 原始快照与重建快照

- `original_snapshot`：在 `T` 之前真实记录，且来源、正文或响应、校验值与抓取时间均可追溯。
- `reconstructed_snapshot`：在 `T` 之后根据官方历史发布、存档或供应商历史接口重建。

重建快照可以研究“公开信息当时应当是什么”，但不能冒充“系统当时实际看到什么”。若缺少足够证据，正式结论为 `SNAPSHOT_NOT_REPRODUCIBLE`，状态、方向和置信度保持 `unknown`。

## 初值和修订值形成追加链

同一 `field_id + data_as_of` 可以有多条观测：

```text
initial observation
  └─ revised observation 1
       └─ revised observation 2
            └─ final observation, if the source defines one
```

每一条都要保存自己的 `published_at`、`available_at`、`recorded_at`、原始快照和 `source_version`。历史判断使用 `T` 时可得的那一版；当前分析可以使用最新版，但必须标出已修订。禁止覆盖初值后再声称历史结果可复现。

样本范围、指数成分、基期、季调模型、历史数据整段回修和数据商替换也属于版本变化，即使某个表面数值没有改变。

## 来源差异

官方来源、授权供应商和镜像站可能在发布时间、数值精度、修订速度和历史覆盖上不同。字段登记必须确定主来源优先级；备用来源只有在口径可比且切换被记录时才能使用。不能用官方 `published_at` 代替供应商 `available_at`，也不能把来源差异平均掉。

## 节假日、延迟和市场日历

- 预期发布日期只是日程，不是实际发布时间；实际发布延迟时状态为 `delayed`。
- 周末和节假日按来源所在时区和日历解释，跨市场不得共用一个“当天收盘”。
- 市场休市、停牌或无成交不是数值零；需要保留对应交易状态。
- 采集延迟和发布延迟是两个事件，应分别记录。

## 正式状态

正式状态由两个正交维度组成。`data_quality` 只使用以下最小集合：

- `available`：来源、口径、时间和快照均满足本次使用；
- `delayed`：超过预期时间但尚未可得；
- `missing`：预期应有但没有观测；
- `stale`：有旧值，但已超过允许的新鲜度；
- `source_failed`：来源访问、下载或鉴权失败；
- `schema_changed`：结构变化导致旧解析规则不再可信；
- `unknown`：信息不足，无法归入以上状态或无法证明可得性。

另用 `revision_status` 表示 `initial`、`revised`、`final` 或 `unknown`。修订值可以同时是 `available`、`stale` 或其他质量状态；不得让修订阶段覆盖可用性。更具体的技术原因写入 `missing_reason` 或 `failure_reason`，不通过扩展“看起来正常”的数值状态来掩盖失败。

## 禁止行为

- 用当前最新值回填过去；
- 把发布日期、网页日期或文件名当成未经验证的可得时间；
- 将未知值自动解释为中性；
- 在来源失败后沿用旧状态但不标记 `stale`；
- 合并两个来源的历史而不留下切换点；
- 修改原始快照；
- 在重建证据不足时输出确定的历史方向、分数或动作。

第一次演示见[中国增长第一次点时回放]({{< relref "pages/first-growth-point-in-time-replay.md" >}})。它故意保留“不可复现”结论，以检验这些规则是否真的能阻止未来数据泄漏。
