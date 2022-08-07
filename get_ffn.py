try:
    from urllib.parse import unquote_plus
except ImportError:
    from urllib import unquote_plus
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import TextUtils, unix
import time

base_url = 'http://fanfiction.net'
parser = "html.parser"


def scrape(link):
    options = uc.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(options=options, version_main=103)
    driver.get(link)

    return driver


def scrape_headless(link):
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument('--headless')
    driver = uc.Chrome(options=options, version_main=103)
    driver.get(link)

    return driver


def display_works(query):
    if "/" in query:
        url = query
    else:
        url = "https://www.fanfiction.net/~" + query

    try:
        driver = scrape_headless(url)
        elements = driver.find_elements(By.XPATH, "//div[@id='st_inside']/div[@class='z-list mystories']")
    except NoSuchElementException:
        driver = scrape(url)
        time.sleep(3)
        elements = driver.find_elements(By.XPATH, "//div[@id='st_inside']/div[@class='z-list mystories']")

    works = {}
    for i, element in enumerate(elements):
        works[i] = get_metadata(element)

    return works


def get_metadata(element):
    story_id = element.get_attribute('data-storyid')
    title = TextUtils.clean(element.get_attribute('data-title').strip())
    url = element.find_element(By.XPATH, ".//a").get_attribute('href').strip()
    fandom = TextUtils.clean(element.get_attribute('data-category').strip())
    chapters = element.get_attribute('data-chapters')
    word_count = element.get_attribute('data-wordcount')
    submit_date = unix.am(element.get_attribute('data-datesubmit').strip())
    summary = TextUtils.clean(element.find_element(By.XPATH, "./div[@class='z-indent z-padtop']").get_attribute('innerHTML').strip().split('<div class="z-padtop2 xgray">')[0])

    metadata_bar = element.find_element(By.XPATH, "./div[@class='z-indent z-padtop']/*[1]").get_attribute('innerHTML').strip().split(' - ')
    rating = metadata_bar[1].split(": ")[1]
    lang = metadata_bar[2]
    genre = get_genres(metadata_bar[3])

    if metadata_bar[len(metadata_bar) - 1] == 'Complete':
        if '</span>' in metadata_bar[len(metadata_bar) - 2]:
            characters = []
        else:
            characters = metadata_bar[len(metadata_bar) - 2].split(', ')
    elif '</span>' in metadata_bar[len(metadata_bar) - 1]:
        characters = []
    else:
        characters = metadata_bar[len(metadata_bar) - 1].split(', ')

    if element.get_attribute('data-statusid') == '2':
        status = "Complete"
    else:
        status = "Incomplete"

    metadata = {
        "title": title,
        "url": url,
        "chapters": chapters,
        "fandom": fandom,
        "submit_date": submit_date,
        "status": status,
        "summary": summary,
        "word_count": word_count,
        "story_id": story_id,
        "rated": rating,
        "lang": lang,
        "genres": genre,
        "characters": characters,
    }

    return metadata


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


def get_chapter_count(link):
    count = 1
    soup = scrape(link)

    parent = soup.find("select", {"title": "Chapter Navigation"})
    if parent is not None:
        children = parent.findAll("option")
        for child in children:
            count = child['value']
    return int(count)


def get_chapter_content(link):
    content = ""
    try:
        driver = scrape_headless(link)
        content = driver.find_element(By.XPATH, "//div[@id='storytext']").get_attribute('innerHTML')
        success = True
    except NoSuchElementException:
        success = False
        while not success:
            try:
                driver = scrape(link)
                time.sleep(5)
                content = driver.find_element(By.XPATH, "//div[@id='storytext']").get_attribute('innerHTML')
                success = True
            except NoSuchElementException:
                print("Unsuccessful. Trying again")

    return content


def get_work_content(work, link):
    print(link)
    update_link = link.split('/')
    ch_ct = int(work['chapters'])
    print("getting a total of %i chapters..." % ch_ct)
    full_work = {}
    for i in range(1, ch_ct + 1):
        chnm = str(i)
        update_link[5] = chnm
        new_link = '/'.join(update_link)

        success = False
        try:
            driver = scrape_headless(new_link)
            content = driver.find_element(By.XPATH, "//div[@id='storytext']").get_attribute('innerHTML')
            success = True
        except NoSuchElementException:
            while not success:
                try:
                    driver = scrape(new_link)
                    time.sleep(3)
                    content = driver.find_element(By.XPATH, "//div[@id='storytext']").get_attribute('innerHTML')
                    success = True
                except NoSuchElementException:
                    time.sleep(10)  # sorry

        full_work[i] = content

    return full_work


def fancy_print(works):
    for id, work in works.items():
        print(id, work['title'])
        for name, value in work.items():
            print("\t", name, ": ", value)


