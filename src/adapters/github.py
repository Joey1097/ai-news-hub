"""
GitHub 仓库适配器
用于监控 GitHub 仓库的更新（commits, releases, issues）
"""
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
from .base import BaseAdapter, NewsItem


class GitHubAdapter(BaseAdapter):
    """GitHub 仓库监控适配器"""
    
    def get_type(self) -> str:
        return 'github'
    
    def _parse_repo_url(self, url: str) -> tuple:
        """解析 GitHub URL 获取 owner 和 repo"""
        # https://github.com/owner/repo -> (owner, repo)
        parts = url.replace('https://github.com/', '').split('/')
        return parts[0], parts[1]
    
    def _get_api_url(self, endpoint: str) -> str:
        """构建 GitHub API URL"""
        owner, repo = self._parse_repo_url(self.config['url'])
        return f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
    
    def fetch(self) -> List[Dict[str, Any]]:
        """
        获取 GitHub 仓库更新
        
        包括:
        - 最新 commits
        - 最新 releases
        - 更新的 issues
        """
        items = []
        headers = {}
        
        # 如果有 token，使用认证
        if 'token' in self.config:
            headers['Authorization'] = f"token {self.config['token']}"
        
        # 获取 commits
        try:
            commits_url = self._get_api_url('commits')
            params = {'per_page': 10}
            
            # 如果指定了 since，只获取之后的提交
            last_check = self.get_last_check_time()
            if last_check:
                params['since'] = last_check.isoformat()
            
            response = requests.get(commits_url, headers=headers, params=params)
            response.raise_for_status()
            
            for commit in response.json():
                items.append({
                    'type': 'commit',
                    'data': commit
                })
        except Exception as e:
            print(f"Error fetching commits: {e}")
        
        # 获取 releases
        try:
            releases_url = self._get_api_url('releases')
            response = requests.get(releases_url, headers=headers, params={'per_page': 5})
            response.raise_for_status()
            
            for release in response.json():
                # 只获取最近发布的
                published_at = datetime.fromisoformat(release['published_at'].replace('Z', '+00:00'))
                if last_check and published_at <= last_check:
                    continue
                    
                items.append({
                    'type': 'release',
                    'data': release
                })
        except Exception as e:
            print(f"Error fetching releases: {e}")
        
        return items
    
    def parse(self, raw_data: Dict[str, Any]) -> NewsItem:
        """解析 GitHub 数据为 NewsItem"""
        item_type = raw_data['type']
        data = raw_data['data']
        
        if item_type == 'commit':
            return self._parse_commit(data)
        elif item_type == 'release':
            return self._parse_release(data)
        else:
            raise ValueError(f"Unknown item type: {item_type}")
    
    def _parse_commit(self, commit: Dict) -> NewsItem:
        """解析 commit"""
        owner, repo = self._parse_repo_url(self.config['url'])
        
        return NewsItem(
            title=f"[{repo}] New commit: {commit['commit']['message'].split(chr(10))[0][:80]}",
            content=commit['commit']['message'],
            url=commit['html_url'],
            source_id=self.source_id,
            source_type='github',
            published_at=datetime.fromisoformat(
                commit['commit']['committer']['date'].replace('Z', '+00:00')
            ),
            categories=['GitHub', 'Commit'],
            metadata={
                'author': commit['commit']['author']['name'],
                'sha': commit['sha'][:7],
                'repo': f"{owner}/{repo}"
            }
        )
    
    def _parse_release(self, release: Dict) -> NewsItem:
        """解析 release"""
        owner, repo = self._parse_repo_url(self.config['url'])
        
        return NewsItem(
            title=f"[{repo}] New release: {release['tag_name']}",
            content=release.get('body', 'No release notes') or 'No release notes',
            url=release['html_url'],
            source_id=self.source_id,
            source_type='github',
            published_at=datetime.fromisoformat(
                release['published_at'].replace('Z', '+00:00')
            ),
            categories=['GitHub', 'Release'],
            metadata={
                'tag': release['tag_name'],
                'author': release['author']['login'],
                'repo': f"{owner}/{repo}",
                'is_prerelease': release.get('prerelease', False)
            }
        )
