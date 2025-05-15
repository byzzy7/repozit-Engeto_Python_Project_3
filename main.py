"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Lukáš Bystroň
email: lbystron@gmail.com
"""

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

def kod_nazev_obce(table):
    rr = {}
    kk = table.find_all("tr")
    for i in kk:
        kod = i.find("td", {"class": "cislo"})
        nazev = i.find("td", {"class": "overflow_name"})
        rr[kod, nazev] = i
    return rr

def volici_v_seznamu():
    seznam = {}
    tt = "https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=14&xobec=512974&xvyber=8105"
    odpoved = requests.get(tt)
    soup = BeautifulSoup(odpoved.text, features="html.parser")
    kk = soup.find_all("td")
    for i in kk:
        volici = i.find("td", {"headers": "sa2"})
        obalky = i.find("td", {"headers": "sa3"})
        hlasy = i.find("td", {"headers": "sa6"})
        seznam[volici, obalky, hlasy] = i
    return seznam

def strany ():
    tt = "https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=14&xobec=512974&xvyber=8105"
    odpoved = requests.get(tt)
    soup = BeautifulSoup(odpoved.text, features="html.parser")
    strana = []
    strany = soup.find_all("td", {"class": "overflow_name"})
    for o in strany:
        strana.append(o.text.strip())
    return strana

def vytvor_csv():
    xx = kod_nazev_obce(download_www())
    #tt = detail_obce(xx, url_2)
    zz = volici_v_seznamu()
    rr = strany()


    print("Ukladam do souboru: vysledky_opava.csv")
    with open("vysledky_opava.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(zz)
        print("Ukočuji web scraping")

if __name__ == '__main__':
    #spuštění programu
    vytvor_csv()


