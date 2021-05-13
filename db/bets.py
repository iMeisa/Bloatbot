import sqlite3

from db.points import get_points, change_points


def _connect_():
    cursor = sqlite3.connect('db/bets.db').cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS active_bets (channel_id text, team1 text, team2 text)')
    cursor.connection.commit()
    return cursor


def check_bets(channel_id):
    """
    Checks for bets on given channel

    :param channel_id: Channel ID `str`
    :return: Teams of bet `tuple`
    """

    cursor = _connect_()
    cursor.execute(f'SELECT team1, team2 FROM active_bets WHERE channel_id = {channel_id}')

    active_bet = cursor.fetchone()
    return active_bet


def check_player_bets(channel_id, discord_id):
    """
    Checks for currently placed bets by users

    :param channel_id: Channel ID `str`
    :param discord_id: Discord ID `str`
    :return: (bet amount, selected team) `tuple`
    """

    cursor = _connect_()
    cursor.execute(f'SELECT bet_amount, selected_team FROM bet_{channel_id} WHERE discord_id = {discord_id}')

    active_bet = cursor.fetchone()
    return active_bet


def check_users_participating(channel_id):
    """
    Gives list of users currently participating in channel bet

    :param channel_id: Channel ID `str`
    :return: Discord IDs `list` of `tuple`
    """

    cursor = _connect_()
    cursor.execute(f'SELECT discord_id FROM bet_{channel_id}')

    discord_ids = cursor.fetchall()
    return discord_ids
    

def open_bet(channel_id, team1, team2):
    """
    Creates new channel bet

    Returns active channel bet if one already exists (team 1, team 2) `tuple`

    :param channel_id: Channel ID `str`
    :param team1: Team 1 name `str`
    :param team2: Team 2 name `str`
    :return: `None` if success
    """

    cursor = _connect_()
    active_bet = check_bets(channel_id)
    if active_bet is not None:
        return active_bet

    cursor.execute(f"INSERT INTO active_bets (channel_id, team1, team2) "
                   f"VALUES ({channel_id}, '{team1}', '{team2}')")
    cursor.execute(f"CREATE TABLE bet_{channel_id} (discord_id text, bet_amount integer, selected_team text)")
    cursor.connection.commit()

    return None


def close_bet(channel_id, winning_team):
    """
    Closes active bet on channel

    :param channel_id: Channel ID `str`
    :param winning_team: Winning team name `str`
    :return: Response `str`
    """

    cursor = _connect_()

    active_bets = check_bets(channel_id)
    if active_bets is None:
        return 'No bets to close'

    if winning_team is not None:
        if winning_team not in active_bets:
            return 'Invalid team'

        cursor.execute(f"SELECT discord_id, bet_amount FROM bet_{channel_id} WHERE selected_team = '{winning_team}'")

        winners = cursor.fetchall()
        for winner in winners:
            winner_id = winner[0]
            winner_bet = winner[1]
            change_points(winner_id, winner_bet*2)

    cursor.execute(f'DROP TABLE bet_{channel_id}')
    cursor.execute(f'DELETE FROM active_bets WHERE channel_id = {channel_id}')
    cursor.connection.commit()

    if winning_team is None:
        return 'Bet deleted'

    return f'{winning_team} wins!'


def add_bet(channel_id, discord_id, bet_amount, selected_team):
    """
    Adds user to current channel bet

    Returns error message if applicable `str`

    :param channel_id: Channel ID `str`
    :param discord_id: Discord ID `str`
    :param bet_amount: Bet amount `int`
    :param selected_team: Team rooting for `str`
    :return: None
    """

    cursor = _connect_()

    active_bet = check_bets(channel_id)
    if active_bet is None:
        return 'No active bets on this channel rn, make a bet using *makebet `[team 1]` vs `[team 2]`'

    active_player_bet = check_player_bets(channel_id, discord_id)
    if active_player_bet is not None and (bet_amount is None or selected_team is None):
        bet_amount = active_player_bet[0]
        bet_team = active_player_bet[1]
        return f'You already bet `{bet_amount}` on `{bet_team}`'
    elif active_player_bet is None and (bet_amount is None or selected_team is None):
        return f'Use format *bet `[bet amount]` `[team]`'

    if selected_team not in active_bet:
        return 'Who tf is that team?'

    user_points = get_points(discord_id)
    if user_points < bet_amount:
        return f'You only have {user_points} circles'

    cursor.execute(f"INSERT INTO bet_{channel_id} VALUES ({discord_id}, {bet_amount}, '{selected_team}')")
    cursor.connection.commit()

    change_points(discord_id, -bet_amount)

    return None
