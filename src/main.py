import argparse
from moduls.utils import utils
from pyrogram import Client
import base64, sys, requests, git

def git_pull(repo_path=".."):
    repo = git.Repo(repo_path)
    origin = repo.remotes.origin
    origin.pull()

def forUpdate(owner, project, local_path=".."):
    repo = git.Repo(local_path)
    local_hash = repo.head.commit.hexsha

    response = requests.get(f"https://api.github.com/repos/{owner}/{project}/commits")
    remote_hash = response.json()[0]["sha"]

    return str(local_hash) == str(remote_hash)

if __name__ == "__main__":
    # Controlador de parámetros
    parser = argparse.ArgumentParser(description="Una plantilla que permite interactuar con la API de Telegram para el desarrollo de bots de telegram.")
    parser.add_argument("-d", help="Activar el modo debug.", action="store_true")
    parser.add_argument("--name", help="Establecer el nombre al bot.")
    parser.add_argument("--mention", help="Establecer un username de mención al bot.")
    parser.add_argument("--url", help="Establecer una URL de contacto del bot.")
    parser.add_argument("--api_id", help="Establecer el API ID del bot.")
    parser.add_argument("--api_hash", help="Establecer el API HASH del bot.")
    parser.add_argument("--bot_token", help="Establecer el token del bot.")
    parser.add_argument("--dir_apps", help="Establecer el nombre de la carpeta que contiene todas las aplicaciones del bot. (default: apps)")
    args = parser.parse_args()

    # Clear the terminal
    utils.clear_terminal()

    # PRINT THE BANNER
    utils.anim(base64.b64decode(f"""CgogICAsLS0sICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAsLS0tLSwgICAgICAg
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAosLS0tLid8ICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAgICAgLC8gICAuYHwgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgX19fXyAgIAp8ICAgfCA6ICAgICAgICwtLS0sLiAsLS0sICAgICAsLS0sICAgICxgICAgLicg
IDogICAsLS0tLC4gICAsLS0tLCAgICAgICAgICAgICAgICwnICAsIGAuIAo6ICAgOiB8ICAgICAs
JyAgLicgfCB8Jy4gXCAgIC8gLmB8ICA7ICAgIDsgICAgIC8gLCcgIC4nIHwgICcgIC4nIFwgICAg
ICAgICAgICwtKy0sLicgXyB8IAp8ICAgJyA6ICAgLC0tLS4nICAgfCA7IFwgYFwgLycgLyA7Lidf
X18sLyAgICAsJywtLS0uJyAgIHwgLyAgOyAgICAnLiAgICAgICwtKy0uIDsgICAsIHx8IAo7ICAg
OyAnICAgfCAgIHwgICAuJyBgLiBcICAvICAvIC4nfCAgICA6ICAgICB8IHwgICB8ICAgLic6ICA6
ICAgICAgIFwgICAgLC0tLid8JyAgIHwgIDt8IAonICAgfCB8X18gOiAgIDogIHwtLCAgXCAgXC8g
IC8gLi8gOyAgICB8Lic7ICA7IDogICA6ICB8LSw6ICB8ICAgL1wgICBcICB8ICAgfCAgLCcsIHwg
ICc6IAp8ICAgfCA6Lid8OiAgIHwgIDsvfCAgIFwgIFwuJyAgLyAgYC0tLS0nICB8ICB8IDogICB8
ICA7L3x8ICA6ICAnIDsuICAgOiB8ICAgfCAvICB8IHwgIHx8IAonICAgOiAgICA7fCAgIDogICAu
JyAgICBcICA7ICA7ICAgICAgICcgICA6ICA7IHwgICA6ICAgLid8ICB8ICA7LyAgXCAgIFwnICAg
fCA6ICB8IDogIHwsIAp8ICAgfCAgLi8gfCAgIHwgIHwtLCAgIC8gXCAgXCAgXCAgICAgIHwgICB8
ICAnIHwgICB8ICB8LSwnICA6ICB8IFwgIFwgLCc7ICAgLiB8ICA7IHwtLScgIAo7ICAgOiA7ICAg
JyAgIDogIDsvfCAgOyAgL1wgIFwgIFwgICAgICcgICA6ICB8ICcgICA6ICA7L3x8ICB8ICAnICAn
LS0nICB8ICAgOiB8ICB8ICwgICAgIAp8ICAgLC8gICAgfCAgIHwgICAgXC4vX187ICBcICA7ICBc
ICAgIDsgICB8LicgIHwgICB8ICAgIFx8ICA6ICA6ICAgICAgICB8ICAgOiAnICB8LyAgICAgIAon
LS0tJyAgICAgfCAgIDogICAuJ3wgICA6IC8gXCAgXCAgOyAgICctLS0nICAgIHwgICA6ICAgLid8
ICB8ICwnICAgICAgICA7ICAgfCB8YC0nICAgICAgIAogICAgICAgICAgfCAgIHwgLCcgIDsgICB8
LyAgIFwgICcgfCAgICAgICAgICAgIHwgICB8ICwnICBgLS0nJyAgICAgICAgICB8ICAgOy8gICAg
ICAgICAgIAogICAgICAgICAgYC0tLS0nICAgIGAtLS0nICAgICBgLS1gICAgICAgICAgICAgIGAt
LS0tJyAgICAgICAgICAgICAgICAgICAnLS0tJyAgICAgICAgICAgIAogICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAgIAoK""").decode("utf-8"))

    print ()

    # LOADING JSON CONFIG
    utils.animINFO("Checking for internet connection....")
    internet = False

    try:
        response = requests.get("http://www.google.com", timeout=5)
        if response.status_code == 200:
            utils.animINFO("Checking for updates...")
            update = forUpdate("xploitLabs", "TGbase")
            if update:
                utils.animDONE("System up to date.")
                internet = True

            else:
                utils.animINFO("El sistema encontró una nueva actualización disponible, ¿Deseas actualizarlo? ")
                responseUser = input("[Si/No] >>> ").lower()

                LISTA_A = ["si", "s", "y", "yes", ""]
                LISTA_B = ["no", "n", "any"]

                if responseUser in LISTA_A:
                    utils.animINFO("Actualizando sistema...")
                    git_pull()
                    utils.animDONE("Sistema actualizado de manera exitosa, ejecuta nuevamente el bot.")                    

                else:
                    internet = True

        else:
            utils.animERROR("No internet connection.")
    except requests.ConnectionError:
        utils.animERROR("No internet connection.")

    if not internet:
        sys.exit()

    # LOADING JSON CONFIG
    utils.animINFO("Loading the json config.")

    try:
        # Importing the config data for start the bot
        config = utils.load_json()

    except Exception as Error:
        utils.animERROR("An error has been occurred!")
        print (Error)
        sys.exit()
    else:
        utils.animDONE("Config loaded successfully.")

    # LOADING JSON CONFIG
    utils.animINFO("Setting the config data.")

    try:
        # Set the config data
        bot = Client(
            config["name"],
            api_id=config["api_id"],
            api_hash=config["api_hash"],
            bot_token=config["bot_token"],
            plugins=dict(root=config["dir_plugins"])
        )

    except Exception as Error:
        utils.animERROR("An error has been occurred!")
        print (Error)
        sys.exit()
    else:
        utils.animDONE("Config data has been set successfully.")

    # TURNING ON THE BOT
    utils.animINFO("Turning on the bot.")

    try:
        utils.animINFO(f"THE BOT IS ON!, You can use in: {config['url']}")
        bot.run()
    except Exception as Error:
        utils.animERROR("An error has been occurred!")
        print (Error)
        sys.exit()