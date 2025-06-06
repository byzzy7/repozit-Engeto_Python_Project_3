# ENGETO Projekt 3 - Web scraping volebních výsledků

Tento projekt je součástí Engeto Online Python Akademie. Cílem je stáhnout a zpracovat volební výsledky z webové stránky [https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) a uložit je do CSV souboru.

Volby do Poslanecké sněmovny Parlamentu České republiky konané ve dnech 20.10. – 21.10.2017

![Image](https://github.com/user-attachments/assets/f9875e6e-3d55-49f8-a1c8-c10ddd0259c8)

## Instalace

- **Python**: Hlavní programovací jazyk.
  - `Python` - version 3.12.10 nebo vyšší
- **Knihovny**:
  - `requests` - Pro stahování obsahu webových stránek.
  - `BeautifulSoup` (z balíčku `beautifulsoup4`) - Pro analýzu HTML.
  - `csv` - Pro práci s CSV soubory.
  - `argparse` - Rozhraní pro příkazovou řádku.
  - `re` - Pro práci s regulárními výrazy.
  
- Knihovný, které jsou použity v kódu jsou uložené requirements.txt.
Pro instalaci doporučuji použit nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:
- ```pip3 -- version```
- ```pip3 instal -r requirements.txt```

## Ukázka projektu
  1. argument: `"https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105"`
  2. argument: `"vysledky_opava.csv"`

## Spouštění programu

Spuštění souboru main.py v rámci přikázového řádku požaduje 2 argumenty.
   ```bash
   python3 main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105" "vysledky_opava.csv"
   ```

## Průběh stahování
`Stahuji data z vybraneho URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105`

`Ukládám do souboru: vysledky_opava.csv`

`Ukončuji election-scraper`

## Struktura projektu
- `main.py` - Hlavní skript pro stažení a zpracování dat.
- `vysledky_opava.csv` - Výstupní soubor obsahující zpracovaná data.
- `requirements.txt` - Seznam závislostí potřebných pro spuštění projektu.\

## Ukázka kódu

```Kód obce,Název obce,Voliči v seznamu,Vydané obálky,Platné hlasy```

```512974,Bělá,559,379,22,0,0,27,1,9,15,3,8,5,1,1,18,0,1,15,150```

```506192,Bohuslavice,1 380,908,,48,3,1,48,0,20,32,3,6,9,1,2```

```506214,Bolatice,3 533,2 309,,99,1,3,126,1,41,101,18,11```

```554197,Branka u Opavy,887,593,,37,0,0,60,0,12,59,0,1,4,1,1```

## Zdroje
**ENGETO**

[https://engeto.cz/](https://engeto.cz/)

Poděkování všem lektorům za skvělý kurz!
