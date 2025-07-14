from auth import crear_usuario, verificar_login
from api_client import consultar_indicador
from database import crear_tablas, obtener_usuario_id, guardar_consulta, listar_consultas_por_usuario 
from datetime import datetime

def menu_principal():
    while True:
        print("\n--- EcoData Chile ---")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            while True:
                usuario = input("Nombre de usuario: ")
                clave = input("Contraseña: ")
                if crear_usuario(usuario, clave):
                    print("Usuario registrado con éxito.")
                    break
                else:
                    print("Usuario ya existente, intente con otro nombre.\n")
        elif opcion == "2":
            usuario = input("Nombre de usuario: ")
            clave = input("Contraseña: ")
            if verificar_login(usuario, clave):
                print(f"Bienvenido, {usuario}")
                menu_usuario(usuario)
            else:
                print("Credenciales incorrectas.")
        elif opcion == "3":
            break

def menu_usuario(nombre_usuario):
    usuario_id = obtener_usuario_id(nombre_usuario)

    while True:
        print("\n--- Menú Usuario ---")
        print("1. Consultar dólar actual")
        print("2. Consultar UF histórica")
        print("3. Ver historial de consultas")
        print("4. Cerrar sesión")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            datos = consultar_indicador("dolar")
            if datos:
                valor = datos["serie"][0]["valor"]
                fecha = datos["serie"][0]["fecha"][:10]
                print(f"Valor actual del dólar: ${valor} ({fecha})")
                guardar_consulta(usuario_id, "dólar", valor, fecha)

        elif opcion == "2":
            datos = consultar_indicador("uf")
            if datos:
                print("\nÚltimos valores de la UF:")
                for item in datos["serie"][:5]:
                    fecha = item['fecha'][:10]
                    valor = item['valor']
                    print(f"{fecha}: ${valor}")
                # Guardamos solo la última como ejemplo
                ultima = datos["serie"][0]
                guardar_consulta(usuario_id, "UF", ultima["valor"], ultima["fecha"][:10])

        elif opcion == "3":
            consultas = listar_consultas_por_usuario(usuario_id)
            if consultas:
                print("\nHistorial de Consultas:")
                for tipo, valor, fecha in consultas:
                    print(f"{fecha} - {tipo}: ${valor}")
            else:
                print("No hay consultas registradas.")

        elif opcion == "4":
            break

if __name__ == "__main__":
    crear_tablas()
    menu_principal()