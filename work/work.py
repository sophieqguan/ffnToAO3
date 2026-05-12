import requests
from util import parser, api

class Work:
    # class meta
    download_html_url = ""
    download_html_content = ""
    ffn_story_url = ""

    # states
    f_cached = False

    # processed story content
    work_meta = {}
    work_title = "UNTITLED"
    work_id = "NO ID"
    # [@DEPRECATED] chapter objs of entire story content, separated by chapters
    chapters = []

    def __init__(self, url, status_callback=None):
        self.ffn_story_url = url
        self._emit = status_callback or (lambda msg: None)

    def __repr__(self):
        return f"<Work [T: {self.work_title}] [ID: {self.work_id}]]>"
    def _has_work_cached(self):
        return self.f_cached

    def retrieve_content(self):
        self._emit("Fetching story from fanfiction.net...")
        self._api_content_request()
        self._emit(f"Story fetched: \"{self.work_title}\" ({self.work_meta.get('chapters', 1)} chapter(s)).")
        # self._parse_work_html()

    """
    # Do not to use; too many chapters = too much memory
    @Deprecated
    def get_chapters(self):
        return self.chapters if self._has_work_cached() else self._parse_work_html()
    """

    def get_chapter(self, ch_num):
        return parser.parse_chapter_html(download_html_content=self.download_html_content,
                                         work_title=self.work_title,
                                         ch_num=ch_num)

    def _api_content_request(self):
        try:
            # get html download url
            response = requests.get(f'{api.API_REQ_URL}{self.ffn_story_url}')
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise Exception(f'fichub API request failed: {err}')

        self._extract_meta(response.json())  # find download_html_url
        self.download_html_content = api.api_content_request(download_html_url=self.download_html_url)
        self.f_cached = True

    def _parse_work_html(self):
        self.chapters = parser.parse_story_html(self.download_html_content, self.work_meta['chapters'], self.work_title)

    def _extract_meta(self, response):
        # TODO: Tags are comma separated, 100 characters per tag. Fandom, relationship, character,
        #  and additional tags must not add up to more than 75.
        #  Archive warning, category, and rating tags do not count toward this limit.

        self.work_id = response['hashes']['epub']
        self.download_slug = response['slug']
        self.download_html_url = response['html_url']

        meta = response['meta']
        self.work_title = self._gv(meta, 'title')

        self.work_meta['title'] = self.work_title
        self.work_meta['author'] = self._gv(meta, 'author')
        self.work_meta['chapters'] = self._gv(meta, 'chapters')
        self.work_meta['summary'] = parser.parse_descr(self._gv(meta, 'description'), '<p>')
        self.work_meta['status'] = self._gv(meta, 'status')

        if self._gv(meta, 'rawExtendedMeta') == "": return

        extended_meta = meta['rawExtendedMeta']

        self.work_meta['rating'] = parser.parse_rating(self._gv(extended_meta, 'rated'))
        self.work_meta['crossover'] = self._gv(extended_meta, 'crossover')
        self.work_meta['fandoms'] = parser.parse_fandoms(
            self._gv(extended_meta, 'crossover'),
            self._gv(extended_meta, 'raw_fandom'))

        self.work_meta['tags'] = parser.parse_genres(self._gv(extended_meta, 'genres'))
        self.work_meta['language'] = self._gv(extended_meta, 'language')
        self.work_meta['publish_date'] = self._gv(extended_meta, 'published')

    def _gv(self, dict, key):
        return dict[key] if key in dict else ""