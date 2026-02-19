# AI News Hub - 可扩展 AI 新闻聚合系统

## 项目概述

一个模块化、可扩展的 AI 新闻聚合系统，支持多源采集、智能分类、定时推送。

## 核心特性

- **多源支持**: GitHub、Newsletter、RSS、Twitter/X 等
- **模块化设计**: 每个数据源独立适配器
- **智能去重**: 基于内容哈希的重复检测
- **分类标签**: 自动/手动分类，支持多维度标签
- **定时任务**: 可配置的采集和推送频率
- **多通道推送**: 飞书、Webchat、邮件等

## 项目结构

```
ai-news-hub/
├── config/                 # 配置文件
│   ├── sources.yaml       # 数据源配置
│   ├── schedule.yaml      # 定时任务配置
│   └── channels.yaml      # 推送通道配置
├── src/                   # 源代码
│   ├── core/             # 核心模块
│   │   ├── __init__.py
│   │   ├── config.py     # 配置管理
│   │   ├── database.py   # 数据存储
│   │   ├── classifier.py # 内容分类
│   │   └── dedup.py      # 去重引擎
│   ├── adapters/         # 数据源适配器
│   │   ├── __init__.py
│   │   ├── base.py       # 适配器基类
│   │   ├── github.py     # GitHub 适配器
│   │   ├── rss.py        # RSS 适配器
│   │   ├── newsletter.py # Newsletter 适配器
│   │   └── twitter.py    # Twitter/X 适配器
│   ├── processors/       # 内容处理器
│   │   ├── __init__.py
│   │   ├── summarizer.py # 内容摘要
│   │   └── translator.py # 翻译处理
│   ├── notifiers/        # 通知推送
│   │   ├── __init__.py
│   │   ├── base.py       # 通知基类
│   │   ├── feishu.py     # 飞书推送
│   │   └── webchat.py    # Webchat 推送
│   └── scheduler.py      # 任务调度器
├── scripts/              # 脚本工具
│   ├── init_db.py       # 初始化数据库
│   ├── add_source.py    # 添加数据源
│   └── manual_run.py    # 手动运行
├── docs/                 # 文档
│   ├── architecture.md  # 架构设计
│   ├── adapters.md      # 适配器开发指南
│   └── api.md           # API 文档
├── tests/                # 测试
│   └── test_adapters.py
├── data/                 # 数据存储 (gitignore)
│   └── news.db
├── requirements.txt      # 依赖
└── README.md            # 项目说明
```

## 快速开始

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

## 配置说明

### 数据源配置 (config/sources.yaml)

```yaml
sources:
  github-ai-handbook:
    type: github
    name: "AI Engineer Handbook"
    url: "https://github.com/DataExpert-io/ai-engineer-handbook"
    check_interval: "daily"  # daily, hourly, weekly
    categories:
      - "学习资源"
      - "AI工程"
    priority: high
    
  # 可添加更多源...
```

### 定时任务配置 (config/schedule.yaml)

```yaml
schedules:
  morning_digest:
    cron: "0 9 * * *"  # 每天9点
    sources: "*"       # 所有源
    channels:
      - feishu
      - webchat
      
  evening_digest:
    cron: "0 20 * * *"  # 每天20点
    sources: "*"
    channels:
      - feishu
```

### 推送通道配置 (config/channels.yaml)

```yaml
channels:
  feishu:
    type: feishu
    target: "ou_ed1c1ef79f13a9462dea718e57fd2b34"
    
  webchat:
    type: webchat
    target: "default"
```

## 扩展开发

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

## 数据模型

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

## 定时任务

| 任务 | 频率 | 说明 |
|------|------|------|
| 采集任务 | 每小时 | 检查所有数据源更新 |
| 早间推送 | 每天 9:00 | 推送昨日汇总 |
| 晚间推送 | 每天 20:00 | 推送今日更新 |
| 清理任务 | 每周 | 清理过期数据 |

---

*项目创建时间: 2026-02-19*
