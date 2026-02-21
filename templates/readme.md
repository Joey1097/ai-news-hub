# AI News Hub

> 可扩展的 AI 新闻聚合系统

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

## 🚀 项目概述

AI News Hub 是一个模块化、可扩展的 AI 新闻聚合系统，支持多源采集、智能分类、定时推送。

### 核心特性

- **多源支持**: GitHub、Newsletter、RSS、Twitter/X 等
- **模块化设计**: 每个数据源独立适配器
- **智能去重**: 基于内容哈希的重复检测
- **分类标签**: 自动/手动分类，支持多维度标签
- **定时任务**: 可配置的采集和推送频率
- **多通道推送**: 飞书、Webchat、邮件等

---

## 📁 项目结构

```
ai-news-hub/
├── reports/               # 每日报告目录
│   └── YYYY-MM-DD.md     # 按日期命名的报告
├── sources/               # 数据源配置目录
│   ├── github-ai-handbook.yaml
│   ├── cheerselfai-blog.yaml
│   └── cheerselfai-resources.yaml
├── templates/             # 报告模板目录
│   ├── daily-report.md   # 日报模板
│   └── readme.md         # README 模板
├── config/                # 系统配置
│   ├── sources.yaml      # 数据源汇总
│   ├── schedule.yaml     # 定时任务
│   └── channels.yaml     # 推送通道
├── src/                   # 源代码
│   ├── core/             # 核心模块
│   ├── adapters/         # 数据源适配器
│   ├── processors/       # 内容处理器
│   └── notifiers/        # 通知推送
├── scripts/               # 脚本工具
├── docs/                  # 文档
└── tests/                 # 测试
```

---

## 📡 当前监控的数据源

| 数据源 | 类型 | 频率 | 分类 | 状态 |
|--------|------|------|------|------|
| [AI Engineer Handbook](https://github.com/DataExpert-io/ai-engineer-handbook) | GitHub | 每日 | 学习资源, AI工程 | ✅ 活跃 |
| [CheerselfAI Blog](https://cheerselfai.com/blog) | RSS | 每日 | 博客, AI教程 | ✅ 活跃 |
| [CheerselfAI Resources](https://cheerselfai.com/resources) | Web | 每日 | 资源, AI工具 | ✅ 活跃 |

---

## 📅 最近报告

{{RECENT_REPORTS}}

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化配置

```bash
python scripts/init_db.py
```

### 3. 添加数据源

```bash
python scripts/add_source.py --type github --url https://github.com/DataExpert-io/ai-engineer-handbook
```

### 4. 手动运行测试

```bash
python scripts/manual_run.py --source github-ai-handbook
```

### 5. 启动定时任务

```bash
python src/scheduler.py
```

---

## ➕ 如何添加新数据源

### 方法 1: 使用脚本（推荐）

```bash
python scripts/add_source.py \
  --name "数据源名称" \
  --type github \
  --url "https://github.com/owner/repo" \
  --interval daily \
  --categories "分类1,分类2"
```

### 方法 2: 手动创建 YAML 配置

在 `sources/` 目录下创建新的 YAML 文件：

```yaml
# sources/my-source.yaml
name: "数据源名称"
description: "数据源描述"
type: github  # 可选: github, rss, web, newsletter
url: "https://example.com"
check_interval: "daily"  # 可选: hourly, daily, weekly
categories:
  - "分类1"
  - "分类2"
priority: medium  # 可选: low, medium, high, critical

notifications:
  enabled: true
  channels:
    - feishu
    - webchat

metadata:
  author: "作者"
  language: "zh"
  created_at: "2026-02-21"
```

### 支持的类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `github` | GitHub 仓库监控 | 监控 Releases、Commits |
| `rss` | RSS 订阅源 | 博客、新闻网站 |
| `web` | 网页监控 | 检测页面内容变化 |
| `newsletter` | 邮件订阅 | 通过邮件接收更新 |

---

## ⚙️ 配置说明

### 数据源配置 (`config/sources.yaml`)

系统会自动加载 `sources/` 目录下的所有 YAML 配置文件。

### 定时任务配置 (`config/schedule.yaml`)

```yaml
schedules:
  morning_digest:
    cron: "0 9 * * *"  # 每天9点
    sources: "*"       # 所有源
    channels:
      - feishu
      - webchat
```

### 推送通道配置 (`config/channels.yaml`)

```yaml
channels:
  feishu:
    type: feishu
    target: "ou_xxx"
  webchat:
    type: webchat
    target: "default"
```

---

## 🏗️ 扩展开发

### 添加新的数据源适配器

1. 继承 `BaseAdapter` 基类
2. 实现 `fetch()` 方法
3. 实现 `parse()` 方法
4. 注册到适配器工厂

示例：

```python
from src.adapters.base import BaseAdapter

class MyCustomAdapter(BaseAdapter):
    def fetch(self, url):
        # 获取原始数据
        pass
    
    def parse(self, raw_data):
        # 解析为标准格式
        return {
            'title': '',
            'content': '',
            'url': '',
            'published_at': '',
            'source': ''
        }
```

---

## 📊 数据模型

### NewsItem

```python
{
    'id': 'uuid',
    'title': '标题',
    'content': '内容',
    'summary': '摘要',
    'url': '链接',
    'source': '来源标识',
    'source_type': 'github/rss/twitter',
    'categories': ['标签1', '标签2'],
    'hash': '内容哈希',
    'published_at': '发布时间',
    'fetched_at': '采集时间',
    'is_notified': False,
    'notify_channels': []
}
```

---

## 📋 定时任务

| 任务 | 频率 | 说明 |
|------|------|------|
| 采集任务 | 每小时 | 检查所有数据源更新 |
| 早间推送 | 每天 9:00 | 推送昨日汇总 |
| 晚间推送 | 每天 20:00 | 推送今日更新 |
| 清理任务 | 每周 | 清理过期数据 |

---

## 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 许可证

本项目采用 [MIT](LICENSE) 许可证。

---

*项目创建时间: 2026-02-19*  
*最后更新: {{LAST_UPDATED}}*
