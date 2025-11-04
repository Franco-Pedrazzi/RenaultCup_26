from flask import Blueprint, request, jsonify, redirect,url_for,render_template
from py.db import db 
from py.LyS import current_user

apis = Blueprint("apis", __name__)


class Equipo(db.Model):
    __tablename__ = "equipo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Deporte = db.Column(db.String(10), default="-")
    Categoria = db.Column(db.String(10), default="-")
    Sexo = db.Column(db.String(10), default="-")
    Colegio = db.Column(db.String(50), default="-")

class Jugador(db.Model):
    __tablename__ = "jugador"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_equipo = db.Column(db.Integer, db.ForeignKey('Equipo.id'))
    Nombre = db.Column(db.String(50), default="-")
    DNI = db.Column(db.String(10))
    Telefono = db.Column(db.String(15))
    Email = db.Column(db.String(40))
    Comida_especial = db.Column(db.String(3), default="N")
    Fecha_nacimiento = db.Column(db.Date)
    Infracciones = db.Column(db.String(10), default="0")

class Responsable(db.Model):
    __tablename__ = "Responsable"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_equipo = db.Column(db.Integer, db.ForeignKey('Equipo.id'))
    Nombre = db.Column(db.String(50), default="-")
    DNI = db.Column(db.String(10))
    Telefono = db.Column(db.String(15))
    Email = db.Column(db.String(40))
    Comida_especial = db.Column(db.String(3), default="N")
    Fecha_nacimiento = db.Column(db.Date)

class Partido(db.Model):
    __tablename__ = "Partido"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Deporte = db.Column(db.String(1))
    Categoria = db.Column(db.String(3))
    Sexo = db.Column(db.String(1))
    Arbitro = db.Column(db.Integer, db.ForeignKey('Staff.id'))
    Planillero = db.Column(db.Integer, db.ForeignKey('Staff.id'))
    Equipo_1 = db.Column(db.Integer, db.ForeignKey('Equipo.id'))
    Equipo_2 = db.Column(db.Integer, db.ForeignKey('Equipo.id'))
    Fase = db.Column(db.String(25))
    Horario_inicio = db.Column(db.Time)
    Horario_final = db.Column(db.Time)
    Puntaje_e1 = db.Column(db.Integer, default=0)
    Puntaje_e2 = db.Column(db.Integer, default=0)
    Resultado = db.Column(db.Integer)
    Infracciones_e1 = db.Column(db.Integer)
    Infracciones_e2 = db.Column(db.Integer)

class Staff(db.Model):
    __tablename__ = "Staff"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(40))
    DNI = db.Column(db.Integer)
    Telefono = db.Column(db.Integer)
    Email = db.Column(db.String(40))
    Trabajo = db.Column(db.String(15))
    Sector = db.Column(db.String(20))

class Example(db.Model):
    __tablename__ = "examples"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), default="-")

class Producto (db.Model):
  __tablename__ = "Producto"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  Nombre= db.Column(db.String(50), default="-")
  Precio = db.Column(db.Integer)
  tipo_img = db.Column(db.String(50))
  tamaño_img = db.Column(db.BigInteger)
  pixel_img = db.Column(db.LargeBinary)



@apis.route("/updatepage/<string:table>/<int:id>")
def update(table,id):
    if not current_user.rango in ["adm","fix"]:
        _class=globals()[table]
        objeto = _class.query.filter_by(id=id).first()
        var_names = [name for name in vars(_class) if not name.startswith('_') and  not name=="id"]   
        return render_template("/update.html",objeto=objeto,var_names=var_names)
    return redirect("/")



def validate_fields(data, required):
    missing = [field for field in required if field not in data or data[field] is None]
    return missing

@apis.route("/api/example", methods=["POST"])
def add_example():
    if request.method == 'POST':
        new_name = request.form['example']
        new_example = Example(nombre=new_name)
        db.session.add(new_example)
        db.session.commit()
        return redirect(url_for("rutas.Index"))

