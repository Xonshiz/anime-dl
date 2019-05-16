#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
import sites
from sys import exit


'''First, the honcho returns the website name and after that, the corresponding methods are called for a particular
website. I don't remember why I added an extra step, I really don't. Oh well, it's working, so let it work.'''


class AnimeDL(object):

    def __init__(self, url, username, password, resolution, language, skipper, logger, episode_range):

        website = str(self.honcho(url=url[0]))

        if website == "Crunchyroll":
            if not url[0] or not username[0] or not password[0]:
                print("Please enter the required arguments. Run __main__.py --help")
                exit()
            else:

                sites.crunchyroll.Crunchyroll(
                    url=url[0], password=password, username=username, resolution=resolution, language=language,
                    skipper=skipper, logger=logger, episode_range=episode_range)

        elif website == "VRV":
            print("Not Implemented")
            exit(1)
            # if not url[0] or not username[0] or not password[0]:
            #     print("Please enter the required arguments. Run __main__.py --help")
            #     exit()
            # else:
            #
            #     sites.vrv.Vrv(url=url, password=password, username=username, resolution=resolution)

        elif website == "Funimation":
            print("Not Implemented")
            exit(1)
            # if not url[0] or not username[0] or not password[0]:
            #     print("Please enter the required arguments. Run __main__.py --help")
            #     exit()
            # else:
            #     sites.funimation.Funimation(url[0], username, password, resolution, language)

    def honcho(self, url):
        # Verify that we have a sane url and return which website it belongs
        # to.

        # Fix for script not responding when www.crunchyrol.com/... type links are given.
        if "https://" in url:
            url = str(url)
        elif "http://" not in url:
            url = "http://" + str(url)

        # if there's not http:/, then netloc is empty.
        # Gotta add the "if crunchyroll in url..."
        # print(url)
        domain = urlparse(url).netloc

        if domain in ["www.funimation.com", "funimation.com"]:
            return "Funimation"

        elif domain in ["www.crunchyroll.com", "crunchyroll.com"]:
            return "Crunchyroll"

        elif domain in ["www.vrv.co", "vrv.co"]:
            return "VRV"