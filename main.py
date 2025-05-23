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
    prog="Projekt: Elections Scraper"
)
parser.add_argument(
    "url", type=str, help="Stahuji data z vybraného url:"
)
parser.add_argument(
    "vysledky_opava.csv", help="Ukladaní dat do csv:"
)
args = parser.parse_args()
url = args.url
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
        #Dosadí číslo obce a načte novou stranku pro stahování dat.
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
        #Najdi číslo obce
        kod_obce = radek.find("td", {"class": "cislo"})
        #Najdi název obce
        nazev_obce = radek.find("td", {"class": "overflow_name"})

        # Odstraní všechný jiné znaky. Výstup text
        if kod_obce and nazev_obce:
            kod_nazev_obce.append({
                "Kód obce": kod_obce.text.strip(),
                "Název obce": nazev_obce.text.strip(),
            })
    return kod_nazev_obce

def volici_obalky_hlasy(stranka: list) -> list:
    '''
    Najdi data (Voliči v seznamu, Vydané obalky, Platné hlasy) z vybrané obce.
    Bělá - 559 , 379, 375
    '''
    seznam = []

    for radek in stranka:
        #Najdi počet voličů v seznamu
        volici_seznam = radek.find("td", {"headers": "sa2"})
        #Najdi počet vydaných obálek
        vydane_obalky = radek.find("td", {"headers": "sa3"})
        #Najdi počet platných hlasů
        platne_hlasy = radek.find("td", {"headers": "sa6"})

        # Odstraní všechný jiné znaky. Výstup text
        if volici_seznam and vydane_obalky and platne_hlasy:
            seznam.append({
                "Voliči v seznamu": volici_seznam.text.strip(),
                "Vydané obálky": vydane_obalky.text.strip(),
                "Platné hlasy": platne_hlasy.text.strip(),
            })
    return seznam

def nazev_hlasy_volebni_strany(stranka: list) -> list:
    '''
    Najde název volebních stran a
    vyhleda celkový počet platných hlasů volebních stran
    '''

    nazev = []

    for radek in stranka:
        #Najdi název volební strany
        nazev_strany = radek.find("td", {"class": "overflow_name"})
        #Najdi v první tabulce hlasy
        hlasy_tabulka_1 = radek.find("td", {"headers": "t1sa2 t1sb3"})
        #Najdi v druhé tabulce hlasy
        hlasy_tabulka_2 = radek.find("td", {"headers": "t2sa2 t2sb3"})

        #Odstraní všechný jiné znaky. Výstup text
        if hlasy_tabulka_1:
            nazev.append({
                nazev_strany.text.strip(): hlasy_tabulka_1.text.strip(),
            })
        #Odstraní všechný jiné znaky. Výstup text
        if hlasy_tabulka_2:
            nazev.append({
                nazev_strany.text.strip(): hlasy_tabulka_2.text.strip(),
            })

    return nazev

def urovnani_dat(data: list) -> dict:
    '''
    hledá stejné klíče.
    když se klíč shoduje, přídá hodnotu
    '''

    seznam = {}

    for slovo in [data]:
        for mnozina in slovo:
            for klic, hodnota in mnozina.items():
                if klic not in seznam:
                    seznam[klic] = []
                seznam[klic].append(hodnota)

    return seznam

def vytvor_csv():
    '''
    Vytvoří csv soubor
    '''
    vyber_uzemi = kod_nazev_obce(download_www())
    otaceni_stranek = stranky_webu(vyber_uzemi)
    vyber_obce = volici_obalky_hlasy(otaceni_stranek)
    volebni_strana = nazev_hlasy_volebni_strany(otaceni_stranek)
    data = urovnani_dat(volebni_strana)
    strana_nazev = list(data.keys())

    print("Ukládám do souboru: vysledky_opava.csv")
    with open("vysledky_opava.csv", "w", newline="", encoding="utf-8") as file:
        #názvy sloupců tabulky
        fieldnames = ["Kód obce", "Název obce", "Voliči v seznamu",
                      "Vydané obálky", "Platné hlasy"] + strana_nazev # Název volební strany
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()  # Hlavička tabulky

        for uzemi, obec, hlasy in zip(vyber_uzemi, vyber_obce, zip(*data.values())):
            row = {
                "Kód obce": uzemi.get("Kód obce", ""),
                "Název obce": uzemi.get("Název obce", ""),
                "Voliči v seznamu": obec.get("Voliči v seznamu", ""),
                "Vydané obálky": obec.get("Vydané obálky", ""),
                "Platné hlasy": obec.get("Platné hlasy", ""),
            }
            for nazev_strany, pocet_hlasu in zip(data.keys(), hlasy):
                row[nazev_strany] = pocet_hlasu
            writer.writerow(row)
        print("Ukončuji election-scraper")

if __name__ == '__main__':
    #spuštění programu
    vytvor_csv()