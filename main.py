"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Lukáš Bystroň
email: lbystron@gmail.com
"""
from os import linesep, write

import requests
import csv
from bs4 import BeautifulSoup
import sys
import argparse

parser = argparse.ArgumentParser(
    description="Web scraping. ČR volby 2017"
)
parser.add_argument(
    "url", type=str, help="Stahuji data z vybraného url:"
)
args = parser.parse_args()
url = args.url
if (args_count := len(sys.argv)) > 2:
    print(f"One argument expected, got {args_count - 1}")
    raise SystemExit(2)
elif args_count < 2:
    print("You must specify the target directory")
    raise SystemExit(2)
print(f"Stahuji data z vybraného url: {url}")

#url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105"
#url_2 = "https://www.volby.cz/pls/ps2017nss/"

def download_www():
    """
    Stáhne obsah webové stránky a vrátí BeautifulSoup objekt.
    """
    # Stažení obsahu stránky
    odpoved = requests.get(url)
    odpoved.raise_for_status()  # Kontrola HTTP odpovědi
    soup = BeautifulSoup(odpoved.text, features="html.parser")
    return soup

def find_table(soup):
    """
    Najde tabulku v BeautifulSoup objektu a vrátí ji.
    """
    # Najít tabulku
    table = soup.find_all("table", {"class": "table"})
    return table

def kod_obce(table):
    rr = []
    kk = table.find_all("td", {"class": "cislo"})
    for i in kk:
        tt = i.get_text().strip()
        rr.append(tt)
    return rr


def nazev_obce(table):
    ff = []
    overflow_name = table.find_all("td", {"class": "overflow_name"})
    for i in overflow_name:
        ff.append(i.text.strip())
    return ff

def detail_obce(kod, url):
    urls = []
    for i in kod:
        urls.append(f"{url}ps311?xjazyk=CZ&xkraj=14&xobec={i}&xvyber=8105")
    return urls

def volici_v_seznamu():
    tt = "https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=14&xobec=512974&xvyber=8105"
    odpoved = requests.get(tt)
    soup = BeautifulSoup(odpoved.text, features="html.parser")
    voli = soup.find("td", {"headers": "sa2"})
    obalky = soup.find("td", {"headers": "sa3"})
    hlasy = soup.find("td", {"headers": "sa6"})
    volici = []
    for i in voli:
        volici.append(i)
        for y in obalky:
            volici.append(y)
            for r in hlasy:
                volici.append(r)


    return volici

def strany ():
    tt = "https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=14&xobec=512974&xvyber=8105"
    odpoved = requests.get(tt)
    soup = BeautifulSoup(odpoved.text, features="html.parser")
    strana = []
    strany = soup.find("td", {"class": "overflow_name"})
    for o in strany:
        strana.append(o)
    return strana

def vytvor_csv():
    xx = kod_obce(download_www())
    ff = nazev_obce(download_www())
    #tt = detail_obce(xx, url_2)
    zz = volici_v_seznamu()
    rr = strany()

    print("Ukladam do souboru: vysledky_opava.csv")
    with open("vysledky_opava.csv", "w", newline="", encoding="utf-8") as file:
        file.write("code")
        for i in xx:
            file.write("\n" + i)
        print("Ukočuji web scraping")

vytvor_csv()


