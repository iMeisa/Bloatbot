import discord
from discord.ext import commands
import pickle
from urllib.parse import urlencode
from Cogs.Tools import osu


class TTT(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ttt(self, ctx, *, params=''):

        with open('Cogs/Tools/osuAPI.pickle', 'rb') as fl:
            api_key = pickle.load(fl)

        # Separate comments from params
        params = params.split()
        match_link = params[0]
        comments = ''
        if len(params) > 1:
            comment_words = params[1:]
            for word in comment_words:
                comments += word + ' '

        # Extract match ID from link
        match_url_split = match_link.split('/')
        match_id = match_url_split[-1]

        # Create URL
        query = urlencode({'k': api_key, 'mp': match_id})
        url_params = 'get_match?' + query

        # Get match data
        match_data = osu.call_api(url_params)
        match_title = match_data['match']['name']
        match_games = match_data['games']

        # Get mappool from file
        mappool = {}
        with open('Cogs/Tools/tttmappool.txt', 'r') as f:
            mappool_raw = f.read().split('\n')
            for beatmap in mappool_raw:
                beatmap_pool_id = beatmap.split(' ')
                pool_id = beatmap_pool_id[1]
                map_id = beatmap_pool_id[0]
                mappool[map_id] = pool_id

        # Analyze scores
        match_scores = []
        player_scores = {}
        user_ids = {}
        for game in match_games:

            game_scores = game['scores']
            beatmap_id = game['beatmap_id']
            if beatmap_id not in mappool:
                continue
            mappool_id = mappool[beatmap_id]

            # Only used for 1v1
            score1 = game_scores[0]
            score2 = game_scores[1]
            user_id1 = score1['user_id']
            user_id2 = score2['user_id']

            player1_score = int(score1['score'])
            player2_score = int(score2['score'])

            # Mod recalculation if necessary
            free_mod = 'FM' in mappool_id
            if free_mod:
                player1_mods = osu.get_mods(score1['enabled_mods'], separate=False)
                player2_mods = osu.get_mods(score2['enabled_mods'], separate=False)
                player1_score = osu.mod_recalculate(player1_score, player1_mods)
                player2_score = osu.mod_recalculate(player2_score, player2_mods)

            # Cache usernames
            if user_id1 not in player_scores:
                player_scores[user_id1] = 0
                player_scores[user_id2] = 0
                user_ids[user_id1] = osu.get_user_data(user_id1)['username']
                user_ids[user_id2] = osu.get_user_data(user_id2)['username']

            if player1_score > player2_score:
                player_scores[user_id1] += 1
            else:
                player_scores[user_id2] += 1

            beatmap_data = osu.get_beatmap_data(beatmap_id)

            # Store round data
            beatmap_title = f'{mappool_id}: _{beatmap_data["artist"]} - {beatmap_data["title"]}_'
            match_scores.append([beatmap_title, user_id1, player1_score, user_id2, player2_score])

        # Highlight the higher final score in bold
        player1_id = list(user_ids.keys())[0]
        player2_id = list(user_ids.keys())[1]
        if player_scores[player1_id] > player_scores[player2_id]:
            final_score = f'**{user_ids[player1_id]} {player_scores[player1_id]}** | ' \
                          f'{player_scores[player2_id]} {user_ids[player2_id]}'
        else:
            final_score = f'{user_ids[player1_id]} {player_scores[player1_id]} | ' \
                          f'**{player_scores[player2_id]} {user_ids[player2_id]}**'

        embed = discord.Embed(
            title=match_title,
            url=match_link,
            colour=discord.Colour.magenta(),
            description=final_score
        )

        for score in match_scores:
            beatmap_title = score[0]
            player1_name = user_ids[score[1]]
            player1_score = int(score[2])
            player2_name = user_ids[score[3]]
            player2_score = int(score[4])

            # Highlight each highest score in bold
            if player1_score > player2_score:
                value_score = f'**{player1_name} {player1_score:,}** | {player2_score:,} {player2_name}'
            else:
                value_score = f'{player1_name} {player1_score:,} | **{player2_score:,} {player2_name}**'

            embed.add_field(name=beatmap_title, value=value_score, inline=False)

        # Thumbnail = "The" Logo
        thumbnail = 'https://cdn.discordapp.com/attachments/734824448137625731/734824581080285265/TheLogoFinal.png'
        embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=comments)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(TTT(client))
