from classes.play import Play


class Game:
    def __init__(self, game_data: dict):
        self.id = game_data['game_id']
        self.start_time = game_data['start_time']
        self.end_time = game_data['end_time']
        self.beatmap_id = game_data['beatmap_id']
        self.game_mode = game_data['play_mode']
        self.match_type = game_data['match_type']
        self.scoring_type = game_data['scoring_type']
        self.team_type = game_data['team_type']
        self.mods = game_data['mods']
        self.scores = [Play(score) for score in game_data['scores']]
