from flask import Flask, render_template, request
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
    datas=dataset[0][2]
    return render_template('seances.html',datas=datas,data=data)


@app.route('/searchSeances')
def searcheances():
    datas=dataset[0][2]
    # data=dataset[0][2]
    for d in datas :
        if(request.args.get('annee') == d['fields']['annee']):
            datas = []
            datas.append(d)
            
    return render_template('seances.html',datas=datas,data=data)

@app.route('/affluences')
def affluence():
    datas=dataset[0][2]
    return render_template('affluences.html',datas=datas,data=data)


@app.route('/searchAffluences')
def searchAffluence():
    datas=dataset[0][2]
    # data=dataset[0][2]
    for d in datas :
        if(request.args.get('annee') == d['fields']['annee']):
            datas = []
            datas.append(d)
            
    return render_template('affluences.html',datas=datas,data=data)


if __name__ == '__main__':
    app.run( debug = True )