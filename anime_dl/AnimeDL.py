#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from urllib.parse import urlparse
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
import anime_dl.sites
from re import match


class AnimeDL(object):

    def __init__(self, url, username, password, resolution, language):

        website = str(self.honcho(url=url[0]))

        if website == "Crunchyroll":
            if not url[0] or not username[0] or not password[0]:
                print("Please enter the required arguments. Run __main__.py --help")
                exit()
            else:
                Crunchy_Show_regex = r'https?://(?:(?P<prefix>www|m)\.)?(?P<url>crunchyroll\.com/(?!(?:news|anime-news|library|forum|launchcalendar|lineup|store|comics|freetrial|login))(?P<id>[\w\-]+))/?(?:\?|$)'
                Crunchy_Video_regex = r'https?:\/\/(?:(?P<prefix>www|m)\.)?(?P<url>crunchyroll\.(?:com|fr)/(?:media(?:-|/\?id=)|[^/]*/[^/?&]*?)(?P<video_id>[0-9]+))(?:[/?&]|$)'
                Crunchy_Show = match(Crunchy_Show_regex, url[0])
                Crunchy_Video = match(Crunchy_Video_regex, url[0])
                if Crunchy_Video:
                    anime_dl.sites.crunchyroll.CrunchyRoll(
                        url=url[0], password=password, username=username, resolution=resolution)
                elif Crunchy_Show:
                    anime_dl.sites.crunchywhole.crunchyRollWhole()

    def honcho(self, url):
        # print("Got url : %s" % url)
        # Verify that we have a sane url and return which website it belongs
        # to.
        domain = urlparse(url).netloc
        # print(domain)

        if domain in ["www.funimation.com", "funimation.com"]:
            anime_dl.sites.funimation.Funimation()

        elif domain in ["www.crunchyroll.com", "crunchyroll.com"]:
            return "Crunchyroll"
