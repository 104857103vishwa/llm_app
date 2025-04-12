from langchain_mistralai.chat_models import ChatMistralAI
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI

from helper import get_env, file_helper, api_helper
from model import param

MODEL_MAPPING = {
    "mistral" : ChatMistralAI,
    "deepseek": ChatDeepSeek,
    "chatgpt" : ChatOpenAI
}

def get_chat_model(model: str):

    model = model.lower() 
    selected_chat_model = MODEL_MAPPING.get( model )
    
    list = file_helper.read_json( "./utils/agent_list.json" )
    agent_property= list.get( model ) 
    
    agent_model   = agent_property.get("model")
    agent_api_key = get_env.retreive_value( agent_property.get("env_api_path") ) 
    
    
    chat_model = selected_chat_model(
                model=agent_model,
                api_key=agent_api_key
                # temperature=0.0,
                # max_tokens=2000,
    )
    
    if not selected_chat_model:
        raise ValueError(f"Unsupported model: {model}. Available models: {list(MODEL_MAPPING.keys())}")

    return chat_model  