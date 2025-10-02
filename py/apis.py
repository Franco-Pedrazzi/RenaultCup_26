from flask import Blueprint, request, jsonify, redirect,url_for
from py.db import db 

apis = Blueprint("apis", __name__)


class Equipo(db.Model):
    __tablename__ = "Equipo"
    id_equipo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Deporte = db.Column(db.String(10), default="-")
    Categoria = db.Column(db.String(10), default="-")
    Sexo = db.Column(db.String(10), default="-")
    Colegio = db.Column(db.String(50), default="-")

class Jugador(db.Model):
    __tablename__ = "jugador"
    id_jugador = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_equipo = db.Column(db.Integer, db.ForeignKey('Equipo.id_equipo'))
    Nombre = db.Column(db.String(50), default="-")
    DNI = db.Column(db.String(10))
    Telefono = db.Column(db.String(15))
    Email = db.Column(db.String(40))
    Comida_especial = db.Column(db.String(3), default="N")
    Fecha_nacimiento = db.Column(db.Date)
    Infracciones = db.Column(db.String(10), default="0")

class Responsable(db.Model):
    __tablename__ = "Responsable"
    id_profesor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_equipo = db.Column(db.Integer, db.ForeignKey('Equipo.id_equipo'))
    Nombre = db.Column(db.String(50), default="-")
    DNI = db.Column(db.String(10))
    Telefono = db.Column(db.String(15))
    Email = db.Column(db.String(40))
    Comida_especial = db.Column(db.String(3), default="N")
    Fecha_nacimiento = db.Column(db.Date)

class Partido(db.Model):
    __tablename__ = "Partido"
    id_partido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Deporte = db.Column(db.String(1))
    Categoria = db.Column(db.String(3))
    Sexo = db.Column(db.String(1))
    Arbitro = db.Column(db.Integer, db.ForeignKey('Staff.id_staff'))
    Planillero = db.Column(db.Integer, db.ForeignKey('Staff.id_staff'))
    Equipo_1 = db.Column(db.Integer, db.ForeignKey('Equipo.id_equipo'))
    Equipo_2 = db.Column(db.Integer, db.ForeignKey('Equipo.id_equipo'))
    Fase = db.Column(db.String(25))
    Horario_inicio = db.Column(db.Time)
    Horario_final = db.Column(db.Time)

class Resultado(db.Model):
    __tablename__ = "Resultado"
    id_partido = db.Column(db.Integer, db.ForeignKey('Partido.id_partido'), primary_key=True)
    Puntaje_e1 = db.Column(db.Integer, default=0)
    Puntaje_e2 = db.Column(db.Integer, default=0)
    Resultado = db.Column(db.Integer)
    Infracciones_e1 = db.Column(db.Integer)
    Infracciones_e2 = db.Column(db.Integer)

class Staff(db.Model):
    __tablename__ = "Staff"
    id_staff = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombre = db.Column(db.String(40))
    DNI = db.Column(db.Integer)
    Telefono = db.Column(db.Integer)
    Email = db.Column(db.String(40))
    Trabajo = db.Column(db.String(15))
    Sector = db.Column(db.String(20))

class Example(db.Model):
    __tablename__ = "examples"
    id_example = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), default="-")

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

@apis.route("/api/example/<int:id_example>", methods=["PUT"])
def update_example(id_example):
    example = Example.query.get_or_404(id_example)
    if request.method == 'POST':
        example.example = request.form['example']
        db.session.commit()
        return redirect(url_for("rutas.Index"))
    
@apis.route("/api/example/<int:id_example>", methods=["DELETE"])
def delete_example(id_example):
    example = Example.query.get(id_example)
    if not example:
        return jsonify(success=False, error="Equipo no encontrado"), 404
    db.session.delete(example)
    db.session.commit()
    return jsonify(success=True, deleted=id_example)

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
    return jsonify(success=True, equipo={"id_equipo": nuevo.id_equipo})

@apis.route("/api/equipo/<int:id_equipo>", methods=["PUT"])
def update_equipo(id_equipo):
    equipo = Equipo.query.get(id_equipo)
    if not equipo:
        return jsonify(success=False, error="Equipo no encontrado"), 404
    data = request.get_json()
    for k in ["Deporte", "Categoria", "Sexo", "Colegio"]:
        if k in data:
            setattr(equipo, k, data[k])
    db.session.commit()
    return jsonify(success=True, equipo={"id_equipo": equipo.id_equipo})

@apis.route("/api/equipo/<int:id_equipo>", methods=["DELETE"])
def delete_equipo(id_equipo):
    equipo = Equipo.query.get(id_equipo)
    if not equipo:
        return jsonify(success=False, error="Equipo no encontrado"), 404
    db.session.delete(equipo)
    db.session.commit()
    return jsonify(success=True, deleted=id_equipo)

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
    return jsonify(success=True, jugador={"id_jugador": nuevo.id_jugador})

@apis.route("/api/jugador/<int:id_jugador>", methods=["PUT"])
def update_jugador(id_jugador):
    jugador = Jugador.query.get(id_jugador)
    if not jugador:
        return jsonify(success=False, error="Jugador no encontrado"), 404
    data = request.get_json()
    for k in ["id_equipo", "Nombre", "DNI", "Telefono", "Email", "Comida_especial", "Fecha_nacimiento", "Infracciones"]:
        if k in data:
            setattr(jugador, k, data[k])
    db.session.commit()
    return jsonify(success=True, jugador={"id_jugador": jugador.id_jugador})

