from curl_cffi.requests import Session
from bs4 import BeautifulSoup
import TextUtils, unix

BASE_URL = 'https://www.fanfiction.net'
_SKIP = ('Chapters:', 'Words:', 'Reviews:', 'Favs:', 'Follows:', 'Published:', 'Updated:', 'Rated:')

_scraper = Session(impersonate='chrome')


def display_works(query):
    if '/' in query:
        url = query
    else:
        url = f'{BASE_URL}/~{query}'

    response = _scraper.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    st = soup.find('div', {'id': 'st_inside'})
    if not st:
        return {}

    works = {}
    for i, element in enumerate(st.find_all('div', class_='mystories')):
        works[i] = get_metadata(element)
    return works


def get_metadata(element):
    story_id = element.get('data-storyid')
    title = TextUtils.clean(element.get('data-title', '').strip())
    fandom = TextUtils.clean(element.get('data-category', '').strip())
    chapters = element.get('data-chapters')
    word_count = element.get('data-wordcount')
    submit_date = unix.am(element.get('data-datesubmit', '0').strip())
    status = 'Complete' if element.get('data-statusid') == '2' else 'Incomplete'

    a_tag = element.find('a')
    url = BASE_URL + a_tag['href'] if a_tag else ''

    indent = element.find('div', class_='z-indent')
    xgray = indent.find('div', class_='xgray') if indent else None
    meta_text = xgray.get_text() if xgray else ''
    if xgray:
        xgray.extract()
    summary = TextUtils.clean(indent.get_text(strip=True)) if indent else ''

    parts = [p.strip() for p in meta_text.split(' - ')]
    rating = next((p.split(': ')[1] for p in parts if p.startswith('Rated:')), '')
    info = [p for p in parts if p and not any(p.startswith(k) for k in _SKIP)]
    lang = info[1] if len(info) > 1 else ''
    genre = get_genres(info[2]) if len(info) > 2 else []
    characters = [p for p in info[3:] if p != 'Complete']

    return {
        'title': title,
        'url': url,
        'chapters': chapters,
        'fandom': fandom,
        'submit_date': submit_date,
        'status': status,
        'summary': summary,
        'word_count': word_count,
        'story_id': story_id,
        'rated': rating,
        'lang': lang,
        'genres': genre,
        'characters': characters,
    }


def get_genres(genre_text):
    genres = genre_text.split('/')
    corrected = []
    for genre in genres:
        if genre == 'Hurt':
            corrected.append('Hurt/Comfort')
        elif genre == 'Comfort':
            continue
        else:
            corrected.append(genre)
    return corrected


if __name__ == '__main__':
    import sys
    works = display_works(sys.argv[1])
    for i, work in works.items():
        print(i, work['title'])
        for k, v in work.items():
            print('\t', k, ':', v)
