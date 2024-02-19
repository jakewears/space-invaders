import json
from pathlib import Path

class GameStats:
    """track statistics for Space Invaders"""

    def __init__(self, ai_game):
        """initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        self.high_score = self.get_saved_high_score()

    def reset_stats(self):
        """initialize stats that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def get_saved_high_score(self):
        path = Path('high_score.json')
        try:
            contents = path.read_text()
            high_score = json.loads(contents)
            return high_score
        except FileNotFoundError:
            return 0
        