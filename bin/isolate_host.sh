#!/bin/bash

LOG="logs/response.log"

iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

echo "$(date) | HOST ISOLATED" >> $LOG
