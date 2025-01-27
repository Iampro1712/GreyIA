from pyrogram import Client, filters
import mysql.connector
from moduls.utils.utils import load_json
from pyrogram.errors import *
#from data_db import host, port, user, password, database

CONFIG_DB = load_json("db")

def connect_db():
    return mysql.connector.connect(
    host=CONFIG_DB["host"],
    port=CONFIG_DB["port"],
    user=CONFIG_DB["user"],
    password=CONFIG_DB["password"],
    database=CONFIG_DB["database"]
    )

@Client.on_message(filters.command("send", prefixes=["/", "."]))
async def send_message_to_all(client, message):
    if message.from_user.id != 6364510923:
        await message.reply("No tienes permiso para enviar mensajes.")
        return

    text = message.text.split(maxsplit=1)[1] if len(message.command) > 1 else "¡Hola! Este es un mensaje de prueba."

    cnx = connect_db()
    cursor = cnx.cursor()

    cursor.execute("SELECT id_tlg FROM Users")
    users = cursor.fetchall()

    for user in users:
        user_id = user[0]
        print(f"Sending message to {user_id}")
        try:
            await client.send_message(6364510923, f"Enviando mensaje a {user_id}")
            await client.send_message(user_id, text)
        except PeerIdInvalid as e:
            await client.send_message(6364510923, f"Usuario borró conversacion: {user_id}")
            print(f"Usuario inválido o borró conversacion: {user_id}")
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")

    cursor.close()
    cnx.close()