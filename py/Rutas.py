from flask import Flask, render_template,Blueprint, request, jsonify, redirect, url_for
from flask_cors import CORS
from jinja2 import TemplateNotFound

rutas = Blueprint('rutas', __name__,template_folder='templates')



@rutas.route("/signup", methods=["GET"])
def signup_page():
    return render_template('signup and login/signup.html')

@rutas.route("/login", methods=["GET"])
def login_page():
    return render_template('signup and login/login.html')
"""@rutas.route("/Add_Player")
def Create_Player():
    return render_template('Add/Add_Player.html')

@rutas.route("/Cantina")
def Cantina():
    return render_template('Add/Cantina.html')
@rutas.route("/Add_Equipo")
def hell():
    return render_template('Add/Add_Equipo.html')

@rutas.route("/Add_Match")
def Create_Match():
    return render_template('Add/Add_Match.html')

@rutas.route("/Add_Staff")
def Create_Staff():
    return render_template('Add/Add_Staff.html')"""

@rutas.route("/fixture")
def fixture():
# Ejemplo de datos, deberías cargar estos de una base de datos o algún archivo
    fase_grupos = [
        {'equipo_1': 'Equipo A', 'equipo_2': 'Equipo B', 'fecha': '2025-09-05', 'hora': '18:00', 'ubicacion': 'Estadio A'},
        {'equipo_1': 'Equipo C', 'equipo_2': 'Equipo D', 'fecha': '2025-09-06', 'hora': '20:00', 'ubicacion': 'Estadio B'},
    ]
    semifinales = [
        {'equipo_1': 'Equipo A', 'equipo_2': 'Equipo C', 'fecha': '2025-09-15', 'hora': '16:00', 'ubicacion': 'Estadio A'},
        {'equipo_1': 'Equipo B', 'equipo_2': 'Equipo D', 'fecha': '2025-09-16', 'hora': '18:00', 'ubicacion': 'Estadio B'},
    ]
    final = [
        {'equipo_1': 'Equipo A', 'equipo_2': 'Equipo B', 'fecha': '2025-09-20', 'hora': '20:00', 'ubicacion': 'Estadio Final'},
    ]

    return render_template('fixture.html', fase_grupos=fase_grupos, semifinales=semifinales, final=final)



if __name__ == "__main__":
    rutas.run(debug=True)