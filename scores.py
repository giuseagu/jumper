import json
import os

SCORES_FILE = os.path.join(os.path.dirname(__file__), 'scores.json')


def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE) as f:
        return json.load(f)


def save_score(score):
    scores = load_scores()
    game_number = len(scores) + 1
    scores.append({'game': game_number, 'score': score})
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)


def top_scores(n=3):
    scores = load_scores()
    return sorted(scores, key=lambda x: x['score'], reverse=True)[:n]
