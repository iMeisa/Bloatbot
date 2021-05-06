from datetime import datetime


def get_time_diff(time_origin):
    fmt = '%Y-%m-%d %H:%M:%S'
    time_now = datetime.utcnow().strftime(fmt)
    time_diff = datetime.strptime(time_now, fmt) - datetime.strptime(time_origin, fmt)

    if time_diff.days < 1:
        if time_diff.seconds >= 3600:
            hours = time_diff.seconds // 3600
            if hours >= 2:
                return f'{hours} hours ago'
            else:
                return '1 hour ago'
        elif time_diff.seconds >= 60:
            minutes = time_diff.seconds // 60
            if minutes >= 2:
                return f'{minutes} minutes ago'
            else:
                return '1 minute ago'
        else:
            if time_diff.seconds >= 2:
                return f'{time_diff.seconds} seconds ago'
            else:
                return '1 second ago'
    else:
        if time_diff.days >= 365:
            years = time_diff.days // 365
            if years >= 2:
                return f'{years} years ago'
            else:
                return '1 year ago'
        elif time_diff.days >= 30:
            months = time_diff.days // 30
            if months >= 2:
                return f'{months} months ago'
            else:
                return '1 month ago'
        else:
            if time_diff.days >= 2:
                return f'{time_diff.days} days ago'
            else:
                return '1 day ago'


def sec_to_min(seconds_raw):
    seconds = int(seconds_raw)
    minutes = seconds // 60
    seconds = seconds - (minutes * 60)
    if seconds < 10:
        seconds = '0' + str(seconds)
    return f'{minutes}:{seconds}'

