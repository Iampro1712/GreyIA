from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from moduls.utils.utils import loading_message
from apps.basics.func import user_exists

prefixes = ["/", ".", "!", "#"]

@Client.on_message(filters.command("buy", prefixes=prefixes))
async def buycr(client, message):
    keyboard = InlineKeyboardMarkup(
        InlineKeyboardButton("📲 Contactar para comprar", url="https://t.me/MasterBinn3r")
    )

    user_id = message.from_user.id
    stk = await loading_message(message, sticker_id=4)
    if not user_exists(user_id):
        await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] No estas registrado, Usa /register para poder usar este comando.</strong>")
        await stk.delete()
        return
    
    await stk.delete()
    await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] Para comprar creditos, Contactar al dm @MasterBinn3r</strong>", reply_markup=keyboard)