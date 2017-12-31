# Anime-DL | [![Build Status](https://travis-ci.org/Xonshiz/anime-dl.svg?branch=master)](https://travis-ci.org/Xonshiz/anime-dl) [![Documentation Status](https://readthedocs.org/projects/anime-dl/badge/?version=latest)](http://anime-dl.readthedocs.io/en/latest/?badge=latest) | [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/xonshiz) | [![GitHub release](https://img.shields.io/github/release/xonshiz/anime-dl.svg?style=flat-square)](https://github.com/xonshiz/anime-dl/releases/latest) | [![Github All Releases](https://img.shields.io/github/downloads/xonshiz/anime-dl/total.svg?style=flat-square)](https://github.com/xonshiz/anime-dl/releases)

Anime-dl is a Command-line program to download anime from CrunchyRoll and Funimation. This script needs you to have a premium subscription for the listed services. If you don't have a subscription, this script is pretty much usless for you.

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
This script can run on multiple Operating Systems. But, the script depends on some external binaries or libs. We need `FFmpeg`, `mkvmerge` and `Node.js` in our paths. There are some old streams on Crunchyroll which only support `rtmpe` streams, as noted from Issue #9. For this, you need `rtmpdump`.

You also need [mkvmerge.exe](https://mkvtoolnix.download/downloads.html) in your `PATH` or `Working Directory`.


**`These dependencies are required on ALL the operating systems, ALL!.`**

1.) Make sure you have Python installed and is present in your system's path.

2.) Grab [FFmpeg from this link](https://ffmpeg.org/download.html), [Node.js from this link](https://nodejs.org/en/download/) and [RTMPDump](https://www.videohelp.com/software/RTMPDump).

3.) Install FFmpeg and Node.js and place it in the directory of this script, or put them in your system's path.

4.) Browse to the directory of this script and open command prompt/shell in that directory and run this command :

```
python pip install -r requirements.txt
```

## Installation
After installing and setting up all the dependencies in your Operating System, you're good to go and use this script.
The instructions for all the OS would remain same. Download [`THIS REPOSITORY`](https://github.com/Xonshiz/anime-dl/archive/master.zip) and put it somewhere in your system. Move over the `anime_dl` folder.

**Windows users**, it's better to not place it places where it requires administrator privileges. Good example of places to avoid would be `C:\Windows` etc.. This goes for both, the Python script and the windows binary file (.exe).

**Linux/Debian** users make sure that this script is executable.Just run this command, if you run into problem(s) :

`chmod +x anime-dl.py`

`chmod +x __main__.py`

and then, execute with this :

`./__main__.py`

## Python Support
This script supports only Pythom 3 currently..

## Windows Binary
It is recommended that windows users use this binary to save both, your head and time from installing all the dependencies. 

You need to download [FFmpeg](https://ffmpeg.org/download.html) and [Node.js](https://nodejs.org/en/download/) and keep them in the same directory as that of this windows binary file.

If you already have these dependencies, then you can download this binary and start using the script right off the bat :
* `Binary (x86)` : [Click Here](https://github.com/Xonshiz/anime-dl/releases/latest)


## List of Arguments
Currently, the script supports these arguments :
```
-h, --help                             Prints the basic help menu of the script and exits.
-i,--input                             Defines the input link to the anime.
-V,--version                           Prints the VERSION and exits.
-u,--username                          Indicates username for a website. [REQUIRED]
-p,--password                          Indicates password for a website. [REQUIRED]
-r,--resolution                        Indicates the desired resolution. (default = 720p)
--skip                                 Skip video downloads (Will only download subtitles)
-v,--verbose                           Starts Verbose Logging for detailed information.
-l,--language                          Selects the language for the show. (default = Japanese) [Langs = english, dub, sub, Japanese, eng]
-rn,--range                            Selects the range of episodes to download (Default = All) [ Ex : --range 1-10 (This will download first 10 episodes of a series)]
```

## Usage
With this script, you have to pass arguments in order to be able to download anything. Passing arguments in a script is pretty easy. Since the script is pretty basic, it doesn't have too many arguments. Go check the [`ARGUMENTS SECTION`](https://github.com/Xonshiz/anime-dl#list-of-arguments) to know more about which arguments the script offers.

Follow the instructions according to your OS :

### Windows
After you've saved this script in a directory/folder, you need to open `command prompt` and browse to that directory and then execute the script. Let's do it step by step :
* Open the folder where you've downloaded the files of this repository.
* Hold down the **`SHIFT`** key and while holding down the SHIFT key, **`RIGHT CLICK`** and select `Open Command Prompt Here` from the options that show up. <sup>*PowerShell users see below*</sup>
* Now, in the command prompt, type this :

*If you're using the windows binary :*

`anime-dl.exe -i "<URL TO THE ANIME>" -u "YourUsername" -p "Password" -r "Resolution"`

*If you're using the Python Script :*

`__main__.py -i "<URL TO THE ANIME>" -u "YourUsername" -p "Password" -r "Resolution"`

URL can be any URL of the [supported websites](https://github.com/Xonshiz/anime-dl/blob/master/Supported_Sites.md).

### PowerShell Note :
* With Windows 10, the default option when shift-right clicking is to open PowerShell instead of a command window.  When using PowerShell instead of the command prompt, you must make sure that the dependencies directory is in the path or it will not be found.
* [It is possible to enable `Open Command Window Here` in Windows 10](https://superuser.com/questions/1201988/how-do-i-change-open-with-powershell-to-open-with-command-prompt-when-shift).

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

### Note :

* If you want to include some fonts in the muxed video, you need to make a folder named "Fonts" in the same directory as that of this script and put all the fonts inside that directory. The script should take them all.

## Features
This is a very basic and small sript, so at the moment it only have a few features.
* Downloads a Single episode along with all the available subtitles for that episode.
* Downloads and puts them all in a directory named "Output".
* Skip if the file has already been downloaded.
* Downloads all the episodes for a show available on Crunchyroll.
* Gives choice for downloading subs or dubs of a series available on Crunchyroll.
* Choice to download only the subs and skip the videos.

## Changelog
You can check the changelog [**`HERE`**](https://github.com/Xonshiz/anime-dl/blob/master/Changelog.md).

## Opening An Issue/Requesting A Site
If your're planning to open an issue for the script or ask for a new feature or anything that requires opening an Issue, then please do keep these things in mind.

### Reporting Issues
PLEASE RUN THIS SCRIPT IN A COMMAND LINE (as mentioned in the Usage section) AND DON'T SAY THAT `THE SCRIPT CLOSED TOO QUICK, I COULDN'T SEE`. If something doesn't work like it's supposed to, run the command with the `--verbose` argument. It'll create a `Error Log.txt` file in the same directory. Upload the content of that file on Github Gists/Pastebin etc. and share that link.

**Please make sure that you remove your loggin credentials from the Error Log.txt file before you post its contents anywhere.**

If you're here to report an issue, please follow the basic syntax to post a request :

**Subject** : Error That You Get.

**Command Line Arguments You Gave** : The whole command that you gave to execute/run this script.

**Verbose Log Link** : Link to the Gist/Pastebin that holds the content of Error Log.txt.

**Long Explanation** : Describe in details what you saw, what should've happened and what actually happened.

This should be enough, but it'll be great if you can add more ;)
 
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
