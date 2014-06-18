"""
Program se pousti tak, ze se pusti soubor rozhrani. Rozhrani zavola fci vytvor_hru, ktera zavola zamichej_karty.  Zamichej_karty vytvori 
nahodne zamichany seznam trojic, kde je cislo karty (odpovidajici karty v cj a en. maji stejne cislo), jazyk a otoceni. Vytvor_hru z toho pak udela slovnik, 
kde je jeden prvek seznam a druhy karta, se kterou se prave pracuje.  
"""

import pprint
from random import shuffle
import os.path
import json

slova = []
cesta = os.path.join(os.path.dirname(__file__), 'slova.txt') # dirname najde jmeno adresare, kde je soubor (slova) se slovama, ktera se hadaji v pexesu, join vlozi slova za nazev te cesty
with open (cesta, encoding='utf-8') as soubor:
	for radek in soubor:
		if radek.strip():
			slova.append(radek.split())
			

def zjisti_delku_nejdelsiho_slova():
	delka = 0
	for radek in slova:
		for slovo in radek:
			if len(slovo) > delka:
				delka = len(slovo)
	return delka

	
def slovo_podle_indexu(cislo, jazyk):
	if jazyk == "cesky":
		index = 0
	elif jazyk == "anglicky":
		index = 1
	else:
		raise ValueError(jazyk) # resi, kdyz se zada spatny jazyk
	return (slova[cislo][index])
	


def vyber_kartu(stav,radek,sloupec): # kdyz zavolam s argumentem(stav,0,0), vrati (0,"cesky")
		return stav[radek][sloupec]
		

def vytvor_hru(stav):
	zakladni_hra = {
		'stav': stav,
		'aktivni_karta': None,
	}
	return zakladni_hra

def zamichej_karty(): # funkce shuffle v modulu random zamicha seznam
	seznam_karet = []
	seznam_zamichanych_karet = []
	otoceno = False
	pocet_slov = len(slova)
	polovicni_pocet_slov = int(pocet_slov/2)
	for cislo in range(pocet_slov):
		for pismeno in "cesky", "anglicky":
			prvek = (cislo,pismeno,otoceno)
			seznam_karet.append(prvek)
	shuffle(seznam_karet)
	for neco in range(polovicni_pocet_slov):
		index = neco * (polovicni_pocet_slov)
		seznam_zamichanych_karet.append(seznam_karet[index:index+polovicni_pocet_slov])		
	return (seznam_zamichanych_karet)
	


def vypis_stav(seznam_karet):
	delka = zjisti_delku_nejdelsiho_slova()
	
	for radek in seznam_karet:
		for karta in radek:
			cislo = karta[0]
			
			jazyk = karta[1]
			
			if karta[2]:
				print (slovo_podle_indexu(cislo, jazyk).ljust(delka),end=" ") # end=" " dela v python 3.4 to same, co carka
			else:
				print (delka*"?",end=" ")
		print ()
	

"""zakladni_stav = [
    [(0, 'C', False), (0, 'A', False), (1, 'C', False), (1, 'A', False)],
    [(2, 'C', False), (2, 'A', False), (3, 'C', False), (3, 'A', False)],
    [(4, 'C', False), (4, 'A', False), (5, 'C', False), (5, 'A', False)],
    [(6, 'C', False), (6, 'A', False), (7, 'C', False), (7, 'A', False)],
]

zakladni_hra = {
    'stav': zakladni_stav,
    'aktivni_karta': None,
}"""

def otoc_kartu(stav,radek,sloupec,nove_otoceni):
	""" sem se maji napsat komentare k funkci """ 
	cislo, jazyk, stare_otoceni = stav[radek][sloupec] # stav[radek][sloupec] vrati trojici, tu tuple, ve ktere mam cislo, jazyk, otoceni
	stav[radek][sloupec] = cislo, jazyk, nove_otoceni
	
def udelej_tah(hra, radek, sloupec):
	
	if (hra['stav'][radek][sloupec][2] == True):
		raise ValueError("Karta je otocena")	
	elif  hra['aktivni_karta'] == None:
		otoc_kartu(hra['stav'],radek,sloupec,True)
		hra['aktivni_karta'] = [(radek,sloupec)]
	else:
		aktivni_radek, aktivni_sloupec = hra['aktivni_karta'][0]
		nove_otoceny_obrazek = vyber_kartu(hra['stav'],radek,sloupec)[0]
		puvodni_obrazek = vyber_kartu(hra['stav'],aktivni_radek,aktivni_sloupec)[0]
		if nove_otoceny_obrazek == puvodni_obrazek:
			otoc_kartu(hra['stav'],radek,sloupec,True)
			hra['aktivni_karta'] = None
		else:
			otoc_kartu(hra['stav'],radek,sloupec,True)
			hra['aktivni_karta'].append((radek,sloupec))
	return hra
	
def ukonci_tah(hra):	
	if hra['aktivni_karta'] != None and len(hra['aktivni_karta'])==2:
		for radek,sloupec in hra['aktivni_karta']:
			otoc_kartu(hra['stav'],radek,sloupec,False)
		hra['aktivni_karta'] = None

def zapis_hru_do_souboru(hra,nazev_souboru):
	with open (nazev_souboru, "w") as soubor:
		soubor.write(json.dumps(hra)) #hra je slovnik a slovnik se neda jen tak zapsat do souboru, tak se na to musi dat ten dumps
		
def nacti_hru_ze_souboru(nazev_souboru):
	with open (nazev_souboru, "r") as soubor:
		obsah_souboru = soubor.read()
		return json.loads(obsah_souboru) #zmeni retezec zpatky na slovnik
# funkce vs. metoda: metodu volam na objektu = napisu seznam.append, u funkce vkladam objekt jako argument - pisu shuffle(seznam_karet)	
		
def kontrola_vstupu(cislo):
	velikost_pexesa = (len(slova)/2)	
	if cislo.isdigit() == False:
		raise ValueError("Je potreba zadat cislo")
	if int(cislo) > velikost_pexesa:
		raise ValueError("Cislo musi byt mensi nez 5")
	
def zjisti_jestli_vyhral(hra):
	for radek in hra['stav']:
		for sloupec in radek:
			if sloupec[2] == False:
				return False
	return True
	
		

	
"""pokud hrac zada spatny vstup, ktery bud neni cislo, nebo je vetsi nez ma byt nebo zada kartu, ktera je otocena, tak by to melo vyhodit chybovou hlasku"""

		
	