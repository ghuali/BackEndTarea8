

import psycopg2
from flask import Flask, jsonify, request
from psycopg2 import connect

app = Flask(__name__)


def ejecutar_sql(sql_text):
    host = "localhost"
    port = "5432"
    dbname = "alexsoft"
    user = "postgres"
    password = "postgres"

    connection = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
    )
    cursor = connection.cursor()

    cursor.execute(sql_text)

    if "INSERT" in sql_text:
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'msg':'insertado'})

    columnas = [desc[0] for desc in cursor.description]

    resultados = cursor.fetchall()
    empleados = [dict(zip(columnas,fila)) for fila in resultados]

    cursor.close()
    connection.close()

    return jsonify(empleados)

@app.route('/Prueba1',methods=['GET'])
def otraCosa():
    resultado = ejecutar_sql(
    'SELECT * FROM public."Empleado" ORDER BY id ASC LIMIT 100')

    return resultado

@app.route('/empleado/empleados',methods=['GET'])
def puestos():
    resultado = ejecutar_sql(
    '''SELECT e.nombre,g.id AS id_puesto, 'Gestor' AS rol FROM "Empleado" e INNER JOIN "Gestor" g ON e.id = g.empleado UNION ALL SELECT e.nombre, p.id AS id_puesto,'Programador' AS rol FROM  "Empleado" e INNER JOIN "Programador" p ON e.id = p.empleado;''')

    return resultado

@app.route('/proyecto/proyectos',methods=['GET'])
def proyectosChill():
    resultado = ejecutar_sql(
    '''SELECT * FROM public."Proyecto" ORDER BY id ASC ''')

    return resultado

@app.route('/proyecto/proyectos_activos',methods=['GET'])
def proyectosActivos():
    resultado = ejecutar_sql(
    '''SELECT * FROM public."Proyecto" where fecha_finalizacion < CURRENT_TIMESTAMP  ''')

    return resultado


@app.route('/proyecto/proyectos_gestor',methods=['GET'])
def proyectosGestor():
    empleado_id = request.args.get('id')
    resultado = ejecutar_sql(f'''Select * from public."Proyecto" p inner join "GestoresProyecto" g on g.proyecto = p.id where g.gestor = {empleado_id} ''')

    return resultado



# login
# crear proyecto
# Asignar gestor a proyecto
# Asignar cliente a proyecto
# Crear tareas a proyecto
# Asignar programador a proyecto
# Asignar programador a tareas
# Obtener programadores
# Obtener proyectos
# Obtener tareas de un proyecto

@app.route('/gestor/login',methods=['POST'])
def login():
    body_request = request.json
    user = body_request["user"]
    passwd = body_request["passwd"]
    is_logged = ejecutar_sql(
        f"SELECT * FROM public.\"Gestor\" WHERE usuario = '{user}' AND passwd = '{passwd}';"
    )
    if len(is_logged.json) == 0:
        return jsonify({"msg":"login error"})
    empleado = ejecutar_sql(
        f"SELECT * FROM public.\"Empleado\" WHERE id = '{is_logged.json[0]["empleado"]}';"
    )
    return jsonify(
        {
            "id_empleado": empleado.json[0]["id"],
            "id_gestor": is_logged.json[0]["id"],
            "nombre": empleado.json[0]["nombre"],
            "email": empleado.json[0]["email"]
        }
    )

@app.route('/proyecto/crear_proyecto', methods=['POST'])
def Newproyectos():
    body_request = request.json
    nombre = body_request["nombre"]
    descripcion = body_request["descripcion"]
    fecha_creacion = body_request["fecha_creacion"]
    fecha_inicio = body_request["fecha_inicio"]
    cliente = body_request["cliente"]

    query = f"""
        INSERT INTO public."Proyecto" (nombre, descripcion, fecha_creacion, fecha_inicio, cliente)
        VALUES (
            '{nombre}',
            '{descripcion}',
            '{fecha_creacion}',
            '{fecha_inicio}',
             {cliente}
        )"""
    return jsonify(ejecutar_sql(query))

@app.route('/proyecto/asignarGestor', methods=['POST'])
def asignarGestorProyecto():
    body_request = request.json
    gestor = body_request["gestor"]
    proyecto = body_request["proyecto"]

    query = f"""
            INSERT INTO public."GestoresProyecto" (gestor, proyecto, fecha_asignacion)
            VALUES (
                {gestor},
                {proyecto},
                NOW()
            )"""

    return jsonify(ejecutar_sql(query))

if __name__ == '__main__':
   app.run(debug=True)