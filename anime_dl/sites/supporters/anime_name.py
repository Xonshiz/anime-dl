#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess


def crunchyroll_name(anime_name, episode_number, resolution):
    anime_name = str(anime_name).replace("039T", "'")
    # rawName = str(animeName).title().strip().replace("Season ", "S") + " - " + \
    #           str(episode_number).strip() + " [" + str(resolution) + "]"

    file_name = str(re.sub(r'[^A-Za-z0-9\ \-\' \\]+', '', str(anime_name))).title().strip().replace("Season ", "S") \
                + " - " + str(episode_number.zfill(2)).strip() + " [" + str(resolution) + "].mp4"

    try:
        max_path = int(subprocess.check_output(['getconf', 'PATH_MAX', '/']))
    except Exception:
        max_path = 4096

    if len(file_name) > max_path:
        file_name = file_name[:max_path]

    return file_name
