# Projekt 3 - Web scraping volebních výsledků

Tento projekt je součástí Engeto Online Python Akademie. Cílem je stáhnout a zpracovat volební výsledky z webové stránky https://www.volby.cz/ a uložit je do CSV souboru.

Volby do Poslanecké sněmovny Parlamentu České republiky konané ve dnech 20.10. – 21.10.2017

![Image](https://github.com/user-attachments/assets/750799e5-004e-41cb-8700-d8a2eb42aeab)

## Struktura projektu

- `main.py` - Hlavní skript pro stažení a zpracování dat.
- `vysledky_opava.csv` - Výstupní soubor obsahující zpracovaná data.
- `requirements.txt` - Seznam závislostí potřebných pro spuštění projektu.

## Použité technologie

- **Python**: Hlavní programovací jazyk.
  - `Python` - version 3.12.10 nebo vyšší
- **Knihovny**:
  - `requests` - Pro stahování obsahu webových stránek.
  - `BeautifulSoup` (z balíčku `beautifulsoup4`) - Pro analýzu HTML.
  - `csv` - Pro práci s CSV soubory.
  - `sys` - 
  - `argparse` - Rozhraní pro příkazovou řádku.

## Spouštění programu

1. Zkopirujte tento odkaz:
   ```bash
   python3 main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8105" "vysledky_opava.csv"
   
## Zdroje
**ENGETO**

https://engeto.cz/

Poděkování všem lektorům za skvělý kurz!
