from database import db
from datetime import datetime


# ---------------------------
# CARRERA
# ---------------------------
class Carrera(db.Model):
    __tablename__ = 'Carrera'
    Id_Car = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nom_Car = db.Column(db.String(150), nullable=False)
    Des_Car = db.Column(db.Text, nullable=True)
    Fec_Cre = db.Column(db.DateTime, default=datetime.utcnow)
    Fec_Mod = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    fichas = db.relationship('Fichas', backref='carrera', lazy=True)


# ---------------------------
# FICHAS
# ---------------------------
class Fichas(db.Model):
    __tablename__ = 'Fichas'
    Id_Fic = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_Car = db.Column(db.Integer, db.ForeignKey('Carrera.Id_Car'), nullable=False)
    Fec_inicio_Fic = db.Column(db.Date, nullable=False)
    Fec_Fin_Fic = db.Column(db.Date, nullable=False)
    Num_Fic = db.Column(db.Integer, nullable=False, unique=True)
    Jor_Fic = db.Column(db.Enum('Mañana', 'Tarde', 'Noche'), nullable=False)
    Fec_Cre = db.Column(db.DateTime, default=datetime.utcnow)
    Fec_Mod = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    aprendices = db.relationship('Aprendiz', backref='ficha', lazy=True)
    resultados_aprendizaje = db.relationship('ResultadoAprendizaje', backref='ficha', lazy=True)
    asistencias = db.relationship('Asistencia', backref='ficha', lazy=True)


# ---------------------------
# COMPETENCIA
# ---------------------------
class Competencia(db.Model):
    __tablename__ = 'competencia'
    Id_Comp = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nom_Comp = db.Column(db.String(150), nullable=False)
    Des_Comp = db.Column(db.Text, nullable=True)
    Fec_Cre = db.Column(db.DateTime, default=datetime.utcnow)
    Fec_Mod = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    resultados_aprendizaje = db.relationship('ResultadoAprendizaje', backref='competencia', lazy=True)


# ---------------------------
# INSTRUCTOR
# ---------------------------
class Instructor(db.Model):
    __tablename__ = 'Instructor'
    Id_Ins = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nom_Ins = db.Column(db.String(100), nullable=False)
    Ape_Ins = db.Column(db.String(100), nullable=False)
    Tip_ide_Ins = db.Column(db.Enum('CC', 'TI', 'CE', 'PEP', 'PPT'), nullable=False)
    Num_ide_Ins = db.Column(db.Integer, nullable=False, unique=True)
    Cor_Ins = db.Column(db.String(100), nullable=False, unique=True)
    Con_Ins = db.Column(db.String(255), nullable=False) 
    Es_Ins = db.Column(db.Boolean, nullable=False, default=True)
    Fec_Cre = db.Column(db.DateTime, default=datetime.utcnow)
    Fec_Mod = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    notificaciones = db.relationship('Notificacion', backref='instructor', lazy=True)


# ---------------------------
# ADMINISTRADOR
# ---------------------------
class Administrador(db.Model):
    __tablename__ = 'Administrador'
    Id_Adm = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nom_Adm = db.Column(db.String(100), nullable=False)
    Ape_Adm = db.Column(db.String(100), nullable=False)
    Tip_ide_Adm = db.Column(db.Enum('CC', 'TI', 'CE', 'PEP', 'PPT'), nullable=False)
    Num_ide_Adm = db.Column(db.Integer, nullable=False, unique=True)
    Cor_Adm = db.Column(db.String(100), nullable=False, unique=True)
    Con_Adm = db.Column(db.String(255), nullable=False)  
    Es_Adm = db.Column(db.Boolean, nullable=False, default=True)
    Fec_Cre = db.Column(db.DateTime, default=datetime.utcnow)
    Fec_Mod = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    notificaciones = db.relationship('Notificacion', backref='administrador', lazy=True)


