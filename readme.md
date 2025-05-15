# Projekt 3 - Web scraping volebních výsledků

Tento projekt je součástí Engeto Online Python Akademie. Cílem je stáhnout a zpracovat volební výsledky z webové stránky https://www.volby.cz/ a uložit je do CSV souboru.

Volby do Poslanecké sněmovny Parlamentu České republiky konané ve dnech 20.10. – 21.10.2017 (promítnuto usnesení NSS)

![Image](https://github.com/user-attachments/assets/750799e5-004e-41cb-8700-d8a2eb42aeab)
![Image](https://github.com/user-attachments/assets/81080014-4176-4656-9ab5-e342fdbe3430)

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

1. Zkopirujte tento repozitář:
   ```bash
   "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8101" "vysledky_opava.csv"
