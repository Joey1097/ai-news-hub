"""
AI News Hub - 数据源适配器基类
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json


@dataclass
class NewsItem:
    """标准化新闻条目"""
    title: str
    content: str
    url: str
    source_id: str
    source_type: str
    published_at: Optional[datetime] = None
    summary: Optional[str] = None
    categories: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.categories is None:
            self.categories = []
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def content_hash(self) -> str:
        """计算内容指纹用于去重"""
        content = f"{self.title}:{self.content[:500]}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'title': self.title,
            'content': self.content,
            'url': self.url,
            'source_id': self.source_id,
            'source_type': self.source_type,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'summary': self.summary,
            'categories': self.categories,
            'metadata': self.metadata,
            'content_hash': self.content_hash
        }


class BaseAdapter(ABC):
    """数据源适配器基类"""
    
    def __init__(self, source_id: str, config: Dict[str, Any]):
        self.source_id = source_id
        self.config = config
        self.source_type = self.get_type()
    
    @abstractmethod
    def get_type(self) -> str:
        """返回适配器类型标识"""
        pass
    
    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]:
        """
        从数据源获取原始数据
        
        Returns:
            List[Dict]: 原始数据列表
        """
        pass
    
    @abstractmethod
    def parse(self, raw_data: Dict[str, Any]) -> NewsItem:
        """
        将原始数据解析为标准 NewsItem
        
        Args:
            raw_data: 原始数据
            
        Returns:
            NewsItem: 标准化的新闻条目
        """
        pass
    
    def fetch_and_parse(self) -> List[NewsItem]:
        """
        获取并解析所有数据
        
        Returns:
            List[NewsItem]: 标准化的新闻条目列表
        """
        raw_items = self.fetch()
        return [self.parse(item) for item in raw_items]
    
    def get_last_check_time(self) -> Optional[datetime]:
        """获取上次检查时间"""
        # 从数据库或状态文件读取
        return None
    
    def set_last_check_time(self, check_time: datetime):
        """设置上次检查时间"""
        # 保存到数据库或状态文件
        pass
