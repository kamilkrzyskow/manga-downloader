import urllib2
import os
import json
import sys
from bs4 import BeautifulSoup

file = "fav.json"

#-----------------------------------------------#

def start():

    os.system('cls' if os.name == 'nt' else 'clear')

    kw = raw_input("\nWrite 'fav' to manage your favourites \nInput keywords \n(it's best to input only one ;_;): ")
    
    if kw.lower()=='fav':
        os.system('cls' if os.name == 'nt' else 'clear')
        os.system("FavChk.py")
        sys.exit(0)

    kw = list(kw)

    for i, sign in enumerate(kw):
        if sign == " ":
            kw[i] = "+"

    kw = "".join(kw)

    page = 1

    getMangs(page, kw)

#-----------------------------------------------#

def getMangs(page, kw):

    url = "http://mangalife.us/search/request.php"
    headers = {'User-Agent' : "Magic Browser"}
    req = urllib2.Request(url, "page="+str(page)+"&keyword="+kw, headers)
    resp = urllib2.urlopen(req)
    html = resp.read()
    urlsy = []
    tytuly = []
    soup = BeautifulSoup(html, 'html.parser')
    soup2 = soup.find_all("a", class_="resultLink")
    soup3 = soup.find_all("div", class_="col-xs-8")

    for a in soup2:
        urlsy.append(a.get('href'))
        tytuly.append(a.contents)

    paraf = []
    paraf2 = []

    for d in soup3:
        paraf.append(d.find_all("p"))

    for i in paraf:
        for p in i:
            paraf2.append(p.text)

    downMangs(urlsy, tytuly, kw, page, paraf2)

#-----------------------------------------------#

def downMangs(u, t, kw, page, desc):

    if len(u)==0:
        raw_input("\nCouldn't find any manga for given keyword(s). Press ENTER...")
        start()
    else:
        print "\nPage "+str(page)+"\n"
        for i, m in enumerate(t):
            print str(i+1)+". "+m[0].encode('utf-8')

        print "\n[S]tart over"
        print "[N]ext page"

        if page > 1: print "[P]revious page"
        
        wybor = raw_input("\nChoose an option: ")
    
        if wybor.lower()=='s':
            os.system('cls' if os.name == 'nt' else 'clear')
            start()
        elif wybor.lower()=='n':
            os.system('cls' if os.name == 'nt' else 'clear')
            getMangs(page+1, kw)
        elif (wybor.lower() == 'p' and page > 1):
            os.system('cls' if os.name == 'nt' else 'clear')
            getMangs(page-1, kw)
        else:
            try:
                wybor = int(wybor)
            except ValueError:
                os.system('cls' if os.name == 'nt' else 'clear')
                print "\n!--Error, wrong value ;_;--!"
                downMangs(u, t, kw, page, desc)
        
        if (len(t) < wybor or wybor < 1):
            print "\n!--No manga with this number--!"
            downMangs(u, t, kw, page, desc)

        wybor -= 1

        a = wybor * 4
        b = a + 4
        wybor = u[wybor]
        wybor = list(wybor)

        manga = []

        while wybor[len(wybor)-1] != "/":
            manga.append(wybor.pop())
    
        manga.reverse()
        tytul = "".join(manga)

        opis = []

        os.system('cls' if os.name == 'nt' else 'clear')

        print "\nTitle: ", tytul, "\n"
        for i in range(a, b):
            if i != (b-2):
                opis.append(desc[i])
                print desc[i]
            else:
                print desc[i]+"*"
                contents = list(desc[i])
                nLastCh = []
                while contents[len(contents)-1]!=" ":
                    nLastCh.append(contents.pop())
                nLastCh.reverse()
                nLastCh = int(float("".join(nLastCh)))
        
        urlw = "http://mangalife.us/read-online/"+tytul+"-chapter-1.html"

        def addFav(tytul, mode = 0, wybor = 0):
            if wybor == 0:
                wybor = raw_input("\nAdd to favorites? [y/n]: ")
            if wybor.lower()=='y':
                pyt = raw_input("\nLast read chapter - 'L' for latest?: ")
                if pyt.lower() != 'l':
                    try:
                        pyt = int(pyt)
                    except ValueError:
                        print "\n!--Wrong value--!"
                        addFav(tytul, mode, 'y')
                else:
                    pyt = nLastCh
                
                manga = {}
                manga[tytul] = opis, [urlw, pyt, nLastCh]
                    
                if mode == 1:
                    with open(file, "r") as fp:
                        favs = json.load(fp)
                    manga.update(favs)
                
                with open(file, "w") as fp:
                    json.dump(manga, fp, sort_keys=True, indent=4)


        if os.path.exists(file):
            with open(file, "r") as fp:
                favs = json.load(fp)
            titles = favs.keys()
            if not tytul in titles:
                addFav(tytul, 1)
        else:
            addFav(tytul)

        choice = raw_input("\nProceed to the download? [y/n]: ")

        if choice.lower()=='y':
            os.system("DL.py "+urlw)

        sys.exit(0)

start()