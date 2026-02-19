"""
网页爬虫适配器
用于监控普通网站的更新
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from datetime import datetime
from urllib.parse import urljoin

from .base import BaseAdapter, NewsItem


class WebScraperAdapter(BaseAdapter):
    """网页爬虫适配器"""
    
    def get_type(self) -> str:
        return 'web_scraper'
    
    def fetch(self) -> List[Dict[str, Any]]:
        """
        抓取网页内容
        
        使用 CSS 选择器提取内容
        """
        items = []
        url = self.config['url']
        selectors = self.config.get('selectors', {})
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 获取文章列表
            article_selector = selectors.get('article', 'article')
            articles = soup.select(article_selector)
            
            for article in articles:
                try:
                    # 提取标题
                    title_selector = selectors.get('title', 'h2')
                    title_elem = article.select_one(title_selector)
                    title = title_elem.get_text(strip=True) if title_elem else 'No title'
                    
                    # 提取链接
                    link_selector = selectors.get('link', 'a')
                    link_elem = article.select_one(link_selector)
                    if link_elem and link_elem.get('href'):
                        link = urljoin(url, link_elem['href'])
                    else:
                        link = url
                    
                    # 提取日期
                    date_selector = selectors.get('date', 'time')
                    date_elem = article.select_one(date_selector)
                    published_at = None
                    if date_elem:
                        date_str = date_elem.get('datetime') or date_elem.get_text(strip=True)
                        # 尝试解析日期
                        try:
                            published_at = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        except:
                            pass
                    
                    # 提取内容摘要
                    content_elem = article.select_one('p') or article
                    content = content_elem.get_text(strip=True)[:500]
                    
                    items.append({
                        'title': title,
                        'link': link,
                        'content': content,
                        'published_at': published_at
                    })
                    
                except Exception as e:
                    print(f"Error parsing article: {e}")
                    continue
            
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        
        return items
    
    def parse(self, raw_data: Dict[str, Any]) -> NewsItem:
        """解析为 NewsItem"""
        return NewsItem(
            title=raw_data['title'],
            content=raw_data['content'],
            url=raw_data['link'],
            source_id=self.source_id,
            source_type='web_scraper',
            published_at=raw_data.get('published_at'),
            categories=self.config.get('categories', ['Web']),
            metadata={
                'source_name': self.config.get('name', 'Unknown'),
                'fetched_at': datetime.now().isoformat()
            }
        )
