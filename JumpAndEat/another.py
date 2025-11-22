import os
import json

class ScoreManager:
    def __init__(self, filename="score_history.json"):
        self.filename = filename
        self.scores = self.load_scores()

    def add_score(self, score):
        self.scores.append(score)
        self.save_scores()

    def get_scores(self):
        return sorted(self.scores, reverse=True)[:10]

    def save_scores(self):
        with open(self.filename, "w") as f:
            json.dump(self.scores, f)

    def load_scores(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return []
