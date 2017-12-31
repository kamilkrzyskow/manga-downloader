# manga-downloader [termux-build]
<br>To make it to work with termux create a *scripts* folder on your sdcard. //scripts can be anything <br>
Termux commands I use to setup everything:<br>
-pkg install python2<br>
-pip2 install beautifulsoup4<br>
-termux-setup-storage<br>
-cd storage/shared/scripts<br>
-python2 name_of_script.py<br>
------------------------------
<br>Python scrtipt made to download mangas in bulk from MangaLife.us
<br>Made with Python 2.7.13 + <a href="https://www.crummy.com/software/BeautifulSoup/">BeautifulSoup4</a>
<br><br>Development Start Date: November 11th 2017 8PM
<br><strike>Development End Date: December 17th 2017 2PM</strike> -- Maybe I'll end it sometime
<br>Amount of lines of code: ~450±70
<br>Hours worked: 15-40
<br><br>-----------------------<br>
Favorites are being saved in the same place where the scripts are.
<br>---------------------------
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
<br>
I'm planning to redo this project in Python3 with FTP support, because it turned out that copying my favorites file between my phone and pc is harder than I have anticipated
