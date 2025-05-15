# Projekt 3 - Web scraping volebních výsledků

Tento projekt je součástí Engeto Online Python Akademie. Cílem je stáhnout a zpracovat volební výsledky z webové stránky https://www.volby.cz/ a uložit je do CSV souboru.

Volby do Poslanecké sněmovny Parlamentu České republiky konané ve dnech 20.10. – 21.10.2017 (promítnuto usnesení NSS)

![Image](https://github.com/user-attachments/assets/9e5c252a-8e1f-4a26-b944-8d6ceb443a5e)
![Image](https://github.com/user-attachments/assets/2bce43cb-9a3e-484d-a6b5-41615c4931f8)

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