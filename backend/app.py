from flask import Flask, render_template
import requests
import json
import urllib.parse
import pandas as pd

app = Flask(__name__)

jsons = requests.get("https://data.culture.gouv.fr/api/records/1.0/search/?dataset=frequentation-dans-les-salles-de-cinema&q=&rows=100&sort=annee&facet=annee").json()
dataset = pd.DataFrame.from_dict(jsons,orient="index")
data=dataset[0][2]

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/seances')
def seance():
    return render_template('seances.html',data=data)

if __name__ == '__main__':
    app.run( debug = True )