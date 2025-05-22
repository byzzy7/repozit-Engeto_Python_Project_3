# Projekt 3 - Web scraping volebních výsledků

Tento projekt je součástí Engeto Online Python Akademie. Cílem je stáhnout a zpracovat volební výsledky z webové stránky https://www.volby.cz/ a uložit je do CSV souboru.

Volby do Poslanecké sněmovny Parlamentu České republiky konané ve dnech 20.10. – 21.10.2017

![Image](https://github.com/user-attachments/assets/0619e05f-4d89-4d15-b7e2-d21969f3b67b)

## Ukázka projektu
  1. argument: `"https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105"`
  2. argument: `"vysledky_opava.csv"`

## Struktura projektu
- `main.py` - Hlavní skript pro stažení a zpracování dat.
- `vysledky_opava.csv` - Výstupní soubor obsahující zpracovaná data.
- `requirements.txt` - Seznam závislostí potřebných pro spuštění projektu.\

## Ukázka kódu

`'Občanská demokratická strana': ['22', '48', '99', '37', '2', '46', '31', '164', '46', '5', '48', '37', '14']`
`'Řád národa - Vlastenecká unie': ['0', '3', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0']`
`'CESTA ODPOVĚDNÉ SPOLEČNOSTI': ['0', '1', '3', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0']`

## Použité technologie

- **Python**: Hlavní programovací jazyk.
  - `Python` - version 3.12.10 nebo vyšší
- **Knihovny**:
  - `requests` - Pro stahování obsahu webových stránek.
  - `BeautifulSoup` (z balíčku `beautifulsoup4`) - Pro analýzu HTML.
  - `csv` - Pro práci s CSV soubory.
  - `argparse` - Rozhraní pro příkazovou řádku.

## Spouštění programu

Spuštění souboru main.py v rámci přikázového řádku požaduje 2 argumenty.
   ```bash
   python3 main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105" "vysledky_opava.csv"
   ```
Následně se Vám stáhnou výsledky jako soubor s příponou ``.csv``.

## Průběh stahování
`Stahuji data z vybraneho URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105`

`ukladam do souboru: vysledky_opava.csv`

`ukoncuji main.py`

## Zdroje
**ENGETO**

https://engeto.cz/

Poděkování všem lektorům za skvělý kurz!
