# UVP-projektna-nalog
# Analiza igralcev hokeja iz zadnjih destih let

Za projektno sem naredil program, ki pobere podatke s elite-prospects.com in jih malo analizira. Podatki ki jih pobere so statistični podatki hokejskih igralcev
lige NHL(National hockey league), ki je najbolša hokejska liga na svetu(največje plače, najboljši igralci, ...). Podatki so iz zadnjih 10 sezon in na sezono v ligi
odigra vsaj eno tekmo približno 1000 igralcev, oz. malo manj. Torej imam podatke za okoli 10 000 igralcev, oz. malo manj.

# Navodilo za uporabo

Da dobimo csv_data.csv mora uporbanik pognati python file Zbiranje_podatkov.py, je pa tudi moj csv_data na githubu, ki dvomim da se bo spremenil, če to storimo
še enkrat saj delamo z podatki iz zadnjih 10 let. Da program napise csv file potrebuje minuto ali dve. Knjiznice, ki sem jih uporabil so csv, os, re, reqeusts, bs4,
pandas, matplotlib.pyplot. Analiza podatkov je v jupyter filu analiza_podatko.ipynb, jupyter_notebooks_testi.ipynb je za uporabnika neuporaben, saj mi je asmo koristil da sem obdelav html in na hitro gledav ce funkcije deljao, kaj vrnejo, ...
