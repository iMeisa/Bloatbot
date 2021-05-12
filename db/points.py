import sqlite3


def connect():
    return sqlite3.connect('db/osu.db').cursor()


def add_user(discord_id):
    """
    Adds non existing discord user

    :param discord_id: Discord ID `str`
    """

    cursor = connect()
    cursor.execute(f'SELECT * FROM point_data WHERE discord_id = {discord_id}')
    
    exists = cursor.fetchone() is not None
    
    if not exists:
        cursor.execute(f'INSERT INTO point_data (discord_id, points) VALUES ({discord_id}, 0)')
        cursor.connection.commit()

    cursor.close()


def update_points(discord_id, miss_count, count_50, count_100, count_300, play_date):
    """
    Update points when *r command is used based on circle count

    :param discord_id: Discord ID `str`
    :param miss_count: Miss count `int`
    :param count_50: 50 count `int`
    :param count_100: 100 count `int`
    :param count_300: 300 count `int`
    :param play_date: Date the play was submitted `str`
    """

    point_difference = count_50 + (count_100*2) + ((count_300-miss_count)*6)
    point_difference = point_difference if point_difference > 0 else 0

    add_user(discord_id)

    cursor = connect()

    # Check play date so same play doesn't give more points
    cursor.execute(f'SELECT last_play_date FROM point_data WHERE discord_id = {discord_id}')
    already_submitted = cursor.fetchone()[0] == play_date

    if already_submitted:
        return

    cursor.execute(f"UPDATE point_data SET points = points + {point_difference}, last_play_date = '{play_date}' "
                   f"WHERE discord_id = {discord_id}")
    cursor.connection.commit()


def change_points(discord_id, amount):
    """
    Modifies points amount of discord user

    :param discord_id: Discord ID `str`
    :param amount: Amount of points to change `int`
    """

    add_user(discord_id)

    cursor = connect()
    cursor.execute(f'UPDATE point_data SET points = points + {amount} WHERE discord_id = {discord_id}')

    cursor.connection.commit()


def get_points(discord_id):
    """
    Retrieves points from discord user

    :param discord_id: Discord ID `str`
    :return: Point amount `int`
    """

    cursor = connect()
    cursor.execute(f'SELECT points FROM point_data WHERE discord_id = {discord_id}')

    point_total = cursor.fetchone()

    if point_total is None:
        return None

    return point_total[0]


def get_points_htl():
    """
    Gives point totals sorted high to low

    :return: Points high to low `list`
    """

    cursor = connect()
    cursor.execute('SELECT discord_id, points FROM point_data ORDER BY points DESC')

    return cursor.fetchall()
