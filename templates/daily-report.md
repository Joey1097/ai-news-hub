# AI 新闻日报 - {{DATE}}

> 本报告由 AI News Hub 自动生成  
> 更新时间: {{GENERATED_AT}}  
> 推送次数: {{PUSH_COUNT}}/2（早间/晚间）

---

## 📋 阅读指南

- **早间推送（7:15）**：包含凌晨至早上7点的AI新闻
- **晚间推送（20:15）**：包含早上7点至晚上8点的AI新闻，并汇总全天内容

---

## 📊 今日概览

| 指标 | 数值 |
|------|------|
| 监控数据源 | {{SOURCE_COUNT}} 个 |
| 本日累计新内容 | {{NEW_ITEMS_COUNT}} 条 |
| 早间推送 | {{MORNING_PUSH_STATUS}} |
| 晚间推送 | {{EVENING_PUSH_STATUS}} |

---

## 📰 早间新闻（7:15）

{{#MORNING_NEWS}}
### {{TITLE}}

**来源**: {{SOURCE}} | **分类**: {{CATEGORIES}} | **时间**: {{PUBLISHED_AT}}

{{SUMMARY}}

🔗 [查看原文]({{URL}})

---

{{/MORNING_NEWS}}

{{^MORNING_NEWS}}
*早间暂无新内容*
{{/MORNING_NEWS}}

---

## 🌙 晚间新闻（20:15）

{{#EVENING_NEWS}}
### {{TITLE}}

**来源**: {{SOURCE}} | **分类**: {{CATEGORIES}} | **时间**: {{PUBLISHED_AT}}

{{SUMMARY}}

🔗 [查看原文]({{URL}})

---

{{/EVENING_NEWS}}

{{^EVENING_NEWS}}
*晚间暂无新内容*
{{/EVENING_NEWS}}

---

## 📁 分类汇总

{{#CATEGORIES}}
### {{NAME}} ({{COUNT}})

{{#ITEMS}}
- [{{TITLE}}]({{URL}}) - {{SOURCE}}
{{/ITEMS}}

{{/CATEGORIES}}

---

## 🔗 相关链接

- [项目主页](https://github.com/Joey1097/ai-news-hub)
- [历史报告](./)
- [数据源配置](../sources/)

---

*报告由 AI News Hub 自动生成*  
*如有问题请联系维护者*
