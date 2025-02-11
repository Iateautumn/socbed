#!/usr/bin/env python3

import argparse
import json

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

ELASTICSEARCH_HOSTS = ['http://192.168.56.12:9200']

QUERIES = [
    {'name': 'syslog', 'search': Search(index='syslog-*')},
    {'name': 'winlogbeat', 'search': Search(index='winlogbeat-*')},
    {'name': 'packetbeat', 'search': Search(index='packetbeat-*')},
    {'name': 'auditbeat', 'search': Search(index='auditbeat-*')}]


def main():
    args = parse_args()
    if args.action == 'download':
        if not args.start or not args.end or not args.suffix:
            print("Error: 'download' action requires --start, --end, and --suffix arguments.")
            return
        download_logs(args.start, args.end, args.suffix)
    elif args.action == 'delete':
        delete_logs()
    else:
        print("Error: Unsupported action. Use 'download' or 'delete'.")


def parse_args():
    parser = argparse.ArgumentParser(description='Download logs')
    parser.add_argument('action', choices=['download', 'delete'], help='Action to perform: download or delete logs')
    parser.add_argument('--start', help='Start time for downloading logs (required for download)')
    parser.add_argument('--end', help='End time for downloading logs (required for download)')
    parser.add_argument('--suffix', help='Filename suffix for downloaded logs (required for download)')
    return parser.parse_args()


def download_logs(start, end, suffix):
    client = Elasticsearch(ELASTICSEARCH_HOSTS, timeout=600, max_retries=10, retry_on_timeout=True)
    for query in QUERIES:
        filename = query['name'] + '_' + str(suffix) + '.jsonl'
        print('Writing ' + filename + '... with start: ' + start + ' end: ' + end)
        with open(filename, 'w') as f:
            for hit in query['search'].using(client).filter(
                    'range', **{'@timestamp': {'gte': start, 'lt': end}}).scan():
                f.write(json.dumps(hit.to_dict(), sort_keys=True) + '\n')


def delete_logs():
    # Index patterns to delete logs from
    INDEX_PATTERNS = ['syslog-*', 'winlogbeat-*', 'packetbeat-*', 'auditbeat-*']
    # Create Elasticsearch client
    client = Elasticsearch(ELASTICSEARCH_HOSTS, timeout=600, max_retries=10, retry_on_timeout=True)

    for index_pattern in INDEX_PATTERNS:
        print(f'Deleting logs from index pattern: {index_pattern}')

        # Use delete_by_query to delete all documents matching the query
        response = client.delete_by_query(
            index=index_pattern,
            body={
                "query": {
                    "match_all": {}  # Deletes all documents
                }
            },
            conflicts="proceed",  # Ignore conflicts
            refresh=True  # Refresh index after deletion
        )

        print(f"Deleted {response['deleted']} documents from index pattern: {index_pattern}")


if __name__ == '__main__':
    main()
