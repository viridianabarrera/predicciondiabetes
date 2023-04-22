"""
Routes and views for the flask application.
"""

from datetime import datetime
import pandas as pd
import pickle
from flask import render_template, request
from PlataformaPrediccionDiabetes import app
import os
import numpy as np

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Plataforma de predicción de diabetes',
        year=datetime.now().year,
    )

@app.route('/clinicos')
def clinicos():
    """Renders the contact page."""
    return render_template(
        'clinicos.html',
        title='Indicadores clínicos',
        year=datetime.now().year,
        message='Ingrese la información solicitada a continuación'
    )

@app.route('/clinicos', methods=['POST'])
def predClinicos():
    edad=int(request.form['edad'])
    presion=int(request.form['presion'])
    glucosa=int(request.form['glucosa'])
    peso =float(request.form['peso'])
    estatura = float(request.form['estatura'])
    insulina=int(request.form['insulina'])

    bmi = peso/(estatura**2)

    data={'glucose_conc':[glucosa],'Diastolic_BP':[presion], '2_hr_insulin':[insulina], 'BMI':[bmi], 'Age':[edad]}
    features=pd.DataFrame(data)

    absolute_path = os.path.dirname(__file__)
    relative_path = "static\content"
    full_path = os.path.join(absolute_path, relative_path)

    modelo = pickle.load(open(full_path + '\clinicos.pkl', 'rb'))

    prediccion = modelo.predict_proba(features)
    probabilidad = np.array_split(prediccion[0], 2)

    noDiabetes = probabilidad[0]
    noDiabetes = noDiabetes[0]
    diabetes = probabilidad[1]
    diabetes = diabetes[0]

    return render_template(
        'prediccion.html',
        title='Indicadores clinicos',
        year=datetime.now().year,
        message='Ingrese la información solicitada a continuación',
        noDiabetes=noDiabetes,
        diabetes=diabetes
    )

@app.route('/personales')
def personales():
    """Renders the about page."""
    return render_template(
        'personales.html',
        title='Indicadores personales',
        year=datetime.now().year,
        message='Ingrese la información solicitada a continuación'
    )

@app.route('/resultado')
def resultadop():
    """Renders the about page."""
    return render_template(
        'prediccion.html',
        title='Resultado de predicción',
        year=datetime.now().year,
        message='Ingrese la información solicitada a continuación'
    )

@app.route('/personales', methods=['POST'])
def predPersonales():
    sexo=int(request.form['sexo'])
    edad=int(request.form['edad'])
    presion=int(request.form['presion'])
    colesterol=int(request.form['colesterol'])
    peso =float(request.form['peso'])
    estatura = float(request.form['estatura'])
   
    fumador=int(request.form['fumador'])
    derrame=int(request.form['derrame'])
    corazon=int(request.form['corazon'])
    ejercicio=int(request.form['ejercicio'])
    alcohol=int(request.form['alcohol'])
    saludgen=int(request.form['saludgen'])
    saludmen=int(request.form['saludmen'])
    saludfis=int(request.form['saludfis'])

    if edad >=18 and edad <=24:
        edad = 1
    elif edad >=25 and edad <=29:
        edad = 2
    elif edad >= 30 and edad <=34:
        edad = 3
    elif edad >= 35 and edad <= 39:
        edad = 4
    elif edad >= 40 and edad <=44:
        edad = 5
    elif edad >= 45 and edad <=49:
        edad = 6
    elif edad >= 50 and edad <=54:
        edad = 7
    elif edad >= 55 and edad<= 59:
        edad = 8
    elif edad >= 60 and edad <=64:
        edad = 9
    elif edad >= 65 and edad <= 69:
        edad = 10
    elif edad >= 70 and edad <= 74:
        edad = 11
    elif edad >= 75 and edad <= 79:
        edad = 12
    elif edad >= 80:
        edad = 13


    bmi = peso/(estatura**2)

    data={'HighBP':[presion],'HighChol':[colesterol], 'BMI':[bmi], 'Smoker':[fumador], 'Stroke':[derrame], 
          'HeartDiseaseorAttack':[corazon], 'PhysActivity':[ejercicio], 
      'HvyAlcoholConsump':[alcohol], 'GenHlth':[saludgen], 'MentHlth':[saludmen], 'PhysHlth':[saludfis], 'Sex':[sexo], 'Age':[edad]}
    features=pd.DataFrame(data)

    absolute_path = os.path.dirname(__file__)
    relative_path = "static\content"
    full_path = os.path.join(absolute_path, relative_path)

    modelo = pickle.load(open(full_path + '\personales.pkl', 'rb'))

    prediccion = modelo.predict_proba(features)
    probabilidad = np.array_split(prediccion[0], 2)

    noDiabetes = probabilidad[0]
    noDiabetes = noDiabetes[0]
    diabetes = probabilidad[1]
    diabetes = diabetes[0]
    return render_template(
        'prediccion.html',
        title='Indicadores personales',
        year=datetime.now().year,
        message='Ingrese la información solicitada a continuación',
        noDiabetes=noDiabetes,
        diabetes=diabetes
    )
