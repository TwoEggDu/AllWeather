---
title: 中国增长最小数据契约（预备草稿）
url: /china-growth-data-contract/
summary: 为中国增长模块定义四个最小证据字段及其发布时间、修订、季节性和缺失边界。
status: published
draft: false
public: true
publication_status: public-review
methodology_maturity: m1-preparatory-draft
data_source_status: not-validated
implementation_status: not-implemented
---

> 前置状态：**M0 未关闭，M1 未正式开始。** 四个字段仅用于冻结契约和点时回放，不构成增长评分、当前判断或投资建议。

本页只列中国增长的领域定义字段。每条实际观测都必须完整继承[全系统 30 字段基础契约]({{< relref "pages/data-contract-overview.md" >}})；本页的 `source` 对应来源发布者说明，不替代 `source_name`、`source_type`、`source_series`、`source_url_or_identifier` 和 `source_priority`，也不豁免原始快照、转换、质量与三个版本字段。

## 为什么先选这四个字段

第一版只覆盖两个调查类领先/同步信号和两个总量确认信号：官方制造业 PMI、制造业 PMI 新订单指数、规模以上工业增加值月度同比、社会消费品零售总额月度同比。它们可以让系统保留“软数据与硬数据是否一致”的问题，同时不把模块扩展成完整仪表盘。

PMI 与新订单来自同一调查，相关性高，不能当作两张独立选票。工业与社零受基数、样本范围和口径变化影响，也不能由单月同比直接推出趋势。

