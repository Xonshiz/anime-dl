#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cfscrape import create_scraper
from requests import session
from bs4 import BeautifulSoup
import re
from subprocess import call
from time import sleep


class Funimation(object):
    def __init__(self, url, username, password, resolution, language):

        self.cookies = self.login(userUserName = username, userPassword = password)
        # print("Cookies : %s\n\n\nSource : \n%s" % (self.cookies, self.pageSource))
        self.singleEpisode(url, self.cookies, resolution, language)

    def login(self, userUserName, userPassword):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Territory': 'US'

        }
        payload = {'username': '%s' % userUserName, 'password': '%s' % userPassword}
        sess = session()
        sess = create_scraper(sess)

        loginPost = sess.post(url='https://prod-api-funimationnow.dadcdigital.com/api/auth/login/', data=payload,
                              headers=headers)

        initialCookies = sess.cookies

        return initialCookies


    def singleEpisode(self, url, userCookies, resolution, language):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Territory': 'US'

        }

        sess = session()
        sess = create_scraper(sess)
        print("This lang : ", language)

        if language.lower() in ["japanese", "sub", "jpn"]:
            finalUrl = str(url) + "?lang=english"
            s = sess.get(finalUrl, headers=headers, cookies=userCookies)

        elif language.lower() in ["english", "dub", "eng"]:
            finalUrl = str(url).replace("simulcast", "uncut") + "?lang=english"
            print(finalUrl)
            s = sess.get(finalUrl, headers=headers, cookies=userCookies)
            print("Got this")
        else:
            s = sess.get(url + "?lang=english", headers=headers, cookies=userCookies)

        cookies = sess.cookies

        page_source = s.text.encode('utf-8')
        htmlSource = str(BeautifulSoup(page_source, "lxml"))

        videoID = int(str(re.search('id\:\ \'(.*?)\'\,', htmlSource).group(1)).strip())
        seasonNumber = int(str(re.search('seasonNum: (.*?),', htmlSource).group(1)).strip())
        episodeNumber = int(str(re.search('episodeNum: (.*?),', htmlSource).group(1)).strip())
        showName = str(
            re.search('KANE_customdimensions.showName\ \=\ \'(.*?)\'\;', htmlSource).group(1)).strip().replace("&#39;",
                                                                                                               "'").replace(
            "&amp;", "$")
        fileName = str(showName) + " - " + str(episodeNumber) + ".mkv"
        bDubNumber = int(str(re.search('"/player/(.*?)/\?bdub=0', htmlSource).group(1)).strip())
        print(videoID, seasonNumber, episodeNumber, showName, bDubNumber)
        videoPlayerLink = "https://www.funimation.com/player/%s/?bdub=0" % bDubNumber
        print(videoPlayerLink)
        sleep(10)
        headersNew = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Territory': 'US',
            'Referer' : '%s' % finalUrl

        }
        playerSource = sess.get(videoPlayerLink, headers=headersNew).text
        print(playerSource)
        main_m3u8Link = str(re.search('"screenshots":(.*?)"],', playerSource).group(1)).strip().replace("[\"", "").replace("exp/", "")
        print(main_m3u8Link)
        try:
            srtLink = str(re.search('"src":(.*?)\.srt"', playerSource).group(1)).strip().replace("[\"", "").replace("exp/", "")
            print(srtLink)
        except:
            pass

        if resolution.lower() in ["1080p", "fhd", "1080"]:
            m3u8LinkFinal = main_m3u8Link.replace(".m3u8", "_Layer9.m3u8")
        elif resolution.lower() in ["720p", "hd", "720"]:
            m3u8LinkFinal = main_m3u8Link.replace(".m3u8", "_Layer7.m3u8")
        elif resolution.lower() in ["540p", "sd", "540"]:
            m3u8LinkFinal = main_m3u8Link.replace(".m3u8", "_Layer5.m3u8")
        elif resolution.lower() in ["360p", "crap", "360"]:
            m3u8LinkFinal = main_m3u8Link.replace(".m3u8", "_Layer4.m3u8")
        elif resolution.lower() in ["270p", "cancer", "270"]:
            m3u8LinkFinal = main_m3u8Link.replace(".m3u8", "_Layer2.m3u8")
        elif resolution.lower() in ["234p", "killme", "234"]:
            m3u8LinkFinal = main_m3u8Link.replace(".m3u8", "_Layer1.m3u8")

        print(m3u8LinkFinal)
        ffmpegCommand = "ffmpeg -i \"%s\" -c copy \"%s\"" % (m3u8LinkFinal, fileName)
        call(ffmpegCommand)
