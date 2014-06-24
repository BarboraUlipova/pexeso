"""
Program se pousti tak, ze se pusti soubor rozhrani (pokud se hraje pres web) nebo hra, pokud se hraje pres prikazovy radek. Rozhrani/hra zavola fci vytvor_hru, 
ktera zavola zamichej_karty.  Zamichej_karty vytvori nahodne zamichany seznam trojic, kde je cislo karty (odpovidajici karty v cj a en maji stejne cislo), 
jazyk a otoceni (False je neotocena karta, True je otocena). Vytvor_hru z toho pak udela slovnik, kde je prvek stav (seznam -radky, sloupce a ve sloupcich 
trojice) a druhy aktivni_karta je seznam karet, se kterymi se prave hraje. Potom se ze souboru hra nebo rozhrani volají udelej_tah - vezme souradnice karty, ktera se ma otocit, zmeni 3. prvek na True a da ji do seznamu aktivni_karta, 
ukonci_tah - pokud jsou v aktivni_karta prave dve karty, nacti_hru_ze_souboru a zapis_hru_do souboru.
Hra vypada takhle:
zakladni_stav = [
    [(0, 'C', False), (0, 'A', False), (1, 'C', False), (1, 'A', False)],
    [(2, 'C', False), (2, 'A', False), (3, 'C', False), (3, 'A', False)],
    [(4, 'C', False), (4, 'A', False), (5, 'C', False), (5, 'A', False)],
    [(6, 'C', False), (6, 'A', False), (7, 'C', False), (7, 'A', False)],
]

zakladni_hra = {
    'stav': zakladni_stav,
    'aktivni_karta': None,
}
"""

import pprint
from random import shuffle
import os.path
import json

slova = []
cesta = os.path.join(os.path.dirname(__file__), 'slova.txt') 
"""
dirname najde jmeno adresare, kde je soubor (slova) se slovama, ktera se hadaji v pexesu, join vlozi slova za nazev te cesty.
Soubor se nacte, rozdeli na slova a ulozi do seznamu slova.
"""
with open (cesta, encoding='utf-8') as soubor:
	for radek in soubor:
		if radek.strip():
			slova.append(radek.split()) #vytvori seznam, jehoz podseznamy jsou dvojice cj-en
			

def zjisti_delku_nejdelsiho_slova():
	""" Zjisti delku nejdelsiho slova v seznamu slova Pouziva se ve fci vypis_stav, aby se vypsalo tolik ?, kolik ma nejdelsi slovo pismen"""	
	delka = 0
	for radek in slova:
		for slovo in radek:
			if len(slovo) > delka:
				delka = len(slovo)
	return delka

	
def slovo_podle_indexu(cislo, jazyk):
	"""Dostane cislo karty a jazyk a kdyz si ji zavola fce vypis_stav, tak kazde karte priradi slovo ze seznamu slov"""
	if jazyk == "cesky":
		index = 0
	elif jazyk == "anglicky":
		index = 1
	else:
		raise ValueError(jazyk) # resi, kdyz se zada spatny jazyk
	return (slova[cislo][index])
	


def vyber_kartu(stav,radek,sloupec): 
		"""dostane dostane radek a sloupec (dve cisla) od hrace (z fce udelej_tah) a udela z toho prvek seznamu"""
		return stav[radek][sloupec]
		

def vytvor_hru(stav):
	"""dostane tabulku s kartami a udela z ni prvek slovniku. Druhy prvek sloviku je seznam 0-2 karet, se kterymi se prave hraje"""
	zakladni_hra = {
		'stav': stav,
		'aktivni_karta': None,
	}
	return zakladni_hra

def zamichej_karty(): 
	"""
	vytvori seznam, prvky jsou tuple trojice cislo, jazyk, otoceni. Cisla se vkladaji po rade, ale funkce shuffle prvky zamicha. Potom se seznam rozdeli na 
	4 casti (radky) a ty se vlozi do seznam_zamichanych_karet jako podseznamy. Seznam potom predela fce vytvor_hru na slovnik.
	"""
	seznam_karet = []
	seznam_zamichanych_karet = []
	otoceno = False
	pocet_dvojic_slov = len(slova)
	pocet_karet_v_radku = int(pocet_dvojic_slov/2)
	for cislo in range(pocet_dvojic_slov):
		for pismeno in "cesky", "anglicky":
			prvek = (cislo,pismeno,otoceno)
			seznam_karet.append(prvek)
	shuffle(seznam_karet)
	for neco in range (int(pocet_dvojic_slov*2 / pocet_karet_v_radku)):
		index = neco * (pocet_karet_v_radku)
		seznam_zamichanych_karet.append(seznam_karet[index:index+pocet_karet_v_radku])
	return (seznam_zamichanych_karet)
	


def vypis_stav(seznam_karet):
	"""pouzije se jenom pokud se hraje pres prikazovy radek. Dostane seznam karet s podseznamama se souboru hra (kde se vytvori funkci zamichej_karty).
	POkud je 3. prvek karty True, zjisti podle cisla a jazyka slovo a vypise ho. Jinak vypise ?
	"""
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
	

def otoc_kartu(stav,radek,sloupec,nove_otoceni):
	"""Pomaha fcim udelej_tah a ukonci_tah menit True na False a False na True. Protoze karta (trojice cislo, jazyk, otoceni) je tuple, nemuzu napsat 
	stav[radek][sloupec][2] = True. Musim si ulozit do promennych jeji udaje a pak ji vytvorit znova, jenom s jinou treti hodnotou.""" 
	cislo, jazyk, stare_otoceni = stav[radek][sloupec] # stav[radek][sloupec] vrati trojici, tu tuple, ve ktere mam cislo, jazyk, otoceni
	stav[radek][sloupec] = cislo, jazyk, nove_otoceni
	
def udelej_tah(hra, radek, sloupec):
	"""Dostane aktualni hru zapsanou v souboru a souradnice karty, kterou chce hrac otocit. Nejdriv zjisti, jestli karta neni otocena. Pokud je seznam 
	aktivni_karta prazdny, otoci kartu (zmeni na True). Pokud tam je karta, tak si ulozi souradnice do promennych aktivni_radek a sloupec, zjisti z hry jeji 
	cislo (1. prvek trojice), zjisti cislo druhe otacene karty. Pokud jsou cisla stejna, nova karta se otoci (aby se hraci ukazalo, co tam je) a 
	seznam vyprazdni. Pokud nejsou stejna, karta se otoci a prida do seznamu, takze jsou tam ted dve karty.
	"""
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
	"""Pokud jsou v sezamu 2 karty (to znamena, ze hrac neuhodl), tak se obe zmeni na False"""
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
# funkce vs. metoda: metodu volam na objektu = napisu seznam.append(), u funkce vkladam objekt jako argument - pisu shuffle(seznam_karet)	
		
def kontrola_vstupu(cislo):
	"""Kontroluje, jestli hrac zadal cislo mensi nez 5"""
	velikost_pexesa = (len(slova)/2)	
	if cislo.isdigit() == False:
		raise ValueError("Je potreba zadat cislo")
	if int(cislo) > velikost_pexesa:
		raise ValueError("Cislo musi byt mensi nez 5")
	
def zjisti_jestli_vyhral(hra):
	"""Vrati True pokud jsou vsechny karty tocene (True)"""
	for radek in hra['stav']:
		for sloupec in radek:
			if sloupec[2] == False:
				return False
	return True
	
		

	
"""pokud hrac zada spatny vstup, ktery bud neni cislo, nebo je vetsi nez ma byt nebo zada kartu, ktera je otocena, tak by to melo vyhodit chybovou hlasku"""

		
	