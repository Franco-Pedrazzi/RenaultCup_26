from flask import Blueprint, request, jsonify
from py.db import db 

apis = Blueprint("apis", __name__)


class Usuario(db.Model):
    __tablename__ = "usuario"
    Nombre = db.Column(db.String(40), nullable=False)
    Email = db.Column(db.String(40), primary_key=True, nullable=False)
    Contraseña = db.Column(db.String(200), nullable=False)
    rango = db.Column(db.String(20))

class Verificacion(db.Model):
    __tablename__ = "Verificacion"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email = db.Column(db.String(40), nullable=False)
    codigo = db.Column(db.String(20), nullable=False)
    contra_codificada = db.Column(db.String(200), nullable=False)
    nombre = db.Column(db.String(40), nullable=False)
    rango = db.Column(db.String(20), nullable=False)

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

def validate_fields(data, required):
    missing = [field for field in required if field not in data or data[field] is None]
    return missing

# tabla USUARIO
@apis.route("/api/usuario", methods=["GET"])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([
        {"Nombre": u.Nombre, "Email": u.Email, "Contraseña": u.Contraseña, "rango": u.rango}
        for u in usuarios
    ])

@apis.route("/api/usuario", methods=["POST"])
def add_usuario():
    data = request.get_json()
    required = ["Nombre", "Email", "Contraseña"]
    missing = validate_fields(data, required)
    if missing:
        return jsonify(success=False, error=f"Faltan campos requeridos: {', '.join(missing)}"), 400
    if Usuario.query.get(data["Email"]):
        return jsonify(success=False, error="El usuario ya existe"), 409
    nuevo = Usuario(**{k: data.get(k) for k in ["Nombre", "Email", "Contraseña", "rango"]})
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(success=True, usuario={"Email": nuevo.Email})

@apis.route("/api/usuario/<email>", methods=["PUT"])
def update_usuario(email):
    usuario = Usuario.query.get(email)
    if not usuario:
        return jsonify(success=False, error="Usuario no encontrado"), 404
    data = request.get_json()
    for k in ["Nombre", "Contraseña", "rango"]:
        if k in data:
            setattr(usuario, k, data[k])
    db.session.commit()
    return jsonify(success=True, usuario={"Email": usuario.Email})

@apis.route("/api/usuario/<email>", methods=["DELETE"])
def delete_usuario(email):
    usuario = Usuario.query.get(email)
    if not usuario:
        return jsonify(success=False, error="Usuario no encontrado"), 404
    db.session.delete(usuario)
    db.session.commit()
    return jsonify(success=True, deleted=email)

# tabla VERIFICACION
@apis.route("/api/verificacion", methods=["GET"])
def get_verificaciones():
    verifs = Verificacion.query.all()
    return jsonify([
        {"id": v.id, "Email": v.Email, "codigo": v.codigo, "contra_codificada": v.contra_codificada, "nombre": v.nombre, "rango": v.rango}
        for v in verifs
    ])

@apis.route("/api/verificacion", methods=["POST"])
def add_verificacion():
    data = request.get_json()
    required = ["Email", "codigo", "contra_codificada", "nombre", "rango"]
    missing = validate_fields(data, required)
    if missing:
        return jsonify(success=False, error=f"Faltan campos requeridos: {', '.join(missing)}"), 400
    nuevo = Verificacion(**{k: data.get(k) for k in required})
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(success=True, verificacion={"id": nuevo.id})

@apis.route("/api/verificacion/<int:id>", methods=["PUT"])
def update_verificacion(id):
    verif = Verificacion.query.get(id)
    if not verif:
        return jsonify(success=False, error="Verificación no encontrada"), 404
    data = request.get_json()
    for k in ["Email", "codigo", "contra_codificada", "nombre", "rango"]:
        if k in data:
            setattr(verif, k, data[k])
    db.session.commit()
    return jsonify(success=True, verificacion={"id": verif.id})

@apis.route("/api/verificacion/<int:id>", methods=["DELETE"])
def delete_verificacion(id):
    verif = Verificacion.query.get(id)
    if not verif:
        return jsonify(success=False, error="Verificación no encontrada"), 404
    db.session.delete(verif)
    db.session.commit()
    return jsonify(success=True, deleted=id)

# tabla EQUIPO
@apis.route("/api/equipo", methods=["GET"])
def get_equipos():
    equipos = Equipo.query.all()
    return jsonify([
        {"id_equipo": e.id_equipo, "Deporte": e.Deporte, "Categoria": e.Categoria, "Sexo": e.Sexo, "Colegio": e.Colegio}
        for e in equipos
    ])

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
@apis.route("/api/jugador", methods=["GET"])
def get_jugadores():
    jugadores = Jugador.query.all()
    return jsonify([
        {"id_jugador": j.id_jugador, "id_equipo": j.id_equipo, "Nombre": j.Nombre, "DNI": j.DNI, "Telefono": j.Telefono, "Email": j.Email, "Comida_especial": j.Comida_especial, "Fecha_nacimiento": str(j.Fecha_nacimiento), "Infracciones": j.Infracciones}
        for j in jugadores
    ])

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
@apis.route("/api/responsable", methods=["GET"])
def get_responsables():
    responsables = Responsable.query.all()
    return jsonify([
        {"id_profesor": r.id_profesor, "id_equipo": r.id_equipo, "Nombre": r.Nombre, "DNI": r.DNI, "Telefono": r.Telefono, "Email": r.Email, "Comida_especial": r.Comida_especial, "Fecha_nacimiento": str(r.Fecha_nacimiento)}
        for r in responsables
    ])

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
@apis.route("/api/partido", methods=["GET"])
def get_partidos():
    partidos = Partido.query.all()
    return jsonify([
        {"id_partido": p.id_partido, "Deporte": p.Deporte, "Categoria": p.Categoria, "Sexo": p.Sexo, "Arbitro": p.Arbitro, "Planillero": p.Planillero, "Equipo_1": p.Equipo_1, "Equipo_2": p.Equipo_2, "Fase": p.Fase, "Horario_inicio": str(p.Horario_inicio), "Horario_final": str(p.Horario_final)}
        for p in partidos
    ])

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
@apis.route("/api/resultados", methods=["GET"])
def get_resultados():
    resultados = Resultado.query.all()
    return jsonify([
        {"id_partido": r.id_partido, "Puntaje_e1": r.Puntaje_e1, "Puntaje_e2": r.Puntaje_e2, "Resultado": r.Resultado, "Infracciones_e1": r.Infracciones_e1, "Infracciones_e2": r.Infracciones_e2}
        for r in resultados
    ])

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
@apis.route("/api/staff", methods=["GET"])
def get_staff():
    staff = Staff.query.all()
    return jsonify([
        {"id_staff": s.id_staff, "Nombre": s.Nombre, "DNI": s.DNI, "Telefono": s.Telefono, "Email": s.Email, "Trabajo": s.Trabajo, "Sector": s.Sector}
        for s in staff
    ])

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