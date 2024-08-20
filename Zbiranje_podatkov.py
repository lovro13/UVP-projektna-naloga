import csv
import os
import re
import requests
from bs4 import BeautifulSoup

zacetni_url = "https://www.eliteprospects.com/league/nhl/stats/2023-2024?page=1"
mapa_za_html = "raw_html"

def pridobivanje_strani(stran, mapa, datoteka): 
    """funkcija vzame 3 paramtre, torej stran s katere bom html kodo bomo prebrali
      s pomočjo knjižnice requests, in napisali kodo v datoreko, ki je v mapi
      koda tudi sporoci ce je prislo do napake pri pridobivanju strani"""
    try:
        response = requests.get(stran)
        response.raise_for_status()
        htmlkoda = response.text
        print("stran pridobljena")
    except requests.exceptions.RequestException as error:
        print("Stran ni dosegljiva ali pa je prišlo da kakšne druge napake")
        print(f"napaka: {error}")
        return
    
    os.makedirs(mapa, exist_ok=True) # naredi mapo
    path = os.path.join(mapa, datoteka) # link oziroma pot do datoteke
    with open(path, "w", encoding="utf-8") as dat: #napise htmlkodo strani v txt datoteko
        dat.write(htmlkoda)
    
    return htmlkoda #vrne html kodo ker jo bomo potrebovali kasneje

rawhtml = pridobivanje_strani(zacetni_url, mapa_za_html, "eliteprospects")

def dobivanje_bloke_kode(koda):
    #zdj rabimo dobiti blok kode v katerem so podatki, saj nimam značk da bi si lahko pomagal brez tega
    vzorec_blok = '<tbody>.*?</tbody>'
    sez_blok = re.findall(vzorec_blok, koda, re.DOTALL) # vse kar je znotraj znack tbody bloki od 2 do 11 vsebujejo podatke vseh 100 igralcev
    
    return sez_blok[2:12]