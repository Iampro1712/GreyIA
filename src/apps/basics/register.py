from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import mysql.connector
import datetime
from moduls.utils.utils import loading_message, load_json
from apps.basics.func import create_table, get_connection, add_credits_column

# Inicializa la base de datos y la tabla
create_table()

@Client.on_message(filters.command("register", prefixes=["/", "."]))
async def register_user(client, message):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Creador", url="https://t.me/MasterBinn3r")],
        ]
    )
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else ""
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name if message.from_user.last_name else ""

    stk = await loading_message(message, sticker_id=4)

    cnx = get_connection()
    cursor = cnx.cursor()

    # Verifica si el usuario ya está registrado
    cursor.execute("SELECT * FROM Users WHERE id_tlg = %s", (user_id,))
    if cursor.fetchone():
        await stk.delete()
        await message.reply("<strong>⚠️ Ya estás registrado ⚠️</strong>")
        cursor.close()
        cnx.close()
        return

    # Inserta el nuevo usuario en la base de datos
    cursor.execute("INSERT INTO Users (username, first_name, last_name, usos_bin, id_tlg) VALUES (%s, %s, %s, %s, %s)", 
                   (username, first_name, last_name, 0, user_id))
    cnx.commit()
    cursor.close()
    cnx.close()

    now = datetime.datetime.now()
    time = now.strftime("%d/%m/%Y, %H:%M")
    
    await stk.delete()
    await message.reply(f"""
¡Te has registrado exitosamente!
<strong> Usuario: @{username}</strong> [<code>{user_id}</code>]
<strong> Nombre </strong>: {first_name} {last_name}
<strong> Tiempo del registro: </strong> <code> {time} </code>
""", reply_markup=keyboard)
    
    await client.send_message(6364510923, f"El usario @{username}, Con el id **ID**: `{user_id}` Se ha registrado")

@Client.on_message(filters.command(["me","info"], prefixes=["/", "."]))
async def info(client, message):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Creador", url="https://t.me/MasterBinn3r")],
        ]
    )
    user_id = message.from_user.id
    stk = await loading_message(message, sticker_id=4)

    cnx = get_connection()
    cursor = cnx.cursor()

    # Verifica si el usuario está registrado
    cursor.execute("SELECT * FROM Users WHERE id_tlg = %s", (user_id,))
    user_info = cursor.fetchone()
    cursor.execute("SELECT credits FROM Users WHERE id_tlg = %s", (user_id,))
    user_credits = cursor.fetchone()
    cursor.close()
    cnx.close()
    
    if not user_info:
        await stk.delete()
        await message.reply("No estás registrado. Usa /register para registrarte.")
        return
    else:
        username, first_name, last_name = user_info[1], user_info[2], user_info[3]
        await stk.delete()
        await message.reply(f""" 
═════════════════
<a href=tg://user?id=>↳</a> Información del usuario 
<a href=tg://user?id=>↳</a> <strong> Usuario </strong>: @{username}
<a href=tg://user?id=>↳</a> <strong> ID </strong>: <code>{user_id}</code>
<a href=tg://user?id=>↳</a> <strong> Nombre </strong>: {first_name} {last_name}
<a href=tg://user?id=>↳</a> <strong> Creditos </strong>: {user_credits[0]}
<a href=tg://user?id=>↳</a> <strong> Bot By </strong>: <strong>@MasterBinn3r</strong>
═════════════════
    """, reply_markup=keyboard)
        
@Client.on_message(filters.command("delete", prefixes=["/", "."]))
async def delete_user(client, message):
    # Obtener el ID del usuario a eliminar

    if message.from_user.id != 6364510923:
        await message.reply("<strong>¡No tienes permiso para realizar esta acción!</strong>")
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id  # ID del usuario al que responde
    else:
        try:
            user_id = int(message.command[1])  # ID proporcionado en el comando
        except (IndexError, ValueError):
            await message.reply("<strong>Por favor, responde a un usuario o proporciona un ID válido.</strong>")
            return
    
    # Conectar a la base de datos
    cnx = get_connection()
    cursor = cnx.cursor()

    # Verificar si el usuario está en la base de datos
    cursor.execute("SELECT username, first_name, last_name FROM Users WHERE id_tlg = %s", (user_id,))
    user_info = cursor.fetchone()

    if not user_info:
        await message.reply(f"<strong>No se encontró el usuario con ID</strong>: <code>{user_id}</code>")
        cursor.close()
        cnx.close()
        return

    # Eliminar al usuario de la base de datos
    cursor.execute("DELETE FROM Users WHERE id_tlg = %s", (user_id,))
    cnx.commit()
    cursor.close()
    cnx.close()

    # Preparar datos para el mensaje de confirmación
    username, first_name, last_name = user_info
    now = datetime.datetime.now()
    time = now.strftime("%d/%m/%Y, %H:%M")

    # Enviar mensaje de confirmación
    await message.reply(f"""
<strong>🎉 Usuario eliminado exitosamente 🎉</strong>
<strong>Usuario</strong>: @{username if username else "Sin username"}
<strong>ID</strong>: <code>{user_id}</code>
<strong>Nombre</strong>: {first_name} {last_name}
<strong>Fecha de eliminación</strong>: <code>{time}</code>
""")
        