from bs4 import BeautifulSoup as bs

from util.util import lprint
from work.chapter import Chapter

def parse_multi_tags(tags):
    comma_tags = ""
    for tag in tags:
        comma_tags += tag + ","
    return comma_tags


def parse_descr(description, tag):
    # remove html tag from string
    description = str(description)
    if description.startswith(tag) and description.endswith(tag[0] + '/' + tag[1:]):
        description = description[len(tag):-(len(tag) + 1)]
    return description


def parse_genres(genre_text):
    genres = genre_text.split('/')
    corrected_genres = []
    for genre in genres:
        if genre == 'Hurt':
            corrected_genres.append('Hurt/Comfort')
        elif genre == 'Comfort':
            continue
        else:
            corrected_genres.append(genre)
    return corrected_genres


def parse_rating(rating):
    if rating == "Fiction K" or rating == "Fiction K+" or rating == "K" or rating == "K+":
        return "General Audiences"
    if rating == "Fiction T" or rating == "T":
        return "Teen And Up Audiences"
    if rating == "Fiction M" or rating == "M":
        return "Mature"

def parse_story_html(download_html_content, num_chapters, work_title):
    soup = bs(download_html_content, "html.parser")
    chapters = []
    for i in range(1, num_chapters + 1):
        chapters.append(parse_chapter_html(work_title=work_title, ch_num=i,
                                           soup=soup, download_html_content=download_html_content))
    return chapters

def parse_chapter_html(work_title, ch_num, soup=None, download_html_content=None):
    soup = soup if soup is not None else bs(download_html_content, "html.parser")

    title = parse_descr(soup.find_all('h2')[ch_num], '<h2>')
    result = soup.find('div', {"id": f'chap_{ch_num}'})
    content = result.find_all('p')[1:]
    content = ''.join(map(str, content[0:]))

    chapter = Chapter(work=work_title, title=title, content=content, serial=ch_num)
    lprint(f'Chapter {ch_num} retrieved')
    return chapter

def parse_fandoms(crossover, raw_fandom):
    if not crossover: return [raw_fandom]
    else: return raw_fandom[:-10].split(" + ")

