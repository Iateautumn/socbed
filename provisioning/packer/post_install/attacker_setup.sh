#!/usr/bin/env bash

# Enable root account, set password and reboot
touch /tmp/runasroot.sh

echo "export http_proxy=http://192.168.1.130:7890" > /tmp/runasroot.sh
echo "export https_proxy=http://192.168.1.130:7890" >> /tmp/runasroot.sh
echo "ping www.baidu.com" >> /tmp/runasroot.sh
echo "wget https://archive.kali.org/archive-key.asc -O /etc/apt/trusted.gpg.d/kali-archive-keyring.asc" >> /tmp/runasroot.sh
echo "apt update" >> /tmp/runasroot.sh
echo "apt install kali-root-login" >> /tmp/runasroot.sh
echo "echo 'root:breach' | chpasswd" >> /tmp/runasroot.sh
echo "reboot" >> /tmp/runasroot.sh

echo breach | sudo -S chmod +x /tmp/runasroot.sh
echo breach | sudo -S /tmp/runasroot.sh
