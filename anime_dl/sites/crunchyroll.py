#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import logging
import os
import re
import subprocess
import sys
import zlib
from glob import glob
from hashlib import sha1
from math import pow, sqrt, floor
from shutil import move

import animeName
import cfscrape
import requests
from external.aes import aes_cbc_decrypt
from external.compat import compat_etree_fromstring
# External libs have been taken from youtube-dl for decoding the subtitles.
from external.utils import bytes_to_intlist, intlist_to_bytes

'''This code Stinx. I'll write a better, faster and compact code when I get time after my exams or in mid.
I literally have NO idea what I was thinking when I wrote this piece of code.
THIS REALLY STINX!
Also, some strangers went here and wrote some more code that REALLY REALLY STINX.
Read the code at your own risk.
'''


class CrunchyRoll(object):
    def __init__(self, url, password, username, resolution, language, skipper, logger, episode_range):
        # print("Username  : {0}".format(username))
        # print("Type Username  : {0}".format(type(username)))
        # print("Type Username  : {0}".format(type(password)))
        # print("Password  : {0}".format(password))
        if logger == "True":
            logging.basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=logging.DEBUG,
                                encoding="utf-8")

        # Extract the language from the input URL
        Crunchy_Language = re.search(r'.+\/([a-z]{2}|[a-z]{2}-[a-z]{2})\/.+', url)
        if not Crunchy_Language:
            Crunchy_Language = "/"
        else:
            Crunchy_Language = Crunchy_Language.group(1) + "/"


        Crunchy_Show_regex = r'https?:\/\/(?:(?P<prefix>www|m)\.)?(?P<url>crunchyroll\.com(\/[a-z]{2}|\/[a-z]{2}-[a-z]{2})?\/(?!(?:news|anime-news|library|forum|launchcalendar|lineup|store|comics|freetrial|login))(?P<id>[\w\-]+))\/?(?:\?|$)'
        Crunchy_Video_regex = r'https?:\/\/(?:(?P<prefix>www|m)\.)?(?P<url>crunchyroll\.(?:com|fr)(\/[a-z]{2}|\/[a-z]{2}-[a-z]{2})?\/(?:media(?:-|\/\?id=)|[^\/]*\/[^\/?&]*?)(?P<video_id>[0-9]+))(?:[\/?&]|$)'

        Crunchy_Show = re.match(Crunchy_Show_regex, url)
        Crunchy_Video = re.match(Crunchy_Video_regex, url)

        if Crunchy_Video:
            cookies, Token = self.webpagedownloader(url=url, username=username[0], password=password[0], country=Crunchy_Language)
            if skipper == "yes":
                self.onlySubs(url=url, cookies=cookies)
            else:
                self.singleEpisode(
                    url=url, cookies=cookies, token=Token, resolution=resolution)
        elif Crunchy_Show:
            cookies, Token = self.webpagedownloader(url=url, username=username[0], password=password[0], country=Crunchy_Language)
            self.wholeShow(url=url, cookie=cookies, token=Token, language=language, resolution=resolution,
                           skipper=skipper, episode_range=episode_range)
        else:
            print("URL does not look like a show or a video, stopping.")

    def login_check(self, htmlsource):
        # Open the page and check the title. CrunchyRoll redirects the user and the title has the text "Redirecting...".
        # If this is not found, you're probably not logged in and you'll just get 360p or 480p.

        # titleCheck = re.search(r'\<title\>(.*?)\</title\>',
        #                        str(htmlsource)).group(1)
        # if str(titleCheck) == "Redirecting...":
        #     return True
        # else:
        #     return False
        return True

    def webpagedownloader(self, url, username, password, country):

        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Referer':
                'https://www.crunchyroll.com/' + country + 'login'
        }

        sess = requests.session()
        sess = cfscrape.create_scraper(sess)
        print("Trying to login...")

        initial_page_fetch = sess.get(url='https://www.crunchyroll.com/' + country + 'login', headers=headers)

        if initial_page_fetch.status_code == 200:
            initial_page_source = initial_page_fetch.text.encode("utf-8")
            initial_cookies = sess.cookies
            csrf_token = re.search(r'login_form\[\_token\]\"\ value\=\"(.*?)\"',
                                   str(initial_page_source)).group(1)

            payload = {
                'login_form[name]': '%s' % username,
                'login_form[password]': '%s' % password,
                'login_form[redirect_url]': '/',
                'login_form[_token]': '%s' % csrf_token
            }

            login_post = sess.post(
                url='https://www.crunchyroll.com/' + country + 'login',
                data=payload,
                headers=headers,
                cookies=initial_cookies)

            # with open("login_source.html", "w")  as wf:
            #     wf.write(login_post.text.encode('utf-8'))

            if self.login_check(htmlsource=login_post.text.encode('utf-8')):
                print("Logged in successfully...")
                resp = sess.get(
                    url=url, headers=headers,
                    cookies=initial_cookies)
                # video_id = int(str(re.search(r'div\[media_id\=(.*?)\]', str(resp)).group(1)).strip())
                #
                return initial_cookies, csrf_token
            else:
                print("Unable to Log you in. Check credentials again.")
        else:
            print("Couldn't connect to the login page...")
            print("Website returned : %s" % str(initial_page_fetch.status_code))

    def rtmpDump(self, host, file, url, filename):
        # print("Downloading RTMP DUMP STREAM!")
        logging.debug("Host : %s", host)
        logging.debug("file : %s", file)
        logging.debug("url : %s", url)
        serverAddress = str(host.split("/ondemand/")[0]) + "/ondemand/"
        authentication = "ondemand/" + str(host.split("/ondemand/")[1])

        rtmpDumpCommand = "rtmpdump -r \"%s\" -a \"%s\" -f \"WIN 25,0,0,148\" -W \"http://www.crunchyroll.com/vendor/ChromelessPlayerApp-c0d121b.swf\" -p \"%s\" -y \"%s\" -o \"%s\"" % (
            serverAddress, authentication, url, file, filename)
        logging.debug("rtmpDumpCommand : %s" % rtmpDumpCommand)

        try:
            subprocess.call(rtmpDumpCommand, shell=True)
        except Exception:
            print("Please make sure that rtmpdump is present in the PATH or THIS DIRECTORY!")
            sys.exit()

    def duplicate_remover(self, seq):
        # https://stackoverflow.com/a/480227
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    def singleEpisode(self, url, cookies, token, resolution):

        video_id = str(url.split('-')[-1]).replace("/", "")
        logging.debug("video_id : %s", video_id)
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Upgrade-Insecure-Requests':
                '1',
            'Accept-Encoding':
                'gzip, deflate'
        }

        sess = requests.session()
        sess = cfscrape.create_scraper(sess)

        info_url = ""

        if str(resolution).lower() in ['1080p', '1080', 'fhd', 'best']:
            info_url = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id=%s&video_format=108&video_quality=80&current_page=%s" % (
                video_id, url)

        elif str(resolution).lower() in ['720p', '720', 'hd']:
            info_url = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id=%s&video_format=106&video_quality=62&current_page=%s" % (
                video_id, url)

        elif str(resolution).lower() in ['480p', '480', 'sd']:
            info_url = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id=%s&video_format=106&video_quality=61&current_page=%s" % (
                video_id, url)
        elif str(resolution).lower() in ['360p', '360', 'cancer']:
            info_url = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id=%s&video_format=106&video_quality=60&current_page=%s" % (
                video_id, url)

        logging.debug("info_url : %s", info_url)

        xml_page_connect = sess.get(url=info_url, headers=headers, cookies=cookies)

        if xml_page_connect.status_code == 200:
            xml_page = xml_page_connect.text.encode("utf-8")

            try:
                m3u8_file_link = str(re.search(r'<file>(.*?)</file>', xml_page).group(1)).replace("&amp;", "&")
                logging.debug("m3u8_file_link : %s", m3u8_file_link)

                if not m3u8_file_link:
                    # If no m3u8 found, try the rtmpdump...
                    try:
                        host_link = re.search(r'<host>(.*?)</host>', xml_page).group(1)
                        logging.debug("Found RTMP DUMP!")
                        print("RTMP streams not supported currently...")
                    except Exception as NoRtmpDump:
                        print("No RTMP Streams Found...")
                        print(NoRtmpDump)
                else:
                    anime_name = re.sub(r'[^A-Za-z0-9\ \-\' \\]+', '', str(
                        re.search(r'<series_title>(.*?)</series_title>', xml_page).group(1))).title().strip()
                    episode_number = re.search(r'<episode_number>(.*?)</episode_number>',
                                               xml_page.decode("utf-8")).group(1)
                    video_width = re.search(r'<width>(.*?)</width>', xml_page.decode("utf-8")).group(1)
                    video_height = re.search(r'<height>(.*?)</height>', xml_page.decode("utf-8")).group(1)

                    video_resolution = str(video_width) + "x" + str(video_height)

                    file_name = animeName.animeName().nameEdit(animeName=anime_name, episodeNumber=episode_number,
                                                               resolution=video_resolution)

                    output_directory = os.path.abspath("Output" + os.sep + str(anime_name) + "/")
                    # print("output_directory : {0}".format(output_directory))

                    if not os.path.exists("Output"):
                        os.makedirs("Output")
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)

                    file_location = str(output_directory) + os.sep + str(file_name).replace(".mp4", ".mkv")

                    logging.debug("anime_name : %s", anime_name)
                    logging.debug("episode_number : %s", episode_number)
                    logging.debug("video_resolution : %s", video_resolution)
                    logging.debug("file_name : %s", file_name)

                    if os.path.isfile(file_location):
                        print('[Anime-dl] File Exists! Skipping %s\n' % file_name)
                        pass
                    else:
                        self.subFetcher(
                            xml=str(xml_page),
                            episode_number=episode_number,
                            file_name=file_name)

                        m3u8_file_connect = sess.get(url=m3u8_file_link, cookies=cookies, headers=headers)
                        try:
                            m3u8_file_text = m3u8_file_connect.text.splitlines()[2]
                            logging.debug("m3u8_file_text : %s", m3u8_file_text)

                            ffmpeg_command = 'ffmpeg -i "{0}" -c copy -bsf:a aac_adtstoasc "{1}/{2}"'.format(
                                m3u8_file_text,
                                os.getcwd(),
                                file_name)
                            logging.debug("ffmpeg_command : %s", ffmpeg_command)
                            subprocess.call(ffmpeg_command, shell=True)

                            subtitles_files = []
                            for sub_file in glob("*.ass"):
                                if sub_file.endswith(".enUS.ass"):
                                    subtitles_files.insert(0,
                                                           "--track-name 0:English(US) --ui-language en --language 0:eng --default-track 0:yes --sub-charset 0:utf-8 " + '"' + str(
                                                               os.path.realpath(sub_file)) + '" ')

                                elif sub_file.endswith(".enGB.ass"):
                                    subtitles_files.append(
                                        "--track-name 0:English(UK) --ui-language en --language 0:eng --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                                            os.path.realpath(sub_file)) + '" ')

                                elif sub_file.endswith(".esLA.ass"):
                                    subtitles_files.append(
                                        "--track-name 0:Espanol --ui-language es --language 0:spa --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                                            os.path.realpath(sub_file)) + '" ')
                                elif sub_file.endswith(".esES.ass"):
                                    subtitles_files.append(
                                        "--track-name 0:Espanol(Espana) --ui-language es --language 0:spa --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                                            os.path.realpath(sub_file)) + '" ')
                                elif sub_file.endswith(".ptBR.ass"):
                                    subtitles_files.append(
                                        "--track-name 0:Portugues(Brasil) --ui-language pt --language 0:por --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                                            os.path.realpath(sub_file)) + '" ')
                                elif sub_file.endswith(".ptPT.ass"):
                                    subtitles_files.append(
                                        "--track-name 0:Portugues(Portugal) --ui-language pt --language 0:por --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                                            os.path.realpath(sub_file)) + '" ')
                                elif sub_file.endswith(".frFR.ass"):
                                    subtitles_files.append(
                                        "--track-name 0:Francais(France) --ui-language fr --language 0:fre --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                                            os.path.realpath(sub_file)) + '" ')
                                elif sub_file.endswith(".deDE.ass"):
                                    subtitles_files.append(
                                        "--track-name 0:Deutsch --ui-language de --language 0:ger --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                                            os.path.realpath(sub_file)) + '" ')
                                elif sub_file.endswith(".arME.ass"):
                                    subtitles_files.append(
                                        "--track-name 0:Arabic --language 0:ara --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                                            os.path.realpath(sub_file)) + '" ')
                                elif sub_file.endswith(".itIT.ass"):
                                    subtitles_files.append(
                                        "--track-name 0:Italiano --ui-language it --language 0:ita --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                                            os.path.realpath(sub_file)) + '" ')
                                elif sub_file.endswith(".trTR.ass"):
                                    subtitles_files.append(
                                        "--track-name 0:Turkce --ui-language tr --language 0:tur --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                                            os.path.realpath(sub_file)) + '" ')
                                else:
                                    subtitles_files.append(
                                        "--track-name 0:und --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                                            os.path.realpath(sub_file)) + '" ')

                            subs_files = self.duplicate_remover(subtitles_files)
                            logging.debug("subs_files : %s", subs_files)

                            font_files = [os.path.realpath(font_file) for font_file in
                                          glob(str(os.getcwd()) + "/Fonts/*.*")]

                            fonts = '--attachment-mime-type application/x-truetype-font --attach-file "' + str(
                                '" --attachment-mime-type application/x-truetype-font --attach-file "'.join(
                                    font_files)) + '"'

                            if len(font_files) == 0:
                                fonts = ''

                            mkv_merge_command = 'mkvmerge --ui-language en --output "%s" ' % str(file_name).replace(
                                ".mp4",
                                ".mkv") + '"' + str(
                                file_name) + '" ' + ' '.join(subs_files) + ' ' + str(fonts)

                            logging.debug("mkv_merge_command : %s", mkv_merge_command)

                            try:
                                subprocess.call(mkv_merge_command, shell=True)

                                for video_file in glob("*.mkv"):
                                    try:
                                        move(video_file, output_directory)
                                    except Exception as e:
                                        print(str(e))
                                        pass

                                for video in glob("*.mp4"):
                                    os.remove(os.path.realpath(video))

                                for sub_file_delete in glob("*.ass"):
                                    os.remove(os.path.realpath(sub_file_delete))

                            except Exception as FileMuxingException:
                                print("Sees like I couldn't mux the files.")
                                print("Check whether the MKVMERGE.exe is in PATH or not.")
                                print(FileMuxingException)

                                for video_file in glob("*.mp4"):
                                    try:
                                        move(video_file, output_directory)
                                    except Exception as e:
                                        print(str(e))
                                        pass
                                for sub_files in glob("*.ass"):
                                    try:
                                        move(sub_files, output_directory)
                                    except Exception as e:
                                        print(str(e))
                                        pass
                        except Exception as NoM3u8File:
                            print("Couldn't connect to the m3u8 file download link...")
                            print(NoM3u8File)
                            sys.exit(1)

            except Exception as NotAvailable:
                print("Seems like this video isn't available...")
                print(NotAvailable)
        else:
            print("Could not connect to Crunchyroll's media page.")
            print("It reurned : {0}".format(xml_page_connect.status_code))

    def wholeShow(self, url, cookie, token, language, resolution, skipper, episode_range):
        # print("Check my patreon for this : http://patreon.com/Xonshiz")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7',
            'Upgrade-Insecure-Requests': '1',
            'Accept-Encoding': 'gzip, deflate'
        }

        sess = requests.session()
        sess = cfscrape.create_scraper(sess)
        page_source = sess.get(url=url, headers=headers, cookies=cookie).text.encode("utf-8")
        # with open("New_way.html", "w") as wf:
        #     wf.write(page_source)

        dub_list = []
        ep_sub_list = []
        for episode_link, episode_type in re.findall(
                r'\<a href\=\"\/(.*?)\"\ title\=\"(.*?)', str(page_source)):
            if "(Dub)" in str(episode_type):
                dub_list.append(str(url) + "/" + str(str(episode_link).split("/")[-1]))
            else:
                ep_sub_list.append(str(url) + "/" + str(str(episode_link).split("/")[-1]))

        if len(dub_list) == 0 and len(ep_sub_list) == 0:
            print("Could not find the show links. Report on https://github.com/Xonshiz/anime-dl/issues/new")
            sys.exit()

        if episode_range != "All":
            # -1 to shift the episode number accordingly to the INDEX of it. List starts from 0 xD!
            starting = int(str(episode_range).split("-")[0]) - 1
            ending = int(str(episode_range).split("-")[1])
            indexes = [x for x in range(starting, ending)]
            # [::-1] in sub_list in beginning to start this from the 1st episode and at the last, it is to reverse the list again, becasue I'm reverting it again at the end.
            sub_list = [ep_sub_list[::-1][x] for x in indexes][::-1]
        else:
            sub_list = ep_sub_list

        if skipper == "yes":
            # print("DLing everything")
            print("Total Subs to download : %s" % len(sub_list))
            for episode_url in sub_list[::-1]:
                # cookies, Token = self.webpagedownloader(url=url)
                # print("Sub list : %s" % sub_list)
                self.onlySubs(url=episode_url, cookies=cookie)

                print("-----------------------------------------------------------")
                print("\n")
        else:
            if str(language).lower() in ["english", "eng", "dub"]:
                # If the "dub_list" is empty, that means there are no English Dubs for the show, or CR changed something.
                if len(dub_list) == 0:
                    print("No English Dub Available For This Series.")
                    print(
                        "If you can see the Dubs, please open an Issue on https://github.com/Xonshiz/anime-dl/issues/new")
                    sys.exit()
                else:
                    print("Total Episodes to download : %s" % len(dub_list))
                    for episode_url in dub_list[::-1]:
                        # cookies, Token = self.webpagedownloader(url=url)
                        # print("Dub list : %s" % dub_list)
                        try:
                            self.singleEpisode(url=episode_url, cookies=cookie, token=token, resolution=resolution)
                        except Exception as SomeError:
                            print("Error Downloading : {0}".format(SomeError))
                            pass
                        print("-----------------------------------------------------------")
                        print("\n")
            else:
                print("Total Episodes to download : %s" % len(sub_list))

                for episode_url in sub_list[::-1]:
                    # cookies, Token = self.webpagedownloader(url=url)
                    # print("Sub list : %s" % sub_list)
                    try:
                        self.singleEpisode(url=episode_url, cookies=cookie, token=token, resolution=resolution)
                    except Exception as SomeError:
                        print("Error Downloading : {0}".format(SomeError))
                        pass
                    print("-----------------------------------------------------------")
                    print("\n")

    def subFetcher(self, xml, episode_number, file_name):
        logging.debug("\n----- Subs Downloading Started -----\n")
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7',
            'Referer':
                'https://www.crunchyroll.com'
        }


        sess = requests.session()
        sess = cfscrape.create_scraper(sess)
        for sub_id, sub_lang, sub_lang2 in re.findall(
                r'subtitle_script_id\=(.*?)\'\ title\=\'\[(.*?)\]\ (.*?)\'',
                str(xml)):

            xml_return = str(
                sess.get(
                    url="http://www.crunchyroll.com/xml/?req=RpcApiSubtitle_GetXml&subtitle_script_id=%s"
                        % sub_id,
                    headers=headers).text)

            iv = str(
                re.search(r'\<iv\>(.*?)\<\/iv\>', xml_return).group(1)).strip()

            data = str(
                re.search(r'\<data\>(.*?)\<\/data\>', xml_return).group(
                    1)).strip()
            # logging.debug("data : %s", data)
            logging.debug("iv : %s", iv)

            # print("Sub ID : %s\t| iv : %s\t| data : %s" % (sub_id, iv, data))
            subtitle = self._decrypt_subtitles(data, iv,
                                               sub_id).decode('utf-8')
            # print(subtitle)
            sub_root = compat_etree_fromstring(subtitle)
            sub_data = self._convert_subtitles_to_ass(sub_root)
            # print(sub_root)
            lang_code = str(
                re.search(r'lang_code\=\"(.*?)\"', str(subtitle)).group(
                    1)).strip()
            sub_file_name = str(file_name).replace(".mp4", ".") + str(lang_code) + ".ass"

            print("Downloading {0} ...".format(sub_file_name))

            try:
                with open(str(os.getcwd()) + "/" + str(sub_file_name), "wb") as sub_file:
                    sub_file.write(sub_data.encode("utf-8"))
            except Exception as EncodingException:
                print("Couldn't write the subtitle file...skipping.")
                pass
        logging.debug("\n----- Subs Downloaded -----\n")

    def onlySubs(self, url, cookies):
        # print("Running only subs")
        current_directory = os.getcwd()
        video_id = str(url.split('-')[-1]).replace("/", "")
        # print("URL : %s\nCookies : %s\nToken : %s\nResolution : %s\nMedia ID : %s" % (url, cookies, token, resolution, video_id))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7',
            'Upgrade-Insecure-Requests': '1',
            'Accept-Encoding': 'gzip, deflate'
        }

        sess = requests.session()
        sess = cfscrape.create_scraper(sess)
        infoURL = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id=%s&video_format=108&video_quality=80&current_page=%s" % (
            video_id, url)
        xml_page = sess.get(url=infoURL, headers=headers, cookies=cookies).text.encode("utf-8")

        # anime_name = re.search(r'<series_title>(.*?)</series_title>', xml_page).group(1)
        anime_name = re.sub(r'[^A-Za-z0-9\ \-\' \\]+', '',
                            str(re.search(r'<series_title>(.*?)</series_title>', xml_page).group(1))).title().strip()

        episode_number = re.search(r'<episode_number>(.*?)</episode_number>', xml_page.decode("utf-8")).group(1)
        video_width = re.search(r'<width>(.*?)</width>', xml_page.decode("utf-8")).group(1)
        video_height = re.search(r'<height>(.*?)</height>', xml_page.decode("utf-8")).group(1)

        video_resolution = str(video_width) + "x" + str(video_height)

        file_name = animeName.animeName().nameEdit(animeName=anime_name, episodeNumber=episode_number,
                                                   resolution=video_resolution)

        output_directory = os.path.abspath("Output" + os.sep + str(anime_name) + os.sep)

        if not os.path.exists("Output"):
            os.makedirs("Output")

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        self.subFetcher(xml=xml_page, episode_number=episode_number, file_name=file_name)

        for sub_file in glob("*.ass"):
            try:
                move(sub_file, current_directory + os.sep + "Output" + os.sep)
            except Exception as e:
                print("Couldn't move the file. Got following error : \n")
                print(e)
                pass

    def _decrypt_subtitles(self, data, iv, id):
        data = bytes_to_intlist(base64.b64decode(data.encode('utf-8')))
        iv = bytes_to_intlist(base64.b64decode(iv.encode('utf-8')))
        id = int(id)

        def obfuscate_key_aux(count, modulo, start):
            output = list(start)
            for _ in range(count):
                output.append(output[-1] + output[-2])
            # cut off start values
            output = output[2:]
            output = list(map(lambda x: x % modulo + 33, output))
            return output

        def obfuscate_key(key):
            num1 = int(floor(pow(2, 25) * sqrt(6.9)))
            num2 = (num1 ^ key) << 5
            num3 = key ^ num1
            num4 = num3 ^ (num3 >> 3) ^ num2
            prefix = intlist_to_bytes(obfuscate_key_aux(20, 97, (1, 2)))
            shaHash = bytes_to_intlist(
                sha1(prefix + str(num4).encode('ascii')).digest())
            # Extend 160 Bit hash to 256 Bit
            return shaHash + [0] * 12

        key = obfuscate_key(id)

        decrypted_data = intlist_to_bytes(aes_cbc_decrypt(data, key, iv))
        return zlib.decompress(decrypted_data)

    def _convert_subtitles_to_ass(self, sub_root):
        output = ''

        def ass_bool(strvalue):
            assvalue = '0'
            if strvalue == '1':
                assvalue = '-1'
            return assvalue

        output = '[Script Info]\n'
        output += 'Title: %s\n' % sub_root.attrib['title']
        output += 'ScriptType: v4.00+\n'
        output += 'WrapStyle: %s\n' % sub_root.attrib['wrap_style']
        output += 'PlayResX: %s\n' % sub_root.attrib['play_res_x']
        output += 'PlayResY: %s\n' % sub_root.attrib['play_res_y']
        output += """
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
"""
        for style in sub_root.findall('./styles/style'):
            output += 'Style: ' + style.attrib['name']
            output += ',' + style.attrib['font_name']
            output += ',' + style.attrib['font_size']
            output += ',' + style.attrib['primary_colour']
            output += ',' + style.attrib['secondary_colour']
            output += ',' + style.attrib['outline_colour']
            output += ',' + style.attrib['back_colour']
            output += ',' + ass_bool(style.attrib['bold'])
            output += ',' + ass_bool(style.attrib['italic'])
            output += ',' + ass_bool(style.attrib['underline'])
            output += ',' + ass_bool(style.attrib['strikeout'])
            output += ',' + style.attrib['scale_x']
            output += ',' + style.attrib['scale_y']
            output += ',' + style.attrib['spacing']
            output += ',' + style.attrib['angle']
            output += ',' + style.attrib['border_style']
            output += ',' + style.attrib['outline']
            output += ',' + style.attrib['shadow']
            output += ',' + style.attrib['alignment']
            output += ',' + style.attrib['margin_l']
            output += ',' + style.attrib['margin_r']
            output += ',' + style.attrib['margin_v']
            output += ',' + style.attrib['encoding']
            output += '\n'

        output += """
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        for event in sub_root.findall('./events/event'):
            output += 'Dialogue: 0'
            output += ',' + event.attrib['start']
            output += ',' + event.attrib['end']
            output += ',' + event.attrib['style']
            output += ',' + event.attrib['name']
            output += ',' + event.attrib['margin_l']
            output += ',' + event.attrib['margin_r']
            output += ',' + event.attrib['margin_v']
            output += ',' + event.attrib['effect']
            output += ',' + event.attrib['text']
            output += '\n'

        return output
