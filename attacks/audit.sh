#!/bin/bash

# Define password
PASSWORD="breach"

# Define remote hosts and paths
REMOTE_HOST_1="192.168.56.11"
REMOTE_PATH_1="/var/log/audit/*"
LOCAL_DIR_1="./internalserver"

REMOTE_HOST_2="192.168.56.20"
REMOTE_PATH_2="/var/log/audit/*"
LOCAL_DIR_2="./dmzserver"

# Ensure the local directories do not exist
if [ -d "$LOCAL_DIR_1" ]; then
  echo "Removing existing directory: $LOCAL_DIR_1"
  rm -rf "$LOCAL_DIR_1"
fi

if [ -d "$LOCAL_DIR_2" ]; then
  echo "Removing existing directory: $LOCAL_DIR_2"
  rm -rf "$LOCAL_DIR_2"
fi

# Ensure local directories exist, create if they don't
mkdir -p "$LOCAL_DIR_1"
mkdir -p "$LOCAL_DIR_2"

# Use sshpass to transfer files
sshpass -p "$PASSWORD" scp root@$REMOTE_HOST_1:"$REMOTE_PATH_1" "$LOCAL_DIR_1"
if [ $? -eq 0 ]; then
  echo "Files from $REMOTE_HOST_1 ($REMOTE_PATH_1) successfully transferred to $LOCAL_DIR_1"
else
  echo "File transfer from $REMOTE_HOST_1 ($REMOTE_PATH_1) failed"
fi

sshpass -p "$PASSWORD" scp root@$REMOTE_HOST_2:"$REMOTE_PATH_2" "$LOCAL_DIR_2"
if [ $? -eq 0 ]; then
  echo "Files from $REMOTE_HOST_2 ($REMOTE_PATH_2) successfully transferred to $LOCAL_DIR_2"
else
  echo "File transfer from $REMOTE_HOST_2 ($REMOTE_PATH_2) failed"
fi
