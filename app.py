import io
from flask import Flask, session, redirect, url_for,request,render_template
import hashlib
import json
import mysql.connector
import mysql.connector.pooling
from mysql.connector import errorcode
import werkzeug.exceptions

app = Flask(__name__)

#Tietokantayhteys
tiedosto = io.open('/home/reetuinkila/vt3/dbconfig.json', encoding="UTF-8")
dbconfig = json.load(tiedosto)
try:
    pool=mysql.connector.pooling.MySQLConnectionPool(pool_name="tietokantayhteydet",
    pool_size=2, #PythonAnywheren ilmaisen tunnuksen maksimi on kolme
    **dbconfig
    ) 
    con = pool.get_connection()
    con.close()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Tunnus tai salasana on väärin")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Tietokantaa ei löydy")
    else:
        print(err)


@app.route('/kirjaudu', methods=['POST','GET'])
def kirjaudu():
    tunnus = request.form.get('tunnus', "")
    salasana = request.form.get('salasana', "")
    kilpailu = request.form.get('kilpailu', "")
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
    
    # Haetaan kilpailut tietokannasta
    con = pool.get_connection()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM my_table')
    results = cursor.fetchall()

    # Convert the results to a JSON response
    response = jsonify(results)

    return render_template('kirjaudu.html', kilpailut=results)



@app.route('/') #tämä rivi kertoo osoitteen, josta tämä sovellus löytyy
def hello_world():
    return 'Hello, World!'


