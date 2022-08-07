try:
    from urllib.parse import unquote_plus
except ImportError:
    from urllib import unquote_plus
import re
from bs4 import BeautifulSoup, Tag
import cloudscraper

base_url = 'http://fanfiction.net'
parser = "html.parser"
# success = False
NOT_FOUND = "Attention Required! | Cloudflare"


def scrape(link):
    found = False
    while not found:
        scraper = cloudscraper.CloudScraper()
        soup = BeautifulSoup(scraper.get(link).text, parser)
        if soup is not None:
            if "Attention Required" not in soup.find("title").text:
                found = True
    return soup

def display_works(query):
    if "/" in query:
        url = query
    else:
        url = "https://www.fanfiction.net/~" + query

    soup = scrape(url)
    div_tag = soup.find("div", {"id": "st_inside"})

    titles = []
    urls = []

    # getting list of works
    if div_tag is not None:
        for tag in div_tag:
            if isinstance(tag, Tag):
                title = tag.find('a', {"class": "stitle"}).text
                titles.append(title)
                link = tag.find('a', href=True)
                urls.append(base_url + link['href'])
            else:
                pass

    works = {}
    # title: url
    for i, title in enumerate(titles):
        works[2 * i] = titles[i]
        works[2 * i + 1] = urls[i]

    return works


def select_work(num, title, link):
    """
    print("\n\nSelect work from %i to %i to move to AO3:\n" % (1, len(titles)))
    work = int(input()) - 1
    while work > len(titles) or work < 0:
        print("please enter a valid entry index number.\n")
        work = int(input())
    
    # transfer to work content function
    title = titles[work]
    link = urls[work]
    """

    print("Story to be transfered -----")
    print("story title: " + title)
    print("story link: " + link)
    print("----------------------------")
    meta = scrape_story_metadata(link)
    
    # get_work_content(title, link, meta)

    return link


def get_chapter_count(link):
    count = 1
    soup = scrape(link)

    parent = soup.find("select", {"title": "Chapter Navigation"})
    if parent is not None:
        children = parent.findAll("option")
        for child in children:
            count = child['value']
    return int(count)


def get_work_content(title, link):
    baseURL = '/tmp/'
    update_link = link.split('/')
    ch_ct = get_chapter_count(link)
    print("getting a total of %i chapters..." % ch_ct)
    fullWork = {}
    for i in range(1, ch_ct + 1):
        print("IN")
        chnm = str(i)
        update_link[5] = chnm
        new_link = '/'.join(update_link)

        soup = scrape(new_link)
        whole = soup.find("div", {"id": "storytext"})
        all_tags = whole.findAll("p")

        work = ""
        #with open(baseURL + title + chnm + ".txt", "w", encoding='utf-8') as writer:
        for tag in all_tags:
            if isinstance(tag, Tag):
                work += "\t" + str(tag) + "\n"
                # writer.write("\t" + str(tag) + "\n")
            else:
                pass
        fullWork[i] = work # CH 1 ~ n : WORKSTRING
        # writer.close()
    return fullWork


def get_genres(genre_text):
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


def scrape_story_metadata(url):
    """
    Returns a dictionary with the metadata for the story.
    Attributes:
        -id: the id of the story
        -canon_type: the type of canon
        -canon: the name of the canon
        -author_id: the user id of the author
        -title: the title of the story
        -updated: the timestamp of the last time the story was updated
        -published: the timestamp of when the story was originally published
        -lang: the language the story is written in
        -genres: a list of the genres that the author categorized the story as
        -summary: summary of work by author
        -num_reviews
        -num_favs
        -num_follows
        -num_words: total number of words in all chapters of the story
        -rated: the story's rating
        -chapters: num of chapters
    """
    url_content = url.split('/')
    story_id = url_content[4]
    soup = scrape(url)

    # find fandom
    lc_bar = soup.find('span', {"class": "lc-left"}).find_all("a")
    fandom = lc_bar[1].text

    psl_whole = soup.find('span', {"class": "xgray xcontrast_txt"})
    pre_story_links = psl_whole.find_all('a')

    # get author id, title, and timestamp and genre
    author_id = int(re.search(r"var userid = (.*);", str(soup)).groups()[0])
    title = re.search(r"var title = (.*);", str(soup)).groups()[0]
    title = unquote_plus(title)[1:-1]
    metadata_div = soup.find(id='profile_top')
    times = metadata_div.find_all(attrs={'data-xutime': True})

    # one chapter stories have no updated time
    if len(times) == 1:
        published = int(times[0]['data-xutime'])
    else:
        published = int(times[1]['data-xutime'])

    metadata_text = metadata_div.find(class_='xgray xcontrast_txt').text
    metadata_parts = metadata_text.split('-')
    genres = get_genres(metadata_parts[2].strip())

    # get summary
    summary = soup.find('div', {'style':"margin-top:2px", 'class':"xcontrast_txt"}).text

    # put into metadata collection
    print("Getting metadata...")
    metadata = {
        'id': story_id,
        'fandom': fandom,
        'rated': pre_story_links[0].text,
        'review': pre_story_links[1].text,
        'author_id': author_id,
        'title': title,
        'updated': int(times[0]['data-xutime']),
        'published': published,
        'lang': metadata_parts[1].strip(),
        'genres': genres,
        'summary': summary,
        'chapters': get_chapter_count(url)
    }
    for parts in metadata_parts:
        parts = parts.strip()
        tag_and_val = parts.split(':')
        if len(tag_and_val) != 2:
            continue
        tag, val = tag_and_val
        tag = tag.strip().lower()
        if tag not in metadata:
            val = val.strip()
            try:
                val = int(val.replace(',', ''))
                metadata['num_' + tag] = val
            except:
                metadata[tag] = val
    if 'status' not in metadata:
        metadata['status'] = 'Incomplete'

    return metadata


if __name__ == "__main__":
    print(display_works("Kadrian"))
