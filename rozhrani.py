# cmd - konsole
import flask

app = flask.Flask(__name__) 

@app.route('/')
def hello():
    return """
    <html>
        <head>
             <title>Ahoj!</title>
        </head>
        <body>
             <h1>Ahoj svete!...</h1>
                <p>
                  <a href="neco">
                     Klikni sem!
                  </a>
                  nebo:
                  <a href="https://www.python.org/downloads/release/python-340/">
                     Sem!
                  </a>
                </p>
                <p>
                   <img src="obrazek">
                </p>
                <form method="POST" action="ahoj">
                   Jak se jmenujes?
                   <input type="text" name="jmeno">
                   <input type="submit" value="JEN SI KLIKNI :)">
                </form>
        </body>
    </html>
    """

@app.route('/neco')
def neco():
    return 'Tady to je!'

@app.route('/ahoj', methods=['POST'])

def ahoj():
    text = 'Ahoj. {} je hezke jmeno.'
    jmeno = flask.request.form['jmeno']
    return text.format(jmeno)

@app.route('/obrazek')
def obrazek():
    jmeno_souboru = r'C:\Sallyino\Fotky\kakadu_ruzovy.jpg' # r je tam kvuli spetnym lomitkum
    with open(jmeno_souboru, 'rb') as f:
        obsah = f.read()
    return flask.Response(
        obsah,
        mimetype='image/png')

app.run(debug=True)

