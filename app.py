from flask import Flask, render_template, request, redirect, url_for
import os
import pymysql
from dotenv import load_dotenv

# Cargar las variables de entorno desde un archivo .env (si se usa)
load_dotenv()

# Configuración de la conexión a la base de datos utilizando variables de entorno
database = pymysql.connect(
    host=os.getenv('DB_HOST'),  # Host de la base de datos desde las variables de entorno
    user=os.getenv('DB_USER'),  # Usuario de la base de datos
    password=os.getenv('DB_PASSWORD'),  # Contraseña del usuario
    database=os.getenv('DB_NAME'),  # Nombre de la base de datos
    cursorclass=pymysql.cursors.DictCursor  # Devuelve los resultados como diccionarios
)

app = Flask(__name__)

# Ruta principal que muestra los usuarios
@app.route("/")
def home():
    cursor = database.cursor()  # Cursor que devuelve los resultados como diccionarios
    cursor.execute("SELECT * FROM clientes")
    users = cursor.fetchall()  # Obtiene todos los usuarios
    cursor.close()
    return render_template("index.html", data=users)

# Ruta para agregar un usuario
@app.route("/user", methods=['POST'])
def add_user():
    Username = request.form["Username"]
    Nombre = request.form["Nombre"]
    Contrasena = request.form["Contrasena"]
    
    if Username and Nombre and Contrasena:
        cursor = database.cursor()
        cursor.execute(
            'INSERT INTO clientes (Username, Nombre, Contrasena) VALUES (%s, %s, %s)', 
            (Username, Nombre, Contrasena)
        )
        database.commit()
        cursor.close()
    
    return redirect(url_for('home'))

# Ruta para eliminar un usuario
@app.route("/delete/<int:id>")
def delete_user(id):
    cursor = database.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
    database.commit()
    cursor.close()
    return redirect(url_for('home'))

# Ruta para mostrar detalles de un usuario
@app.route("/user/<int:id>")
def view_user(id):
    cursor = database.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    user = cursor.fetchone()  # Obtiene un único usuario
    cursor.close()
    if user:
        return render_template("user_detail.html", user=user)
    else:
        return "Usuario no encontrado", 404



# Ruta para editar un usuario
@app.route("/edit/<int:id>", methods=['POST'])
def edit_user(id):
    Username = request.form["Username"]
    Nombre = request.form["Nombre"]
    Contrasena = request.form["Contrasena"]
    
    if Username and Nombre and Contrasena:
        cursor = database.cursor()
        cursor.execute(
            'UPDATE clientes SET Username = %s, Nombre = %s, Contrasena = %s WHERE id = %s', 
            (Username, Nombre, Contrasena, id)
        )
        database.commit()
        cursor.close()
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    