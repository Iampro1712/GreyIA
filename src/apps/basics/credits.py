from pyrogram import Client, filters
from moduls.utils.utils import loading_message
from apps.basics.func import user_exists, add_credits, remove_credits

prefixes = ["/", ".", "!", "#"]

@Client.on_message(filters.command("addcr", prefixes=prefixes))
async def addcr(client, message):
    user_id = message.from_user.id
    stk = await loading_message(message, sticker_id=4)
    if not user_exists(user_id):
        await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] No estas registrado, Usa /register para poder usar este comando.</strong>")
        await stk.delete()
        return

    if user_id != 6364510923:
        await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] No tienes permisos para usar este comando.</strong>")
        await stk.delete()
        return
    
    msg_parts = message.text.split()

    if len(msg_parts) < 3:
        await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] Por favor, ingrese la cantidad de creditos a agregar y el id de destino.</strong>")
        await stk.delete()
        return
    if len(msg_parts) > 3:
        await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] Argumentos Invalidos.</strong>")
        await stk.delete()
        return
    if not msg_parts[1].isdigit():
        await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] La cantidad de creditos debe ser un número entero.</strong>")
        await stk.delete()
        return
    if not msg_parts[2].isdigit():
        await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] El ID de destino debe ser un número entero.</strong>")
        await stk.delete()
        return

    print(f"Adding {msg_parts[2]} credits to {msg_parts[1]}")
    add_credits(int(msg_parts[1]), int(msg_parts[2]))
    await stk.delete()
    await message.reply_text(f"<strong>[<a href=tg://user?id=>⽷</a>] Creditos agregados correctamente.</strong>")
    

@Client.on_message(filters.command("rmcr", prefixes=prefixes))    
async def rmcr(client, message):
    user_id = message.from_user.id
    stk = await loading_message(message, sticker_id=4)
    if not user_exists(user_id):
        await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] No estas registrado, Usa /register para poder usar este comando.</strong>")
        await stk.delete()
        return

    if user_id != 6364510923:
        await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] No tienes permisos para usar este comando.</strong>")
        await stk.delete()
        return
    
    msg_parts = message.text.split()

    if len(msg_parts) < 3:
        await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] Por favor, ingrese la cantidad de creditos a eliminar y el id de destino.</strong>")
        await stk.delete()
        return
    if len(msg_parts) > 3:
        await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] Argumentos Invalidos.</strong>")
        await stk.delete()
        return
    if not msg_parts[1].isdigit():
        await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] La cantidad de creditos debe ser un número entero.</strong>")
        await stk.delete()
        return
    if not msg_parts[2].isdigit():
        await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] El ID de destino debe ser un número entero.</strong>")
        await stk.delete()
        return

    print(f"Removing {msg_parts[2]} credits to {msg_parts[1]}")
    remove_credits(int(msg_parts[1]), int(msg_parts[2]))
    await stk.delete()
    await message.reply_text(f"<strong>[<a href=tg://user?id=>⽷</a>] Creditos eliminados correctamente.</strong>")
    