from flask import render_template,Blueprint,redirect
from py.apis import Example,Equipo,Jugador,Responsable,Staff,Partido,Producto
import base64
from py.LyS import current_user,Usuario
rutas = Blueprint('rutas', __name__,template_folder='templates')

@rutas.route("/")
def Index():   
    examples = Example.query.order_by(Example.id).all()
    return render_template('Index.html',examples=examples)

@rutas.route("/sponsors")
def Sponsors():
    return render_template('Sponsors.html')

@rutas.route("/fixtures/<string:sport>")
def Fixrute(sport="Deporte"):
    letters= list(sport)
    partidos=Partido.query.filter_by(Deporte=letters[0]).all()
    equipos=Equipo.query.all()
    return render_template('fixture.html',sport=sport,partidos=partidos,equipos=equipos)

@rutas.route("/Add_Player")
def Create_Player():
    return render_template('Add/Add_Player.html')

@rutas.route("/cantina")
def Cantina():
    productos = Producto.query.order_by(Producto.id).all()
    
    products = []
    for p in productos:
        products.append({
            "id":p.id,
            "nombre": p.Nombre,
            "precio": p.Precio,
            "tipo_img": p.tipo_img, 
            "pixel_img": base64.b64encode(p.pixel_img).decode("utf-8") if p.pixel_img else None
        })
        
    return render_template('cantina.html',products=products,Len=len(products))
@rutas.route("/Add_Equipo")
def hell():
    return render_template('Add/Add_Equipo.html')


@rutas.route("/Add_Match")
def Create_Match():
    return render_template('Add/Add_Match.html')

@rutas.route("/staff/<string:error>")
def Create_Staff(error):
    if current_user.rango=="admin":
        usuarios=Usuario.query.all()
    if error=="error":
        error="No se a encontro ningun usuario con ese mail"
    else:
        error=""
    return render_template('Add/Add_Staff.html',usuarios=usuarios,error=error)
    

@rutas.route("/inscripcion")
def Inscripcion():
    return render_template('inscripcion.html')

@rutas.route("/equipos")
def Equipos():
    return render_template('equipos.html')
#edicion y borrado de usuario
@rutas.route("/edit_user/<int:id>", methods=["GET", "POST"])
def edit_user(id):
    return render_template("EditUser/Edit_User.html")

@rutas.route("/delete_user/<int:id>", methods=["GET", "POST"])
def delete_user(id):
    return render_template("EditDelete/Delete_User.html")

if __name__ == "__main__":
    rutas.run(debug=True)