import csv
import os
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

zacetni_url = "https://www.eliteprospects.com/league/nhl/stats/2023-2024?page=1"
mapa_za_html = "raw_html"
csv_mapa = "data_csv"
csv_datoteka = "elite_prospects_data1"

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
        print(f"Stran{stran} ni dosegljiva ali pa je prišlo da kakšne druge napake")
        print(f"napaka: {error}")
        return
    
    os.makedirs(mapa, exist_ok=True) # naredi mapo
    safe_filename = datoteka.replace("https://", "").replace("/", "_").replace("?", "_").replace(":", "_") #ti vsi znaki delajo probleme
    path = os.path.join(mapa, safe_filename) # link oziroma pot do datoteke
    with open(path, "w", encoding="utf-8") as dat: #napise htmlkodo strani v txt datoteko
        dat.write(htmlkoda)
    
    return htmlkoda #vrne html kodo ker jo bomo potrebovali kasneje

#rabimo 100 strani
# rawhtml = pridobivanje_strani(zacetni_url, mapa_za_html, "eliteprospects") # to je samo za eno stran, zdaj rabimo za 100

sez_strani = []
leta = ["2023-2024", "2022-2023", "2021-2022", "2020-2021", "2019-2020", "2018-2019", "2017-2018", "2016-2017", "2015-2016", "2014-2015"]
#za vsako leto 10 strani, kar je približno slabih 1000 igralcev na leto
for leto in leta[0:1]:
    for i in range(1):
        sez_strani.append(f"https://www.eliteprospects.com/league/nhl/stats/{leto}?page={i+1}")

#print(sez_strani)

seznam_kod_strani = []
for stran in sez_strani:
    seznam_kod_strani.append(pridobivanje_strani(stran, mapa_za_html, f"stran{stran}.html"))

def dobivanje_bloke_kode(koda):
    #zdj rabimo dobiti blok kode v katerem so podatki, saj nimam značk da bi si lahko pomagal brez tega
    sez_blok_1_igralec = []

    if isinstance(koda, list):
        # Če je seznam, ga združite v en niz
        koda = ''.join([str(element) for element in koda])

    soup = BeautifulSoup(koda, 'html.parser')

    sez_blok = soup.find_all('tbody') # vse kar je znotraj znack tbody bloki od 2 do 11 vsebujejo podatke vseh 100 igralcev
    for blok in sez_blok[2:12]:
        vrstice = blok.find_all('tr')
        for vrstica in vrstice:
            sez_blok_1_igralec.append(vrstica)
    return sez_blok_1_igralec


bloki_igralcev = []
for koda in seznam_kod_strani:
    bloki_igralcev.extend(str(dobivanje_bloke_kode(koda)))
print(bloki_igralcev[0])



#blok = dobivanje_bloke_kode(rawhtml)[0]

def dobivaje_slovarja(blok): # torej za enega igralca
    """mesto na lestvici, ime, pozicija katero igra, ekipa, odigrane tekmi,
    goli, podaje, točke(podaje in goli skupaj, torej vsak gol ali podaja je ena točka), kazenske minute(koliko časa je biu igralec isključen)
    +/- torej razlika med prejetimi in danimi goli ko je bil igralec prisoten na ledu"""
    soup = BeautifulSoup(blok, 'html.parser')
    slovar = {} 
    print(soup)
    mesto = soup.find("td", class_="position").text
    slovar["Mesto na lestvici"] = mesto


    if slovar["Mesto na lestvici"] != " \xa0 ":
        ime_in_pozicija = soup.find("td", class_ = "player").text.strip()
        re_text_ime = r"(.*?) \((.*?)\)"
        pozicija = re.search(re_text_ime, ime_in_pozicija).group(2)
        ime = re.search(re_text_ime, ime_in_pozicija).group(1)
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

def seznam_slovarjev_za_vse_igralce(bloki_igralcev):
    sez_slovarjev = []
    for blok in bloki_igralcev:
            slovar = dobivaje_slovarja(blok)
            sez_slovarjev.append(slovar)
            print(1)
    return sez_slovarjev

seznam_slovarjev = seznam_slovarjev_za_vse_igralce(bloki_igralcev)
print(seznam_slovarjev)

def csv_file_iz_slovarjev(stolpci, seznam_slovarjev, mapa, ime_datoteke):
    os.makedirs(mapa, exist_ok=True)
    path = os.path.join(mapa, ime_datoteke)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=stolpci)
        writer.writeheader()
        for row in seznam_slovarjev:
            writer.writerow(row)
    return

def dobivanje_stolpcev(seznam_slovarjev):
    slovar = seznam_slovarjev[0]
    stolpci = []
    for key in slovar.keys():
        stolpci.append(key)
    return stolpci

#stolpci = dobivanje_stolpcev(seznam_slovarjev)

#csv_file_iz_slovarjev(stolpci, seznam_slovarjev, csv_mapa, csv_datoteka)