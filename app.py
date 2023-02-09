from flask import Flask, session, redirect, url_for, escape, request, Response, render_template
import hashlib
import sys
from functools import wraps
import sqlite3
import os
import werkzeug.exceptions

app = Flask(__name__)

# set the secret key.  keep this really secret:
app.secret_key = b'\xf5\x18\x8cV\xce\xdd\xfc\x90\xd5\xee\x1b\xbf\xe0\xda\xc5\x87\xc8\xac\xa0\xe9#4"R'

@app.route('/kirjaudu', methods=['POST','GET'])
def kirjaudu():
    tunnus = request.form.get('tunnus', "")
    salasana = request.form.get('salasana', "")
    # tähän pitää rakentaa varsinainen salasanan tarkistaminen
    # koskaan ei pidä tallentaa tai vertailla selkokielisiä salasanoja!
    # salasanan hexdigest-versio haettaisiin oikeasti esim. tietokannasta
    # Tässä salasana on nyt vakio
    m = hashlib.sha512()
    avain = "omasalainenavain"
    m.update(avain.encode("UTF-8"))
    m.update(salasana.encode("UTF-8"))
    if tunnus=="ties4080" and m.hexdigest() == '366e90b5fe29a9d9c1420afa334c4b19c4d63dcd200f424b7a9fe3328a352da5818fc03cffa463c2362db3535b612df4eb27df33d4720fbf592964571ad7572e':
        session['kirjautunut'] = "ok"
        return redirect(url_for('laskuri'))
    return render_template('kirjaudu.html')



@app.route('/') #tämä rivi kertoo osoitteen, josta tämä sovellus löytyy
def hello_world():
    return 'Hello, World!'