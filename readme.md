# Projekt 3 - Web scraping volebních výsledků

Tento projekt je součástí Engeto Online Python Akademie. Cílem je stáhnout a zpracovat volební výsledky z webové stránky a uložit je do CSV souboru.

![Image](https://github.com/user-attachments/assets/43b08486-a94a-4375-8037-eb5cb5969684)

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

## Instalace

1. Naklonujte tento repozitář:
   ```bash
   https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8101
   vysledky_opava.csv.