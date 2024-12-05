from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from apps.basics.func import user_exists

@Client.on_message(filters.command(["ayuda", "help"], prefixes=["/", "."]))
async def help(Client, message):

    user_id = message.from_user.id

    if not user_exists(user_id):
        await message.reply_text("[<a href=tg://user?id=>⽷</a>] <strong>No estas registrado, Usa /register para poder usar este comando.</strong>")
        return

    keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Creador", url="https://t.me/MasterBinn3r")],
                #[InlineKeyboardButton("Option 2", callback_data="2")],
                #[InlineKeyboardButton("Option 3", callback_data="3")],
            ]
        )

    await message.reply("""
༻𝐂𝐨𝐦𝐚𝐧𝐝𝐨𝐬 𝐃𝐢𝐬𝐩𝐨𝐧𝐢𝐛𝐥𝐞𝐬༺

⇛𝙋𝙧𝙚𝙛𝙞𝙭 ⤏ / 
               ⤏ .

⤷help - Ayuda al usuario a conocer los comandos del bot.
⤷bin - Visualizacion de la informacio del bin proporcionado.
⤷grey - Comando para hablar con la IA.                                                                         
""", reply_markup=keyboard)
