#!/usr/bin/env python
# -*- coding: utf-8 -*-

import anime_dl.common
from anime_dl.external.aes import aes_cbc_decrypt
from anime_dl.external.compat import compat_etree_fromstring
from anime_dl.external.utils import bytes_to_intlist, intlist_to_bytes
import re
import logging
import os
import base64
import zlib
from hashlib import sha1
from math import pow, sqrt, floor


def crunchyroll_subs(xml, episode_number, file_name):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7',
        'Referer':
            'https://www.crunchyroll.com'
    }
    for sub_id, sub_lang, sub_lang2 in re.findall(
            r'subtitle_script_id\=(.*?)\"\ title\=\"\[(.*?)\]\ (.*?)\"',
            str(xml)):
        xml_return = anime_dl.common.browser_instance.page_downloader(url="http://www.crunchyroll.com/xml/?req=RpcApiSubtitle_GetXml&subtitle_script_id={0}".format(sub_id), headers=headers)

        iv = str(re.search(r'\<iv\>(.*?)\<\/iv\>', str(xml_return)).group(1)).strip()
        data = str(re.search(r'\<data\>(.*?)\<\/data\>', str(xml_return)).group(1)).strip()
        subtitle = _decrypt_subtitles(data, iv, sub_id).decode('utf-8')
        sub_root = compat_etree_fromstring(subtitle)
        sub_data = _convert_subtitles_to_ass(sub_root)
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
    return True


def _decrypt_subtitles(data, iv, id):
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


def _convert_subtitles_to_ass(sub_root):
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
