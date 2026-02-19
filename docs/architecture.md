# AI News Hub 架构设计

## 系统架构图

```mermaid
graph TB
    subgraph "数据源层"
        GH[GitHub]
        RSS[RSS]
        TW[Twitter/X]
        NL[Newsletter]
        OTHER[其他源...]
    end
    
    subgraph "适配器层"
        GA[GitHub Adapter]
        RA[RSS Adapter]
        TA[Twitter Adapter]
        NA[Newsletter Adapter]
    end
    
    subgraph "核心处理层"
        FETCH[采集引擎]
        PARSE[解析引擎]
        DEDUP[去重引擎]
        CLASS[分类引擎]
        SUMM[摘要引擎]
    end
    
    subgraph "存储层"
        DB[(SQLite/PostgreSQL)]
        CACHE[(Redis Cache)]
    end
    
    subgraph "推送层"
        FEISHU[飞书推送]
        WEBCHAT[Webchat推送]
        EMAIL[邮件推送]
    end
    
    GH --> GA
    RSS --> RA
    TW --> TA
    NL --> NA
    
    GA --> FETCH
    RA --> FETCH
    TA --> FETCH
    NA --> FETCH
    
    FETCH --> PARSE
    PARSE --> DEDUP
    DEDUP --> CLASS
    CLASS --> SUMM
    
    SUMM --> DB
    DB --> CACHE
    
    DB --> FEISHU
    DB --> WEBCHAT
    DB --> EMAIL
```

## 数据流

```mermaid
sequenceDiagram
    participant Scheduler
    participant Adapter
    participant Processor
    participant Database
    participant Notifier
    
    Scheduler->>Adapter: 触发采集
    Adapter->>Adapter: fetch() 获取原始数据
    Adapter->>Processor: 传递原始数据
    
    Processor->>Processor: parse() 解析内容
    Processor->>Processor: hash() 计算指纹
    Processor->>Database: 检查是否已存在
    
    alt 新内容
        Processor->>Processor: classify() 分类
        Processor->>Processor: summarize() 摘要
        Processor->>Database: 存储
        Database->>Notifier: 触发推送
        Notifier->>Notifier: 发送到各通道
    else 已存在
        Processor->>Processor: 跳过
    end
```

## 模块职责

### 1. 适配器层 (Adapters)

| 适配器 | 职责 | 关键方法 |
|--------|------|---------|
| BaseAdapter | 定义接口规范 | `fetch()`, `parse()` |
| GitHubAdapter | 监控 GitHub 仓库更新 | 读取 commits, releases, issues |
| RSSAdapter | 订阅 RSS 源 | 解析 XML, 提取文章 |
| TwitterAdapter | 监控 Twitter 账号 | API 调用, 推文抓取 |
| NewsletterAdapter | 邮件订阅处理 | IMAP 读取, 内容解析 |

### 2. 核心处理层 (Core)

| 模块 | 职责 | 算法/技术 |
|------|------|----------|
| ConfigManager | 配置管理 | YAML 解析, 热更新 |
| Database | 数据持久化 | SQLite/PostgreSQL |
| DedupEngine | 去重检测 | SimHash, 内容指纹 |
| Classifier | 自动分类 | 关键词匹配, LLM 分类 |
| Summarizer | 内容摘要 | LLM 摘要, 提取关键句 |

### 3. 推送层 (Notifiers)

| 推送器 | 职责 | 格式 |
|--------|------|------|
| FeishuNotifier | 飞书消息推送 | Markdown/卡片 |
| WebchatNotifier | Webchat 推送 | Markdown |
| EmailNotifier | 邮件推送 | HTML/纯文本 |

## 扩展点设计

### 添加新数据源

```mermaid
graph LR
    A[创建 Adapter 类] --> B[继承 BaseAdapter]
    B --> C[实现 fetch 方法]
    C --> D[实现 parse 方法]
    D --> E[注册到工厂]
    E --> F[配置 sources.yaml]
```

### 添加新推送通道

```mermaid
graph LR
    A[创建 Notifier 类] --> B[继承 BaseNotifier]
    B --> C[实现 send 方法]
    C --> D[注册到工厂]
    D --> E[配置 channels.yaml]
```

## 数据库设计

### 表结构

```sql
-- 新闻内容表
CREATE TABLE news_items (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    summary TEXT,
    url TEXT UNIQUE NOT NULL,
    source_id TEXT NOT NULL,
    source_type TEXT NOT NULL,
    categories TEXT, -- JSON array
    content_hash TEXT UNIQUE NOT NULL,
    published_at TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_notified BOOLEAN DEFAULT FALSE,
    notify_channels TEXT -- JSON array
);

-- 数据源表
CREATE TABLE sources (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    url TEXT NOT NULL,
    config TEXT, -- JSON
    last_check_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 推送记录表
CREATE TABLE notifications (
    id TEXT PRIMARY KEY,
    news_id TEXT REFERENCES news_items(id),
    channel TEXT NOT NULL,
    status TEXT, -- sent, failed, pending
    sent_at TIMESTAMP,
    error_message TEXT
);

-- 内容指纹表 (用于去重)
CREATE TABLE content_fingerprints (
    hash TEXT PRIMARY KEY,
    news_id TEXT REFERENCES news_items(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 配置热更新

```mermaid
graph TB
    A[配置文件修改] --> B[文件系统监听]
    B --> C[配置重新加载]
    C --> D[验证配置]
    D -->|有效| E[应用到运行时]
    D -->|无效| F[记录错误, 保持旧配置]
```

## 错误处理与重试

```mermaid
graph TB
    A[任务执行] --> B{成功?}
    B -->|是| C[记录成功]
    B -->|否| D[记录失败]
    D --> E{重试次数 < 3?}
    E -->|是| F[指数退避等待]
    F --> A
    E -->|否| G[标记为失败]
    G --> H[发送告警]
```

## 性能优化

| 优化点 | 策略 |
|--------|------|
| 采集频率 | 自适应频率调整 |
| 去重检测 | Bloom Filter 预过滤 |
| 内容存储 | 压缩存储大文本 |
| 推送队列 | 批量推送, 异步处理 |
| 缓存策略 | Redis 缓存热点数据 |

## 监控指标

| 指标 | 说明 |
|------|------|
| fetch_latency | 采集延迟 |
| parse_success_rate | 解析成功率 |
| dedup_ratio | 去重比例 |
| notify_success_rate | 推送成功率 |
| queue_depth | 待处理队列深度 |
