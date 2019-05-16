#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def path_creator(anime_name):
    output_directory = os.path.abspath("Output" + os.sep + str(anime_name) + "/")
    if not os.path.exists("Output"):
        os.makedirs("Output")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    return output_directory
