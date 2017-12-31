import json
import os
import urllib2
import sys
from bs4 import BeautifulSoup
from collections import OrderedDict

f = "fav.json"

#-----------------------------------------------#

def ch(type, quest):
    if (type == 1):
        try:
            choice = int(raw_input(quest))
        except ValueError:
            print "\n!--Fatal error. Wrong input--!"
            choice = ch(type, quest)
    elif (type == 2):
        choice = raw_input(quest)
    return choice

#-----------------------------------------------#

def show(titles, favs):
    
    os.system('cls' if os.name == 'nt' else 'clear')

    print "\nYour favorites: \n"

    for i, x in enumerate(titles):
        print str(i+1)+". "+x

    print "\nWhat would you like to do with your favorites?\n"
    print "1 - Check for updates (all favorites)"
    print "2 - Manage one manga"
    print "3 - Exit"

    choice = ch(1, "\nYour choice?: ")

    os.system('cls' if os.name == 'nt' else 'clear')

    if choice == 1: update(titles, favs)
    elif choice == 2: manage(titles, favs)
    elif choice == 3: sys.exit(0)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print "\n!--No such option--!"
        show(titles, favs)

#-----------------------------------------------#

def update(titles, favs):
    print "\nChecking for updates for..."
    for t in titles:
        print "..."+t
        url = "http://mangalife.us/manga/"+t
        headers = {'User-Agent' : "Magic Browser"}
        req = urllib2.Request(url, "", headers)
        resp = urllib2.urlopen(req)
        html = resp.read()
        soup = BeautifulSoup(html, 'html.parser')
        soup2 = soup.find("span", class_="chapterLabel")
        contents = list(soup2.contents[0])
        nLastCh = []
        while contents[len(contents)-1]!=" ":
            nLastCh.append(contents.pop())
        nLastCh.reverse()
        nLastCh = int(float("".join(nLastCh)))
        oLastCh = favs[t][1][2]
        lastRd = favs[t][1][1]
        os.system('cls' if os.name == 'nt' else 'clear')
        if (nLastCh > oLastCh) or (lastRd < nLastCh) :
            url = favs[t][1][0]
            if (nLastCh != oLastCh):
                print "\n"+t+" had an update "+str(oLastCh)+" -> "+str(nLastCh)
            else:
                print "\nThe latest chapter for "+t+" is still "+str(nLastCh)+", but..."
            print "Last read / downloaded chapter: "+str(lastRd)
            choice = raw_input("\nWould you like to download new chapters from last read (included) [y/n]?: ")
            if choice.lower()=='y':
                choice = ch(1, "\nHow many chapters? Input 0 for all available: ")
                if choice == 0:
                    amount = nLastCh - lastRd + 1
                else:
                    amount = choice
                os.system("python2 DL.py "+url+" "+str(lastRd)+" "+str(amount))
                favs[t][1][1] = lastRd + amount - 1
            elif choice.lower()=='n':
                choice = raw_input("Set newest chapter ("+str(nLastCh)+") as last read instead of ("+str(lastRd)+") [y/n]: ")
                if choice.lower()=='y':
                    favs[t][1][1] = nLastCh
            favs[t][1][2] = nLastCh
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print "\nNo updates for "+t
     
    save(favs)

#-----------------------------------------------#

def manage(titles, favs, mem = 0):

    print "\nYour favorites: \n"

    for i, x in enumerate(titles):
        print str(i+1)+". "+x

    if (mem == 0):
        mangaChoice = ch(1, "\nWhich manga would you like to manage?: ")
        if (len(titles) < mangaChoice or mangaChoice < 1):
            print "\n!--No manga with this number--!"
            manage(titles, favs)
        mangaChoice -= 1
    else:
        mangaChoice = mem

    print ""
    
    oneTitle = [titles[mangaChoice]]

    os.system('cls' if os.name == 'nt' else 'clear')

    print "\nTitle: "+oneTitle[0]

    manga = favs[oneTitle[0]]
    
    for d in manga[0]:
        print d
    
    print "\nChapters read: "+str(manga[1][1])
    print "Latest chapter: "+str(manga[1][2])

    print "\nWhat would you like to do with this manga?: "
    print "\n1. Check for updates"
    print "2. Delete from favorites"
    print "3. Change last read"
    print "4. Download from last read"
    print "5. Start over"

    choice = ch(1, "\nYour choice?: ")

    if (choice > 5 or choice < 1):
        print "\n!--No option with this number--!"
        os.system('cls' if os.name == 'nt' else 'clear')
        manage(titles, favs)
    elif (choice == 1):
        update(oneTitle, favs)
        manage(titles, favs, mangaChoice)
    elif (choice == 2):
        choice = ch(2, "\nAre you sure? [y/n]: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        if (choice == 'y'):
            del favs[oneTitle[0]]
            save(favs)
            print oneTitle[0]+" has beed deleted"
            start()
        manage(titles, favs, mangaChoice)
    elif (choice == 3):
        choice = ch(1, "\nSet last read: ")
        favs[oneTitle[0]][1][1] = choice
        save(favs)
        os.system('cls' if os.name == 'nt' else 'clear')
        print "Last read has beed changed"
        manage(titles, favs, mangaChoice)
    elif (choice == 4):
        choice = ch(1, "\nHow many chapters? Input 0 for all available: ")
        if choice == 0:
            amount = manga[1][2] - manga[1][1] + 1
        else:
            amount = choice
        os.system("python2 DL.py "+str(manga[1][0])+" "+str(manga[1][1])+" "+str(amount))
    elif (choice == 5):
        os.system('cls' if os.name == 'nt' else 'clear')
        start()

#-----------------------------------------------#

def start():
    if os.path.exists(f):
        with open(f, "r") as fp:
            favs = json.load(fp, object_pairs_hook=OrderedDict)
        titles = favs.keys()
        show(titles, favs)
    else:
        raw_input("Couldn't find your "+f+" file ;_; Press [Enter] to exit...")

#-----------------------------------------------#

def save(favs):
    with open(f, "w") as fp:
        json.dump(favs, fp, sort_keys=True, indent=4)

#-----------------------------------------------#

start()