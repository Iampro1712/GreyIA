from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from moduls.utils.utils import loading_message
from apps.basics.func import user_exists

@Client.on_message(filters.command(["ip", "ipQ", "IP"], prefixes=["/", "."]))
async def ip(client, message):
    user_id = message.from_user.id

    if not user_exists(user_id):
        await message.reply_text("[<a href=tg://user?id=>⽷</a>] <strong>No estas registrado, Usa /register para poder usar este comando.</strong>")
        return

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Creador", url="https://t.me/MasterBinn3r")],
        ]
    )

    TEXT = message.text.split()
    ip_query = " ".join(TEXT[1:]) if len(TEXT) > 1 else None

    if not ip_query:
        await message.reply("No introduciste ningun valor", reply_markup=keyboard)
        return

    try:
        stk = await loading_message(message, sticker_id=4)
        response = requests.get(f"http://ip-api.com/json/{ip_query}")
        if response.status_code == 200:
            datos = response.json()
            query = datos['query']
            ct = datos['country']
            ccd = datos['countryCode']
            rg = datos['regionName']
            cd = datos['city']
            cp = datos['zip']
            lati = datos['lat']
            long = datos['lon']
            orgz = datos['org']
            if cp == "":
                cp = 0
            if ct == "":
                ct = "Paìs no disponible"
            await stk.delete()
            await message.reply(f""" 
└ Informacion del dominio o IP ┐
     ☞ Query: {query}
     ☞ Pais: {ct}
     ☞ CodigoPais: {ccd}
     ☞ Ciudad: {cd}
     ☞ Region: {rg}
     ☞ Codigo Postal: {cp}
     ☞ Latitud Aprox: {lati}
     ☞ Longitud Aprox: {long}
     ☞ Organizacion: {orgz}""", reply_markup=keyboard)
    except Exception as e:
        await message.reply(f"Error al realizar la consulta: {str(e)}")
        print(e)
    
