from flask import Flask, render_template, request
import requests
import json
import urllib.parse
import pandas as pd
import pygal
from pygal.style import DarkStyle
from pygal.style import NeonStyle
app = Flask(__name__)

jsons = requests.get("https://data.culture.gouv.fr/api/records/1.0/search/?dataset=frequentation-dans-les-salles-de-cinema&q=&rows=100&sort=annee&facet=annee").json()
dataset = pd.DataFrame.from_dict(jsons,orient="index")
data=dataset[0][2]

#bar_chart.x_labels = map(str, range(1980, 1985))

criteres = ["entrees_millions","recette_guichet_meu_courants","recette_moyenne_par_entree_eu","seances_milliers"]
types = ["bar","line"]
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html',data=data,fields=criteres,types=types)

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


@app.route('/evoRecette')
def evoRecette():
    datas=dataset[0][2]
    return render_template('evoRecette.html',datas=datas,data=data)
    

@app.route('/details/<string:annee>')
def details(annee):
    datas=dataset[0][2]
    data = 0
    for d in datas:
        if(annee == d['fields']['annee']):
            data = d

    return render_template('details.html',datas=data)

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

@app.route('/searchRecette')
def searchRecette():
    datas=dataset[0][2]
    # data=dataset[0][2]
    for d in datas :
        if(request.args.get('annee') == d['fields']['annee']):
            datas = []
            datas.append(d)
    
    return render_template('evoRecette.html',datas=datas,data=data)



@app.route('/viz_seances_milliers')
def viz_seances_milliers():
    if(request.args.get('type') == "bar"):
        bar_chart = pygal.Bar(style=NeonStyle)
        bar_chart.title = request.args.get('critere')
        l=list()
        for j in range(len(data)):
            if(data[j]['fields']['annee']==request.args.get('start')):
                for i in range(j,j+int(request.args.get('step'))+1):
                    l.append(data[i]['fields'][request.args.get('critere')])
        bar_chart.x_labels = map(str, range(int(request.args.get('start')), int(request.args.get('step'))+int(request.args.get('start'))+1))
        bar_chart.add(request.args.get('critere'),  l)
        bar=bar_chart.render_data_uri()
    else:
        line_chart = pygal.Line(style=NeonStyle)
        line_chart.title = request.args.get('critere')
        l=list()
        for j in range(len(data)):
            if(data[j]['fields']['annee']==request.args.get('start')):
                for i in range(j,j+int(request.args.get('step'))+1):
                    l.append(data[i]['fields'][request.args.get('critere')])
        line_chart.x_labels = map(str, range(int(request.args.get('start')), int(request.args.get('step'))+int(request.args.get('start'))+1))
        line_chart.add(request.args.get('critere'),  l)
        bar=line_chart.render_data_uri()
    return render_template('index.html',data=data,bar=bar,fields=criteres,types=types)

@app.route('/comparer')
def comparer():
    return render_template('comparer.html',fields=criteres,data=data)

@app.route('/comparaison')
def comparaison():
    start=0
    end=0
    datas=dataset[0][2]
    if(request.args.get('type') == "stackedbar"):
        bar_chart = pygal.StackedBar(style=NeonStyle)
        bar_chart.title = request.args.get('critere')
        bar_chart.x_labels = map(str, range(int(request.args.get('start')), int(request.args.get('end'))))
        for i in range(len(data)):
            if(data[i]['fields']['annee']==request.args.get('start')):
                start = i
            if(data[i]['fields']['annee']==request.args.get('end')):
                end = i
        bar_chart.add(request.args.get('start'), [data[start]['fields'][request.args.get('critere')]])
        bar_chart.add(request.args.get('end'), [data[end]['fields'][request.args.get('critere')]])
        bar = bar_chart.render_data_uri()
    else:
        bar_chart = pygal.Bar(style=NeonStyle)
        bar_chart.title = request.args.get('critere')
        bar_chart.x_labels = map(str, range(int(request.args.get('start')), int(request.args.get('end'))))
        for i in range(len(data)):
            if(data[i]['fields']['annee']==request.args.get('start')):
                start = i
            if(data[i]['fields']['annee']==request.args.get('end')):
                end = i
        bar_chart.add(request.args.get('start'), [data[start]['fields'][request.args.get('critere')]])
        bar_chart.add(request.args.get('end'), [data[end]['fields'][request.args.get('critere')]])
        bar = bar_chart.render_data_uri()
    return render_template('comparer.html',datas=datas,bar=bar,fields=criteres,data=data)

if __name__ == '__main__':
    app.run( debug = True )
