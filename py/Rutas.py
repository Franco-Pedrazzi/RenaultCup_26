from flask import render_template,Blueprint
from py.apis import Example,Equipo,Jugador,Responsable,Staff,Partido

rutas = Blueprint('rutas', __name__,template_folder='templates')

@rutas.route("/")
def Index():   
    examples = Example.query.order_by(Example.id).all()
    return render_template('Index.html',examples=examples)

@rutas.route("/sponsors")
def Sponsors():
    return render_template('Sponsors.html')

@rutas.route("/equipos/<string:sport>")
def Fixrute(sport="Deporte"):
    letters= list(sport)
    partidos=Partido.query.filter_by(Deporte=letters[0]).all()
    equipos=Equipo.query.all()
    print(letters)
    return render_template('fixture.html',sport=sport,partidos=partidos,equipos=equipos)

@rutas.route("/Add_Player")
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
    return render_template('Add/Add_Staff.html')

@rutas.route("/Fixture")
def Equipos():
    return render_template('fixture.html')
#edicion y borrado de usuario
@rutas.route("/edit_user/<int:id>", methods=["GET", "POST"])
def edit_user(id):
    return render_template("EditUser/Edit_User.html")

@rutas.route("/delete_user/<int:id>", methods=["GET", "POST"])
def delete_user(id):
    return render_template("EditDelete/Delete_User.html")

if __name__ == "__main__":
    rutas.run(debug=True)