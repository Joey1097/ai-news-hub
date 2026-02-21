# AI 新闻日报 - {{DATE}}

> 本报告由 AI News Hub 自动生成  
> 生成时间: {{GENERATED_AT}}

---

## 📊 今日概览

| 指标 | 数值 |
|------|------|
| 监控数据源 | {{SOURCE_COUNT}} 个 |
| 新发现内容 | {{NEW_ITEMS_COUNT}} 条 |
| 更新数据源 | {{UPDATED_SOURCES}} 个 |

---

## 📰 数据源状态

{{#SOURCES}}
### {{NAME}}
- **状态**: {{STATUS}}
- **类型**: {{TYPE}}
- **最后检查**: {{LAST_CHECKED}}
- **新内容**: {{NEW_ITEMS}} 条

{{/SOURCES}}

---

## 🔥 热门新闻

{{#NEWS_ITEMS}}
### {{TITLE}}

**来源**: {{SOURCE}} | **分类**: {{CATEGORIES}} | **时间**: {{PUBLISHED_AT}}

{{SUMMARY}}

🔗 [查看原文]({{URL}})

---

{{/NEWS_ITEMS}}

{{^NEWS_ITEMS}}
*今日暂无新内容*
{{/NEWS_ITEMS}}

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

- [项目主页](https://github.com/yourusername/ai-news-hub)
- [历史报告](./)
- [数据源配置](../sources/)

---

*报告由 AI News Hub 自动生成*  
*如有问题请联系维护者*
