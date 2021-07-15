# sukebei-crwaler-v2
Sukebei-crawler brings you latest torrents and magnet links with most seeders.

## Watch [demo]
Execution snapshot
![N|Solid](https://github.com/Freddy930727/sukebei-crawler-v2/blob/master/snapshot.JPG?raw=true)
## Features
- Magnet link is available.
- Automatically save download history in order to prevent overlapping torrents
- Several filters are supported, inclusive of date, category, keyword, and quantity.
- Gui based on html and js, so you can execute it on any system with any browser.
## Usage
 - In /div, execute`python3 main.py`(This version is made for windows system instead of linux.)

## pip setup
```
pip install eel
pip install requests
pip install lxml
pip install bs4
```

## Notice
 - Browser is required.
 - Don't kill the programe while running, else the history.csv will crash.
 - This python script works well on windows machine. If you want to run it on Linux, several modifications related to os path is required.
 - Hinet(色情守門員) would block sukebei.nyaa.si ,so don't forget to gain a vpn access if you need to bypass it.
 - If your torrent software have a function that asks you where to download or set some setting, don't forget to turn it off, so that your computer won't crash when you execute it with magnet link argument.(Like the .gif below).
![N|Solid](https://github.com/Freddy930727/sukebei-crawler-v2/blob/master/disaster.gif?raw=true)

## Goal given up😢
 - I can't distinguish wether current page is the last one or not. Since sukebei.nyaa.si crashs so FREQUENTLY that I can't tell a crashed web from the page out of index.
## Contribution
 - Contributions and issues are wellcomed. If you are interested in this project or you have some innovative ideas, be free to tell me.(930727fre@gmail.com)


[//]: # ()
   [pages]: <https://sukebei.nyaa.si/?s=seeders&o=desc&p=500>
   [demo]: <https://youtu.be/gxzD0JmmtJo>
