#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
import anime_dl
from . import supporters
import os
import subprocess
from glob import glob
from shutil import move


class Crunchyroll(object):
    def __init__(self, url, password, username, resolution, language, skipper, logger, episode_range):
        if logger == "True":
            logging.basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=logging.DEBUG,
                                encoding="utf-8")

            # Extract the language from the input URL
        crunchy_language = re.search(r'.+\/([a-z]{2}|[a-z]{2}-[a-z]{2})\/.+', url)
        if not crunchy_language:
            crunchy_language = "/"
        else:
            crunchy_language = crunchy_language.group(1) + "/"

        crunchy_show_regex = r'https?:\/\/(?:(?P<prefix>www|m)\.)?(?P<url>crunchyroll\.com(\/[a-z]{2}|\/[a-z]{2}-[a-z]{2})?\/(?!(?:news|anime-news|library|forum|launchcalendar|lineup|store|comics|freetrial|login))(?P<id>[\w\-]+))\/?(?:\?|$)'
        crunchy_video_regex = r'https?:\/\/(?:(?P<prefix>www|m)\.)?(?P<url>crunchyroll\.(?:com|fr)(\/[a-z]{2}|\/[a-z]{2}-[a-z]{2})?\/(?:media(?:-|\/\?id=)|[^\/]*\/[^\/?&]*?)(?P<video_id>[0-9]+))(?:[\/?&]|$)'

        crunchy_show = re.match(crunchy_show_regex, url)
        crunchy_video = re.match(crunchy_video_regex, url)

        login_response, cookies, token = anime_dl.common.browser_instance.login_crunchyroll(url=url,
                                                                                            username=username[0],
                                                                                            password=password[0],
                                                                                            country=crunchy_language)
        if login_response:
            if crunchy_video:
                if skipper == "yes":
                    self.only_subs(url=url, cookies=cookies, resolution=resolution)
                else:
                    self.single_episode(url=url, cookies=cookies, token=token, resolution=resolution)
            elif crunchy_show:
                self.whole_show(url=url, cookie=cookies, token=token, language=language, resolution=resolution, skipper=skipper, episode_range=episode_range)
            else:
                print("URL does not look like a show or a video, stopping.")
        else:
            print("Failed Login!!!")
            exit(1)

    def single_episode(self, url, cookies, token, resolution):
        video_id = str(url.split('-')[-1]).replace("/", "")
        logging.debug("video_id : {0}".format(video_id))

        response, resolution_to_find, info_url = self.resolution_finder(resolution=resolution, video_id=video_id, url=url)

        if not response:
            print("No Resolution Found")
            exit(1)

        response_value, xml_page_connect, xml_cookies = anime_dl.common.browser_instance.page_downloader(url=info_url, cookies=cookies)

        if xml_page_connect:
            xml_page_connect = str(xml_page_connect)
            stream_exists, m3u8_file_link = self.m3u8_finder(xml_page_source=xml_page_connect)

            if stream_exists:
                anime_name, episode_number, video_resolution = self.episode_information_extractor(page_source=xml_page_connect, resolution_to_find=resolution_to_find)
                file_name = supporters.anime_name.crunchyroll_name(anime_name=anime_name, episode_number=episode_number, resolution=video_resolution)
                output_directory = supporters.path_works.path_creator(anime_name=anime_name)
                file_location = str(output_directory) + os.sep + str(file_name).replace(".mp4", ".mkv")

                if os.path.isfile(file_location):
                    print('[anime-dl] File Exists! Skipping {0}\n'.format(file_name))
                    pass
                else:
                    subs_downloaded = supporters.sub_fetcher.crunchyroll_subs(xml=str(xml_page_connect), episode_number=episode_number, file_name=file_name)
                    if not subs_downloaded:
                        pass
                    m3u8_downloaded = self.m3u8_downloader(url=m3u8_file_link, cookies=cookies, resolution_to_find=resolution_to_find, file_name=file_name)
                    if m3u8_downloaded:
                        sub_files = self.sub_prepare()
                        font_files = [os.path.realpath(font_file) for font_file in
                                      glob(str(os.getcwd()) + "/Fonts/*.*")]

                        fonts = '--attachment-mime-type application/x-truetype-font --attach-file "' + str(
                            '" --attachment-mime-type application/x-truetype-font --attach-file "'.join(
                                font_files)) + '"'

                        if len(font_files) == 0:
                            fonts = ''

                        is_stream_muxed = self.stream_muxing(file_name=file_name, subs_files=sub_files, fonts=fonts, output_directory=output_directory)
                        if is_stream_muxed:
                            is_file_moved = self.move_video_file(output_directory = output_directory)
                            if is_file_moved:
                                is_cleaned = self.material_cleaner()
                                if is_cleaned:
                                    print("{0} - {1} successfully downloaded.\n".format(anime_name, episode_number))
                                else:
                                    print("Couldn't remove the leftover files.")
                                    pass
                            else:
                                print("Couldn't move the file.")
                                pass
                        else:
                            print("Stream couldn't be muxed. Make sure MKVMERGE is in the path.")
                            pass
                    else:
                        print("Couldn't download the m3u8 file.")
                        pass
            else:
                print("Couldn't find the stream.")
                pass
        else:
            print("Couldn't Connect To XML Page.")
            pass

    def whole_show(self, url, cookie, token, language, resolution, skipper, episode_range):
        response, page_source, episode_list_cookies = anime_dl.common.browser_instance.page_downloader(url=url, cookies=cookie)

        if response:
            dub_list, ep_sub_list = self.episode_list_extractor(page_source=page_source, url=url)
            ep_sub_list = self.sub_list_editor(episode_range=episode_range, ep_sub_list=ep_sub_list)

            if skipper == "yes":
                # print("DLing everything")
                print("Total Subs to download : %s" % len(ep_sub_list))
                for episode_url in ep_sub_list[::-1]:
                    # cookies, Token = self.webpagedownloader(url=url)
                    # print("Sub list : %s" % sub_list)
                    self.only_subs(url=episode_url, cookies=cookie, resolution=resolution)

                    print("-----------------------------------------------------------")
                    print("\n")
            else:
                if str(language).lower() in ["english", "eng", "dub"]:
                    # If the "dub_list" is empty, that means there are no English Dubs for the show, or CR changed something.
                    if len(dub_list) == 0:
                        print("No English Dub Available For This Series.")
                        print(
                            "If you can see the Dubs, please open an Issue on https://github.com/Xonshiz/anime-dl/issues/new")
                        exit(1)
                    else:
                        print("Total Episodes to download : %s" % len(dub_list))
                        for episode_url in dub_list[::-1]:
                            # cookies, Token = self.webpagedownloader(url=url)
                            # print("Dub list : %s" % dub_list)
                            try:
                                self.single_episode(url=episode_url, cookies=cookie, token=token, resolution=resolution)
                            except Exception as SomeError:
                                print("Error Downloading : {0}".format(SomeError))
                                pass
                            print("-----------------------------------------------------------")
                            print("\n")
                else:
                    print("Total Episodes to download : %s" % len(ep_sub_list))

                    for episode_url in ep_sub_list[::-1]:
                        # cookies, Token = self.webpagedownloader(url=url)
                        # print("Sub list : %s" % sub_list)
                        try:
                            self.single_episode(url=episode_url, cookies=cookie, token=token, resolution=resolution)
                        except Exception as SomeError:
                            print("Error Downloading : {0}".format(SomeError))
                            pass
                        print("-----------------------------------------------------------")
                        print("\n")
        else:
            print("Couldn't connect to Crunchyroll. Failed.")
            exit(1)

    def episode_list_extractor(self, page_source, url):
        dub_list = []
        ep_sub_list = []
        chap_holder_div = page_source.find_all('a', {'class': 'portrait-element block-link titlefix episode'})

        for single_node in chap_holder_div:
            href_value = single_node["href"]
            title_value = single_node["title"]
            if "(Dub)" in str(title_value):
                dub_list.append(str(url) + "/" + str(str(href_value).split("/")[-1]))
            else:
                ep_sub_list.append(str(url) + "/" + str(str(href_value).split("/")[-1]))

        if len(dub_list) == 0 and len(ep_sub_list) == 0:
            print("Could not find the show links. Report on https://github.com/Xonshiz/anime-dl/issues/new")
            exit(0)
        else:
            return dub_list, ep_sub_list

    def sub_list_editor(self, episode_range, ep_sub_list):
        if episode_range != "All":
            # -1 to shift the episode number accordingly to the INDEX of it. List starts from 0 xD!
            starting = int(str(episode_range).split("-")[0]) - 1
            ending = int(str(episode_range).split("-")[1])
            indexes = [x for x in range(starting, ending)]
            # [::-1] in sub_list in beginning to start this from the 1st episode and at the last, it is to reverse the list again, becasue I'm reverting it again at the end.
            return [ep_sub_list[::-1][x] for x in indexes][::-1]
        else:
            return ep_sub_list

    def episode_information_extractor(self, page_source, resolution_to_find):
        anime_name = re.sub(r'[^A-Za-z0-9\ \-\' \\]+', '', str(re.search(r'<series_title>(.*?)</series_title>', page_source).group(1))).title().strip()
        episode_number = re.search(r'<episode_number>(.*?)</episode_number>', page_source.decode("utf-8")).group(1)
        video_width, video_height = resolution_to_find.split("x")
        video_resolution = str(video_width) + "x" + str(video_height)

        return anime_name, episode_number, video_resolution

    def stream_muxing(self, file_name, subs_files, fonts, output_directory):
        mkv_merge_command = 'mkvmerge --output "%s" ' % str(file_name).replace(".mp4", ".mkv") + '"' + str(file_name) + '" ' + ' '.join(subs_files) + ' ' + str(fonts)

        logging.debug("mkv_merge_command : %s", mkv_merge_command)

        try:
            subprocess.check_call(mkv_merge_command, shell=True)
            return True
            # if call:
            #     return True
            # else:
            #     return False
        except Exception as FileMuxingException:
            print("Sees like I couldn't mux the files.\n")
            print("Check whether the MKVMERGE.exe is in PATH or not.\n")
            print(str(FileMuxingException) + "\n")
            fallback = self.stream_not_muxed_fallback(output_directory=output_directory)
            return False

    def stream_not_muxed_fallback(self, output_directory):
        try:
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
            return True
        except Exception:
            return False

    def move_video_file(self, output_directory):
        try:
            for video_file in glob("*.mkv"):
                try:
                    move(video_file, output_directory)
                except Exception as e:
                    # print(str(e))
                    pass
            return True
        except Exception:
            exit(1)

    def move_subtitle_file(self, output_directory):
        try:
            for video_file in glob("*.ass"):
                try:
                    move(video_file, output_directory)
                except Exception as e:
                    # print(str(e))
                    pass
            return True
        except Exception:
            exit(1)

    def material_cleaner(self):
        try:
            for video in glob("*.mp4"):
                os.remove(os.path.realpath(video))

            for sub_file_delete in glob("*.ass"):
                os.remove(os.path.realpath(sub_file_delete))
            return True
        except Exception:
            exit(1)

    def m3u8_downloader(self, url, cookies, resolution_to_find, file_name):
        response_value, m3u8_file_connect, updated_cookies = anime_dl.common.browser_instance.page_downloader(url=url, cookies=cookies)
        try:
            m3u8_file_text = None

            next_line_is_good = False
            for i, currentLine in enumerate(m3u8_file_connect.text.splitlines()):
                if next_line_is_good:
                    m3u8_file_text = currentLine
                    logging.debug("file to download : {0}".format(m3u8_file_text))
                    break
                elif currentLine.startswith("#EXT-X") and resolution_to_find in currentLine:
                    next_line_is_good = True

            if m3u8_file_text is None:
                print('Could not find the requested resolution {0} in the m3u8 file\n'.format(file_name))
                exit(1)

            self.ffmpeg_call(m3u8_file_text, file_name)
            return True

        except Exception:
            print("Exception Occurred In m3u8 File.")
            exit(1)

    def sub_prepare(self):
        subtitles_files = []
        for sub_file in glob("*.ass"):
            if sub_file.endswith(".enUS.ass"):
                subtitles_files.insert(0,
                                       "--track-name 0:English_US --ui-language en_US --language 0:eng --default-track 0:yes --sub-charset 0:utf-8 " + '"' + str(
                                           os.path.realpath(sub_file)) + '" ')

            elif sub_file.endswith(".enGB.ass"):
                subtitles_files.append(
                    "--track-name 0:English_UK --ui-language en_US --language 0:eng --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                        os.path.realpath(sub_file)) + '" ')

            elif sub_file.endswith(".esLA.ass"):
                subtitles_files.append(
                    "--track-name 0:Espanol --ui-language es_ES --language 0:spa --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                        os.path.realpath(sub_file)) + '" ')
            elif sub_file.endswith(".esES.ass"):
                subtitles_files.append(
                    "--track-name 0:Espanol_Espana --ui-language es_ES --language 0:spa --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                        os.path.realpath(sub_file)) + '" ')
            elif sub_file.endswith(".ptBR.ass"):
                subtitles_files.append(
                    "--track-name 0:Portugues_Brasil --ui-language pt_BR --language 0:por --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                        os.path.realpath(sub_file)) + '" ')
            elif sub_file.endswith(".ptPT.ass"):
                subtitles_files.append(
                    "--track-name 0:Portugues_Portugal --ui-language pt_PT --language 0:por --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                        os.path.realpath(sub_file)) + '" ')
            elif sub_file.endswith(".frFR.ass"):
                subtitles_files.append(
                    "--track-name 0:Francais_France --ui-language fr_FR --language 0:fre --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                        os.path.realpath(sub_file)) + '" ')
            elif sub_file.endswith(".deDE.ass"):
                subtitles_files.append(
                    "--track-name 0:Deutsch --ui-language de_DE --language 0:ger --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                        os.path.realpath(sub_file)) + '" ')
            elif sub_file.endswith(".arME.ass"):
                subtitles_files.append(
                    "--track-name 0:Arabic --language 0:ara --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                        os.path.realpath(sub_file)) + '" ')
            elif sub_file.endswith(".itIT.ass"):
                subtitles_files.append(
                    "--track-name 0:Italiano --ui-language it_IT --language 0:ita --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                        os.path.realpath(sub_file)) + '" ')
            elif sub_file.endswith(".trTR.ass"):
                subtitles_files.append(
                    "--track-name 0:Turkce --ui-language tr_TR --language 0:tur --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                        os.path.realpath(sub_file)) + '" ')
            else:
                subtitles_files.append(
                    "--track-name 0:und --default-track 0:no --sub-charset 0:utf-8 " + '"' + str(
                        os.path.realpath(sub_file)) + '" ')

        subs_files = anime_dl.common.misc.duplicate_remover(subtitles_files)
        logging.debug("subs_files : {0}".format(subs_files))
        return subs_files

    def only_subs(self, url, cookies, resolution):
        video_id = str(url.split('-')[-1]).replace("/", "")
        logging.debug("video_id : {0}".format(video_id))

        response, resolution_to_find, info_url = self.resolution_finder(resolution=resolution, video_id=video_id, url=url)

        if not response:
            print("No Resolution Found")
            exit(1)

        response_value, xml_page_connect, xml_cookies = anime_dl.common.browser_instance.page_downloader(url=info_url,
                                                                                                         cookies=cookies)

        if xml_page_connect:
            xml_page_connect = str(xml_page_connect)
            stream_exists, m3u8_file_link = self.m3u8_finder(xml_page_source=xml_page_connect)

            if stream_exists:
                anime_name, episode_number, video_resolution = self.episode_information_extractor(
                    page_source=xml_page_connect, resolution_to_find=resolution_to_find)
                file_name = supporters.anime_name.crunchyroll_name(anime_name=anime_name, episode_number=episode_number,
                                                                   resolution=video_resolution)
                output_directory = supporters.path_works.path_creator(anime_name=anime_name)
                file_location = str(output_directory) + os.sep + str(file_name).replace(".mp4", ".ass")

                if os.path.isfile(file_location):
                    print('[anime-dl] File Exists! Skipping {0}\n'.format(file_name))
                    pass
                else:
                    subs_downloaded = supporters.sub_fetcher.crunchyroll_subs(xml=str(xml_page_connect),
                                                                              episode_number=episode_number,
                                                                              file_name=file_name)
                    if not subs_downloaded:
                        pass
                    else:
                        subtitles_moved = self.move_subtitle_file(output_directory)
                        if subtitles_moved:
                            return True
                        else:
                            return False
            else:
                print("Stream Not Found. Subtitle Downloading Failed.")
                return False


    def ffmpeg_call(self, m3u8_text, file_name):
        try:
            ffmpeg_command = 'ffmpeg -i "{0}" -c copy -bsf:a aac_adtstoasc "{1}/{2}"'.format(m3u8_text, os.getcwd(),
                                                                                             file_name)
            logging.debug("ffmpeg_command : {0}\n".format(ffmpeg_command))
            call = subprocess.check_call(ffmpeg_command, shell=True)
            if call:
                return True
            else:
                return False
        except Exception:
            return False

    def m3u8_finder(self, xml_page_source):
        m3u8_file_link = str(re.search(r'<file>(.*?)</file>', xml_page_source).group(1)).replace("&amp;", "&")
        logging.debug("m3u8_file_link : %s", m3u8_file_link)

        if not m3u8_file_link:
            # If no m3u8 found, try the rtmpdump...
            try:
                host_link = re.search(r'<host>(.*?)</host>', xml_page_source).group(1)
                logging.debug("Found RTMP DUMP!")
                print("RTMP streams not supported currently...")
                return False, None
            except Exception as NoRtmpDump:
                print("No RTMP Streams Found...")
                print(NoRtmpDump)
        else:
            return True, m3u8_file_link

    def resolution_finder(self, resolution, video_id, url):
        resolution_to_find = None
        info_url = ""

        if str(resolution).lower() in ['1080p', '1080', 'fhd', 'best']:
            info_url = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id=%s&video_format=108&video_quality=80&current_page=%s" % (
                video_id, url)
            resolution_to_find = "1920x1080"

        elif str(resolution).lower() in ['720p', '720', 'hd']:
            info_url = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id=%s&video_format=106&video_quality=62&current_page=%s" % (
                video_id, url)
            resolution_to_find = "1280x720"

        elif str(resolution).lower() in ['480p', '480', 'sd']:
            info_url = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id=%s&video_format=106&video_quality=61&current_page=%s" % (
                video_id, url)
            resolution_to_find = "848x480"
        elif str(resolution).lower() in ['360p', '360', 'cancer']:
            info_url = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id=%s&video_format=106&video_quality=60&current_page=%s" % (
                video_id, url)
            resolution_to_find = "640x360"
        elif str(resolution).lower() in ['240p', '240', 'supracancer']:
            info_url = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id=%s&video_format=106&video_quality=60&current_page=%s" % (
                video_id, url)
            resolution_to_find = "428x240"

        logging.debug("info_url : {0}".format(info_url))

        if resolution_to_find is None:
            print('Unknown requested resolution %s' % str(resolution).lower())
            return False, None, None

        else:
            return True, resolution_to_find, info_url
