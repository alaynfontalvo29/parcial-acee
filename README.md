# SISTEMA DE INVENTARIO DE ZAPATOS
### Implementación de operaciones CRUD con SQLAlchemy ORM

## 1. Información del proyecto

| Información | Descripción |
|---|---|
| Estudiante | Alayn Fontalvo Castro |
| Asignatura | Desarrollo con Acceso a Datos |
| Docente | Eduardo Pimienta |
| Lenguaje | Python |
| ORM | SQLAlchemy 2.0 |
| Base de datos | SQLite |
| Entorno de desarrollo | Visual Studio Code |

---

## 2. Descripción del proyecto

### ¿En qué consiste el programa?

El proyecto consiste en una aplicación desarrollada en Python para llevar un control básico de los zapatos disponibles en una tienda. Su objetivo es facilitar el manejo de la información de cada producto, incluyendo el modelo, la talla y el precio.

Para almacenar los datos se utiliza SQLite, mientras que SQLAlchemy permite realizar las operaciones sobre la base de datos mediante objetos de Python.

### ¿Qué funcionalidades tiene?

El sistema permite realizar cinco operaciones principales:

1. *Registrar zapatos:* agregar nuevos productos con su modelo, talla y precio.
2. *Consultar inventario:* visualizar los zapatos almacenados.
3. *Buscar por ID:* localizar un producto utilizando su identificador.
4. *Actualizar precios:* modificar el valor de un zapato registrado.
5. *Eliminar zapatos:* retirar productos de la base de datos.

Estas operaciones conforman un CRUD: Create, Read, Update y Delete.

---

## 3. Estructura del proyecto

text
tienda_zapatos/
│
├── main.py
├── datos.py
├── requirements.txt
├── README.md
├── zapateria.db
│
└── evidencias/
    ├── registro.png
    ├── listado.png
    ├── busqueda.png
    ├── actualizacion.png
    ├── eliminacion.png
    └── persistencia.png


### Explicación de los archivos

| Archivo | Responsabilidad |
|---|---|
| main.py | Archivo principal destinado a ejecutar el programa y presentar las opciones al usuario. |
| datos.py | Contiene el modelo ORM, la conexión y las funciones que trabajan con la base de datos. |
| requirements.txt | Indica la dependencia SQLAlchemy necesaria para el funcionamiento del proyecto. |
| README.md | Presenta la documentación y explicación técnica de la aplicación. |
| zapateria.db | Archivo SQLite donde se conservan los registros. Se genera al inicializar la base de datos. |
| evidencias/ | Carpeta destinada a las capturas de las pruebas realizadas. |

---

## 4. Instalación y ejecución

### Paso 1. Requisitos

Para utilizar la aplicación se necesita:

- Python 3.
- Visual Studio Code o una terminal.
- La biblioteca SQLAlchemy.
- Los archivos del proyecto.

### Paso 2. Instalación de dependencias

Abrir una terminal en la carpeta del proyecto y ejecutar:

bash
python -m pip install -r requirements.txt


### Paso 3. Ejecución

Ejecutar el archivo principal mediante:

bash
python main.py


### Paso 4. Resultado esperado

Al iniciar correctamente, la aplicación debe permitir acceder a las funciones de administración del inventario.

Desde el programa se podrán registrar zapatos, consultar productos, buscar registros individuales, modificar precios y eliminar elementos.

La información registrada se almacena en SQLite para conservarla después de cerrar la aplicación.

---

# 5. Documentación técnica — Preguntas obligatorias

## Pregunta 1. Modelo y tabla

*¿Qué clase de Python representa la tabla de la base de datos? Explica cómo SQLAlchemy identifica el nombre de la tabla y sus columnas.*

### Respuesta

La clase Zapato representa los productos almacenados dentro de la base de datos.

Esta clase hereda de Base, lo que permite que SQLAlchemy la reconozca como un modelo de datos.

La propiedad __tablename__ establece que la tabla se llama zapatos.

Los atributos id, modelo, talla y precio corresponden a las columnas de esa tabla.

### Fragmento de código relacionado

python
class Zapato(Base):
    __tablename__ = "zapatos"

    id: Mapped[int] = mapped_column(primary_key=True)
    modelo: Mapped[str] = mapped_column(String, nullable=False)
    talla: Mapped[int] = mapped_column(Integer, nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)


*Explicación:*

mapped_column() permite establecer las características de cada columna. El campo id funciona como clave primaria y los demás campos almacenan los datos del zapato.

---

## Pregunta 2. Creación de la base de datos

*¿Qué ocurre cuando ejecutas el programa por primera vez? Explica cómo se crea la base de datos zapateria.db y la tabla zapatos.*

### Respuesta

La aplicación utiliza un motor de conexión que apunta al archivo zapateria.db.

Cuando se ejecuta la función inicializar_bd(), SQLAlchemy revisa los modelos declarados y crea las tablas que todavía no existen.

SQLite genera el archivo de base de datos cuando se establece la conexión necesaria para realizar estas operaciones.

