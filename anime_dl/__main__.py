#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__author__ = "Xonshiz"
__email__ = "xonshiz@psychoticelites.com"
"""

from AnimeDL import *
# from anime_dl import AnimeDL
from sys import exit
from version import __version__
import argparse
import logging
import platform


class main():
    if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='Anime_DL downloads anime from CrunchyRoll and Funimation.')

        parser.add_argument('--version', action='store_true', help='Shows version and exits.')

        required_args = parser.add_argument_group('Required Arguments :')
        required_args.add_argument('-p', '--password', nargs=1, help='Indicates password for a website.')
        required_args.add_argument('-u', '--username', nargs=1, help='Indicates username for a website.')
        required_args.add_argument('-i', '--input', nargs=1, help='Inputs the URL to anime.')
        parser.add_argument('-r', '--resolution', nargs=1, help='Inputs the URL to anime.', default='720p')
        parser.add_argument('-l', '--language', nargs=1, help='Selects the language for the show.', default='Japanese')
        parser.add_argument('-rn', '--range', nargs=1, help='Specifies the range of episodes to download.',
                            default='All')
        parser.add_argument('--skip', action='store_true', help='skips the video download and downloads only subs.')
        parser.add_argument("-v", "--verbose", help="Prints important debugging messages on screen.",
                            action="store_true")
        logger = "False"
        args = parser.parse_args()
        skipper = "no"

        if args.verbose:
            logging.basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=logging.DEBUG)
            logging.debug('You have successfully set the Debugging On.')
            logging.debug("Arguments Provided : %s" % (args))
            logging.debug(
                "Operating System : %s - %s - %s" % (platform.system(), platform.release(), platform.version()))
            logging.debug("Python Version : %s (%s)" % (platform.python_version(), platform.architecture()[0]))
            logger = "True"

        if args.version:
            print("Current Version : %s" % __version__)
            exit()

        if args.skip:
            print("Will be skipping video downloads")
            skipper = "yes"

        if args.username is None or args.password is None or args.input is None:
            print("Please enter the required arguments. Run __main__.py --help")
            exit()
        else:
            # If the argument has been provided for resolution and language,
            # they're going to be lists, otherwise, they're
            # going to be simple value == 720p.
            # So, if return type comes out to be list, send the first element, otherwise, send 720p as it is.
            # Same approach for the audio as well.

            if type(args.resolution) == list:
                args.resolution = args.resolution[0]
            if type(args.language) == list:
                args.language = args.language[0]
            if type(args.range) == list:
                args.range = args.range[0]

            AnimeDL(url=args.input, username=args.username, password=args.password,
                    resolution=args.resolution, language=args.language, skipper=skipper,
                    logger=logger, episode_range=args.range)
