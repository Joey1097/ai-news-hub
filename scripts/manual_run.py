#!/usr/bin/env python3
"""
手动运行采集任务
用于测试和调试
"""
import sys
import argparse
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from scheduler import NewsScheduler


def main():
    parser = argparse.ArgumentParser(description='AI News Hub - Manual Run')
    parser.add_argument('--source', '-s', help='指定数据源 ID')
    parser.add_argument('--all', '-a', action='store_true', help='采集所有源')
    parser.add_argument('--digest', '-d', help='发送汇总 (指定 schedule 名称)')
    
    args = parser.parse_args()
    
    scheduler = NewsScheduler()
    
    if args.source:
        print(f"Fetching source: {args.source}")
        scheduler.fetch_source(args.source)
    elif args.all:
        print("Fetching all sources...")
        scheduler.fetch_all_sources()
    elif args.digest:
        print(f"Sending digest: {args.digest}")
        scheduler.send_digest(args.digest)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
