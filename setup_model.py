from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

import os
import json

# 模型设置
def setup_llm(model_name: str, temperature: float = 0.3):
    """
    设置LLM，默认deepseek
    """
    with open("./json/model_list.json", "r") as f:
        models = json.load(f)
    model_value = models[model_name]
    api_key = os.getenv(model_value["API_KEY"])
    if not api_key:
        raise ValueError("请设置API_KEY环境变量")
    model = model_value["model"]
    base_url = model_value["base_url"]
    llm = ChatOpenAI(
        model=model,
        base_url=base_url,
        api_key=api_key,
        temperature=temperature
    )

    return llm

def setup_embedding(path: str):
    embedding_model = HuggingFaceEmbeddings(model_name=path)
    return embedding_model