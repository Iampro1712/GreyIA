from pyrogram import Client, filters
from moduls.utils.utils import loading_message
from apps.basics.func import user_exists, delete_conversation_ky
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import os

prefixes = ["/", ".", "!", "#"]

@Client.on_message(filters.command("menu", prefixes=prefixes))
async def menu(client, message):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👨‍💻 Comandos", callback_data="commands"),
                InlineKeyboardButton("🗑️ Borrar Conversacion", callback_data="delete")
            ]
        ]
    )
    await message.reply_text("Menú principal:", reply_markup=keyboard)

@Client.on_callback_query()
async def handle_callback_query(client, callback_query: CallbackQuery):
    data = callback_query.data

    if data == "commands":
        # Mostrar los comandos disponibles con botón de regresar
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("⬅️ Regresar", callback_data="menu")]
            ]
        )
        await callback_query.answer("Comandos disponibles:")
        await callback_query.edit_message_text(
            "Comandos disponibles:\n\n"
            "• /menu - Muestra el menú principal\n"
            "• /me ó /info - Muestra tu informacion almacenada en el bot.\n"
            "• /del_contx - Borra la conversación actual.\n"
            "• /bin <bin> -  Buscar info de bins.\n"
            "• /grey <peticion> ó <foto con la peticion> - Para hablar con la GreyIA.\n"
            "• /help - Muestra este menú de ayuda.\n"
            "\n<i>Selecciona una opción del menú para más detalles.</i>",
            reply_markup=keyboard,
        )

    elif data == "delete":
        stk = await loading_message(callback_query.message, sticker_id=4)

        try:
            chat_id = callback_query.message.chat.id

            if user_exists(chat_id):
                result = delete_conversation_ky(chat_id)
                await callback_query.answer(result, show_alert=True)
                await Client.send_message(6364510923, f"<strong>[<a href=tg://user?id=>⽷</a>] Se ha eliminado el contexto de la conversación de un usuario con ID {chat_id}.</strong>")
            else:
                await callback_query.answer("Usuario no encontrado en la base de datos.", show_alert=True)
        finally:
            await stk.delete()

    elif data == "menu":
        # Volver al menú principal
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👨‍💻 Comandos", callback_data="commands"),
                    InlineKeyboardButton("🗑️ Borrar Conversacion", callback_data="delete")
                ]
            ]
        )
        await callback_query.answer("Regresando al menú principal.")
        await callback_query.edit_message_text("Menú principal:", reply_markup=keyboard)
