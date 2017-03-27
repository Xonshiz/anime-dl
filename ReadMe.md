# Anime-DL | [![Build Status](https://travis-ci.org/Xonshiz/anime-dl.svg?branch=master)](https://travis-ci.org/Xonshiz/anime-dl) [![Documentation Status](https://readthedocs.org/projects/anime-dl/badge/?version=latest)](http://anime-dl.readthedocs.io/en/latest/?badge=latest) | [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/xonshiz)

Anime-dl is a Command-line program to download anime from CrunchyRoll and Funimation. This script needs you to have a premium subscription to the listed services. If you don't have a subscription, this script is pretty much usless for you.

> Downloading and distributing this content may be illegal.This script was written for education purposes purely and you are responsible for its use.

> Support these anime streaming websites by buying a premium account.

> Taking some libs directly from youtube-dl to decrypt CrunchyRoll's subtitles.

## Table of Content

* [Supported Sites](https://github.com/Xonshiz/anime-dl/blob/master/Supported_Sites.md)
* [Dependencies Installation](#dependencies-installation)
* [Installation](#installation)
* [Python Support](#python-support)
* [Windows Binary](#windows-binary)
* [List of Arguments](#list-of-arguments)
* [Usage](#usage)
    * [Windows](#windows)
    * [Linux/Debian](#linuxdebian)
    * [Example URLs](#example-urls)
* [Features](#features)
* [Changelog](https://github.com/Xonshiz/anime-dl/blob/master/Changelog.md)
* [Opening An Issue/Requesting A Site](#opening-an-issuerequesting-a-site)
    * [Reporting Issues](#reporting-issues)
    * [Suggesting A Feature](#suggesting-a-feature)
* [Donations](#donations)

## Supported Websites
You can check the list of supported websites [**`HERE`**](https://github.com/Xonshiz/anime-dl/blob/master/Supported_Sites.md).

## Dependencies Installation
This script can run on multiple Operating Systems. So, if you're using the `python` script instead of the `windows binary` of this script, then you'll need to get things ready first. Since this script doesn't rely on a lot of external dependencies, you just need to grab a few things, same for all operating systems.

1.) Make sure you have Python installed and is present in your system's path.
2.) Grab [FFmpeg from this link.](https://ffmpeg.org/download.html)
3.) Install FFmpeg and place it in the directory of this script, or put FFmpeg in your system's path.
4.) Browse to the directory of this script and open command prompt/shell in that directory and run this command :
```
python pip install -r requirements.txt
```

## Installation
After installing and setting up all the dependencies in your Operating System, you're good to go and use this script.
The instructions for all the OS would remain same. Download [`THIS REPOSITORY`](https://github.com/Xonshiz/anime-dl/archive/master.zip) and put it somewhere in your system. Move over the `anime_dl` folder.

**Windows users**, it's better to not place it places where it requires administrator privileges. Good example would be `C:\Windows`. This goes for both, the Python script and the windows binary file (.exe).

**Linux/Debian** users make sure that this script is executable.just run this command, if you run into problem(s) :

`chmod +x anime-dl.py`
`chmod +x __main__.py`

and then, execute with this :

`./anime-dl.py`
`./__main__.py`

## Python Support
This script supports only Pythom 3 currently..

## Windows Binary
It is recommended that windows users use this binary to save both, your head and time from installing all the dependencies. 

You need to download [FFmpeg](https://ffmpeg.org/download.html) and keep it in the same directory as that of this windows binary file or you need to have PhantomJS in your path. 

If you already have it, then you can download this binary and start using the script right off the bat :
* `Binary (x86)` : [Click Here](https://github.com/Xonshiz/anime-dl/releases/latest)


## List of Arguments
Currently, the script supports these arguments :
```
-h, --help                             Prints the basic help menu of the script and exits.
-i,--input                             Defines the input link to the anime.
-V,--version                           Prints the VERSION and exits.
-u,--username                          Indicates username for a website.
-p,--password                          Indicates password for a website.
-r,--resolution                        Indicates the desired resolution. (default = 720p)
-l,--language                          Selects the language for the show. (default = Japanese) [Langs = english, dub, sub, Japanese, eng]
```

## Usage
With this script, you have to pass arguments in order to be able to download anything. Passing arguments in a script is pretty easy. Since the script is pretty basic, it doesn't have too many arguments. Go check the [`ARGUMENTS SECTION`](https://github.com/Xonshiz/anime-dl#list-of-arguments) to know more about which arguments the script offers.

Follow the instructions according to your OS :

### Windows
After you've saved this script in a directory/folder, you need to open `command prompt` and browse to that directory and then execute the script. Let's do it step by step :
* Open the folder where you've downloaded the files of this repository.
* Hold down the **`SHIFT`** key and while holding down the SHIFT key, **`RIGHT CLICK`** and select `Open Command Prompy Here` from the options that show up.
* Now, in the command prompt, type this :

*If you're using the windows binary :*

`anime-dl.exe -i "<URL TO THE ANIME>" -u "YourUsername" -p "Password" -r "Resolution"`

*If you're using the Python Script :*

`__main__.py -i "<URL TO THE ANIME>" -u "YourUsername" -p "Password" -r "Resolution"`

URL can be any URL of the [supported websites](https://github.com/Xonshiz/anime-dl/blob/master/Supported_Sites.md).

### Linux/Debian
After you've saved this script in a directory/folder, you need to open `command prompt` and browse to that directory and then execute the script. Let's do it step by step :
* Open a terminal, `Ctrl + Alt + T` is the shortcut to do so (if you didn't know).
* Now, change the current working directory of the terminal to the one where you've downloaded this repository.
* Now, in the Terminal, type this :

`__main__.py -i "<URL TO THE ANIME>" -u "YourUsername" -p "Password" -r "Resolution"`

URL can be any URL of the [supported websites](https://github.com/Xonshiz/anime-dl/blob/master/Supported_Sites.md).

### Example URLs
* Crunchyroll :
    * Single Episode : [http://www.crunchyroll.com/i-cant-understand-what-my-husband-is-saying/episode-13-happy-days-678059](http://www.crunchyroll.com/i-cant-understand-what-my-husband-is-saying/episode-13-happy-days-678059)
    * Whole Show : [http://www.crunchyroll.com/i-cant-understand-what-my-husband-is-saying](http://www.crunchyroll.com/i-cant-understand-what-my-husband-is-saying)


## Features
This is a very basic and small sript, so at the moment it only have a few features.
* Downloads a Single episode along with all the available subtitles for that episode.
* Downloads and puts them all in a directory named "Output".
* Skip if the file has already been downloaded.

## Changelog
You can check the changelog [**`HERE`**](https://github.com/Xonshiz/anime-dl/blob/master/Changelog.md).

## Opening An Issue/Requesting A Site
If your're planning to open an issue for the script or ask for a new feature or anything that requires opening an Issue, then please do keep these things in mind.

### Reporting Issues
Please do make sure that you read and follow this :
 
### Suggesting A Feature
If you're here to make suggestions, please follow the basic syntax to post a request :

**Subject** : Something that briefly tells us about the feature.

**Long Explanation** : Describe in details what you want and how you want.

This should be enough, but it'll be great if you can add more ;)

# Donations
You can always send some money over from this :

Paypal : [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/xonshiz)

Patreon Link : https://www.patreon.com/xonshiz

Any amount is appreciated :)
