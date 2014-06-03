import sys
import os.path
import pexeso
from pprint import pprint

def hrej():
	"""1. dostane na prikazovem radku jmeno souboru
	2. pokusoubor existuje, nacte hru, pokud ne, vytvori novou hru pomoci zamichej karty os.path.exists()
	3. vypise na cmd osbah hry
	4. zepta se hrace, kam chce tahnout
	5. udela tah a vypise novy stav hry
	6. novy stav zapise do souboru (ktery dostane v argumentu """	
	jmeno_souboru = sys.argv[1]
	if os.path.exists(jmeno_souboru):
		hra = pexeso.nacti_hru_ze_souboru(jmeno_souboru)
	else:
		hra = pexeso.vytvor_hru(pexeso.zamichej_karty())
	pexeso.vypis_stav(hra['stav'])
	
	radek = int(input("zadej radek")) - 1
	sloupec = int(input("zadej sloupec")) - 1
	nova_hra = pexeso.udelej_tah(hra, radek, sloupec)
	pexeso.vypis_stav(nova_hra['stav'])
	
	pexeso.zapis_hru_do_souboru(nova_hra,jmeno_souboru)
hrej()
