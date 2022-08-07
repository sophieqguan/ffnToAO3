
import get_ffn, ratings
import mechanicalsoup
import json


def convert_ffn_to_ao3():
    work_url = get_ffn.select_work()
    return get_ffn.scrape_story_metadata(work_url)


def get_new_work_link(browser, username):
    browser.open("https://archiveofourown.org/users/" + username)
    soup = browser.page()
    work_url = "https://archiveofourown.org"
    for line in soup:
        header = line.find_all('div', {'class': 'header module'})
        if header is not None:
            for h in header:
                element = h.find_all('h4', {'class': 'heading'})
                for e in element:
                    work_url += e.find('a')['href']
                break
        break
    return work_url


def upload_chapter(link, ffn_url, browser, chapter):
    new_ch_url = link + "/chapters/new"
    updated_ffn_url = ffn_url.split('/')
    updated_ffn_url[5] = str(chapter)
    chapter_url = '/'.join(updated_ffn_url)
    print(chapter_url)

    try:
        browser.open(new_ch_url)
        form = browser.select_form('form', 1)
        ch_content = get_ffn.get_chapter_content(chapter_url)
        form.set('chapter[content]', ch_content)
        form.choose_submit("post_without_preview_button")
        browser.submit_selected()
        print("Chapter %i posted." % chapter)
        return 0
    except:
        return 1


def upload(user, ffnmeta):
    print("Heading to AO3...")
    login_url = "https://archiveofourown.org/users/login"
    url = "https://archiveofourown.org/works/new"
    # login information:
    user_info = {
        "user[login]": user['name'],
        "user[password]": user['word'],
    }    
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(login_url)
    form = browser.select_form('form')

    try:
        # login to AO3
        form.set_input(user_info)
        browser.submit_selected()

        browser.open(url)

        # 0 = search-bar form (which we don't want...), 1 = work form
        form = browser.select_form('form', 1)
    except:
        return 1

    # this allows only choosing from a list of works, and not directly via a url
    rating = ratings.convert(ffnmeta['rated'])
    inputs = {
        "fandom": ffnmeta["fandom"],
        "tags": ffnmeta["genres"],
        "title": ffnmeta["title"],
        "summary": ffnmeta["summary"],
        "rating": rating,
        "lang": ffnmeta["lang"],
        "chapters": ffnmeta['chapters']
    }

    # print("transferring metadata and story content...")
    # default to no archive warnings, since ffnet's rating is rather vague
    default_warning = "No Archive Warnings Apply"
    form.set('work[rating_string]', inputs['rating'])
    form.set('work[archive_warning_strings][]', default_warning)
    form.set('work[fandom_string]', inputs['fandom'])
    # default category is Gen (if your work is not gen, you should change it manually)
    form.set('work[category_strings][]', "Gen")
    megatag = ""
    for tag in inputs['tags']:
        megatag += tag + ","
    form.set('work[freeform_string]', megatag)
    form.set('work[title]', inputs['title'])
    form.set('work[summary]', inputs['summary'])
    form.set('work[language_id]', inputs['lang'])

    # post ch1 first
    ch1 = get_ffn.get_chapter_content(ffnmeta['url'])
    form.set('work[chapter_attributes][content]', ch1)
    form.choose_submit("post_button")
    browser.submit_selected()
    # print("Chapter 1 posted.")

    new_work_url = get_new_work_link(browser, user_info['user[login]'])


    # post additional chapters, if exist
    if int(inputs['chapters']) > 1:
        for i in range(2, int(inputs['chapters']) + 1):
            upload_chapter(new_work_url, ffnmeta['url'], browser, i)

    # print('new work: ' + new_work_url)
    # print("Done.")

    return new_work_url
