# Importando los modulos
from pyrogram import Client, filters
from moduls.utils.buttons import keymakers
from moduls.utils import utils

# Controlando el mensaje con las siguientes características
@Client.on_message(filters.command(["start", "iniciar", "inicio", "comenzar"], prefixes=["!", "/", "."]) & filters.text)
async def start(client, response, postdata=0):
    # Page initial
    if not postdata:
        var = "This is a large text"
        continuevar = 1
        codeVARstr = utils.saveVAR(var) # Save the key
        codeVARint = utils.saveVAR(continuevar) # Save the key
        buttons = keymakers(["SUPPORT THIS", "PROJECT WITH", "YOUR RATING"], [f"start-{codeVARint}", "ipQ-0", f"start-{codeVARstr}"])
        await response.reply("""\t\t\t\t✅ Grey is on now!. \n\n 👾Puedes usar /grey + prompt para hablar con GREY AI. Tambien puedes usar /help para saber todos los coamndos de Grey.""", reply_markup=buttons)

    elif type(postdata) is str:
        await response.reply(f"Postdata VAR received: {postdata}")

    # Process other pages
    else:
        botones = keymakers(
            [f"{number}" for number in range(postdata-1, postdata+3)],
            [f"start-{number}" for number in range(postdata-1, postdata+3)],
        )
        await response.reply(f"Postdata INT received: {postdata}", reply_markup=botones)