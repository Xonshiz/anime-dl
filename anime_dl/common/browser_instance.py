#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cfscrape import create_scraper
from requests import session
from bs4 import BeautifulSoup
import re


def page_downloader(url, scrapper_delay=5, **kwargs):
    headers = kwargs.get("headers")
    received_cookies = kwargs.get("cookies")
    if not headers:
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate'
        }

    sess = session()
    sess = create_scraper(sess, delay=scrapper_delay)

    connection = sess.get(url, headers=headers, cookies=received_cookies)

    if connection.status_code != 200:
        print("Whoops! Seems like I can't connect to website.")
        print("It's showing : %s" % connection)
        print("Run this script with the --verbose argument and report the issue along with log file on Github.")
        # raise Warning("can't connect to website %s" % manga_url)
        return False, None, None
    else:
        page_source = BeautifulSoup(connection.text.encode("utf-8"), "html.parser")
        connection_cookies = sess.cookies

        return True, page_source, received_cookies


def login_crunchyroll(url, username, password, country):
    headers = {
        'user-agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referer': 'https://www.crunchyroll.com/login',
        'origin': 'https://www.crunchyroll.com',
        'upgrade-insecure-requests': '1'
    }

    sess = session()
    sess = create_scraper(sess)
    print("Trying to login...")

    initial_page_fetch = sess.get(url='https://www.crunchyroll.com/login', headers=headers)

    if initial_page_fetch.status_code == 200:
        initial_page_source = initial_page_fetch.text.encode("utf-8")
        initial_cookies = sess.cookies
        csrf_token = ""
        try:
            csrf_token = re.search(r'login_form\[_token\]" value="(.*?)"', str(initial_page_source)).group(1)
        except Exception:
            csrf_token = re.search(r'login_form\[_token\]" type="hidden" value="(.*?)"',
                                   str(initial_page_source)).group(1)

        payload = {
            'login_form[name]': '%s' % username,
            'login_form[password]': '%s' % password,
            'login_form[redirect_url]': '/',
            'login_form[_token]': '%s' % csrf_token
        }

        login_post = sess.post(
            url='https://www.crunchyroll.com/login',
            data=payload,
            headers=headers,
            cookies=initial_cookies)

        login_check_response, login_cookies = login_check(html_source=login_post.text.encode('utf-8'), cookies=login_post.cookies)
        if login_check_response:
            print("Logged in successfully...")
            return True, initial_cookies, csrf_token
        else:
            print("Unable to Log you in. Check credentials again.")
            return False, None, None
    else:
        # print("Couldn't connect to the login page...")
        # print("Website returned : %s" % str(initial_page_fetch.status_code))
        return False, None, None


def login_check(html_source, cookies=None):
    # Open the page and check the title. CrunchyRoll redirects the user and the title has the text "Redirecting...".
    # If this is not found, you're probably not logged in and you'll just get 360p or 480p.
    if "href=\"/logout\"" in html_source:
        return True, cookies
    else:
        print("Let me check again...")
        second_try_response, html_source, cookies = page_downloader(url="https://www.crunchyroll.com/", cookies=cookies)
        if second_try_response:
            if "href=\"/logout\"" in html_source:
                return True, cookies
            else:
                return False, cookies