# ---------------------------
# APRENDIZ
# ---------------------------
class Aprendiz(db.Model):
    __tablename__ = 'Aprendiz'
    Id_Apr = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nom_Apr = db.Column(db.String(100), nullable=False)
    Ape_Apr = db.Column(db.String(100), nullable=False)
    Tip_ide_Apr = db.Column(db.Enum('CC', 'TI', 'CE', 'PEP', 'PPT'), nullable=False)
    Num_ide_Apr = db.Column(db.Integer, nullable=False, unique=True)
    Cor_Apr = db.Column(db.String(100), nullable=False, unique=True)
    Con_Apr = db.Column(db.String(255), nullable=False)  
    Es_Apr = db.Column(db.Boolean, nullable=False, default=True)
    Id_Fic = db.Column(db.Integer, db.ForeignKey('Fichas.Id_Fic'), nullable=True)
    Fec_Cre = db.Column(db.DateTime, default=datetime.utcnow)
    Fec_Mod = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    asistencias = db.relationship('Asistencia', backref='aprendiz', lazy=True)
    notificaciones = db.relationship('Notificacion', backref='aprendiz', lazy=True)


# ---------------------------
# FICHA_INSTRUCTOR (tabla intermedia, PK compuesta)
# ---------------------------
class FichaInstructor(db.Model):
    __tablename__ = 'Ficha_Instructor'
    Id_Fic = db.Column(db.Integer, db.ForeignKey('Fichas.Id_Fic'), primary_key=True)
    Id_Ins = db.Column(db.Integer, db.ForeignKey('Instructor.Id_Ins'), primary_key=True)

    ficha = db.relationship('Fichas', backref='instructores_asignados')
    instructor = db.relationship('Instructor', backref='fichas_asignadas')


# ---------------------------
# RESULTADO DE APRENDIZAJE
# ---------------------------
class ResultadoAprendizaje(db.Model):
    __tablename__ = 'ResultadoAprendizaje'
    Id_RA = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nom_RA = db.Column(db.String(150), nullable=False)
    Des_RA = db.Column(db.Text, nullable=True)
    Id_Fic = db.Column(db.Integer, db.ForeignKey('Fichas.Id_Fic'), nullable=False)
    Id_Comp = db.Column(db.Integer, db.ForeignKey('competencia.Id_Comp'), nullable=False)
    Fec_Cre = db.Column(db.DateTime, default=datetime.utcnow)
    Fec_Mod = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ---------------------------
# ASISTENCIA
# ---------------------------
class Asistencia(db.Model):
    __tablename__ = 'Asistencia'
    Id_Asi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Fec_Asi = db.Column(db.Date, nullable=False)
    Es_Asi = db.Column(db.Enum('Retardo', 'Excusa', 'Falla', 'Presente'), nullable=False)
    Id_Apr = db.Column(db.Integer, db.ForeignKey('Aprendiz.Id_Apr'), nullable=False)
    Id_Fic = db.Column(db.Integer, db.ForeignKey('Fichas.Id_Fic'), nullable=False)
    Fec_Cre = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------
# NOTIFICACION
# ---------------------------
class Notificacion(db.Model):
    __tablename__ = 'Notificacion'
    Id_Not = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Asu_Not = db.Column(db.Text, nullable=False)
    Men_Not = db.Column(db.Text, nullable=False)
    Fec_Not = db.Column(db.Date, nullable=False)
    Id_Apr = db.Column(db.Integer, db.ForeignKey('Aprendiz.Id_Apr'), nullable=True)
    Id_Ins = db.Column(db.Integer, db.ForeignKey('Instructor.Id_Ins'), nullable=True)
    Id_Adm = db.Column(db.Integer, db.ForeignKey('Administrador.Id_Adm'), nullable=True)
    Fec_Cre = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------
# LOG (auditoría)
# ---------------------------
class Log(db.Model):
    __tablename__ = 'Log'
    Id_Log = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Tabla_Afectada = db.Column(db.String(50), nullable=False)
    Id_Registro = db.Column(db.Integer, nullable=False)
    Accion = db.Column(db.Enum('INSERT', 'UPDATE', 'DELETE'), nullable=False)
    Usu_Log = db.Column(db.String(100), nullable=False)
    Fec_Log = db.Column(db.DateTime, default=datetime.utcnow)
    Det_Log = db.Column(db.Text, nullable=True)