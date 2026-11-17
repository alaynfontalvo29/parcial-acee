from sqlalchemy import Float, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


# =====================================
# TODO ORM 1 - CONFIGURAR LA CONEXION
# =====================================

# Crear el engine para conectar con una base SQLite llamada zapateria.db
engine = create_engine("sqlite:///zapateria.db", echo=False)


# =====================================
# TODO ORM 2 - CREAR LA CLASE BASE
# =====================================

# Crear la clase Base utilizando DeclarativeBase.
class Base(DeclarativeBase):
    pass


# =====================================
# TODO ORM 3 - CREAR EL MODELO ZAPATO
# =====================================

# Construir la clase Zapato utilizando Mapped y mapped_column.
class Zapato(Base):
    __tablename__ = "zapatos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    modelo: Mapped[str] = mapped_column(String, nullable=False)
    talla: Mapped[int] = mapped_column(Integer, nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f"<Zapato(id={self.id}, modelo='{self.modelo}', talla={self.talla}, precio={self.precio})>"


# =====================================
# TODO ORM 4 - CREAR LA TABLA
# =====================================

def inicializar_bd():
    """Crea las tablas del modelo utilizando el engine si no existen."""
    Base.metadata.create_all(bind=engine)


# =====================================
# TODO ORM 5 - REGISTRAR ZAPATO
# =====================================

def crear_zapato(modelo, talla, precio):
    """Crea un objeto Zapato, lo almacena en la BD y retorna True si tiene éxito."""
    inicializar_bd()
    try:
        session = Session(engine)
        nuevo_zapato = Zapato(modelo=modelo, talla=talla, precio=precio)
        session.add(nuevo_zapato)
        session.commit()
        session.close()
        return True
    except Exception as e:
        print(f"Error al registrar el zapato: {e}")
        return False


# =====================================
# TODO ORM 6 - LISTAR ZAPATOS
# =====================================

def listar_zapatos():
    """Consulta todos los objetos Zapato utilizando SQLAlchemy y retorna una lista."""
    inicializar_bd()
    try:
        session = Session(engine)
        zapatos = session.scalars(select(Zapato)).all()
        resultado = list(zapatos)
        session.close()
        return resultado
    except Exception as e:
        print(f"Error al listar los zapatos: {e}")
        return []


# =====================================
# TODO ORM 7 - BUSCAR POR ID
# =====================================

def buscar_zapato(id_zapato):
    """Busca un Zapato por su ID. Retorna el objeto encontrado o None si no existe."""
    inicializar_bd()
    try:
        session = Session(engine)
        zapato = session.get(Zapato, id_zapato)
        # Nota: Retornamos el objeto. Como la sesión se cierra, SQLAlchemy 
        # permite leer atributos cargados, pero para mayor seguridad aseguramos la consulta.
        session.close()
        return zapato
    except Exception as e:
        print(f"Error al buscar el zapato: {e}")
        return None


# =====================================
# TODO ORM 8 - ACTUALIZAR PRECIO
# =====================================

def actualizar_precio(id_zapato, nuevo_precio):
    """Busca el zapato por ID, modifica su precio y confirma. Retorna True o False."""
    inicializar_bd()
    try:
        session = Session(engine)
        zapato = session.get(Zapato, id_zapato)
        if zapato:
            zapato.precio = nuevo_precio
            session.commit()
            session.close()
            return True
        session.close()
        return False
    except Exception as e:
        print(f"Error al actualizar el precio: {e}")
        return False


# =====================================
# TODO ORM 9 - ELIMINAR ZAPATO
# =====================================

def eliminar_zapato(id_zapato):
    """Busca el zapato por ID, lo elimina con el ORM y confirma. Retorna True o False."""
    inicializar_bd()
    try:
        session = Session(engine)
        zapato = session.get(Zapato, id_zapato)
        if zapato:
            session.delete(zapato)
            session.commit()
            session.close()
            return True
        session.close()
        return False
    except Exception as e:
        print(f"Error al eliminar el zapato: {e}")
        return False