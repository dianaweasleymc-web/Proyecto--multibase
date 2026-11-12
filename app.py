from flask import Flask, jsonify, request
import psycopg
from pymongo import MongoClient
import redis

app = Flask(__name__)

# PostgreSQL
def get_postgres_connection():
    return psycopg.connect(
        host="127.0.0.1",
        dbname="xxxxxxxxxx",
        user="xxxxxxx",
        password="xxxxxxxxxx",
        port=5432
    )

# MongoDB
mongoClient = MongoClient("mongodb://localhost:27017")
mongo_db = mongoClient["Libreria_db"]

# Redis
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# GET en los libros 
@app.route('/Coleccion-de-Libros-La-Bibloteca:)', methods=['GET'])
def get_Coleccion_de_Libros_La_Bibloteca():
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute(""" SELECT id_Libro, nombre, autor, editorial FROM Libros WHERE activo = TRUE; """)
        libros_postgres = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error detallado en Postgres: {e}")
        return jsonify({"error": str(e)}), 500

    resultado_final = []

    for libro in libros_postgres:

        id_libro_pg = libro[0]
        nombre = libro[1]
        autor = libro[2]
        editorial = libro[3]

        detalle_mongo = mongo_db.Libros.find_one(
            {"id_libro": id_libro_pg}
        )

        if detalle_mongo and "_id" in detalle_mongo:
            del detalle_mongo["_id"]

        resultado_final.append({
            "id_libro": id_libro_pg,
            "nombre": nombre,
            "autor": autor,
            "editorial": editorial,
            "detalles_mongo": detalle_mongo if detalle_mongo else {}
        })

    return jsonify(resultado_final), 200

#GET para los prestammos
@app.route('/Prestamos', methods=['GET'])
def get_prestamos():
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Prestamo WHERE activo = TRUE; """)
        prestamos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(prestamos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#GET para los Estudinates -> Alumnos
@app.route('/Alumnos', methods=['GET'])
def get_alumos():
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Estudiantes WHERE activo = TRUE; """)
        alumnos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(alumnos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#GET  para los generos de los libros 
@app.route('/Genero', methods=['GET'])
def get_generos():
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Genero; """)
        genero = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(genero)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#GET para Editoriales 
@app.route('/Editoriales', methods=['GET'])
def get_editoriales():
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Editoriales WHERE activo = TRUE; """)
        editoriales = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(editoriales)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#GET para Autores
