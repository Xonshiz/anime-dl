#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cfscrape import create_scraper
from requests import session
from re import search, findall
from os import getcwd
from subprocess import call
# External libs have been taken from youtube-dl for decoding the subtitles.
from anime_dl.external.utils import bytes_to_intlist, intlist_to_bytes
from anime_dl.external.aes import aes_cbc_decrypt
from anime_dl.external.compat import compat_etree_fromstring
import zlib
import base64
from hashlib import sha1
from math import pow, sqrt, floor
from os import path, makedirs
from glob import glob
from shutil import move


class CrunchyRoll(object):
    def __init__(self, url, password, username, resolution):
        # cookies + Token are required to login after CR put their login page behind CloudFlare.
        cookies, Token = self.webpagedownloader(url=url)
        self.singleEpisode(
            url=url, cookies=cookies, token=Token, resolution=resolution)

    def loginCheck(self, htmlsource):
        # Open the page and check the title. CrunchyRoll redirects the user and the title has the text "Redirecting...".
        # If this is not found, you're probably not logged in and you'll just get 360p or 480p.

        titleCheck = search(r'\<title\>(.*?)\</title\>',
                            str(htmlsource)).group(1)
        if str(titleCheck) == "Redirecting...":
            return True
        else:
            return False

    def webpagedownloader(self, url):
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Referer':
            'https://www.crunchyroll.com/login'
        }

        sess = session()
        sess = create_scraper(sess)
        print("Trying to login...")
        initialPagefetch = sess.get(
            url='https://www.crunchyroll.com/login', headers=headers).text
        initialCookies = sess.cookies
        csrfToken = search(r'login_form\[\_token\]\"\ value\=\"(.*?)\"',
                           str(initialPagefetch)).group(1)
        # print(csrfToken)

        payload = {
            'login_form[name]': 'sharnitanjones@yahoo.com',
            'login_form[password]': 'gemini617',
            'login_form[redirect_url]': '/',
            'login_form[_token]': '%s' % csrfToken
        }

        loginPost = sess.post(
            url='https://www.crunchyroll.com/login',
            data=payload,
            headers=headers,
            cookies=initialCookies)

        if self.loginCheck(htmlsource=loginPost.text):
            print("Logged in successfully...")
            resp = sess.get(
                url=url, headers=headers,
                cookies=initialCookies).text.encode('utf-8')
            # video_id = int(str(search(r'div\[media_id\=(.*?)\]', str(resp)).group(1)).strip())
            #
            return initialCookies, csrfToken
        else:
            print("Unable to Log you in. Check credentials again.")

    def singleEpisode(self, url, cookies, token, resolution):
        # print("Inside single episode")
        current_directory = getcwd()
        video_id = str(url.split('-')[-1]).replace("/", "")
        # print("URL : %s\nCookies : %s\nToken : %s\nResolution : %s\nMedia ID : %s" % (url, cookies, token, resolution, video_id))
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Upgrade-Insecure-Requests':
            '1',
            'Accept-Encoding':
            'gzip, deflate'
        }

        sess = session()
        sess = create_scraper(sess)

        if str(resolution).lower() in ['1080p', '1080', 'best', 'fhd']:
            print("Grabbing Links for 1080p Streams.")
            infoURL = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id=%s&video_format=108&video_quality=80&current_page=%s" % (
                video_id, url)
            xml_page = sess.get(
                url=infoURL, headers=headers, cookies=cookies).text

            m3u8_link_raw = str(
                search(r'\<file\>(.*?)\<\/file\>', xml_page).group(
                    1)).strip().replace("&amp;", "&")
            anime_name = str(
                search(r'\<series_title\>(.*?)\<\/series_title\>', xml_page)
                .group(1)).strip().replace("â", "'").replace(
                    ":", " - ").replace("&#039;", "'")
            episode_number = str(
                search(r'\<episode_number\>(.*?)\<\/episode_number\>',
                       xml_page).group(1)).strip()
            width = str(
                search(r'\<width\>(.*?)\<\/width\>', xml_page).group(
                    1)).strip()
            height = str(
                search(r'\<height\>(.*?)\<\/height\>', xml_page).group(
                    1)).strip()
            # print("m3u8_link : %s\nanime_name : %s\nepisode_number : %s\nwidth : %s\nheight : %s\n" % (m3u8_link_raw, anime_name, episode_number, width, height))
            # self.subFetcher(xml=str(xml_page), anime_name=anime_name, episode_number=episode_number)
            file_name = str(anime_name) + " - " + str(
                episode_number) + " [%sx%s].mp4" % (width, height)
            # print("File Name : %s\n" % file_name)

            if not path.exists("Output"):
                makedirs("Output")

            if path.isfile("Output/" + file_name):
                print('[Anime-dl] File Exist! Skipping ', file_name, '\n')
                pass
            else:
                self.subFetcher(
                    xml=str(xml_page),
                    anime_name=anime_name,
                    episode_number=episode_number)
                # UNCOMMENT THIS LINE!!!
                m3u8_file = sess.get(
                    url=m3u8_link_raw, cookies=cookies,
                    headers=headers).text.splitlines()[2]
                # print("M3u8 : %s" % m3u8_file)
                ffmpeg_command = "ffmpeg -i \"%s\" -c copy -bsf:a aac_adtstoasc \"%s\"" % (
                    m3u8_file, file_name)
                call(ffmpeg_command)

                for video_file in glob("*.mp4"):
                    try:
                        move(video_file, "Output")
                    except Exception as e:
                        print(str(e))
                        pass
                for sub_files in glob("*.ass"):
                    try:
                        move(sub_files, "Output")
                    except Exception as e:
                        print(str(e))
                        pass

        if str(resolution).lower() in ['720p', '720', 'hd']:
            print("Grabbing Links for 720p Streams.")
            infoURL = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id=%s&video_format=106&video_quality=62&current_page=%s" % (
                video_id, url)
            xml_page = sess.get(
                url=infoURL, headers=headers, cookies=cookies).text

            m3u8_link_raw = str(
                search(r'\<file\>(.*?)\<\/file\>', xml_page).group(
                    1)).strip().replace("&amp;", "&")
            anime_name = str(
                search(r'\<series_title\>(.*?)\<\/series_title\>', xml_page)
                .group(1)).strip().replace("â", "'").replace(
                    ":", " - ").replace("&#039;", "'")
            episode_number = str(
                search(r'\<episode_number\>(.*?)\<\/episode_number\>',
                       xml_page).group(1)).strip()
            width = str(
                search(r'\<width\>(.*?)\<\/width\>', xml_page).group(
                    1)).strip()
            height = str(
                search(r'\<height\>(.*?)\<\/height\>', xml_page).group(
                    1)).strip()
            # print("m3u8_link : %s\nanime_name : %s\nepisode_number : %s\nwidth : %s\nheight : %s\n" % (m3u8_link_raw, anime_name, episode_number, width, height))
            # self.subFetcher(xml=str(xml_page), anime_name=anime_name, episode_number=episode_number)
            file_name = str(anime_name) + " - " + str(
                episode_number) + " [%sx%s].mp4" % (width, height)
            # print("File Name : %s\n" % file_name)

            if not path.exists("Output"):
                makedirs("Output")

            if path.isfile("Output/" + file_name):
                print('[Anime-dl] File Exist! Skipping %s\n' % file_name)
                pass
            else:
                self.subFetcher(
                    xml=str(xml_page),
                    anime_name=anime_name,
                    episode_number=episode_number)
                # UNCOMMENT THIS LINE!!!
                m3u8_file = sess.get(
                    url=m3u8_link_raw, cookies=cookies,
                    headers=headers).text.splitlines()[2]
                # print("M3u8 : %s" % m3u8_file)
                ffmpeg_command = "ffmpeg -i \"%s\" -c copy -bsf:a aac_adtstoasc \"%s\"" % (
                    m3u8_file, file_name)
                call(ffmpeg_command)

                for video_file in glob("*.mp4"):
                    try:
                        move(video_file, "Output")
                    except Exception as e:
                        print(str(e))
                        pass
                for sub_files in glob("*.ass"):
                    try:
                        move(sub_files, "Output")
                    except Exception as e:
                        print(str(e))
                        pass

        if str(resolution).lower() in ['480p', '480', 'sd']:
            print("Grabbing Links for 480p Streams.")
            infoURL = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id=%s&video_format=106&video_quality=61&current_page=%s" % (
                video_id, url)
            xml_page = sess.get(
                url=infoURL, headers=headers, cookies=cookies).text

            m3u8_link_raw = str(
                search(r'\<file\>(.*?)\<\/file\>', xml_page).group(
                    1)).strip().replace("&amp;", "&")
            anime_name = str(
                search(r'\<series_title\>(.*?)\<\/series_title\>', xml_page)
                .group(1)).strip().replace("â", "'").replace(
                    ":", " - ").replace("&#039;", "'")
            episode_number = str(
                search(r'\<episode_number\>(.*?)\<\/episode_number\>',
                       xml_page).group(1)).strip()
            width = str(
                search(r'\<width\>(.*?)\<\/width\>', xml_page).group(
                    1)).strip()
            height = str(
                search(r'\<height\>(.*?)\<\/height\>', xml_page).group(
                    1)).strip()
            # print("m3u8_link : %s\nanime_name : %s\nepisode_number : %s\nwidth : %s\nheight : %s\n" % (m3u8_link_raw, anime_name, episode_number, width, height))
            # self.subFetcher(xml=str(xml_page), anime_name=anime_name, episode_number=episode_number)
            file_name = str(anime_name) + " - " + str(
                episode_number) + " [%sx%s].mp4" % (width, height)
            # print("File Name : %s\n" % file_name)

            if not path.exists("Output"):
                makedirs("Output")

            if path.isfile("Output/" + file_name):
                print('[Anime-dl] File Exist! Skipping ', file_name, '\n')
                pass
            else:
                self.subFetcher(
                    xml=str(xml_page),
                    anime_name=anime_name,
                    episode_number=episode_number)
                # UNCOMMENT THIS LINE!!!
                m3u8_file = sess.get(
                    url=m3u8_link_raw, cookies=cookies,
                    headers=headers).text.splitlines()[2]
                # print("M3u8 : %s" % m3u8_file)
                ffmpeg_command = "ffmpeg -i \"%s\" -c copy -bsf:a aac_adtstoasc \"%s\"" % (
                    m3u8_file, file_name)
                call(ffmpeg_command)

                for video_file in glob("*.mp4"):
                    try:
                        move(video_file, "Output")
                    except Exception as e:
                        print(str(e))
                        pass
                for sub_files in glob("*.ass"):
                    try:
                        move(sub_files, "Output")
                    except Exception as e:
                        print(str(e))
                        pass

        if str(resolution).lower() in ['360p', '360', 'mobile']:
            print("Grabbing Links for 360p Streams.")
            infoURL = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id=%s&video_format=106&video_quality=60&current_page=%s" % (
                video_id, url)
            xml_page = sess.get(
                url=infoURL, headers=headers, cookies=cookies).text

            m3u8_link_raw = str(
                search(r'\<file\>(.*?)\<\/file\>', xml_page).group(
                    1)).strip().replace("&amp;", "&")
            anime_name = str(
                search(r'\<series_title\>(.*?)\<\/series_title\>', xml_page)
                .group(1)).strip().replace("â", "'").replace(
                    ":", " - ").replace("&#039;", "'")
            episode_number = str(
                search(r'\<episode_number\>(.*?)\<\/episode_number\>',
                       xml_page).group(1)).strip()
            width = str(
                search(r'\<width\>(.*?)\<\/width\>', xml_page).group(
                    1)).strip()
            height = str(
                search(r'\<height\>(.*?)\<\/height\>', xml_page).group(
                    1)).strip()
            # print("m3u8_link : %s\nanime_name : %s\nepisode_number : %s\nwidth : %s\nheight : %s\n" % (m3u8_link_raw, anime_name, episode_number, width, height))
            # self.subFetcher(xml=str(xml_page), anime_name=anime_name, episode_number=episode_number)
            file_name = str(anime_name) + " - " + str(
                episode_number) + " [%sx%s].mp4" % (width, height)
            # print("File Name : %s\n" % file_name)

            if not path.exists("Output"):
                makedirs("Output")

            if path.isfile("Output/" + file_name):
                print('[Anime-dl] File Exist! Skipping ', file_name, '\n')
                pass
            else:
                self.subFetcher(
                    xml=str(xml_page),
                    anime_name=anime_name,
                    episode_number=episode_number)
                # UNCOMMENT THIS LINE!!!
                m3u8_file = sess.get(
                    url=m3u8_link_raw, cookies=cookies,
                    headers=headers).text.splitlines()[2]
                # print("M3u8 : %s" % m3u8_file)
                ffmpeg_command = "ffmpeg -i \"%s\" -c copy -bsf:a aac_adtstoasc \"%s\"" % (
                    m3u8_file, file_name)
                call(ffmpeg_command)

                for video_file in glob("*.mp4"):
                    try:
                        move(video_file, "Output")
                    except Exception as e:
                        print(str(e))
                        pass
                for sub_files in glob("*.ass"):
                    try:
                        move(sub_files, "Output")
                    except Exception as e:
                        print(str(e))
                        pass

        print("Completed Downloading : %s" % anime_name)

        return (video_id, m3u8_link_raw, anime_name, episode_number, width,
                height, file_name, cookies, token)

    def subFetcher(self, xml, anime_name, episode_number):
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7',
            'Referer':
            'https://www.crunchyroll.com'
        }

        sess = session()
        sess = create_scraper(sess)
        for sub_id, sub_lang, sub_lang2 in findall(
                r'subtitle_script_id\=(.*?)\'\ title\=\'\[(.*?)\]\ (.*?)\'',
                str(xml)):
            # print("Sub ID : %s\t| Sub Lang : %s" % (sub_id, sub_lang))
            xml_return = str(
                sess.get(
                    url="http://www.crunchyroll.com/xml/?req=RpcApiSubtitle_GetXml&subtitle_script_id=%s"
                    % sub_id,
                    headers=headers).text)
            # print(xml_return)
            iv = str(
                search(r'\<iv\>(.*?)\<\/iv\>', xml_return).group(1)).strip()
            data = str(
                search(r'\<data\>(.*?)\<\/data\>', xml_return).group(
                    1)).strip()
            # print("Sub ID : %s\t| iv : %s\t| data : %s" % (sub_id, iv, data))
            subtitle = self._decrypt_subtitles(data, iv,
                                               sub_id).decode('utf-8')
            # print(subtitle)
            sub_root = compat_etree_fromstring(subtitle)
            sub_data = self._convert_subtitles_to_ass(sub_root)
            # print(sub_root)
            lang_code = str(
                search(r'lang_code\=\"(.*?)\"', str(subtitle)).group(
                    1)).strip()
            sub_file_name = str(anime_name) + " - " + str(
                episode_number) + ".%s.ass" % lang_code
            # print(sub_file_name)
            print("Writing subtitles to files...")
            with open(sub_file_name, "w", encoding="utf-8") as sub_file:
                sub_file.write(str(sub_data))

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
