from google import genai
from google.genai import types
from moduls.utils.utils import load_json

CONFIG = load_json("llmConfig")

# Initialize the client with API key
client = genai.Client(api_key=CONFIG["API_KEY"])

async def iaSpeech(CONTEXT):
    try:
        response = await client.aio.models.generate_content(
            model=CONFIG["model"],
            contents=CONTEXT,
            config=types.GenerateContentConfig(
                temperature=CONFIG["config_model"]["temperature"],
                top_p=CONFIG["config_model"]["top_p"],
                top_k=CONFIG["config_model"]["top_k"],
                max_output_tokens=CONFIG["config_model"]["max_output_tokens"],
                safety_settings=[
                    types.SafetySetting(
                        category=setting["category"],
                        threshold=setting["threshold"]
                    ) for setting in CONFIG["security"]
                ]
            )
        )
        return response.text
    except Exception as e:
        print(f"Error in iaSpeech: {e}")
        return "Lo siento, hubo un error al procesar tu solicitud."