@apis.route("/update/examples/<int:id>", methods=["POST","GET"])
def update_example(id):
    if not current_user.rango in ["adm","fix"]:
        example = Example.query.filter_by(id=id).first()
        print(id)
        data = request.form
        example.nombre=data.get("example")
        db.session.commit()
    return redirect(f"/")

    
@apis.route("/api/example/delete/<int:id>")
def delete_example(id):
    if not current_user.rango in ["adm","cant","fix"]:
        example = Example.query.get(id)
        db.session.delete(example)
        db.session.commit()
    return redirect("/")

# tabla EQUIPO

@apis.route("/api/equipo", methods=["POST"])
def add_equipo():
    data = request.get_json()
    required = ["Deporte", "Categoria", "Sexo", "Colegio"]
    missing = validate_fields(data, required)
    if missing:
        return jsonify(success=False, error=f"Faltan campos requeridos: {', '.join(missing)}"), 400
    nuevo = Equipo(**{k: data.get(k) for k in required})
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(success=True, equipo={"id": nuevo.id})

@apis.route("/update/equipo/<int:id>", methods=["POST","GET"])
def update_equipo(id):
    if not current_user.rango in ["adm","fix"]:
        equipo = Equipo.query.filter_by(id=id).first()
        
        data = request.form
        equipo.Deporte=data.get("Deporte")
        equipo.Categoria=data.get("Categoria")
        equipo.Sexo=data.get("Sexo")
        equipo.Colegio=data.get("Colegio")
        db.session.commit()
    return redirect(f"/")

@apis.route("/api/equipo/delete/<int:id>")
def delete_equipo(id):
    if current_user.rango in ["adm","cant","fix"]:
        equipo = Equipo.query.get(id)
        db.session.delete(equipo)
        db.session.commit()
    return redirect("/")

# tabla JUGADOR

@apis.route("/api/jugador", methods=["POST"])
def add_jugador():
    data = request.get_json()
    required = ["id_equipo", "Nombre"]
    missing = validate_fields(data, required)
    if missing:
        return jsonify(success=False, error=f"Faltan campos requeridos: {', '.join(missing)}"), 400
    nuevo = Jugador(**{k: data.get(k) for k in ["id_equipo", "Nombre", "DNI", "Telefono", "Email", "Comida_especial", "Fecha_nacimiento", "Infracciones"]})
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(success=True, jugador={"id": nuevo.id})

@apis.route("/update/jugador/<int:id>", methods=["POST","GET"])
def update_jugador(id):
    if not current_user.rango in ["adm","fix"]:
        jugador = Equipo.query.filter_by(id=id).first()
        
        data = request.form
        jugador.Deporte=data.get("Deporte")
        jugador.Categoria=data.get("Categoria")
        jugador.Sexo=data.get("Sexo")
        jugador.Colegio=data.get("Colegio")
        db.session.commit()
    return redirect(f"/")

@apis.route("/api/jugador/<int:id>", methods=["DELETE"])
def delete_jugador(id):
    jugador = Jugador.query.get(id)
    if not jugador:
        return jsonify(success=False, error="Jugador no encontrado"), 404
    db.session.delete(jugador)
    db.session.commit()
    return jsonify(success=True, deleted=id)

# tabla RESPONSABLE

@apis.route("/api/responsable", methods=["POST"])
def add_responsable():
    data = request.get_json()
    required = ["id_equipo", "Nombre"]
    missing = validate_fields(data, required)
    if missing:
        return jsonify(success=False, error=f"Faltan campos requeridos: {', '.join(missing)}"), 400
    nuevo = Responsable(**{k: data.get(k) for k in ["id_equipo", "Nombre", "DNI", "Telefono", "Email", "Comida_especial", "Fecha_nacimiento"]})
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(success=True, responsable={"id": nuevo.id})

@apis.route("/api/responsable/<int:id>", methods=["PUT"])
def update_responsable(id):
    pass

