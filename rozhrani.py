# cmd - konsole
import pexeso
import flask
import os
from flask import request
from flask import redirect
import string
app = flask.Flask(__name__) 



@app.route('/') #retezec v argumentu je webova adresa, na kterou to ma jit. Adresa v okne prohlizece
def uvodni_stranka():
	cesta_k_uvodni_strance = os.path.join(os.path.dirname(__file__), 'uvodni_stranka.html')
	with open (cesta_k_uvodni_strance, "r") as soubor:
		obsah_souboru = soubor.read()
	return obsah_souboru
	
def zkontroluj_jmeno_hry(jmeno_hry):
	for pismeno in jmeno_hry:
		if pismeno not in (string.ascii_letters + string.digits + "_"): 
				return False
	return True
	
@app.route('/prihlaseni', methods=['POST'])
def prihlaseni():
	jmeno_hry = request.form['uzivatelske_jmeno']
	if zkontroluj_jmeno_hry(jmeno_hry):
		return redirect('/h/' + jmeno_hry) 
		
@app.route('/h/<jmeno_hry>')
def hello(jmeno_hry):
	if zkontroluj_jmeno_hry(jmeno_hry):
		jmeno_souboru = jmeno_hry + '.pexeso'
	else:
		flask.abort(400)
	if os.path.exists(jmeno_souboru):
		hra = pexeso.nacti_hru_ze_souboru(jmeno_souboru)
	else:
		hra = pexeso.vytvor_hru(pexeso.zamichej_karty())
	
	odpoved = []
	odpoved.append("<html><head><title>Pexeso</title></head><body><form action = '/tah/{}' method = 'POST'>".format(jmeno_hry))
	odpoved.append("<table align=center border=1>")
	for cislo_radku, radek in enumerate(hra['stav']): # v cislo_radku je diky enumerate cislo a v radku je obsah radku
		odpoved.append("  <tr>")
		for cislo_sloupce, sloupec in enumerate(radek):
			cislo, jazyk,otoceni = sloupec
			odpoved.append("  <td>")
			if otoceni:
				odpoved.append(pexeso.slovo_podle_indexu(cislo, jazyk))
			else:
				odpoved.append("<button name = 'tah' type='submit' value='{} {}'>???</button>".format(cislo_radku, cislo_sloupce)) # ve value nemuze byt promenna, tak se do {} strci to, co je ve format
			odpoved.append("  </td>")
		odpoved.append("  </tr>")
	odpoved.append("</table>")
	odpoved.append("</form>")
	odpoved.append("<form action = '/reset/{}' method = 'POST'>".format(jmeno_hry))
	if pexeso.zjisti_jestli_vyhral(hra):		
		odpoved.append("Vyhravas! Chces <button name = 'Ano' type='submit' value='Ano'>hrat znova</button>?")
	odpoved.append("</form></body></html>")			
	return "\n".join(odpoved)
	
@app.route('/reset/<jmeno_hry>', methods = ['POST']) # formular zacne hledat adresu reset, app.route('/reset') rekne, ze ma pustit funkci reset
def reset(jmeno_hry):
	if zkontroluj_jmeno_hry(jmeno_hry):
		jmeno_souboru = jmeno_hry + '.pexeso'
	else:
		flask.abort(400)
	os.remove(jmeno_souboru)
	return redirect("/") # redirect mi vrati na funkci hello()
	
@app.route('/tah/<jmeno_hry>', methods = ['POST']) #jsou dve metody na ziskani udaju od uzivatele: post a get. get mi neumozni menit udaje na serveru, takze musim pouzit post
def hra(jmeno_hry):
	"""
	1. zjisti, na co hrac klikl (nacte value = souradnice buttonu, ktery se jmenuje tah)
	2. rozdeli value na dve cisla a prevede na int
	3. nacte si hru ze souboru, ukonci tah, pokud jsou otocene 2 karty, jinak udela tah a zapise hru do souboru
	cim se ta fce spousti? Kliknutim na button?
	"""
	radek, sloupec = request.form['tah'].split(" ")
	radek = int(radek)
	sloupec = int(sloupec)
	if zkontroluj_jmeno_hry(jmeno_hry):
		jmeno_souboru = jmeno_hry + '.pexeso'
	else:
		flask.abort(400)
	if os.path.exists(jmeno_souboru):
		hra = pexeso.nacti_hru_ze_souboru(jmeno_souboru)
	else:
		hra = pexeso.vytvor_hru(pexeso.zamichej_karty())		
	pexeso.ukonci_tah(hra)
	hra = pexeso.udelej_tah(hra, radek, sloupec)
	pexeso.zapis_hru_do_souboru(hra,jmeno_souboru)
	return redirect("/h/" + jmeno_hry)
	
app.run()

