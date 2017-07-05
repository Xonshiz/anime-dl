#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cfscrape import create_scraper
from requests import session
from tqdm import tqdm




class downloader(object):

    def File_Downloader(self, ddl, fileName, referer, cookies):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Territory': 'US',
            'Referer': referer
        }

        sess = session()
        sess = create_scraper(sess)

        dlr = sess.get(ddl, stream=True, cookies = cookies, headers = headers)  # Downloading the content using python.
        with open(fileName, "wb") as handle:
            for data in tqdm(dlr.iter_content(chunk_size=1024)):  # Added chunk size to speed up the downloads
                handle.write(data)
        print("Download has been completed.")  # Viola

    # coding: utf8
