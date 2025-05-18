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
if args.url == 2: #očekává dva argumenty
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

def stranky_webu(cislo):
    '''
    prohledává všechny stránky webu
    Běla ......... X
    Bohuslavice .. X
    ..
    ..
    Závada ....... X
    '''
    vsechny_radky = []

    for i in range(len(list(cislo))):
        stranka_webu = (f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=14&xobec="
              f"{int(list(cislo)[i][0])}&xvyber=8105")
        odpoved = requests.get(stranka_webu)
        soup = BeautifulSoup(odpoved.text, features="html.parser")
        vsechny_tr = soup.find_all("tr")
        vsechny_radky.extend(vsechny_tr)
    return vsechny_radky

def kod_nazev_obce(table) -> dict:
    '''
    Nalezení Kódu obce a názevu obce.
    551929 - Andělská Hora
    '''
    kod_nazev_obce = {}

    vsechny_tr = table.find_all("tr")
    for i in vsechny_tr:
        kod_obce = i.find("td", {"class": "cislo"})
        nazev_obce = i.find("td", {"class": "overflow_name"})
        if kod_obce and nazev_obce:
            kod_nazev_obce[kod_obce.text.strip(), nazev_obce.text.strip()] = i
    return kod_nazev_obce

def volici_v_seznamu(stranka) -> dict:
    '''
    Najdi data (Voliči v seznamu, Vydané obalky, Platné hlasy)z vybrané obce.
    Bělá - 559 , 379, 375
    '''
    seznam = {}

    for i in stranka:
        volici_seznam = i.find("td", {"headers": "sa2"})
        vydane_obalky = i.find("td", {"headers": "sa3"})
        platne_hlasy = i.find("td", {"headers": "sa6"})
        if volici_seznam and vydane_obalky and platne_hlasy:
            seznam[volici_seznam.text.strip(), vydane_obalky.text.strip(),
            platne_hlasy.text.strip()] = i
    return seznam

def strany (stranka)-> dict:
    '''
    Najde seznam názvu volební strany a celkový počet platných hlasů
    '''
    strana = {}

    for i in stranka:
        nazev_strany = i.find("td", {"class": "overflow_name"})
        hlasy_celkem = i.find("td", {"headers": "t1sa2 t1sb3"})
        if nazev_strany and hlasy_celkem:
            strana[nazev_strany.text.strip(), hlasy_celkem.text.strip()] = i
    return strana

def vytvor_csv():
    '''
    Vytvoří csv soubor
    '''
    vyber_uzemi = kod_nazev_obce(download_www())
    otaceni_stranek = stranky_webu(vyber_uzemi)
    vyber_obce = volici_v_seznamu(otaceni_stranek)
    kandidati = strany(otaceni_stranek)

    print("Ukladam do souboru: vysledky_opava.csv")
    with open("vysledky_opava.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Kód obce"] + ["Název obce"] +
                        ["Voliči v seznamu"] +
                        ["Vydané obálky"] + ["Platné hlasy"])
        for row in range(len(vyber_uzemi)):
            writer.writerow(list(vyber_uzemi)[int(row)] + list(vyber_obce)[int(row)] + list(kandidati)[1])
        print("Ukočuji web scraping")

if __name__ == '__main__':
    #spuštění programu
    vytvor_csv()


