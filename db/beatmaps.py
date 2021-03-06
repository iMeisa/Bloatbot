import sqlite3


def _connect_():
    db = sqlite3.connect('db/osu.db')
    cursor = db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS recent_beatmaps (channel_id text, beatmap_id text)')
    cursor.connection.commit()
    return cursor


def get_recent_beatmap(channel_id: str):
    """
    Gives beatmap ID most recently shown in given channel

    :param channel_id: Channel ID `string`
    :return: Beatmap ID `string`
    """

    cursor = _connect_()
    cursor.execute(f"SELECT beatmap_id FROM recent_beatmaps WHERE channel_id = {channel_id}")

    beatmap_id = cursor.fetchone()
    if beatmap_id is not None:
        beatmap_id = beatmap_id[0]

    cursor.close()
    return beatmap_id


def add_channel_id(channel_id: str):
    """
    Adds channel ID to db if ID is not in db
    """

    cursor = _connect_()
    cursor.execute(f"SELECT channel_id FROM recent_beatmaps WHERE channel_id = {channel_id}")

    channels = cursor.fetchone()
    if channels is None:
        cursor.execute(f"INSERT INTO recent_beatmaps (channel_id) VALUES ({channel_id})")
        cursor.connection.commit()

    cursor.close()


def add_recent_beatmap(channel_id: str, beatmap_id: str):
    """
    Update most recently shown beatmap in given channel

    :param channel_id: Channel ID `string`
    :param beatmap_id: Beatmap ID `string`
    """

    cursor = _connect_()
    add_channel_id(channel_id)
    cursor.execute(f"UPDATE recent_beatmaps SET beatmap_id = {beatmap_id} WHERE channel_id = {channel_id}")

    cursor.connection.commit()
    cursor.close()
