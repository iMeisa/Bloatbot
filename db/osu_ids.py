import sqlite3


def _connect_():
    cursor = sqlite3.connect('db/osu.db').cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS osu_ids (discord_id text, osu_id text)')
    cursor.connection.commit()
    return cursor


def check_registration(discord_id) -> bool:
    """
    Checks if discord user is linked with an osu! user
    
    :param discord_id: Discord ID of discord user
    :return: `bool` if in db
    """

    cursor = _connect_()
    cursor.execute(f"SELECT * FROM osu_ids WHERE discord_id = {discord_id}")

    ids = cursor.fetchone()

    cursor.close()
    return ids is not None


def register_user(discord_id, osu_id) -> bool:
    """
    Inserts new user into osu_id table
    """
    
    cursor = _connect_()
    cursor.execute(f"INSERT INTO osu_ids VALUES ({discord_id}, {osu_id})")
    cursor.connection.commit()

    return check_registration(discord_id)


def get_registered_user(discord_id):
    """
    Gives osu! id of registered discord user

    Returns None if not registered

    :param discord_id: Discord ID of user `string`
    :return: osu! ID of user `string`
    """

    registered = check_registration(discord_id)
    if not registered:
        return None

    cursor = _connect_()
    cursor.execute(f"SELECT osu_id FROM osu_ids WHERE discord_id = {discord_id}")

    osu_id = cursor.fetchone()[0]
    return osu_id
