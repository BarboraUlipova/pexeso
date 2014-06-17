# cmd - konsole
import pexeso
import flask
import os
from flask import request
app = flask.Flask(__name__) 

jmeno_souboru="soubor_s_hrou"

@app.route('/')
def hello():
	if os.path.exists(jmeno_souboru):
		hra = pexeso.nacti_hru_ze_souboru(jmeno_souboru)
	else:
		hra = pexeso.vytvor_hru(pexeso.zamichej_karty())
		
	
	odpoved = []
	odpoved.append("<form action = 'hra' method = 'POST'>")
	odpoved.append("<table border=1>")
	for radek in hra['stav']:
		odpoved.append("  <tr>")
		for sloupec in radek:
			cislo, jazyk,otoceni = sloupec
			odpoved.append("  <td>")
			if otoceni:
				odpoved.append(pexeso.slovo_podle_indexu(cislo, jazyk))
			else:
				odpoved.append("<button name = 'tah' type='submit' value='0 0'>???</button>")
			odpoved.append("  </td>")
		odpoved.append("  </tr>")
	odpoved.append("</table>")
	odpoved.append("</form>")
	
	return "\n".join(odpoved)

@app.route('/hra', methods = ['POST'])
def hra():
	return request.form['tah']
app.run(debug=True)

