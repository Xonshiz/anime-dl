#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from urllib.parse import urlparse
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
import sites
from re import match
from sys import exit


class AnimeDL(object):

    def __init__(self, url, username, password, resolution, language):

        website = str(self.honcho(url=url[0]))

        if website == "Crunchyroll":
            if not url[0] or not username[0] or not password[0]:
                print("Please enter the required arguments. Run __main__.py --help")
                exit()
            else:

                sites.crunchyroll.CrunchyRoll(
                    url=url[0], password=password, username=username, resolution=resolution, language=language)

    def honcho(self, url):
        # print("Got url : %s" % url)
        # Verify that we have a sane url and return which website it belongs
        # to.
        domain = urlparse(url).netloc
        # print(domain)

        if domain in ["www.funimation.com", "funimation.com"]:
            sites.funimation.Funimation()

        elif domain in ["www.crunchyroll.com", "crunchyroll.com"]:
            return "Crunchyroll"