@app.route('/Autores', methods=['GET'])
def get_autores():
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM Autores WHERE activo = TRUE; """)
        autores = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(autores)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#GET de cada una de las tablas 


# POST --Libros 
@app.route('/Coleccion-de-Libros-La-Bibloteca:)', methods=['POST'])
def create_Libro():
    data = request.json
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO Libros (nombre, autor, editorial, id_Genero, activo) VALUES (%s, %s, %s, %s,TRUE) RETURNING id_Libro; """, (
                data['nombre'],
                data['autor'],
                data['editorial'],
                data['id_Genero']
            )
        )

        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        mongo_db.Libros.insert_one({
            "id_libro": nuevo_id,
            "nombre": data['nombre'],
            "autor": data['autor']
        })
        redis_client.set(
            f"Libro:estado:{nuevo_id}",
            "disponible"
        )
        return jsonify({
            "mensaje": "Libro creado correctamente",
            "id_Libro": nuevo_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#POST para los alumnos o Estudiantes
@app.route('/Alumnos', methods=['POST'])
def create_Alumno():
    data = request.json
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO Estudiantes(numeroControl, nombre, apellidoPaterno, apellidoMaterno, carrera, activo) VALUES (%s, %s, %s, %s, %s, TRUE); """, 
                       (
                          data['numeroControl'],
                          data['nombre'],
                          data['apellidoPaterno'],
                          data['apellidoMaterno'],
                          data['carrera'] 
                       )
                    )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Se registro el alumno"}), 201
    except Exception as e:
        return jsonify({"error": str(e)})

#POST para  los prestamos
@app.route('/Prestamos', methods=['POST'])
def create_Prestamo():
    data = request.json
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO Prestamo (id_Alumno, id_Libro, fechaPrestamo, fechaEntrega, activo) VALUES (%s, %s, %s, %s, TRUE); """,
                       (
                           data['id_Alumno'],
                           data['id_Libro'],
                           data['fechaPrestamo'],
                           data['fechaEntrega']
                       )
                    )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Se registro el prestamo"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#POST para los autores
@app.route('/Autores', methods=['POST'])
def create_autor():
    data = request.json
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO Autores (nombre, nacionalidad, activo) VALUES (%s, %s, TRUE); """, 
                       (
                          data['nombre'],
                          data['nacionalidad']       
                       )
                    )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Se registro el autor"}),201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#POST para genero
@app.route('/Genero', methods=['POST'])
def create_genero():
    data = request.json
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO Genero (tipoGenero) VALUES (%s); """, (data['tipoGenero'],))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Se registro el nuevo genero"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#POST para 
@app.route('/Editoriales', methods=['POST'])
def create_editoriales():
    data = request.json
    try:
        conn= get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO Editoriales (nombre, pais, activo) VALUES (%s,%s, TRUE); """, 
                       (
                         data['nombre'],
                         data['pais']       
                       )
                    )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Se registro la editorial"}), 201
    except  Exception as e:
        return jsonify({"error": str(e)}), 500

# PATCH
@app.route('/Coleccion-de-Libros-La-Bibloteca:/<int:id_libro>', methods=['PATCH'])
def update_Libro(id_libro):
    data = request.json
    nueva_editorial = data.get('editorial')
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute(""" UPDATE Libros SET editorial = %s WHERE id_Libro = %s; """, (nueva_editorial, id_libro))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Libro actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#PATCH para prestamo 
@app.route('/Prestamos:/<int:id_Prestamo>', methods=['PATCH'])
def update_Prestamo(id_Prestamo):
    data = request.json
    nueva_Fecha = data.get('fechaEntrega')
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("""UPDATE Prestamo SET fechaEntrega = %s WHERE id_Prestamo = %s; """, (nueva_Fecha, id_Prestamo))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "La fecha se actualizo correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#PATCH para el nombre de las editoriales  
@app.route('/Editoriales:/<int:id_Editorial>', methods=['PATCH'])
def update_editoriales(id_Editorial):
    data = request.json
    nuevo_nombre = data.get('nombre')
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("""UPDATE Editoriales SET nombre = %s WHERE  id_Editorial = %s; """, (nuevo_nombre, id_Editorial))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Se cambio el nombre de la editorial"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#PATCH para autores
@app.route('/Autores:/<int:id_Autor>', methods=['PATCH'])
def update_autor( id_Autor):
    data = request.json
    nombre_nuevo = data.get('nombre')
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("""UPDATE Autores SET nombre = %s WHERE id_Autor = %s; """, (nombre_nuevo, id_Autor))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Se cambio el nombre del autor corectamente"}), 200
    except Exception as e:
            return jsonify({"error": str(e)}), 500

#PATCH para  Estudiantes
@app.route('/Alumnos/<int:id_Alumno>', methods=['PATCH'])
def update_Alumno(id_Alumno):
    data = request.json
    nueva_carrera = data.get('carrera')
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE Estudiantes SET carrera = %s WHERE id_Alumno = %s;""", (nueva_carrera, id_Alumno)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Se cambio la carrera del alumno"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE
@app.route('/Coleccion-de-Libros-La-Bibloteca:/<int:id_Libro>', methods=['DELETE'])
def delete_Libro(id_Libro):
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute(""" UPDATE Libros SET activo = FALSE WHERE id_Libro = %s; """, (id_Libro,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": f"Borrado lógico aplicado al libro {id_Libro}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#DELETE de editores
@app.route('/Editoriales/<int:id_Editorial>', methods=['DELETE'])
def delete_editorial(id_Editorial):
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute(""" UPDATE Editoriales SET activo = FALSE WHERE id_Editorial = %s; """, (id_Editorial,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Se borro la editorial"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Delete de autores
@app.route('/Autores/<int:id_Autor>', methods=['DELETE'])
def delete_autor(id_Autor):
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute(""" UPDATE Autores SET activo = FALSE WHERE id_Autor = %s; """, (id_Autor,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Se borro el autor"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#DELETE para almunos 
@app.route('/Alumnos/<int:id_Alumno>', methods=['DELETE'])
def delete_alumno(id_Alumno):
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute(""" UPDATE Estudiantes SET activo = FALSE WHERE id_Alumno = %s; """, (id_Alumno,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Se borro el alumno"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#Borramos-- boton logico 
@app.route('/Prestamos/<int:id_Prestamo>', methods=['DELETE'])
def delete_prestamo(id_Prestamo):
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute(""" UPDATE Prestamo SET activo = FALSE WHERE id_Prestamo = %s; """, (id_Prestamo,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Se borro el prestamo"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 


if __name__ == '__main__':
    app.run(debug=True, port=3000)