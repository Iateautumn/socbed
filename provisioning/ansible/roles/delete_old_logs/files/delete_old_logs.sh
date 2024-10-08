#!/bin/bash
# 清除指定天数前的日志，默认15天
past_day_count=${1:-15}
# 修改以下索引以更改要删除的日志
index_prefixes=("syslog-*" "auditbeat-*" "winlogbeat-*" "packetbeat-*")
es_host=${2:-"localhost:9200"}

echo "准备清理掉ES[$es_host]内索引前缀为[${index_prefixes[*]}]的超过当前时间前$past_day_count天的信息..."
function delete_indices() {
    index_name=$1
    index_date=$2
    comp_date=$(date -d "$past_day_count day ago" +"%Y-%m-%d")
    date1="$index_date 00:00:00"
    date2="$comp_date 00:00:00"
    t1=$(date -d "$date1" +%s)
    t2=$(date -d "$date2" +%s)
    if [ $t1 -le $t2 ]; then
        curl -XDELETE "http://$es_host/$index_name"
    fi
}

for index_prefix in "${index_prefixes[@]}"; do
    curl -XGET "http://$es_host/_cat/indices" | awk -F" " '{print $3}' | grep "$index_prefix" | sort | while read LINE; do
        index_name=$LINE
        index_date=$(echo $LINE | awk -F"-" '{print $NF}' | grep "[0-9]*\.[0-9]*\.[0-9]*" | uniq | sed 's/\./-/g')
        if [ $index_date ]; then
            delete_indices $index_name $index_date
        fi
    done
done
