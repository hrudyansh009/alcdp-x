def score(bruteforce, reputation):
    score=0
    if bruteforce: score+=30
    if reputation>50: score+=30
    return "critical" if score>=60 else "high"
