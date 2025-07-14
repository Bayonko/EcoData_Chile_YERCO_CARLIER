import sqlite3

def crear_tablas():
    with sqlite3.connect("ecodata.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT UNIQUE,
                contrasena TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                tipo TEXT,
                valor REAL,
                fecha TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        conn.commit()

def obtener_usuario_id(nombre_usuario):
    with sqlite3.connect("ecodata.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = ?", (nombre_usuario,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None

def guardar_consulta(usuario_id, tipo, valor, fecha):
    with sqlite3.connect("ecodata.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO consultas (usuario_id, tipo, valor, fecha)
            VALUES (?, ?, ?, ?)
        ''', (usuario_id, tipo, valor, fecha))
        conn.commit()

def listar_consultas_por_usuario(usuario_id):
    with sqlite3.connect("ecodata.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT tipo, valor, fecha
            FROM consultas
            WHERE usuario_id = ?
            ORDER BY fecha DESC
        ''', (usuario_id,))
        return cursor.fetchall()