@apis.route("/api/jugador/<int:id_jugador>", methods=["DELETE"])
def delete_jugador(id_jugador):
    jugador = Jugador.query.get(id_jugador)
    if not jugador:
        return jsonify(success=False, error="Jugador no encontrado"), 404
    db.session.delete(jugador)
    db.session.commit()
    return jsonify(success=True, deleted=id_jugador)

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
    return jsonify(success=True, responsable={"id_profesor": nuevo.id_profesor})

@apis.route("/api/responsable/<int:id_profesor>", methods=["PUT"])
def update_responsable(id_profesor):
    responsable = Responsable.query.get(id_profesor)
    if not responsable:
        return jsonify(success=False, error="Responsable no encontrado"), 404
    data = request.get_json()
    for k in ["id_equipo", "Nombre", "DNI", "Telefono", "Email", "Comida_especial", "Fecha_nacimiento"]:
        if k in data:
            setattr(responsable, k, data[k])
    db.session.commit()
    return jsonify(success=True, responsable={"id_profesor": responsable.id_profesor})

@apis.route("/api/responsable/<int:id_profesor>", methods=["DELETE"])
def delete_responsable(id_profesor):
    responsable = Responsable.query.get(id_profesor)
    if not responsable:
        return jsonify(success=False, error="Responsable no encontrado"), 404
    db.session.delete(responsable)
    db.session.commit()
    return jsonify(success=True, deleted=id_profesor)

# tabla PARTIDO

@apis.route("/api/partido", methods=["POST"])
def add_partido():
    data = request.get_json()
    required = ["Deporte", "Categoria", "Sexo", "Arbitro", "Planillero", "Equipo_1", "Equipo_2", "Fase", "Horario_inicio", "Horario_final"]
    missing = validate_fields(data, required)
    if missing:
        return jsonify(success=False, error=f"Faltan campos requeridos: {', '.join(missing)}"), 400
    nuevo = Partido(**{k: data.get(k) for k in required})
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(success=True, partido={"id_partido": nuevo.id_partido})

@apis.route("/api/partido/<int:id_partido>", methods=["PUT"])
def update_partido(id_partido):
    partido = Partido.query.get(id_partido)
    if not partido:
        return jsonify(success=False, error="Partido no encontrado"), 404
    data = request.get_json()
    for k in ["Deporte", "Categoria", "Sexo", "Arbitro", "Planillero", "Equipo_1", "Equipo_2", "Fase", "Horario_inicio", "Horario_final"]:
        if k in data:
            setattr(partido, k, data[k])
    db.session.commit()
    return jsonify(success=True, partido={"id_partido": partido.id_partido})

@apis.route("/api/partido/<int:id_partido>", methods=["DELETE"])
def delete_partido(id_partido):
    partido = Partido.query.get(id_partido)
    if not partido:
        return jsonify(success=False, error="Partido no encontrado"), 404
    db.session.delete(partido)
    db.session.commit()
    return jsonify(success=True, deleted=id_partido)

# tabla RESULTADO

@apis.route("/api/resultados", methods=["POST"])
def add_resultado():
    data = request.get_json()
    required = ["id_partido", "Puntaje_e1", "Puntaje_e2", "Resultado", "Infracciones_e1", "Infracciones_e2"]
    missing = validate_fields(data, required)
    if missing:
        return jsonify(success=False, error=f"Faltan campos requeridos: {', '.join(missing)}"), 400
    if Resultado.query.get(data["id_partido"]):
        return jsonify(success=False, error="Resultado para ese partido ya existe"), 409
    nuevo = Resultado(**{k: data.get(k) for k in required})
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(success=True, resultado={"id_partido": nuevo.id_partido})

@apis.route("/api/resultados/<int:id_partido>", methods=["PUT"])
def update_resultado(id_partido):
    resultado = Resultado.query.get(id_partido)
    if not resultado:
        return jsonify(success=False, error="Resultado no encontrado"), 404
    data = request.get_json()
    for k in ["Puntaje_e1", "Puntaje_e2", "Resultado", "Infracciones_e1", "Infracciones_e2"]:
        if k in data:
            setattr(resultado, k, data[k])
    db.session.commit()
    return jsonify(success=True, resultado={"id_partido": resultado.id_partido})

@apis.route("/api/resultados/<int:id_partido>", methods=["DELETE"])
def delete_resultado(id_partido):
    resultado = Resultado.query.get(id_partido)
    if not resultado:
        return jsonify(success=False, error="Resultado no encontrado"), 404
    db.session.delete(resultado)
    db.session.commit()
    return jsonify(success=True, deleted=id_partido)

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
    return jsonify(success=True, staff={"id_staff": nuevo.id_staff})

@apis.route("/api/staff/<int:id_staff>", methods=["PUT"])
def update_staff(id_staff):
    staff = Staff.query.get(id_staff)
    if not staff:
        return jsonify(success=False, error="Staff no encontrado"), 404
    data = request.get_json()
    for k in ["Nombre", "DNI", "Telefono", "Email", "Trabajo", "Sector"]:
        if k in data:
            setattr(staff, k, data[k])
    db.session.commit()
    return jsonify(success=True, staff={"id_staff": staff.id_staff})

@apis.route("/api/staff/<int:id_staff>", methods=["DELETE"])
def delete_staff(id_staff):
    staff = Staff.query.get(id_staff)
    if not staff:
        return jsonify(success=False, error="Staff no encontrado"), 404
    db.session.delete(staff)
    db.session.commit()
    return jsonify(success=True, deleted=id_staff)


