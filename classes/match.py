from classes.game import Game


class Match:
    def __init__(self, match_data: dict):
        self.match_id = match_data['match']['match_id']
        self.match_name = match_data['match']['name']
        self.start_time = match_data['match']['start_time']
        self.end_time = match_data['match']['end_time']
        self.games = [Game(game) for game in match_data['games']]

