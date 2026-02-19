"""
AI News Hub - 任务调度器
"""
import schedule
import time
import yaml
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from .adapters.github import GitHubAdapter
from .core.database import Database
from .core.dedup import DedupEngine
from .core.classifier import Classifier
from .core.summarizer import Summarizer
from .notifiers.feishu import FeishuNotifier


class NewsScheduler:
    """新闻采集调度器"""
    
    def __init__(self, config_dir: str = 'config'):
        self.config_dir = Path(config_dir)
        self.db = Database()
        self.dedup = DedupEngine()
        self.classifier = Classifier()
        self.summarizer = Summarizer()
        
        # 加载配置
        self.sources = self._load_config('sources.yaml')
        self.schedules = self._load_config('schedule.yaml')
        self.channels = self._load_config('channels.yaml')
        
        # 初始化推送器
        self.notifiers = self._init_notifiers()
    
    def _load_config(self, filename: str) -> Dict[str, Any]:
        """加载 YAML 配置"""
        config_path = self.config_dir / filename
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    def _init_notifiers(self) -> Dict[str, Any]:
        """初始化推送器"""
        notifiers = {}
        
        for channel_id, config in self.channels.get('channels', {}).items():
            if config['type'] == 'feishu':
                notifiers[channel_id] = FeishuNotifier(config)
            # 可添加更多推送器...
        
        return notifiers
    
    def _get_adapter(self, source_id: str, source_config: Dict) -> Any:
        """根据配置获取适配器"""
        source_type = source_config['type']
        
        if source_type == 'github':
            return GitHubAdapter(source_id, source_config)
        # 可添加更多适配器...
        
        raise ValueError(f"Unknown source type: {source_type}")
    
    def fetch_source(self, source_id: str):
        """采集单个数据源"""
        print(f"[{datetime.now()}] Fetching source: {source_id}")
        
        source_config = self.sources['sources'].get(source_id)
        if not source_config:
            print(f"Source not found: {source_id}")
            return
        
        try:
            # 获取适配器
            adapter = self._get_adapter(source_id, source_config)
            
            # 获取并解析数据
            news_items = adapter.fetch_and_parse()
            print(f"  Fetched {len(news_items)} items")
            
            # 处理每个条目
            new_items = []
            for item in news_items:
                # 去重检查
                if self.dedup.exists(item.content_hash):
                    print(f"  Skipping duplicate: {item.title[:50]}...")
                    continue
                
                # 分类
                if not item.categories:
                    item.categories = self.classifier.classify(item)
                
                # 生成摘要
                if not item.summary:
                    item.summary = self.summarizer.summarize(item.content)
                
                # 保存到数据库
                self.db.save_news(item)
                new_items.append(item)
                
                print(f"  New item: {item.title[:50]}...")
            
            # 更新检查时间
            adapter.set_last_check_time(datetime.now())
            
            print(f"  Saved {len(new_items)} new items")
            
        except Exception as e:
            print(f"Error fetching {source_id}: {e}")
    
    def fetch_all_sources(self):
        """采集所有数据源"""
        for source_id in self.sources.get('sources', {}).keys():
            self.fetch_source(source_id)
    
    def send_digest(self, schedule_name: str):
        """发送汇总推送"""
        print(f"[{datetime.now()}] Sending digest: {schedule_name}")
        
        schedule_config = self.schedules.get('schedules', {}).get(schedule_name)
        if not schedule_config:
            print(f"Schedule not found: {schedule_name}")
            return
        
        # 获取未推送的新闻
        news_items = self.db.get_unnotified_news()
        
        if not news_items:
            print("  No new items to notify")
            return
        
        # 按渠道推送
        for channel_id in schedule_config.get('channels', []):
            notifier = self.notifiers.get(channel_id)
            if not notifier:
                print(f"  Notifier not found: {channel_id}")
                continue
            
            try:
                notifier.send_digest(news_items)
                print(f"  Sent to {channel_id}: {len(news_items)} items")
                
                # 标记为已推送
                for item in news_items:
                    self.db.mark_notified(item.url, channel_id)
                    
            except Exception as e:
                print(f"  Error sending to {channel_id}: {e}")
    
    def setup_schedules(self):
        """设置定时任务"""
        # 采集任务 - 每小时
        schedule.every().hour.do(self.fetch_all_sources)
        
        # 配置的定时推送
        for schedule_name, config in self.schedules.get('schedules', {}).items():
            cron = config.get('cron', '')
            
            # 解析 cron 表达式 (简化版)
            if cron == '0 9 * * *':  # 每天9点
                schedule.every().day.at("09:00").do(
                    self.send_digest, schedule_name
                )
            elif cron == '0 20 * * *':  # 每天20点
                schedule.every().day.at("20:00").do(
                    self.send_digest, schedule_name
                )
            
            print(f"Scheduled: {schedule_name} at {cron}")
    
    def run(self):
        """运行调度器"""
        print("=" * 50)
        print("AI News Hub Scheduler Started")
        print("=" * 50)
        
        # 设置定时任务
        self.setup_schedules()
        
        # 立即执行一次采集
        self.fetch_all_sources()
        
        # 主循环
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次


if __name__ == '__main__':
    scheduler = NewsScheduler()
    scheduler.run()
