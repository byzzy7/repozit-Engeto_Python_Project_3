"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Lukáš Bystroň
email: lbystron@gmail.com
"""

import requests
import csv
from bs4 import BeautifulSoup
import argparse
from collections import defaultdict

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

def stranky_webu(cislo) -> list:
    '''
    otáčí všechny stránky obci.
    "int(obec["Kód obce"])" - cislo obce
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

def kod_nazev_obce(table) -> list:
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

def volici_obalky_hlasy(stranka) -> list:
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

def nazev_hlasy_volebni_strany(stranka):
    '''
    Najde seznam názvu volební strany
    Vyhleda celkový počet platných hlasů volebních stran
    '''

    nazev = []

    for radek in stranka:
        nazev_strany = radek.find("td", {"class": "overflow_name"})
        hlasy_tabulka_1 = radek.find("td", {"headers": "t1sa2 t1sb3"})
        hlasy_tabulka_2 = radek.find("td", {"headers": "t2sa2 t2sb3"})

        if hlasy_tabulka_1:
            nazev.append({
                nazev_strany.text.strip(): hlasy_tabulka_1.text.strip(),
            })
        if hlasy_tabulka_2:
            nazev.append({
                nazev_strany.text.strip(): hlasy_tabulka_2.text.strip(),
            })

    return nazev

def pokus(list):
    '''
    hledá stejné klíče.
    když se klíč shoduje, přídá hodnotu
    '''

    seznam = {}

    for slovo in [list]:
        for dictionary in slovo:
            for klíč, hodnota in dictionary.items():
                if klíč not in seznam:
                    seznam[klíč] = []
                seznam[klíč].append(hodnota)

    return seznam

def vytvor_csv():
    '''
    Vytvoří csv soubor
    '''
    vyber_uzemi = kod_nazev_obce(download_www())
    otaceni_stranek = stranky_webu(vyber_uzemi)
    vyber_obce = volici_obalky_hlasy(otaceni_stranek)
    oo = nazev_hlasy_volebni_strany(otaceni_stranek)
    pokus(oo)

    print("Ukladam do souboru: vysledky_opava.csv")
    with open("vysledky_opava.csv", "w", newline="", encoding="utf-8") as file:
        fieldnames = ["Kód obce", "Název obce", "Voliči v seznamu",
                      "Vydané obálky", "Platné hlasy"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()  # Zapíše hlavičku

        for uzemi, obec in zip(vyber_uzemi, vyber_obce):
            row = {
                "Kód obce": uzemi.get("Kód obce", ""),
                "Název obce": uzemi.get("Název obce", ""),
                "Voliči v seznamu": obec.get("Voliči v seznamu", ""),
                "Vydané obálky": obec.get("Vydané obálky", ""),
                "Platné hlasy": obec.get("Platné hlasy", ""),
            }
            writer.writerow(row)
        print("Ukončuji web scraping")

if __name__ == '__main__':
    #spuštění programu
    vytvor_csv()

