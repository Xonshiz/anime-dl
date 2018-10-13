#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess

class animeName(object):

    def nameEdit(self, animeName, episodeNumber, resolution):
        animeName = str(animeName).replace("039T", "'")
        rawName = str(animeName).title().strip().replace("Season ", "S") + " - " +\
                  str(episodeNumber).strip() + " [" + str(resolution) + "]"
        file_name = str(re.sub(r'[^A-Za-z0-9\ \-\' \\]+', '', str(animeName))).title().strip().replace("Season ", "S")\
                   + " - " + str(episodeNumber.zfill(2)).strip() + " [" + str(resolution) + "].mp4"

        try:
            max_path = int(subprocess.check_output(['getconf', 'PATH_MAX', '/']))
            # print(MAX_PATH)
        except (Exception):
            max_path = 4096

        if len(file_name) > max_path:
            file_name = file_name[:max_path]

        return file_name

    def nameEditFuni(self, animeName, seasonNumber, episodeNumber, resolution):
        rawName = str(animeName).title().strip().replace("Season ", "S") + " - " + "S%s E%s" %\
                                                                                   (str(seasonNumber).strip(),
                                                                                    str(episodeNumber).strip())\
                  + " [" + str(resolution) + "]"
        file_name = str(re.sub(r'[^A-Za-z0-9\ \-\' \\]+', '', str(animeName))).title().strip().replace("Season ", "S") \
                   + " - " + str(episodeNumber.zfill(2)).strip() + " [" + str(resolution) + "].mp4"

        try:
            max_path = int(subprocess.check_output(['getconf', 'PATH_MAX', '/']))
            # print(MAX_PATH)
        except (Exception):
            max_path = 4096

        if len(file_name) > max_path:
            file_name = file_name[:max_path]

        return file_name
