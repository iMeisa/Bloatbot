class User:
    def __init__(self, user_data: dict):
        self.id = user_data['user_id']
        self.name = user_data['username']
        self.url = 'https://osu.ppy.sh/users/' + self.id
        self.pfp = 'https://a.ppy.sh/' + self.id
        self.join_date = user_data['join_date']
        self.count300 = int(user_data['count300'])
        self.count100 = int(user_data['count100'])
        self.count50 = int(user_data['count50'])
        self.play_count = int(user_data['playcount'])
        self.ranked_score = user_data['ranked_score']
        self.total_score = user_data['total_score']
        self.global_rank = int(user_data['pp_rank'])
        self.level = float(user_data['level'])
        self.pp = float(user_data['pp_raw'])
        self.acc = float(user_data['accuracy'])
        self.count_rank_ss = int(user_data['count_rank_ss'])
        self.count_rank_ssh = int(user_data['count_rank_ssh'])
        self.count_rank_s = int(user_data['count_rank_s'])
        self.count_rank_sh = int(user_data['count_rank_sh'])
        self.count_rank_a = int(user_data['count_rank_a'])
        self.country = user_data['country']
        self.total_seconds_played = int(user_data['total_seconds_played'])
        self.country_rank = int(user_data['pp_country_rank'])
        self.events = user_data['events']
