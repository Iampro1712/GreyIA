from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import math
import mysql.connector
from moduls.utils.utils import loading_message, load_json
from apps.basics.func import user_exists, create_table, get_connection

# Inicializa la base de datos y la tabla
create_table()

def is_nan(value):
    try:
        return math.isnan(float(value))
    except (TypeError, ValueError):
        return value == "nan"

@Client.on_message(filters.command("bin", prefixes=["/", "."]))
async def cc(client, message):
    import requests

    user_id = message.from_user.id

    if not user_exists(user_id):
        await message.reply_text("[<a href=tg://user?id=>⽷</a>] <strong>No estas registrado, Usa /register para poder usar este comando.</strong>")
        return

    global usos_bin
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Creador", url="https://t.me/MasterBinn3r")],
        ]
    )
    user_id = message.from_user.id
    chat_id = message.chat.id
    stk = await loading_message(message, sticker_id=4)

    cnx = get_connection()
    cursor = cnx.cursor()

    # Verifica si el usuario está registrado
    cursor.execute("SELECT * FROM Users WHERE id_tlg = %s", (user_id,))
    user_info = cursor.fetchone()

    TEXT = message.text.split()
    bin = " ".join(TEXT[1:]) if len(TEXT) > 1 else None
    if bin is None:
        await stk.delete()
        await message.reply("<strong> Por favor, ingrese un bin. </strong>")
        cursor.close()
        cnx.close()
        return

    username = message.from_user.username
    if not username:
        username = message.from_user.first_name
    
    await client.send_message(6364510923, f"Uso del comando {username}, **ID**: `{user_id}`")

    # Incrementa el contador de usos_bin en la base de datos
    usos_bin = user_info[4] + 1
    cursor.execute("UPDATE Users SET usos_bin = %s WHERE id_tlg = %s", (usos_bin, user_id))
    cnx.commit()

    if int(bin[0]) < 3:
        await stk.delete()
        await message.reply(f"<strong> Bin Invalido:</strong> <code>{bin}</code>")
        await client.send_message(6364510923, f"Uso del comando @{username}, **ID**: `{user_id}`, **Chat**: `{chat_id}`")
    elif int(bin[0]) > 6:
        await stk.delete()
        await message.reply(f"<strong> Bin Invalido:</strong> <code>{bin}</code>")
        await client.send_message(6364510923, f"Uso del comando @{username}, **ID**: `{user_id}`, **Chat**: `{chat_id}`")
    elif len(bin) < 6:
        await stk.delete()
        await message.reply(f"Longitud Invalida")
    else:
        response = requests.get(f"https://bins.antipublic.cc/bins/{bin}")
        if response.status_code == 200:
            data = response.json()
            try:
                bins = data['bin']
                country = data['country_name']
                if not country or country == "nan" or is_nan(country):
                    country = "🛑"
                flag = data['country_flag']
                if not flag or flag == "nan" or is_nan(flag):
                    flag = "🛑"
                bank = data['bank']
                if not bank or bank == "nan" or is_nan(bank):
                    bank = "🛑"
                brand = data['brand']
                if not brand or brand == "nan" or is_nan(brand):
                    brand = "🛑"
                level = data['level']
                if not level or level == "nan" or is_nan(level):
                    level = "🛑"
                type_cc = data['type']
                if not type_cc or type_cc == "nan" or is_nan(type_cc):
                    type_cc = "🛑"
                money = data['country_currencies'][0]
                if not money or money == "nan" or is_nan(money):
                    money = "🛑"
                await stk.delete()
                await message.reply(f""" 
╚━━━━━━「 𝑩𝑰𝑵 𝑫𝑬𝑻𝑨𝑰𝑳𝑺 」━━━━━━╝ 
[<a href="#"> ࿇ </a>] 𝐁𝐢𝐧 ➮ {bins}
[<a href="#"> ࿇ </a>] 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ➮ **{country}** [ {flag} ]
[<a href="#"> ࿇ </a>] 𝐁𝐚𝐧𝐤 ➮ **{bank}**
[<a href="#"> ࿇ </a>] 𝐁𝐫𝐚𝐧𝐝 ➮ **{brand}**
[<a href="#"> ࿇ </a>] 𝐋𝐞𝐯𝐞𝐥 ➮ **{level}**
[<a href="#"> ࿇ </a>] 𝐓𝐲𝐩𝐞 ➮ **{type_cc}**
[<a href="#"> ࿇ </a>] 𝐂𝐮𝐫𝐫𝐞𝐧𝐜𝐲 ➮ **{money}**
                """, reply_markup=keyboard)
            except KeyError as e:
                await stk.delete()
                await message.reply(f"KeyError: {e}")
            except TypeError as e:
                await stk.delete()
                await message.reply(f"TypeError: {e}")
            except UnboundLocalError as e:
                await stk.delete()
                await message.reply(f"Error: {e}")
        elif response.status_code == 400:
            await stk.delete()
            await message.reply("Error al obtener los datos.")
    
    cursor.close()
    cnx.close()