字段口径以国家统计局的[采购经理调查说明](https://www.stats.gov.cn/zs/tjws/zytjzbqs/cgzlzs/202411/t20241128_1957610.html)、[社会消费品零售总额说明](https://www.stats.gov.cn/zs/tjws/zytjzbqs/shxfp/202410/t20241025_1957174.html)和各期实际发布页为第一优先来源。[年度发布日程](https://www.stats.gov.cn/xxgk/sjfb/fbrcb/202312/t20231229_1946090.html)只表示预期安排；实际日期可能调整，国家数据平台也可能晚于新闻发布页更新。

## 字段一：官方制造业 PMI

```yaml
field_id: cn_growth_official_manufacturing_pmi
question_answered: 制造业经营活动相对上月是在扩张还是收缩？
economic_meaning: 采购经理对生产、订单、库存、就业和供应时间等月度变化的综合扩散指数
level_or_direction: level_and_change
leading_or_confirming: leading_to_coincident_soft_data
source: 国家统计局服务业调查中心、中国物流与采购联合会
source_series: 中国制造业采购经理指数（PMI）
frequency: monthly
unit: index_points
data_as_of: 调查月份
expected_release_schedule: 原则上月末最后一天；以实际官方发布为准
published_at: 每条观测必填，保留北京时间和原始精度
available_at: 每条观测必填；未实测时为 unknown，不以 published_at 代替
revision_policy: 保存原发布快照；节假日调查安排、季调或方法变化以新 source_version 追加
base_effect_risk: low_for_level_but_change_is_affected_by_prior_month_and_holidays
seasonality: 官方调查与季节影响并存；节假日月份需结合官方说明
known_limitations: 扩散指数不等于产出增速；50 只表示与上月比较的临界点；调查感受与硬数据可能背离
missing_state: unknown
```

## 字段二：制造业 PMI 新订单指数

```yaml
field_id: cn_growth_official_manufacturing_pmi_new_orders
question_answered: 制造业新订单相对上月的扩张或收缩方向是什么？
economic_meaning: 制造业企业新接订单量月度变化的扩散指数
level_or_direction: level_and_change
leading_or_confirming: leading_soft_data
source: 国家统计局服务业调查中心、中国物流与采购联合会
source_series: 制造业 PMI 分类指数—新订单指数
frequency: monthly
unit: index_points
data_as_of: 调查月份
expected_release_schedule: 随官方制造业 PMI 发布；以实际官方发布为准
published_at: 每条观测必填，保留北京时间和原始精度
available_at: 每条观测必填；未实测时为 unknown
revision_policy: 与对应 PMI 发布快照绑定；口径或调查安排变化时追加版本
base_effect_risk: low_for_level_but_monthly_comparison_is_sensitive_to_holidays
seasonality: 节假日和生产周期可能造成明显月度扰动
known_limitations: 与总体 PMI 同源且部分重叠；不是订单金额或实际产出的直接度量
missing_state: unknown
```

## 字段三：规模以上工业增加值月度同比

```yaml
field_id: cn_growth_industrial_value_added_yoy
question_answered: 规模以上工业实际产出相对上年同月增长多少？
economic_meaning: 扣除价格因素后的规模以上工业增加值同比增速
level_or_direction: year_over_year_rate_and_change
leading_or_confirming: confirming_hard_data
source: 国家统计局
source_series: 规模以上工业增加值—当月同比实际增长
frequency: monthly_with_january_february_combined_release
unit: percent_yoy_real
data_as_of: 统计月份；1—2 月合并发布时必须保留合并期间
expected_release_schedule: 随国民经济运行发布；以国家统计局年度发布日程和实际页面为准
published_at: 每条观测必填，保留北京时间和原始精度
available_at: 每条观测必填；数据平台晚于新闻发布时使用本系统实际来源时间
revision_policy: 初值、季调环比修订、普查与样本范围变化分别追加；不得覆盖历史快照
base_effect_risk: high_for_single_month_yoy
seasonality: 同比减弱但不消除春节错位；1—2 月合并和季调环比需单独处理
known_limitations: 仅覆盖规模以上工业；企业范围会年度变化；同比不能替代产出水平
missing_state: unknown
```

## 字段四：社会消费品零售总额月度同比

```yaml
field_id: cn_growth_retail_sales_yoy
question_answered: 商品零售和餐饮等社会消费品零售额相对上年同月增长多少？
economic_meaning: 社会消费品零售总额名义同比增速
level_or_direction: year_over_year_rate_and_change
leading_or_confirming: confirming_hard_data
source: 国家统计局
source_series: 社会消费品零售总额—当月同比名义增长
frequency: monthly_with_january_february_combined_release
unit: percent_yoy_nominal
data_as_of: 统计月份；1—2 月合并发布时必须保留合并期间
expected_release_schedule: 随国民经济运行发布；以国家统计局年度发布日程和实际页面为准
published_at: 每条观测必填，保留北京时间和原始精度
available_at: 每条观测必填；未实测时为 unknown
revision_policy: 初值、季调环比修订、普查和限额以上单位范围变化分别追加
base_effect_risk: high_for_single_month_yoy
seasonality: 春节错位、促销节奏和月度天数影响显著；名义值还受价格变化影响
known_limitations: 不等同于全部居民消费或实际消费量；网上零售等分项口径需另建字段
missing_state: unknown
```

## 共同准入规则

- 每条实际观测必须补全全系统基础契约，尤其是 `published_at`、`available_at`、`recorded_at`、`raw_snapshot_id`、来源定位、质量和版本字段，否则不能进入正式状态判断。
- 对 `1—2 月` 合并数据不得伪造两个独立月值。
- PMI 与新订单只形成一个调查证据簇；工业与社零形成硬数据确认簇。冲突必须保留在 `conflicts`，不能通过平均或打分消失。
- 同比方向、水平和边际变化是不同事实；本契约不规定评分、权重、阈值或增长状态映射。
- 出口可作为后续候选扩展，但第一版不纳入。它需要先核实海关总署的精确序列、美元/人民币口径、发布时点、修订和春节合并方式。

## 空证据卡

在没有通过准入的数据时，模块只能输出以下空卡：

```yaml
module: china_growth
snapshot_at: null
status: unknown
direction: unknown
field_versions: []
supporting_evidence: []
contrary_evidence: []
conflicts: []
unknowns: []
confidence: unknown
invalidation_conditions: []
next_review_at: unknown
```

这张卡是数据层向后续状态层的候选交接面，不是已实现的运行结果。第一次测试见[历史点时回放]({{< relref "pages/first-growth-point-in-time-replay.md" >}})。
