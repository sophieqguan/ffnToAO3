import re
from datetime import datetime as dt

def lprint(info, end="\n"):
    current_time = str(dt.now().strftime("%d %B %Y, %H:%M:%S"))
    msg = f'[{current_time}] {info}'

    print(msg, end=end)

def validate_url(url):
    if bool(re.fullmatch("^https://www.fanfiction.net/s/[0-9]{8}(.*)$", url)):
        return '/'.join(map(str, url.split("/")[:5]))
    elif bool(re.fullmatch('^www.fanfiction.net/s/[0-9]{8}(.*)$', url)):
        return 'https://' + '/'.join(map(str, url.split("/")[:3]))
    elif bool(re.fullmatch('^fanfiction.net/s/[0-9]{8}(.*)$', url)):
        return 'https://www.' + '/'.join(map(str, url.split("/")[:3]))
    elif bool(re.fullmatch("^[0-9]{8}$", url)):
        return f'https://www.fanfiction.net/s/{url}'
    else: return None