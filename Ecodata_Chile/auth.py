import bcrypt
import sqlite3

def crear_usuario(nombre_usuario, contrasena):
    hashed = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())
    try:
        with sqlite3.connect("ecodata.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (?, ?)", (nombre_usuario, hashed))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def verificar_login(nombre_usuario, contrasena):
    with sqlite3.connect("ecodata.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT contrasena FROM usuarios WHERE nombre_usuario = ?", (nombre_usuario,))
        resultado = cursor.fetchone()
        if resultado:
            return bcrypt.checkpw(contrasena.encode(), resultado[0])
    return False