import json
import os

SCORES_FILE = os.path.join(os.path.dirname(__file__), 'scores.json')


def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE) as f:
        return json.load(f)


def save_score(score, difficulty):
    scores = load_scores()
    scores.append({'score': score, 'difficulty': difficulty})
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)


def top_scores(difficulty, n=3):
    scores = load_scores()
    filtered = [s for s in scores if s.get('difficulty') == difficulty]
    return sorted(filtered, key=lambda x: x['score'], reverse=True)[:n]
