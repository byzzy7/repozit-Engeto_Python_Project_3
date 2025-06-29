"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Lukáš Bystroň
email: lbystron@gmail.com
"""

import argparse
import csv

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode


def argumenty():
    # Argumenty pro spuštění programu
    global url
    parser = argparse.ArgumentParser(
        prog='Projekt: Elections Scraper'
    )
    parser.add_argument(
        'url', type=str, help='Stahuji data z vybraného url:'
    )
    parser.add_argument(
        'vysledky_opava.csv', help='Ukladaní dat do csv:'
    )
    args = parser.parse_args()
    url = args.url
    print(f'Stahuji data z vybraneho url: {url}')

def stahni_www():
    """
    Stáhne obsah webové stránky a vrátí BeautifulSoup objekt.
    """
    # Stažení obsahu stránky
    odpoved = requests.get(url)
    odpoved.raise_for_status()  # Kontrola HTTP odpovědi
    soup = BeautifulSoup(odpoved.text, features='html.parser')
    return soup

def najdi_tabulku(soup):
    """
    Najde tabulku.
    """
    # Najít tabulku
    table = soup.find_all('table', {'class': 'table'})
    return table

def nazev_csv(soup):
    """
    Najde název název Města a použijeho k
    pojmenování csv souboru.
    Odstraní diakritiku a převede na malá písmena.
    [7:] - odstraní název "Okres:"
    Okres: Český Krumlov = cesky_krumlov
    """
    nazev_pro_csv = soup.find_all('h3')[1].text.strip().lower()[7:]
    cisty_nazev = unidecode(nazev_pro_csv, 'utf-8')
    return cisty_nazev

def stranky_webu(soup) -> list:
    '''
    Najde odkazy na obce.
    zakldni url - https://www.volby.cz/pls/ps2017nss/
    odkaz obce  - ps311/vysledky?xjazyk=CZ&xkraj=1&xobec=551929&xvyber=0
    for cyklus načte stranky obci
    '''

    vsechny_radky = []
    zakladni_url = url[:35]
    odkaz_obci = []

    # Vyhledává odkazy na obce
    for i in soup.find_all('a', href=True):
        if 'href' in i.attrs and 'ps311' in i['href']:
            odkaz_obci.append(i['href'])

    for obec in odkaz_obci:
        #URL pro každou obec
        stranka_webu = zakladni_url + obec
        odpoved = requests.get(stranka_webu)
        soup = BeautifulSoup(odpoved.text, features='html.parser')
        vsechny_tr = soup.find_all('tr')
        vsechny_radky.extend(vsechny_tr)
    return vsechny_radky


def kod_nazev_obce(table) -> list:
    '''
    Nalezení Kódu obce a názevu obce.
    551929 - Andělská Hora
    '''
    seznam_obce = []

    vsechny_tr = table.find_all('tr')
    for radek in vsechny_tr:
        #Najdi číslo obce
        kod_obce = radek.find('td', {'class': 'cislo'})
        #Najdi název obce
        nazev_obce = radek.find('td', {'class': 'overflow_name'})

        # Odstraní všechný jiné znaky. Výstup text
        if kod_obce and nazev_obce:
            seznam_obce.append({
                sloupec_A: kod_obce.text.strip(),
                sloupec_B: nazev_obce.text.strip(),
            })
    return seznam_obce

def volici_obalky_hlasy(stranka: list) -> list:
    '''
    Najdi data (Voliči v seznamu, Vydané obalky, Platné hlasy)
    z vybrané obce.
    Bělá - 559 , 379, 375
    '''
    seznam = []

    for radek in stranka:
        #Najdi počet voličů v seznamu
        volici_seznam = radek.find('td', {'headers': 'sa2'})
        #Najdi počet vydaných obálek
        vydane_obalky = radek.find('td', {'headers': 'sa3'})
        #Najdi počet platných hlasů
        platne_hlasy = radek.find('td', {'headers': 'sa6'})

        # Odstraní všechný jiné znaky. Výstup text
        if volici_seznam and vydane_obalky and platne_hlasy:
            seznam.append({
                sloupec_C: volici_seznam.text.strip(),
                sloupec_D: vydane_obalky.text.strip(),
                sloupec_E: platne_hlasy.text.strip(),
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
        nazev_strany = radek.find('td', {'class': 'overflow_name'})
        #Najdi v první tabulce hlasy
        hlasy_tabulka_1 = radek.find('td', {'headers': 't1sa2 t1sb3'})
        #Najdi v druhé tabulce hlasy
        hlasy_tabulka_2 = radek.find('td', {'headers': 't2sa2 t2sb3'})

        #Odstraní všechný jiné znaky. Výstup text
        if hlasy_tabulka_1:
            nazev.append({
                nazev_strany.text.strip(): hlasy_tabulka_1.text.strip(),
            })
        #Odstraní všechný jiné znaky. Výstup text
        if hlasy_tabulka_2 and nazev_strany:
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
    argumenty()
    vyber_uzemi = kod_nazev_obce(stahni_www())
    otaceni_stranek = stranky_webu(stahni_www())
    vyber_obce = volici_obalky_hlasy(otaceni_stranek)
    volebni_strana = nazev_hlasy_volebni_strany(otaceni_stranek)
    data = urovnani_dat(volebni_strana)
    strana_nazev = list(data.keys())
    pojmenovani_csv = nazev_csv(stahni_www())

    print(f'Ukládám do souboru: vysledky_{pojmenovani_csv}.csv')
    with open(f'vysledky_{pojmenovani_csv}.csv', 'w',
               newline='', encoding='utf-8') as soubor:
        #názvy sloupců tabulky + Název volební strany
        nazev_sloupce = [sloupec_A, sloupec_B, sloupec_C, sloupec_D,
                      sloupec_E] + strana_nazev
        writer = csv.DictWriter(soubor, fieldnames=nazev_sloupce)

        writer.writeheader()  # Hlavička tabulky

        for uzemi, obec, hlasy in zip(vyber_uzemi, vyber_obce,
                                      zip(*data.values())):
            row = {
                sloupec_A: uzemi.get(sloupec_A, ''),
                sloupec_B: uzemi.get(sloupec_B, ''),
                sloupec_C: obec.get(sloupec_C, ''),
                sloupec_D: obec.get(sloupec_D, ''),
                sloupec_E: obec.get(sloupec_E, ''),
            }
            for nazev_strany, pocet_hlasu in zip(data.keys(), hlasy):
                if nazev_strany and pocet_hlasu:
                    row[nazev_strany] = pocet_hlasu
            writer.writerow(row)
        print('Ukončuji election-scraper')


# Url čeká na zadání z příkazové řádky
url = ''
# proměnné pro názvy sloupců
sloupec_A = 'číslo'
sloupec_B = 'název'
sloupec_C = 'Voliči v seznamu'
sloupec_D = 'Vydané obálky'
sloupec_E = 'Odevzdané obálky'

if __name__ == '__main__':
    #spuštění programu
    vytvor_csv()