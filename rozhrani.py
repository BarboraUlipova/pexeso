# cmd - konsole
import pexeso
import flask
import os
from flask import request
from flask import redirect
app = flask.Flask(__name__) 

jmeno_souboru="soubor_s_hrou"

@app.route('/')
def hello():
	if os.path.exists(jmeno_souboru):
		hra = pexeso.nacti_hru_ze_souboru(jmeno_souboru)
	else:
		hra = pexeso.vytvor_hru(pexeso.zamichej_karty())
	
	odpoved = []
	odpoved.append("<html><head><title>Pexeso</title></head><body><form action = 'hra' method = 'POST'>")
	odpoved.append("<table border=1>")
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
	odpoved.append("<form action = 'reset' method = 'POST'>")
	if pexeso.zjisti_jestli_vyhral(hra):		
		odpoved.append("Vyhravas! Chces <button name = 'Ano' type='submit' value='Ano'>hrat znova</button>?")
	odpoved.append("</form></body></html>")			
	return "\n".join(odpoved)
	
@app.route('/reset', methods = ['POST']) # formular zacne hledat adresu reset, app.route('/reset') rekne, ze ma pustit funkci reset
def reset():
	os.remove(jmeno_souboru)
	return redirect("/") # redirect mi vrati na funkci hello()
	
@app.route('/hra', methods = ['POST']) #jsou dve metody na ziskani udaju od uzivatele: post a get. get mi neumozni menit udaje na serveru, takze musim pouzit post
def hra():
	"""
	1. zjisti, na co hrac klikl (nacte value = souradnice buttonu, ktery se jmenuje tah)
	2. rozdeli value na dve cisla a prevede na int
	3. nacte si hru ze souboru, ukonci tah, pokud jsou otocene 2 karty, jinak udela tah a zapise hru do souboru
	cim se ta fce spousti? Kliknutim na button?
	"""
	radek, sloupec = request.form['tah'].split(" ")
	radek = int(radek)
	sloupec = int(sloupec)
	if os.path.exists(jmeno_souboru):
		hra = pexeso.nacti_hru_ze_souboru(jmeno_souboru)
	else:
		hra = pexeso.vytvor_hru(pexeso.zamichej_karty())		
	pexeso.ukonci_tah(hra)
	hra = pexeso.udelej_tah(hra, radek, sloupec)
	pexeso.zapis_hru_do_souboru(hra,jmeno_souboru)
	return redirect("/")
	
app.run(debug=True)

