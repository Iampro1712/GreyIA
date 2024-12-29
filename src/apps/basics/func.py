import mysql.connector
from moduls.utils.utils import load_json

CONFIG_DB = load_json("db")

db_config = { 
    "host" : CONFIG_DB["host"],
    "port" : CONFIG_DB["port"],
    "user" : CONFIG_DB["user"],
    "password" : CONFIG_DB["password"],
    "database" : CONFIG_DB["database"]
}
def get_connection():
    """Crea y retorna una conexión a la base de datos MySQL."""
    return mysql.connector.connect(**db_config)

def user_exists(user_id):
    """Verifica si un ID de usuario ya está en la tabla."""
    try:
        conexion = get_connection()
        cursor = conexion.cursor()

        cursor.execute("SELECT id_tlg FROM Users WHERE id_tlg = %s", (user_id,))
        resultado = cursor.fetchone()

        return resultado is not None
    
    except mysql.connector.Error as error:
        print(f"Error al consultar la base de datos: {error}")
        return False

    finally:
        if conexion:
            conexion.close()

def alter():
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute("ALTER TABLE Users MODIFY id_tlg BIGINT;")
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as e:
        print(e)

# Crear la nueva columna "credits" en la tabla "Users"
def add_credits_column():
    try:
        cnx = get_connection()      
        cursor = cnx.cursor()          
        cursor.execute("ALTER TABLE Users ADD COLUMN credits INT DEFAULT 0;")
        cnx.commit()
        print("Columna agregada correctamente")
    except Exception as e:
        print(f"Error al agregar la columna: {e}")
    finally:
        cnx.close()

def add_credits(user_id, credits):
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute("UPDATE Users SET credits = credits + %s WHERE id_tlg = %s", (credits, user_id))
        cnx.commit()
        cursor.execute("SELECT credits FROM Users WHERE id_tlg = %s", (user_id,))
        credits_tt = cursor.fetchone()
        print("Créditos agregados correctamente")
        print(f"Créditos agregados: {credits}, Creditos totales: {credits_tt}")
    except Exception as e:
        print(f"Error al agregar créditos: {e}")
    finally:
        cnx.close()

def remove_credits(user_id, credits):
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute("UPDATE Users SET credits = credits - %s WHERE id_tlg = %s", (credits, user_id))
        cnx.commit()
        cursor.execute("SELECT credits FROM Users WHERE id_tlg = %s", (user_id,))
        credits_tt = cursor.fetchone()
        print("Créditos eliminados correctamente")
        print(f"Créditos eliminados: {credits}, Creditos totales: {credits_tt}")
    except Exception as e:
        print(f"Error al eliminar créditos: {e}")
    finally:
        cnx.close()

def see_credits(user_id):
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT credits FROM Users WHERE id_tlg = %s", (user_id,))
        credits_tt = cursor.fetchone()
        print(f"Creditos totales: {credits_tt}, del id {user_id}")
    except Exception as e:
        print(f"Error al ver los créditos: {e}")
    finally:
        cnx.close()
    return credits_tt

# Función para crear la tabla si no existe
def create_table():
    cnx = get_connection()
    cursor = cnx.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255),
                        first_name VARCHAR(255),
                        last_name VARCHAR(255),
                        usos_bin INT DEFAULT 0,
                        id_tlg INT UNIQUE
                    )''')
    cnx.commit()
    cursor.close()
    cnx.close()