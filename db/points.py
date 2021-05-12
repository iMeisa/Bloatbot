import sqlite3


def connect():
    return sqlite3.connect('db/osu.db').cursor()


def add_user(discord_id):
    cursor = connect()
    cursor.execute(f'SELECT * FROM points WHERE discord_id = {discord_id}')
    
    exists = cursor.fetchone() is not None
    
    if not exists:
        cursor.execute(f'INSERT INTO points (discord_id, points) VALUES ({discord_id}, 0)')
        cursor.connection.commit()

    cursor.close()


def update_points(discord_id, miss_count, count_50, count_100, count_300, play_date):
    point_difference = count_50 + (count_100*2) + ((count_300-miss_count)*6)
    point_difference = point_difference if point_difference > 0 else 0

    add_user(discord_id)

    cursor = connect()
    cursor.execute(f'SELECT points FROM points WHERE discord_id = {discord_id}')
    user_points = int(cursor.fetchone()[0])

    # Check play date so same play doesn't give more points
    cursor.execute(f'SELECT last_play_date FROM points WHERE discord_id = {discord_id}')
    already_submitted = cursor.fetchone()[0] == play_date

    if already_submitted:
        return

    cursor.execute(f"UPDATE points SET points = {user_points + point_difference}, last_play_date = '{play_date}' "
                   f"WHERE discord_id = {discord_id}")
    cursor.connection.commit()


def change_points(discord_id, amount):
    add_user(discord_id)

    cursor = connect()
    cursor.execute(f'UPDATE points SET points = points + {amount} WHERE discord_id = {discord_id}')

    cursor.connection.commit()


def get_points(discord_id):
    cursor = connect()
    cursor.execute(f'SELECT points FROM points WHERE discord_id = {discord_id}')

    point_total = cursor.fetchone()

    if point_total is None:
        return None

    return point_total[0]


def get_points_htl():
    cursor = connect()
    cursor.execute('select discord_id, points from points order by points DESC')

    return cursor.fetchall()
