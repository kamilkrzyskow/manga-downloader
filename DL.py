import urllib
import urllib2
import os
import ctypes
import sys
import json
from bs4 import BeautifulSoup

#-----------------------------------------------#

os.system('cls' if os.name == 'nt' else 'clear')

if len(sys.argv) > 1:
    url = sys.argv[1]
    print "\nSet URL: " + url
else:
    url = raw_input("Input URL: ")

#url = "http://mangalife.us/read-online/Vinland-Saga-chapter-143.html"

url = list(url)
if url[0]!='h':
    i = 0
    purl = ['h', 't', 't', 'p', ':', '/', '/']
    while i < 7:
        url.insert(i, purl[i])
        i += 1
while url[len(url)-1]!='-':
    url.pop()
url1 = "".join(url)

tytul = []

while url[len(url)-1]!="/":
    tytul.append(url.pop())
tytul.reverse()
tytul.pop()
while tytul[len(tytul)-1]!='-':
    tytul.pop()
tytul.pop()
tytul = "".join(tytul)

#-----------------------------------------------#

if len(sys.argv) > 2:
    startCh = int(sys.argv[2])
    print "Start Chapter: " + sys.argv[2]
else:
    startCh = int(raw_input("Input start Chapter: "))
if len(sys.argv) > 3:
    ileCh = int(sys.argv[3])
    print "Amount of chapters: " + sys.argv[3]
else:
    ileCh = int(raw_input("Input amount of chapters: "))
if len(sys.argv) > 4:
    partCh = int(sys.argv[4])
    print "Part: " + sys.argv[4]
else:
    partCh = 0

currCh = startCh

dirPath = "../Manga/"+tytul

if not os.path.exists(dirPath):
    os.makedirs(dirPath)

er_count = 0    

#-----------------------------------------------#

while currCh < (startCh+ileCh):
    if partCh==0:
        url2 = url1+str(currCh)+".html"
    else:
        url2 = url1+str(currCh)+"."+str(partCh)+".html"
#	print "\n"+url2
    headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"}
    req = urllib2.Request(url2, "", headers)
    try:
        resp = urllib2.urlopen(req)
    except urllib2.HTTPError, err:
        if err.code == 404:
#            print "\n404 - Page not found ;_;", str(currCh)+"."+str(partCh)
            if partCh<9:
                partCh += 1
            else:
                partCh = 0
                currCh += 1
            continue
        elif err.code == 403:
            print "\n403 - Access denied ;_;"
            break
        elif err.code == 500:
            print "\n500 - Something went wrong...on the "+str(er_count+1)+"try"
            if er_count < 50:
                continue
            else: 
                break
        else:
            print "\n"+url2+"\nWeird error...: ", err.code
            break
    except urllib2.URLError, err:
        print "\nURL error ;_;: ", err.reason
        break
    html = resp.read()
    urlsy = []

    soup = BeautifulSoup(html, 'html.parser')

    soup2 = soup.find_all("div", class_="fullchapimage")

    for div in soup2:
        urlsy.append(div.img.get('src'))
    strona = 1
    print ""
    for item in urlsy:
        
        if strona < 100:
            if strona < 10:
                nrStrony = "00"+str(strona)
            else:
                nrStrony = "0"+str(strona)
        else:
            nrStrony = str(strona)
            
        if currCh < 1000:
            if currCh < 100:
                if currCh < 10:
                    nrChap = "000"+str(currCh)
                else:
                    nrChap = "00"+str(currCh)
            else:
                nrChap = "0"+str(currCh)
        else:
            nrChap = str(currCh)
        
        if partCh!=0:
            nrChap += str(partCh)
        else:
            nrChap += "0"
        
        path = dirPath+"/chapter_"+nrChap+"_page"+nrStrony+".png"

        if not os.path.exists(path):
            urllib.urlretrieve(str(item), path)
            print "chapter_"+nrChap+"_page"+nrStrony+" has been downloaded"
            strona += 1
        else:
            print "File / chapter ("+nrChap+") already exists"
            break
    del urlsy[:]
    if partCh<9:
        partCh += 1
    else:
        er_count = 0
        currCh += 1
        partCh = 0	

f = "fav.json"

#-----------------------------------------------#

if os.path.exists(f):
    with open(f, "r") as fp:
        favs = json.load(fp)
    if tytul in favs:
        lastDl = currCh - 1
        lastRd = favs[tytul][1][1]
        if (lastRd != lastDl):
            favs[tytul][1][1] = lastDl
            with open(f, "w") as fp:
                json.dump(favs, fp, sort_keys=True, indent=4)

ctypes.windll.user32.FlashWindow(ctypes.windll.kernel32.GetConsoleWindow(), True )

raw_input("\nDownload complete. Press [ENTER] to exit...")
sys.exit(0)
