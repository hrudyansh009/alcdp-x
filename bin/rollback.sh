#!/bin/bash

LOG="logs/response.log"

iptables -F
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT

echo "$(date) | FIREWALL ROLLBACK EXECUTED" >> $LOG
