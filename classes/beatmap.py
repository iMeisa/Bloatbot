from util.osu_tools import rank_emoji, oppai


class Beatmap:
    def __init__(self, beatmap_data: dict):
        self.set_id = beatmap_data['beatmapset_id']
        self.id = beatmap_data['beatmap_id']
        self.url = 'https://osu.ppy.sh/b/' + self.id
        self.cover_url = 'https://assets.ppy.sh/beatmaps/' + self.set_id + '/covers/cover.jpg'
        self.approved = int(beatmap_data['approved'])
        self.approved_emoji, self.approved_status = rank_emoji(self.approved)
        self.total_length = int(beatmap_data['total_length'])
        self.hit_length = int(beatmap_data['hit_length'])
        self.version = beatmap_data['version']
        self.file_md5 = beatmap_data['file_md5']
        self.cs = float(beatmap_data['diff_size'])
        self.od = float(beatmap_data['diff_overall'])
        self.ar = float(beatmap_data['diff_approach'])
        self.hp = float(beatmap_data['diff_drain'])
        self.game_mode = int(beatmap_data['mode'])
        self.circle_count = int(beatmap_data['count_normal'])
        self.slider_count = int(beatmap_data['count_slider'])
        self.spinner_count = int(beatmap_data['count_spinner'])
        self.submit_date = beatmap_data['submit_date']
        self.approved_date = beatmap_data['approved_date']
        self.last_update = beatmap_data['last_update']
        self.artist = beatmap_data['artist']
        self.artist_unicode = beatmap_data['artist_unicode']
        self.title = beatmap_data['title']
        self.title_unicode = beatmap_data['title_unicode']
        self.mapper = beatmap_data['creator']
        self.mapper_id = beatmap_data['creator_id']
        self.bpm = float(beatmap_data['bpm'])
        self.source = beatmap_data['source']
        self.tags = beatmap_data['tags'].split()
        self.genre_id = beatmap_data['genre_id']
        self.language_id = beatmap_data['language_id']
        self.favorite_count = self.favourite_count = int(beatmap_data['favourite_count'])
        self.rating = float(beatmap_data['rating'])
        self.storyboard = beatmap_data['storyboard'] == '1'
        self.video = beatmap_data['video'] == '1'
        self.download_unavailable = beatmap_data['download_unavailable'] == '1'
        self.audio_unavailable = beatmap_data['audio_unavailable'] == '1'
        self.play_count = int(beatmap_data['playcount'])
        self.pass_count = int(beatmap_data['passcount'])
        self.packs = beatmap_data['packs']
        self.max_combo = int(beatmap_data['max_combo'])
        self.diff_aim = float(beatmap_data['diff_aim'])
        self.diff_speed = float(beatmap_data['diff_speed'])
        self.sr = f'{float(beatmap_data["difficultyrating"]):.2f}'

    def mod_adjust(self, mods: str):
        if mods is None:
            return

        mods = mods.upper()
        params = '+' + mods
        adjusted_stats = oppai(map_id=self.id, oppai_params=params)

        difficulty = adjusted_stats[2].split()
        self.ar = float(difficulty[0][2:])
        self.od = float(difficulty[1][2:])
        self.cs = float(difficulty[2][2:])
        self.hp = float(difficulty[3][2:])

        if 'DT' in mods or 'NC' in mods:
            self.bpm *= 1.5
            self.hit_length *= 0.66
            self.total_length *= 0.66

        if 'HT' in mods:
            self.bpm *= 0.66
            self.hit_length *= 1.5
            self.total_length *= 1.5
