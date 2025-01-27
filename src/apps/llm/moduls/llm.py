import google.generativeai as genai
from moduls.utils.utils import load_json
from dotenv import load_dotenv
import os

load_dotenv()

CONFIG = load_json("llmConfig")
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel(model_name=CONFIG["model"],
                              generation_config=CONFIG["config_model"],
                              safety_settings=CONFIG["security"])

async def iaSpeech(CONTEXT):
    response = await model.generate_content_async(CONTEXT)
    return response.text