import re
import time
from bs4 import BeautifulSoup
from curl_cffi.requests import Session
from datetime import datetime as dt

from util import parser
from util.util import lprint


class AO3Session:
    _ARCHIVE_URL = "https://archiveofourown.org"
    _LOGIN_URL = f"{_ARCHIVE_URL}/users/login"
    _LANGUAGE_EN = '1'

    username = ""
    password = ""
    logged_in = False

    def __init__(self, username, password, status_callback=None):
        self.username = username
        self.password = password
        self.DASHBOARD_URL = f"{self._ARCHIVE_URL}/users/{self.username}"
        self._session = Session(impersonate="chrome")
        self._emit = status_callback or (lambda msg: None)

    def _status(self, msg):
        lprint(msg)
        self._emit(msg)

    def new_session(self):
        self._status("Logging into AO3...")
        login_page = self._session.get(self._LOGIN_URL)
        login_page.raise_for_status()

        soup = BeautifulSoup(login_page.text, 'html.parser')
        token_el = soup.find('input', {'name': 'authenticity_token'})
        if not token_el:
            raise Exception('Could not find CSRF token on AO3 login page')
        token = token_el['value']

        resp = self._session.post(self._LOGIN_URL, data={
            'authenticity_token': token,
            'user[login]': self.username,
            'user[password]': self.password,
            'commit': 'Log in',
        }, allow_redirects=True)

        if 'login' in resp.url or 'auth_error' in resp.url:
            raise Exception('AO3 login failed — check username/password')

        self.logged_in = True
        self._status("Logged into AO3 successfully.")

    def _parse_form(self, page_html):
        soup = BeautifulSoup(page_html, 'html.parser')
        token_el = soup.find('input', {'name': 'authenticity_token'})
        if not token_el:
            raise Exception('Could not find CSRF token')
        token = token_el['value']

        pseud_id = None
        # Multi-pseud accounts show a select; single-pseud accounts may use a hidden input or nothing.
        pseud_sel = soup.find('select', {'name': 'work[author_attributes][ids][]'})
        if pseud_sel:
            opt = pseud_sel.find('option', selected=True) or pseud_sel.find('option')
            if opt:
                pseud_id = opt['value']
        else:
            hidden = soup.find('input', {'type': 'hidden', 'name': 'work[author_attributes][ids][]'})
            if hidden and hidden.get('value'):
                pseud_id = hidden['value']

        return token, pseud_id

    def _get_token(self, page_html):
        token, _ = self._parse_form(page_html)
        return token

    def _new_chapter(self, work_url, story, chapter_num):
        chapter = story.get_chapter(chapter_num)
        new_ch_url = f'{work_url}/chapters/new'

        page = self._session.get(new_ch_url)
        page.raise_for_status()
        token = self._get_token(page.text)

        data = {
            'authenticity_token': token,
            'chapter[title]': chapter.title or '',
            'chapter[content]': chapter.content or '',
            'chapter[position]': str(chapter_num),
            'post_without_preview_button': 'Post',
        }
        resp = self._session.post(f'{work_url}/chapters', data=data, allow_redirects=True)
        resp.raise_for_status()
        self._status(f"Posted chapter {chapter_num}.")

    def new_story(self, work):
        if not work.f_cached:
            raise Exception('No story found.')

        new_work_url = f"{self._ARCHIVE_URL}/works/new"
        page = self._session.get(new_work_url)
        page.raise_for_status()
        token, pseud_id = self._parse_form(page.text)

        self._status("Submitting work to AO3...")

        meta = work.work_meta
        num_chapters = meta.get('chapters', 1)
        if isinstance(num_chapters, str):
            num_chapters = int(num_chapters)

        ch1 = work.get_chapter(1)

        rating_str = meta.get('rating', 'Not Rated')
        fandoms = parser.parse_multi_tags(meta.get('fandoms', []))
        tags = parser.parse_multi_tags(meta.get('tags', []))

        data = {
            'authenticity_token': token,
            'work[rating_string]': rating_str,
            'work[archive_warning_strings][]': 'No Archive Warnings Apply',
            'work[fandom_string]': fandoms,
            'work[category_strings][]': 'Gen',
            'work[freeform_string]': tags,
            'work[title]': meta.get('title', ''),
            'work[summary]': meta.get('summary', ''),
            'work[language_id]': self._LANGUAGE_EN,
            'work[chapter_attributes][content]': ch1.content or '',
            'post_button': 'Post',
        }

        if pseud_id:
            data['work[author_attributes][ids][]'] = pseud_id

        if num_chapters > 1:
            data['work[wip_length]'] = str(num_chapters)
            data['work[chapter_attributes][title]'] = str(ch1.title or '')

        publish_date = meta.get('publish_date', '')
        if publish_date:
            date_obj = dt.utcfromtimestamp(int(publish_date))
            data['work[backdate]'] = '1'
            data['work[chapter_attributes][published_at(3i)]'] = str(date_obj.day)
            data['work[chapter_attributes][published_at(2i)]'] = str(date_obj.month)
            data['work[chapter_attributes][published_at(1i)]'] = str(date_obj.year)

        lprint(f"Posting work data: title={data.get('work[title]')!r}, fandom={data.get('work[fandom_string]')!r}, rating={data.get('work[rating_string]')!r}, pseud={data.get('work[author_attributes][ids][]')!r}")
        resp = self._session.post(f"{self._ARCHIVE_URL}/works", data=data, allow_redirects=True)
        resp.raise_for_status()

        m = re.search(r'(https://archiveofourown\.org/works/\d+)', resp.url)
        if not m:
            soup = BeautifulSoup(resp.text, 'html.parser')
            canonical = soup.find('link', {'rel': 'canonical'})
            if canonical:
                m = re.search(r'(https://archiveofourown\.org/works/\d+)', canonical.get('href', ''))
        if not m:
            soup = BeautifulSoup(resp.text, 'html.parser')
            error_items = soup.select('ul.errors li, .error li, #error_explanation li')
            if error_items:
                errors = '; '.join(e.get_text(strip=True) for e in error_items)
                raise Exception(f'AO3 rejected the work: {errors}')
            raise Exception(f'Could not determine new work URL. Final URL: {resp.url}')

        created_url = m.group(1)
        self._status(f"Posted chapter 1.")

        if num_chapters > 1:
            for i in range(2, num_chapters + 1):
                self._status(f"Posting chapter {i} of {num_chapters}...")
                self._new_chapter(created_url, work, i)
                time.sleep(1)

        return created_url
