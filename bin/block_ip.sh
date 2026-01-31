#!/bin/bash

IP=$1
LOG="logs/response.log"

iptables -C INPUT -s $IP -j DROP 2>/dev/null
if [ $? -ne 0 ]; then
    iptables -A INPUT -s $IP -j DROP
    echo "$(date) | BLOCKED IP: $IP" >> $LOG
fi

