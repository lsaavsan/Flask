from flask import Flask, render_template, request, redirect, url_for
import os
import pymysql
from dotenv import load_dotenv

# Cargar las variables de entorno desde un archivo .env (si se usa)
# Esto permite mantener información sensible (como credenciales) fuera del código fuente.
load_dotenv()

# Configuración de la conexión a la base de datos utilizando variables de entorno
database = pymysql.connect(
    host=os.getenv('DB_HOST'),  # Dirección del servidor de la base de datos (obtenida de las variables de entorno)
    user=os.getenv('DB_USER'),  # Usuario autorizado para acceder a la base de datos
    password=os.getenv('DB_PASSWORD'),  # Contraseña del usuario
    database=os.getenv('DB_NAME'),  # Nombre de la base de datos
    cursorclass=pymysql.cursors.DictCursor  # Configuración para obtener resultados como diccionarios
)

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Ruta principal que muestra la lista de usuarios
@app.route("/")
def home():
    # Crear un cursor para interactuar con la base de datos
    cursor = database.cursor()
    
    # Ejecutar una consulta SQL para obtener todos los registros de la tabla 'clientes'
    cursor.execute("SELECT * FROM clientes")
    
    # Recuperar todos los resultados de la consulta como una lista de diccionarios
    users = cursor.fetchall()
    print(users)
    # Cerrar el cursor para liberar recursos
    cursor.close()
    
    # Renderizar la plantilla 'index.html' y pasar los datos de usuarios a la plantilla
    return render_template("index.html", data=users)

# Ruta para agregar un nuevo usuario
@app.route("/user", methods=['POST'])
def add_user():
    # Obtener los valores enviados desde el formulario HTML
    Username = request.form["Username"]  # Nombre de usuario
    Nombre = request.form["Nombre"]      # Nombre del cliente
    Contrasena = request.form["Contrasena"]  # Contraseña del usuario
    
    # Verificar que los campos requeridos no estén vacíos
    if Username and Nombre and Contrasena:
        # Crear un cursor para interactuar con la base de datos
        cursor = database.cursor()
        
        # Ejecutar una consulta SQL para insertar un nuevo usuario
        cursor.execute(
            'INSERT INTO clientes (Username, Nombre, Contrasena) VALUES (%s, %s, %s)', 
            (Username, Nombre, Contrasena)
        )
        
        # Confirmar los cambios en la base de datos
        database.commit()
        
        # Cerrar el cursor para liberar recursos
        cursor.close()
    
    # Redirigir al usuario de nuevo a la página principal
    return redirect(url_for('home'))

# Ruta para eliminar un usuario
@app.route("/delete/<int:id>")
def delete_user(id):
    # Crear un cursor para interactuar con la base de datos
    cursor = database.cursor()
    
    # Ejecutar una consulta SQL para eliminar un usuario por su ID
    cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
    
    # Confirmar los cambios en la base de datos
    database.commit()
    
    # Cerrar el cursor para liberar recursos
    cursor.close()
    
    # Redirigir al usuario de nuevo a la página principal
    return redirect(url_for('home'))

# Ruta para mostrar detalles de un usuario específico
@app.route("/user/<int:id>")
def view_user(id):
    # Crear un cursor para interactuar con la base de datos
    cursor = database.cursor()
    
    # Ejecutar una consulta SQL para obtener los datos de un usuario por su ID
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    
    # Recuperar el resultado de la consulta (un único registro)
    user = cursor.fetchone()
    
    # Cerrar el cursor para liberar recursos
    cursor.close()
    
    # Verificar si el usuario existe
    if user:
        # Renderizar la plantilla 'user_detail.html' con los datos del usuario
        return render_template("user_detail.html", user=user)
    else:
        # Si no se encuentra el usuario, devolver un mensaje de error con el código HTTP 404
        return "Usuario no encontrado", 404

# Ruta para editar los datos de un usuario
@app.route("/edit/<int:id>", methods=['POST'])
def edit_user(id):
    # Obtener los valores enviados desde el formulario HTML
    Username = request.form["Username"]  # Nuevo nombre de usuario
    Nombre = request.form["Nombre"]      # Nuevo nombre del cliente
    Contrasena = request.form["Contrasena"]  # Nueva contraseña
    
    # Verificar que los campos requeridos no estén vacíos
    if Username and Nombre and Contrasena:
        # Crear un cursor para interactuar con la base de datos
        cursor = database.cursor()
        
        # Ejecutar una consulta SQL para actualizar los datos del usuario
        cursor.execute(
            'UPDATE clientes SET Username = %s, Nombre = %s, Contrasena = %s WHERE id = %s', 
            (Username, Nombre, Contrasena, id)
        )
        
        # Confirmar los cambios en la base de datos
        database.commit()
        
        # Cerrar el cursor para liberar recursos
        cursor.close()
    
    # Redirigir al usuario de nuevo a la página principal
    return redirect(url_for('home'))

# Punto de entrada de la aplicación
if __name__ == '__main__':
    # Ejecutar la aplicación en modo de depuración para desarrollo
    # Escucha en el puerto 5000 por defecto
    app.run(debug=True, port=5000)