@apis.route("/api/responsable/<int:id>", methods=["DELETE"])
def delete_responsable(id):
    responsable = Responsable.query.get(id)
    if not responsable:
        return jsonify(success=False, error="Responsable no encontrado"), 404
    db.session.delete(responsable)
    db.session.commit()
    return jsonify(success=True, deleted=id)

# tabla PARTIDO

@apis.route("/api/partido", methods=["POST"])
def add_partido():
    data = request.get_json()
    required = ["Deporte", "Categoria", "Sexo", "Arbitro", "Planillero", "Equipo_1", "Equipo_2", "Fase", "Horario_inicio", "Horario_final","Puntaje_e1", "Puntaje_e2", "Resultado", "Infracciones_e1", "Infracciones_e2"]
    missing = validate_fields(data, required)
    if missing:
        return jsonify(success=False, error=f"Faltan campos requeridos: {', '.join(missing)}"), 400
    nuevo = Partido(**{k: data.get(k) for k in required})
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(success=True, partido={"id": nuevo.id})

@apis.route("/api/partido/<int:id>", methods=["PUT"])
def update_partido(id):
    pass

@apis.route("/api/partido/<int:id>", methods=["DELETE"])
def delete_partido(id):
    partido = Partido.query.get(id)
    if not partido:
        return jsonify(success=False, error="Partido no encontrado"), 404
    db.session.delete(partido)
    db.session.commit()
    return jsonify(success=True, deleted=id)


# tabla STAFF

@apis.route("/api/staff", methods=["POST"])
def add_staff():
    data = request.get_json()
    required = ["Nombre", "DNI", "Telefono", "Email", "Trabajo", "Sector"]
    missing = validate_fields(data, required)
    if missing:
        return jsonify(success=False, error=f"Faltan campos requeridos: {', '.join(missing)}"), 400
    nuevo = Staff(**{k: data.get(k) for k in required})
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(success=True, staff={"id": nuevo.id})

@apis.route("/api/staff/<int:id>", methods=["PUT"])
def update_staff(id):
    pass

@apis.route("/api/staff/<int:id>", methods=["DELETE"])
def delete_staff(id):
    staff = Staff.query.get(id)
    if not staff:
        return jsonify(success=False, error="Staff no encontrado"), 404
    db.session.delete(staff)
    db.session.commit()
    return jsonify(success=True, deleted=id)

@apis.route("/cantina/agregar", methods=["POST","Get"])
def add_product():
    if current_user.rango in ["admin","cantina"]:
        data = request.form

        
        archivo = request.files.get("archivo")

        tipo = ""
        tamano = 0
        pixel = None

        tipo = archivo.content_type
        cont = archivo.read()
        tamano = len(cont)
        pixel = cont

        nuevo = Producto(
            Nombre=data.get("nombre"),
            Precio=float(data.get("precio")),
            tipo_img=tipo,
            tamaño_img=tamano,
            pixel_img=pixel
        )

        try:
            db.session.add(nuevo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Error al guardar: {e}", 500

        return redirect("/cantina")

@apis.route("/update/examples/<int:id>", methods=["POST","GET"])
def update_product(id):
    if current_user.rango in ["admin","cantina"]:
        producto = Producto.query.filter_by(id=id).first()
        data = request.form
        archivo = request.files.get("archivo")
        tipo = archivo.content_type
        cont = archivo.read()
        tamano = len(cont)
        pixel = cont

        producto.Nombre=data.get("Nombre")
        producto.Precio=data.get("Precio")
        tipo_img=tipo,
        tamaño_img=tamano,
        pixel_img=pixel

        db.session.commit()
    return redirect(f"/cantina")

    
@apis.route("/api/product/delete/<int:id>")
def delete_product(id):
    if current_user.rango in ["admin","cantina"]:
        producto = Producto.query.get(id)
        db.session.delete(producto)
        db.session.commit()
    return redirect("/cantina")

