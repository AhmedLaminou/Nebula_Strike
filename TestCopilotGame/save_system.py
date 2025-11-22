"""
TestCopilotGame - Save System
Handles saving and loading high scores and game state.
"""

import json
import os
from typing import List, Dict
from settings import SAVE_FILE, MAX_HIGH_SCORES


class SaveSystem:
    """Manages game saves and high scores."""
    
    def __init__(self):
        """Initialize save system."""
        self.save_file = SAVE_FILE
        self.scores: List[Dict] = []
        self.load_scores()
    
    def load_scores(self):
        """Load high scores from file."""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    self.scores = data.get('scores', [])
                    # Sort by score descending
                    self.scores.sort(key=lambda x: x.get('score', 0), reverse=True)
            else:
                self.scores = []
        except:
            self.scores = []
    
    def save_scores(self):
        """Save high scores to file."""
        try:
            data = {
                'scores': self.scores[:MAX_HIGH_SCORES]
            }
            with open(self.save_file, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass  # Ignore save errors
    
    def add_score(self, score: int, level: int):
        """Add a new score entry."""
        if score <= 0:
            return
        
        entry = {
            'score': score,
            'level': level,
            'date': self.get_current_date_string()
        }
        
        self.scores.append(entry)
        self.scores.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        # Keep only top scores
        self.scores = self.scores[:MAX_HIGH_SCORES]
        
        # Save immediately
        self.save_scores()
    
    def get_high_score(self) -> int:
        """Get the highest score."""
        if self.scores:
            return self.scores[0].get('score', 0)
        return 0
    
    def get_scores(self) -> List[Dict]:
        """Get all high scores."""
        return self.scores.copy()
    
    def get_current_date_string(self) -> str:
        """Get current date as string."""
        try:
            from datetime import datetime
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except:
            return "Unknown"
    
    def clear_scores(self):
        """Clear all scores."""
        self.scores = []
        self.save_scores()
    
    def is_high_score(self, score: int) -> bool:
        """Check if score qualifies as high score."""
        if len(self.scores) < MAX_HIGH_SCORES:
            return True
        return score > self.get_high_score() or score > self.scores[-1].get('score', 0)

