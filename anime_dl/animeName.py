import re
import subprocess

class animeName(object):

    def nameEdit(self, animeName, episodeNumber, resolution):
        rawName = str(animeName).title().strip().replace("Season ", "S") + " - " + str(episodeNumber).strip() + " [" + str(resolution) + "]"
        fileName = str(re.sub(r'[^A-Za-z0-9\ \-\' \\]+', '', str(animeName))).title().strip().replace("Season ", "S") + " - " + str(episodeNumber).strip() + " [" + str(resolution) + "].mp4"

        try:
            MAX_PATH = int(subprocess.check_output(['getconf', 'PATH_MAX', '/']))
                # print(MAX_PATH)
        except (Exception):
            MAX_PATH = 4096

        if len(fileName) > MAX_PATH:
            file_name = fileName[:MAX_PATH]

        return fileName

    def nameEditFuni(self, animeName, seasonNumber, episodeNumber, resolution):
        rawName = str(animeName).title().strip().replace("Season ", "S") + " - " + "S%s E%s" % (str(seasonNumber).strip(), str(episodeNumber).strip()) + " [" + str(resolution) + "]"
        fileName = str(re.sub(r'[^A-Za-z0-9\ \-\' \\]+', '', str(animeName))).title().strip().replace("Season ", "S") + " - " + str(episodeNumber).strip() + " [" + str(resolution) + "].mp4"

        try:
            MAX_PATH = int(subprocess.check_output(['getconf', 'PATH_MAX', '/']))
                # print(MAX_PATH)
        except (Exception):
            MAX_PATH = 4096

        if len(fileName) > MAX_PATH:
            file_name = fileName[:MAX_PATH]

        return fileName