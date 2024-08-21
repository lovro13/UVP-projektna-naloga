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
    sez_blok_1_igralec = []

    vzorec_blok = '<tbody>.*?</tbody>'
    sez_blok = re.findall(vzorec_blok, koda, re.DOTALL) # vse kar je znotraj znack tbody bloki od 2 do 11 vsebujejo podatke vseh 100 igralcev
    vzorec_igralec = "<tr>.*?</tr>"
    for blok in sez_blok[2:12]:
        sez_blok_1_igralec += (re.findall(vzorec_igralec, blok, re.DOTALL))
    return sez_blok_1_igralec

blok = dobivanje_bloke_kode(rawhtml)[0]

def dobivaje_slovarja(blok): # torej za enega igralca
    """mesto na lestvici, ime, pozicija katero igra, ekipa, odigrane tekmi,
    goli, podaje, točke(podaje in goli skupaj, torej vsak gol ali podaja je ena točka), kazenske minute(koliko časa je biu igralec isključen)
    +/- torej razlika med prejetimi in danimi goli ko je bil igralec prisoten na ledu"""
    soup = BeautifulSoup(blok, 'html.parser')
    slovar = {} 

    mesto = soup.find("td", class_="position").text
    slovar["Mesto na lestvici"] = mesto

    ime_pozicija = soup.find("td", class_ = "player").text.strip()
    re_text_ime = r"(.*?) \((.*?)\)"
    pozicija = re.search(re_text_ime, ime_pozicija).group(2)
    ime = re.search(re_text_ime, ime_pozicija).group(1)

    slovar["Ime in Priimek"] = ime
    slovar["Pozijcija"] = pozicija    
    ekipa = soup.find("td", class_ = "team")
    slovar["Ekipa"] = ekipa.text.strip()

    odigrane_tekme = soup.find("td", class_="gp").text.strip()
    slovar["Odigrane tekme"] = odigrane_tekme

    goli = soup.find("td", class_="g").text.strip()
    slovar["Goli"] = goli

    asistence = soup.find("td", class_="a").text.strip()
    slovar["Asistence"] = asistence

    slovar["Točke"] = f"{int(goli) + int(asistence)}"

    kazenske_minute = soup.find("td", class_="pim").text.strip()
    slovar["Kazenske minute"] = kazenske_minute

    plus_minus = soup.find("td", class_="pm").text.strip()
    slovar["Razlika prejetih in danih golov"] = plus_minus
 
    return  slovar

print(dobivaje_slovarja(blok))