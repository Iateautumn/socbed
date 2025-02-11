#!/usr/bin/env python3

import argparse
import json
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

ELASTICSEARCH_HOSTS = ['http://192.168.56.12:9200']

def parse_args():
    parser = argparse.ArgumentParser(description='Upload logs to Elasticsearch')
    parser.add_argument('file', help='Path to the JSONL file to upload')
    parser.add_argument('prefix', help='Prefix for the index name')
    return parser.parse_args()

def get_index_name(prefix, timestamp):
    """
    根据日志的时间戳生成索引名称，格式为：prefix-YYYY.MM.DD
    """
    date_str = timestamp.strftime('%Y.%m.%d')
    return f"{prefix}-{date_str}"

def prepare_document(log_line, prefix):
    """
    为每一行日志添加时间戳，并生成符合ES要求的文档结构
    """
    try:
        log = json.loads(log_line)
        
        # 获取日志中的时间戳，假设时间戳字段为 'timestamp'，可以根据实际情况修改
        timestamp = log.get('timestamp')
        if timestamp:
            # 解析时间戳字段，假设是ISO 8601格式，例如 '2023-11-27T12:34:56Z'
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        else:
            # 如果没有时间戳，使用当前时间
            timestamp = datetime.utcnow()

        # 使用时间戳来生成索引名称
        index_name = get_index_name(prefix, timestamp)

        # 这里假设日志结构已包含 timestamp 字段，我们可以直接使用它，确保 Kibana 能识别
        # 如果需要，也可以将时间戳字段重命名为 `@timestamp` 来与 Kibana 默认字段兼容
        document = {
            "_op_type": "index",  # 操作类型为插入（如果存在则更新）
            "_index": index_name,  # 使用动态生成的索引名称
            "_source": log,  # 日志的原始数据
            "@timestamp": timestamp  # 显式添加时间戳字段（如果不存在）
        }
        return document
    except Exception as e:
        print(f"Error processing log line: {log_line}. Error: {e}")
        return None

def upload_logs(file_path, prefix):
    """
    读取 JSONL 文件并上传日志到 Elasticsearch
    """
    documents = []
    with open(file_path, 'r') as f:
        for line in f:
            doc = prepare_document(line.strip(), prefix)
            if doc:
                documents.append(doc)

            # 每500条日志提交一次
            if len(documents) >= 500:
                try:
                    # 批量提交到 Elasticsearch
                    success, failed = bulk(Elasticsearch(ELASTICSEARCH_HOSTS), documents)
                    print(f"Successfully indexed {success} documents.")
                    print(f"Failed to index {failed} documents.")
                except Exception as e:
                    print(f"Error during bulk upload: {e}")

                # 清空已提交的文档列表
                documents = []

        # 提交剩余的文档
        if documents:
            try:
                success, failed = bulk(Elasticsearch(ELASTICSEARCH_HOSTS), documents)
                print(f"Successfully indexed {success} documents.")
                print(f"Failed to index {failed} documents.")
            except Exception as e:
                print(f"Error during final bulk upload: {e}")

def main():
    args = parse_args()
    upload_logs(args.file, args.prefix)

if __name__ == '__main__':
    main()

