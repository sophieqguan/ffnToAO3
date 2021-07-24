
import get_ffn
import ratings
import mechanicalsoup


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

    print("New work url: " + work_url)
    return work_url


def upload_chapters(link, browser, title, ch_ct):
    new_ch_url = link + "/chapters/new"
    for i in range(2, ch_ct + 1):
        browser.open(new_ch_url)
        form = browser.select_form('form', 1)
        ch = open(title + str(i) + ".txt")
        ch_content = ch.read()
        form.set('chapter[content]', ch_content)
        ch.close()
        form.choose_submit("post_without_preview_button")
        browser.submit_selected()
        print("Chapter %i posted." % i)


def upload():
    print("Heading to AO3...")
    login_url = "https://archiveofourown.org/users/login"
    url = "https://archiveofourown.org/works/new"
    # login information:
    user_info = {
        "username": input("Enter your AO3 username: "),
        "password": input("Enter your AO3 password: "),
    }
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(login_url)
    form = browser.select_form('form')

    # login to AO3
    form.set_input({"user[login]": user_info["username"], "user[password]": user_info["password"]})
    browser.submit_selected()
    print("Logged in successfully...")

    browser.open(url)

    # 0 = search-bar form (which we don't want...), 1 = work form
    form = browser.select_form('form', 1)

    # this allows only choosing from a list of works, and not directly via a url
    ffnmeta = convert_ffn_to_ao3()
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

    print("transferring metadata and story content...")
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
    ch1 = open(inputs['title'] + "1.txt")
    form.set('work[chapter_attributes][content]', ch1.read())
    ch1.close()
    form.choose_submit("post_button")
    browser.submit_selected()
    print("Chapter 1 posted.")

    if inputs['chapters'] > 1:
        upload_chapters(get_new_work_link(browser,
                        user_info['username']),
                        browser, inputs['title'],
                        inputs['chapters'])
    print("Done.")


