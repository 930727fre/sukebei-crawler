# sukebei-crwaler
Sukebei-crawler brings you latest torrents and magnet links with most seeders.

## Watch [demo]
Execution snapshot(Gui is no longer supported after stable release v6, but it's still available in stable release [v5])
![N|Solid](https://github.com/Freddy930727/sukebei-crawler-v2/blob/master/Screenshot.png?raw=true)
## Features
- Works well on Ubuntu and Windows.
- Flexible choice between downloading .bt directly or opening magnet link.
- Automatically save download history in order to prevent overlapping torrents.
- Several filters are supported, inclusive of category, keyword, and quantity.
- Gui(versions prior to [v5]) is based on html and js, so you can execute it on Ubuntu/Windows with any browser.

## pip setup
```
pip install eel
pip install requests
pip install lxml
pip install bs4
```

## Notice
 - Since this script no longer support gui, it only works in terminal.
 - Browser is required for showing gui.
 - Don't kill the programe while running, else the history.csv will crash.

## Goal given up😢
 - Since sukebei.nyaa.si crashes so FREQUENTLY, I can't tell a crashed web from a page out of index.
## Contribution
 - Contributions and issues are wellcomed. If you are interested in this project or you have some innovative ideas, feel free to tell me.(930727fre@gmail.com)


[//]: # ()
   [pages]: <https://sukebei.nyaa.si/?s=seeders&o=desc&p=500>
   [demo]: <https://youtu.be/gxzD0JmmtJo>
   [v5]: <https://github.com/Freddy930727/sukebei-crawler/tree/2f0e7c4d451013a5d5bfd81ff593ff05f65866b5>