from bs4 import BeautifulSoup
import re


class Vrv(object):
    def __init__(self, url, password, username, resolution):
        self.web_page_downloader(url, username, password)

    def web_page_downloader(self, url, username, password):
        # Make a function to fetch the webpage.
        with open("episode.html", "r") as rf:
            page_source = rf.read()
        clean_html = str(BeautifulSoup(page_source, "html.parser"))
        # print(clean_html)
        key_pair_id = re.search(r'Key-Pair-Id=(.*?)"', clean_html).group(1)
        print(key_pair_id)
        policy = re.search(r'Policy=(.*?)&amp;Key-Pair-Id=', clean_html).group(1)
        print(policy)