### Fragmento de código relacionado

python
engine = create_engine("sqlite:///zapateria.db")

def inicializar_bd():
    Base.metadata.create_all(engine)


*Explicación:*

create_engine() configura la conexión con SQLite y create_all() se encarga de crear la estructura definida en los modelos.

Si la tabla ya existe, no vuelve a crearla ni elimina los registros almacenados.

---

## Pregunta 3. Registro de zapatos

*Cuando seleccionas la opción de registrar un zapato, ¿qué recorrido siguen los datos desde el menú hasta quedar almacenados en SQLite? Identifica las funciones utilizadas.*

### Respuesta

El registro comienza cuando se proporcionan los datos del producto: modelo, talla y precio.

Estos valores deben enviarse a la función crear_zapato(), ubicada en datos.py.

La función construye un objeto de la clase Zapato, abre una sesión y lo incorpora a ella mediante session.add().

Finalmente, session.commit() confirma la operación y guarda la información en SQLite.

### Fragmento de código relacionado

python
def crear_zapato(modelo, talla, precio):
    with Session(engine) as session:
        zapato = Zapato(
            modelo=modelo,
            talla=talla,
            precio=precio
        )
        session.add(zapato)
        session.commit()
        return True


*Explicación:*

El método add() incorpora el nuevo objeto a la sesión, mientras que commit() confirma su almacenamiento.

La función devuelve True cuando finaliza sin errores.

---

## Pregunta 4. Sesiones y transacciones

*¿Para qué se utiliza una sesión de SQLAlchemy? ¿Qué ocurriría si agregas o modificas un objeto, pero no confirmas la transacción con commit()?*

### Respuesta

Una sesión permite mantener la comunicación entre los objetos de Python y la base de datos.

Mediante ella se pueden consultar registros, agregar productos y realizar modificaciones.

En este proyecto se utiliza Session(engine) para administrar esas operaciones.

Si se agrega o modifica un objeto sin ejecutar commit(), los cambios no quedan confirmados de forma permanente. Al cerrar la sesión sin confirmar la transacción, los cambios pendientes normalmente se revierten.

### Fragmento de código relacionado

python
with Session(engine) as session:
    session.add(zapato)
    session.commit()


*Explicación:*

La sesión administra la operación y commit() permite confirmar los cambios realizados.

---

## Pregunta 5. Búsqueda por ID

*¿Cómo funciona la búsqueda de zapatos por ID? Explica qué devuelve tu función cuando encuentra el registro y qué devuelve cuando no existe.*

### Respuesta

La búsqueda se realiza utilizando el identificador único del producto.

La función buscar_zapato() recibe el ID y consulta la tabla mediante session.get().

Cuando encuentra una coincidencia, devuelve el objeto correspondiente al zapato, con sus atributos.

Si el identificador no pertenece a ningún registro, devuelve None.

### Fragmento de código relacionado

python
def buscar_zapato(id_zapato):
    with Session(engine) as session:
        return session.get(Zapato, id_zapato)


*Explicación:*

session.get() permite localizar directamente un registro mediante su clave primaria, evitando escribir manualmente una consulta SQL.

---

## Pregunta 6. Actualización de precios

*¿Cómo se actualiza el precio de un zapato mediante el ORM? Explica cómo se obtiene el objeto, cómo se modifica su atributo y cómo se guarda el cambio.*

### Respuesta

Para modificar un precio, primero se identifica el producto mediante su ID.

La función actualizar_precio() recupera el objeto almacenado utilizando session.get().

Después se reemplaza el contenido del atributo precio por el nuevo valor.

El cambio se confirma mediante session.commit().

Cuando el producto solicitado no existe, la función devuelve False y no realiza modificaciones.

### Fragmento de código relacionado

python
def actualizar_precio(id_zapato, nuevo_precio):
    with Session(engine) as session:
        zapato = session.get(Zapato, id_zapato)

        if zapato is None:
            return False

        zapato.precio = nuevo_precio
        session.commit()
        return True


*Explicación:*

SQLAlchemy identifica el objeto modificado y genera la operación necesaria para actualizar su información en SQLite.

---

## Pregunta 7. Eliminación de registros

*¿Qué ocurre cuando eliminas un zapato? Explica cómo compruebas que el registro ya no existe en la base de datos.*

### Respuesta

Para eliminar un producto, el sistema primero intenta encontrarlo mediante su identificador.

Si existe, la función eliminar_zapato() lo marca para eliminación utilizando session.delete().

Posteriormente se ejecuta commit() para confirmar el cambio.

La eliminación puede comprobarse realizando otra búsqueda con el mismo ID. Si la operación se completó, la consulta devuelve None.

### Fragmento de código relacionado

python
def eliminar_zapato(id_zapato):
    with Session(engine) as session:
        zapato = session.get(Zapato, id_zapato)

        if zapato is None:
            return False

        session.delete(zapato)
        session.commit()
        return True


*Explicación:*

