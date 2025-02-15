from pyrogram import Client, filters
from moduls.utils.utils import loading_message
from apps.basics.func import user_exists, delete_conversation

prefixes = ["/", ".", "!", "#"]

@Client.on_message(filters.command("del_contx", prefixes=prefixes))
async def del_contx(client, message):
    chat_type = message.chat.type
    stk = await loading_message(message, sticker_id=4)
    if not user_exists(message.from_user.id):
        await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] No estas registrado, Usa /register para poder usar este comando.</strong>")
        await stk.delete()
        return
    if chat_type == "private":
        p = delete_conversation(message.from_user.id)
    elif chat_type == "supergroup" or chat_type == "group":
        p = delete_conversation(message.chat.id)
    await stk.delete()
    await message.reply_text(p)
    await client.send_message(6364510923, "<strong>[<a href=tg://user?id=>⽷</a>] Se ha eliminado el contexto de la conversación de un usuario.</strong>")
    
