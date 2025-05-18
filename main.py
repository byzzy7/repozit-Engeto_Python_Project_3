"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Lukáš Bystroň
email: lbystron@gmail.com
"""

import requests
import csv
from bs4 import BeautifulSoup
import argparse


parser = argparse.ArgumentParser(
    prog="Web scraping. ČR volby 2017"
)
parser.add_argument(
    "url", type=str, help="Stahuji data z vybraného url:"
)
parser.add_argument(
    "vysledky_opava.csv", help="Ukladaní dat do csv:"
)
args = parser.parse_args()
url = args.url
if args.url == 2:
    print("Špatný argument")
else:
    print(f"Stahuji data z vybraneho url: {url}")

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
    '''
    Nalezení Kódu obce a názevu obce.
    551929 - Andělská Hora
    '''
    rr = {}
    kk = table.find_all("tr")
    for i in kk:
        kod = i.find("td", {"class": "cislo"})
        nazev = i.find("td", {"class": "overflow_name"})
        if kod and nazev:
            rr[kod.text.strip(), nazev.text.strip()] = kod
    return rr

def volici_v_seznamu(cislo):
    '''
    Najdi data (Voliči v seznamu, Vydané obalky, Platné hlasy)z vybrané obce.
    Bělá - 559 , 379, 375
    '''
    ee = list(cislo)
    seznam = {}

    for i in range(len(ee)):
        tt = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=14&xobec={int(ee[i][0])}&xvyber=8105"
        odpoved = requests.get(str(tt))
        soup = BeautifulSoup(odpoved.text, features="html.parser")
        kk = soup.find_all("tr")
        for i in kk:
            volici = i.find("td", {"headers": "sa2"})
            obalky = i.find("td", {"headers": "sa3"})
            hlasy = i.find("td", {"headers": "sa6"})
            if volici and obalky and hlasy:
                seznam[volici.text.strip(), obalky.text.strip(), hlasy.text.strip()] = i
    return seznam

def strany ():
    '''
    Najde seznam názvu volební strany a celkový počet platných hlasů
    '''
    tt = "https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=14&xobec=512974&xvyber=8105"
    odpoved = requests.get(tt)
    soup = BeautifulSoup(odpoved.text, features="html.parser")
    strana = {}
    strany = soup.find_all("tr")
    for o in strany:
        pp = o.find("td", {"class": "overflow_name"})
        ll = o.find("td", {"headers": "t1sa2 t1sb3"})
        if pp and ll:
            strana[pp.text.strip(), ll.text.strip()] = o
    return strana

def vytvor_csv():
    '''
    Vytvoří csv soubor
    '''
    xx = kod_nazev_obce(download_www())
    zz = volici_v_seznamu(xx)
    rr = strany()

    print("Ukladam do souboru: vysledky_opava.csv")
    with open("vysledky_opava.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        #hlavička tabulky
        writer.writerow(["Kód obce"] + ["Název obce"] +
                        ["Voliči v seznamu"] +
                        ["Vydané obálky"] + ["Platné hlasy"] + list(rr))
        for i in range(len(xx)):
            writer.writerow(list(xx)[int(i)] + list(zz)[int(i)])
        print("Ukočuji web scraping")

if __name__ == '__main__':
    #spuštění programu
    vytvor_csv()


