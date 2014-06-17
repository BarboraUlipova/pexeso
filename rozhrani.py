# cmd - konsole
import pexeso
import flask
import os

app = flask.Flask(__name__) 

jmeno_souboru="soubor_s_hrou"

@app.route('/')
def hello():
	if os.path.exists(jmeno_souboru):
		hra = pexeso.nacti_hru_ze_souboru(jmeno_souboru)
	else:
		hra = pexeso.vytvor_hru(pexeso.zamichej_karty())
		
	
	odpoved = []
	odpoved.append("<table>")
	for radek in hra['stav']:
		odpoved.append("  <tr>")
		for sloupec in radek:
			cislo, jazyk,otoceni = sloupec
			odpoved.append("    <td>" + pexeso.slovo_podle_indexu(cislo, jazyk) + "</td>")
		odpoved.append("  </tr>")
	odpoved.append("</table>")
	
	return "\n".join(odpoved)


app.run(debug=True)