session.delete() prepara la eliminación del objeto y commit() confirma que el registro sea retirado de la tabla.

---

## Pregunta 8. Persistencia de datos

*¿Qué sucede con los zapatos registrados cuando cierras y vuelves a ejecutar el programa? Explica por qué permanecen almacenados.*

### Respuesta

Los registros confirmados permanecen guardados después de finalizar la ejecución porque SQLite utiliza un archivo físico para almacenar la información.

En este proyecto, dicho archivo se llama zapateria.db.

Cuando el programa vuelve a ejecutarse desde el mismo directorio, utiliza nuevamente esa base de datos y puede recuperar los productos anteriores.

La persistencia puede verificarse registrando productos, cerrando el programa, ejecutándolo nuevamente y consultando el inventario.

---

# 6. Pruebas de funcionamiento y evidencias

En este apartado se presentan las operaciones que deben verificarse durante la ejecución del programa.

## Prueba 1. Registrar zapatos

*Acción realizada:* registrar dos productos en el inventario.

*Datos utilizados:* modelo, talla y precio de cada zapato.

*Resultado esperado:* los productos quedan almacenados con identificadores únicos.

### Evidencia

![Registro de zapatos](evidencias/registro.png)

---

## Prueba 2. Listar inventario

*Acción realizada:* consultar los productos registrados.

*Resultado esperado:* se visualizan los zapatos almacenados, incluyendo sus identificadores, modelos, tallas y precios.

### Evidencia

![Listado del inventario](evidencias/listado.png)

---

## Prueba 3. Buscar por ID

*Acción realizada:* consultar un zapato utilizando su identificador.

*Resultado esperado:* el programa recupera la información del producto cuando el ID existe.

### Evidencia

![Busqueda de zapatos](evidencias/busqueda.png)

---

## Prueba 4. Actualizar precio

*Acción realizada:* seleccionar un producto y modificar su precio.

*Resultado esperado:* el nuevo valor queda almacenado y puede comprobarse mediante otra consulta.

### Evidencia

![Actualizacion de precio](evidencias/actualizacion.png)

---

## Prueba 5. Eliminar zapato

*Acción realizada:* eliminar un producto utilizando su ID.

*Resultado esperado:* el producto deja de aparecer en las consultas posteriores.

### Evidencia

![Eliminacion de zapato](evidencias/eliminacion.png)

---

## Prueba 6. Comprobar persistencia

*Acción realizada:* finalizar la ejecución y volver a iniciar el programa.

*Resultado esperado:* los registros que no fueron eliminados continúan disponibles en el inventario.

### Evidencia

![Persistencia de datos](evidencias/persistencia.png)

---

## Pruebas con registros inexistentes

El código contempla situaciones en las que se intenta trabajar con identificadores que no están registrados.

| Operación | Comportamiento definido en el código |
|---|---|
| Buscar ID inexistente | La función devuelve None. |
| Actualizar ID inexistente | La función devuelve False sin modificar registros. |
| Eliminar ID inexistente | La función devuelve False sin eliminar registros. |

Estas condiciones permiten controlar operaciones sobre productos que no se encuentran en la base de datos.

---

# 7. Conclusiones

### 1. ¿Qué aprendiste al implementar las operaciones CRUD utilizando SQLAlchemy?

Durante el desarrollo comprendí cómo utilizar un ORM para administrar información almacenada en una base de datos. Aprendí a representar tablas mediante clases de Python y a realizar operaciones de registro, consulta, modificación y eliminación utilizando sesiones.

### 2. ¿Qué diferencia identificaste entre trabajar con objetos Python y escribir sentencias SQL directamente?

La diferencia principal es la manera de interactuar con los datos. Al utilizar SQLAlchemy puedo trabajar con clases y atributos de Python, mientras que con SQL tradicional tendría que construir las instrucciones de consulta y modificación manualmente.

El ORM facilita la organización del código y permite mantener una relación clara entre los objetos y las tablas.

### 3. ¿Cuál fue la principal dificultad durante el desarrollo y cómo la solucionaste?

Uno de los aspectos que requirió mayor atención fue comprender cómo se relacionan los objetos creados en Python con los registros almacenados en SQLite.

Para abordar este proceso fue necesario revisar el funcionamiento de las sesiones, identificar cuándo utilizar add(), get(), delete() y commit(), y organizar las operaciones dentro de funciones independientes.

---

## 8. Consideraciones finales

El proyecto permite comprender los fundamentos del manejo de bases de datos relacionales mediante SQLAlchemy ORM.

La separación de las funciones de acceso a datos facilita la lectura del código y permite ampliar las funcionalidades del programa en futuras versiones.

Para completar la entrega se deben verificar las ejecuciones reales, incorporar las capturas correspondientes y comprobar que todas las imágenes se visualicen correctamente en GitHub.

---

*Estudiante:* Alayn Fontalvo Castro

*Asignatura:* Desarrollo con Acceso a Datos

*Docente:* Eduardo Pimienta