# manga-downloader [termux-build]
To make it to work with termux create a *scripts* folder on your sdcard. //scripts can be anything <br>
Termux command I use to setup everything:<br>
-pkg install python2<br>
-pip2 install beautifulsoup4<br>
-termux-setup-storage<br>
-cd storage/shared/scripts<br>
-python2 name_of_script.py<br>
------------------------------
Python scrtipt made to download mangas in bulk from MangaLife.us
<br>Made with Python 2.7.13 + <a href="https://www.crummy.com/software/BeautifulSoup/">BeautifulSoup4</a>
<br><br>Development Start Date: November 11th 2017 8PM
<br>Development End Date: December 17th 2017 2PM
<br>Amount of lines of code: ~450±70
<br>Hours worked: 15-40
<br><br>Unfinished stuff:
<ul>
    <li>Whole project
        <ul>
            <li>Deleting code duplicates and redundant code</li>
            <li>Favorites on an ftp</li>
        </ul>
    </li>
    <li>FavChk.py
        <ul>
            <li>Run update() on script execution</li>
        </ul>
    </li>
    <li>Dl.py
        <ul>
            <li>error handling</li>
        </ul>
    </li>
    <li>And a lot more, but I'm happy with the current end results</li>
</ul>
