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
    Najde tabulku.
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

    for obec in cislo:
        stranka_webu = (f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=14&xobec="
              f"{int(obec["Kód obce"])}&xvyber=8105")
        odpoved = requests.get(stranka_webu)
        soup = BeautifulSoup(odpoved.text, features="html.parser")
        vsechny_tr = soup.find_all("tr")
        vsechny_radky.extend(vsechny_tr)
    return vsechny_radky

def kod_nazev_obce(table):
    '''
    Nalezení Kódu obce a názevu obce.
    551929 - Andělská Hora
    '''
    kod_nazev_obce = []

    vsechny_tr = table.find_all("tr")
    for radek in vsechny_tr:
        kod_obce = radek.find("td", {"class": "cislo"})
        nazev_obce = radek.find("td", {"class": "overflow_name"})

        if kod_obce and nazev_obce:
            kod_nazev_obce.append({
                "Kód obce": kod_obce.text.strip(),
                "Název obce": nazev_obce.text.strip(),
            })
    return kod_nazev_obce

def volici_v_seznamu(stranka):
    '''
    Najdi data (Voliči v seznamu, Vydané obalky, Platné hlasy)z vybrané obce.
    Bělá - 559 , 379, 375
    '''
    seznam = []

    for radek in stranka:
        volici_seznam = radek.find("td", {"headers": "sa2"})
        vydane_obalky = radek.find("td", {"headers": "sa3"})
        platne_hlasy = radek.find("td", {"headers": "sa6"})

        if volici_seznam and vydane_obalky and platne_hlasy:
            seznam.append({
                "Voliči v seznamu": volici_seznam.text.strip(),
                "Vydané obálky": vydane_obalky.text.strip(),
                "Platné hlasy": platne_hlasy.text.strip(),
            })
    return seznam

def strany (stranka):
    '''
    Najde seznam názvu volební strany a celkový počet platných hlasů
    '''
    strana = []

    for radek in stranka:
        nazev_strany = radek.find("td", {"class": "overflow_name"})
        hlasy_strany = radek.find("td", {"headers": "t1sa2 t1sb3"})

        if nazev_strany and hlasy_strany:
            strana.append({
                "Název strany": nazev_strany.text.strip(),
                "Hlasy strany": hlasy_strany.text.strip(),
            })
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
    with (open("vysledky_opava.csv", "w", newline="", encoding="utf-8") as file):
        writer = csv.writer(file)
        hlavicka = (["Kód obce"] + ["Název obce"] +
                        ["Voliči v seznamu"] +
                        ["Vydané obálky"] + ["Platné hlasy"])
        writer.writerow(hlavicka)
        for uzemi in vyber_uzemi:
            writer.writerow(uzemi.values())
        for obec in vyber_obce:
            writer.writerow(obec.values())
        for hlasy in kandidati:
            writer.writerow(hlasy.values())
        print("Ukočuji web scraping")

if __name__ == '__main__':
    #spuštění programu
    vytvor_csv()

