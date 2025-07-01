from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import google.generativeai as genai
import PIL.Image as pil
import json, mysql.connector
from moduls.utils.utils import load_json, loading_message
from apps.basics.func import user_exists, remove_credits, see_credits

CONFIG = load_json("llmConfig")
CONFIG_DB = load_json("db")

genai.configure(api_key=CONFIG["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

async def process_image_and_generate_content(image_path, prompt):
    try:
        if not prompt:
            prompt = "Describe eficientemente el contenido visual con un vocabulario muy fino en español."

        # Contexto explícito en español
        initial_context = (
            "Eres un asistente avanzado de inteligencia artificial. Siempre debes responder en español, "
            "con descripciones detalladas, precisas y claras. Si se te proporciona una imagen, analiza su contenido visual "
            "y responde únicamente en español, Si no ves muy bien la imagen, puedes pedir que mande una con mejor calidad."
        )

        # Combinar contexto inicial con el prompt del usuario
        full_prompt = f"{initial_context}\nUsuario: {prompt}"
        security = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        }
        ]

        img = pil.open(image_path)
        response = model.generate_content([full_prompt, img], safety_settings=security,stream=False)
        return response.text
    except ValueError as e:
        return f"Error: {e}"
    
@Client.on_message(filters.command(CONFIG["COMMAND_VS"], prefixes=CONFIG["prefixes"]) & filters.photo)
async def start1(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    usr = message.from_user.username # Obtener el estado actual del chat
    OWNER = 6364510923
    
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Creador", url="https://t.me/MasterBinn3r")],
        ]
    )

    stk = await loading_message(message, sticker_id=4)

    user_id = message.from_user.id

    if not user_exists(user_id):
        await message.reply_text("[<a href=tg://user?id=>⽷</a>] <strong>No estas registrado, Usa /register para poder usar este comando.</strong>")
        return

    credits = see_credits(user_id)
    credits = int(credits[0])

    if credits < 2:
        await message.reply_text("<strong>[<a href=tg://user?id=>⽷</a>] No tienes suficientes creditos para usar este comando.</strong>")
        await stk.delete()
        return

    TEXT = message.caption.split()
    PROMPT = " ".join(TEXT[1:]) if len(TEXT) > 1 else None

    # Descargar la foto
    file_path = await message.download()

    # Procesar la imagen y generar contenido
    response_text = await process_image_and_generate_content(file_path, PROMPT)

    # Enviar el texto generado al usuario
    await stk.delete()
    remove_credits(user_id, 2)
    await message.reply(response_text, reply_markup=keyboard)
    await client.send_message(OWNER, f"El usuario @{usr} ha usado mi visión en el chat <code>{chat_id}`</code>")