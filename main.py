import internetarchive as ia
import os
import sys
import json
import requests
import time
import urllib.parse

def download_titles_restricted(urls):
    print("Downloading titles...")
    for site in urls:
        print("Downloading from site %d" % (urls.index(site) + 1))
        r = requests.get(site)
        if('<table class="directory-listing-table">' in r.text ):
            table_games = r.text.split('<table class="directory-listing-table">')[1].split('</table>')[0]
        else:
            raise Exception("Error: Could not find table")
        table_body = table_games.split('<tbody>')[1].split('</tbody>')[0]
        if( not "directory-listing-table__restricted-file" in table_body ):
            break
        table_games = table_body.split('directory-listing-table__restricted-file') 

        for i in table_games[1:]:
            link = ""
            gametitle = i.split('<td>')[1].split('</td>')[0]
            GAMES.append(Game( site + "/" + link, gametitle))

    print("Downloaded %d titles" % len(GAMES))
    print()

def download_titles(urls):
    print("Downloading titles...")
    for site in urls:
        print("Downloading from site %d" % (urls.index(site) + 1))
        r = requests.get(site)
        table_games = r.text.split('<table class="directory-listing-table">')[1].split('</table>')[0]
        table_body = table_games.split('<tbody>')[1].split('</tbody>')[0]
        table_games = table_body.split('</tr>')

        for i in table_games[1:]:
            if( not "View Contents" in i ):
                break
            link = i.split('<a href="')[1].split('">')[0]
            gametitle = i.split('">')[1].split('</a>')[0]
            GAMES.append(Game( site + "/" + link, gametitle))

    print("Downloaded %d titles" % len(GAMES))
    print()

def write_on_file(file):
    print("Writing on file...")
    f = open(file, "w")
    for game in GAMES:
        f.write(game.gametitle + " <> " + game.link + "\n")
    f.close()
    print("Done")
    print()


def search_title(title):
    print("Searching for title: %s" % title)
    found = []
    for game in GAMES:
        if title in game.gametitle:
            found.append(game)
    print("Done")
    print()
    return found

def download_game(game):
    print("Downloading game...")
    encoded_link = urllib.parse.quote(game.link, safe=':/')
    os.system(f"wget -r -np -nH --cut-dirs=1 -R index.html {encoded_link}")
    print("Done")
    print()

def open_game_list(file):
    print("Opening game list...")
    f = open(file, "r")
    for line in f:
        game = Game(line.split(" <> ")[1].replace("\n", ""), line.split(" <> ")[0])
        GAMES.append(game)
    f.close()
    print("Done")
    print()

GAMES = []

class Game:
    def __init__(self, link, gametitle):
        self.link = link
        self.gametitle = gametitle



sites = []
sites.append("https://archive.org/download/PS3_ALVRO_PART_1")
sites.append("https://archive.org/download/PS3_ALVRO_PART_2")
sites.append("https://archive.org/download/PS3_ALVRO_PART_2_OTHER")
sites.append("https://archive.org/download/PS3_ALVRO_PART_3")
sites.append("https://archive.org/download/PS3_ALVRO_PART_3_OTHER")
sites.append("https://archive.org/download/PS3_ALVRO_PART_4")
sites.append("https://archive.org/download/PS3_ALVRO_PART__5")
sites.append("https://archive.org/download/PS3_ALVRO_PART_6")
sites.append("https://archive.org/download/PS3_ALVRO_PART_7")
sites.append("https://archive.org/download/PS3_ALVRO_PART_8")
sites.append("https://archive.org/download/PS3_ALVRO_PART_9")
sites.append("https://archive.org/download/PS3_ALVRO_PART_10")
sites.append("https://archive.org/download/PS3_ALVRO_PART_11")
sites.append("https://archive.org/download/PS3_ALVRO_PART_12")
sites.append("https://archive.org/download/PS3_ALVRO_PART_13")
sites.append("https://archive.org/download/PS3_ALVRO_PART_14")


#download_titles(sites)
download_titles_restricted(sites)
write_on_file("games_alvaro.txt")

""" open_game_list("games.txt")
games_found = search_title("Unch")
print("Which game do you want to download?")
for game in games_found:
    print(game.gametitle)
game = games_found[int(input("select a number: ")) - 1]
print("Do you want to download this game? (y/n)")
if input() == "y":
    download_game(game)
else:
    print("Bye") """
