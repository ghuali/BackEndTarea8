

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

@app.route('/Prueba',methods=['GET'])
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


@app.route('/login',methods=['POST'])
def login():
    Body = { "user": "Angel", "passwd": "1234" }
    body_request = request.json
    user = body_request["user"]
    passwd = body_request["passwd"]
    resultado = ejecutar_sql(f'''Select * from public."Proyecto" p inner join "GestoresProyecto" g on g.proyecto = p.id where g.gestor = {empleado_id} ''')

    return resultado


@app.route('/proyectoss',methods=['POST'])
def crear_proyecto():
    body_request = request.json
    nombre = body_request["nombre"]
    descripcion = body_request["descripcion"]
    fecha_inicio = body_request["fecha_inicio"]
    cliente = body_request["cliente"]

    sql = f"""INSERT INTO public."Proyecto" (nombre, descripcion, fecha_creacion, fecha_inicio, fecha_finalizacion, cliente)
              VALUES (
                    '{nombre}',
                    '{descripcion}',
                    NOW(),
                    '{fecha_inicio}',
                    null,
                    {cliente});
"""
    return ejecutar_sql(sql)

if __name__ == '__main__':
   app.run(debug=True)