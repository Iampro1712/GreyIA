import json
import os
import requests
import subprocess
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from bs4 import BeautifulSoup
from moduls.utils.utils import load_json, loading_message
from apps.llm.moduls import llm  # Importar iaSpeech desde el módulo correcto

CONFIG = load_json("llmConfig")  # Ruta correcta al archivo de configuración

def search_Google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    resultados = []
    for result in soup.find_all("div", class_="g"):
        titulo = result.find("h3", class_="LC20lb DKV0Md").text
        enlace = result.find("a", href=True)["href"]
        descripcion = result.find("span", class_="aCOpRe").text
        resultados.append({
            "titulo": titulo,
            "enlace": enlace,
            "descripcion": descripcion
        })

    return resultados

@Client.on_message(filters.command(CONFIG["COMMAND"], CONFIG["prefixes"]))
async def llmUse(clientC, responseR, postdata=0):
    TEXT = responseR.text.split()
    ID_CHAT = responseR.chat.id
    
    NAME = responseR.from_user.username if responseR.chat.type == ChatType.PRIVATE else responseR.chat.title
    PROMPT = " ".join(TEXT[1:]) if len(TEXT) > 1 else None

    if not PROMPT:
        await responseR.reply(CONFIG["manual"])
        return
    
    CHATS = [f.split(".")[0] for f in os.listdir(CONFIG["DIR_CHATS"])]

    PROMPT_INIT = CONFIG["PROMPT"]

    if str(ID_CHAT) in CHATS:
        CONTEXT = json.load(open(f"{CONFIG['DIR_CHATS']}/{ID_CHAT}.json", "r"))
        CONTEXT["chat"] += [f"{CONFIG['name_USER']}: {PROMPT}", f"{CONFIG['name_LLM']}: "]
        TEMPORAL = CONTEXT["chat"].copy()
        TEMPORAL.insert(0, PROMPT_INIT)

        sticker = await loading_message(responseR, CONFIG["sticker_loading"])
        responseIA_text = await llm.iaSpeech(TEMPORAL)
        await sticker.delete()

        try:
            responseIA = json.loads(responseIA_text)
        except json.JSONDecodeError:
            responseIA = {"chat": responseIA_text}

        mensaje = responseIA.get("chat", "")
        busqueda = search_Google(responseIA.get("search", "")) if "search" in responseIA else None
        mensaje_bash = None

        if "bash" in responseIA:
            cmd = responseIA["bash"]
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            mensaje_bash = result.stdout

        await responseR.reply(mensaje, busqueda, mensaje_bash)

        CONTEXT["chat"][-1] += mensaje
        json.dump(CONTEXT, open(f"{CONFIG['DIR_CHATS']}/{ID_CHAT}.json", "w"), indent=4)

    else:
        plantilla = {
            "chat": [
                f"{CONFIG['name_USER']}: {PROMPT}",
                f"{CONFIG['name_LLM']}: "
            ]
        }

        if responseR.chat.type == ChatType.PRIVATE:
            plantilla["username"] = NAME
        elif responseR.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]:
            plantilla["Title Group"] = NAME

        TEMPORAL = plantilla["chat"].copy()
        TEMPORAL.insert(0, PROMPT_INIT)

        sticker = await loading_message(responseR, 0)
        responseIA_text = await llm.iaSpeech(TEMPORAL)
        await sticker.delete()

        try:
            responseIA = json.loads(responseIA_text)
        except json.JSONDecodeError:
            responseIA = {"chat": responseIA_text}

        await responseR.reply(responseIA.get("chat", ""))

        plantilla["chat"][-1] += responseIA.get("chat", "")
        json.dump(plantilla, open(f"{CONFIG['DIR_CHATS']}/{ID_CHAT}.json", "w"), indent=4)
