# soar/ip_reputation.py

BAD_IPS = {
    "10.0.2.15": 80,
    "192.168.56.101": 70
}

def score_ip(ip):
    base_score = 10

    if ip in BAD_IPS:
        base_score += BAD_IPS[ip]

    return min(base_score, 100)

