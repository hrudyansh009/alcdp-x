from collections import Counter

HEATMAP = Counter()

def update_heatmap(techniques):
    for t in techniques:
        HEATMAP[t] += 1

def get_heatmap():
    return dict(HEATMAP)
