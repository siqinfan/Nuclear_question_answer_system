from langchain_core.prompts import PromptTemplate
import json

# 定义提示模板
def get_prompt_template(situation: str = "学习"):
    with open("./json/prompt.json", "r", encoding="utf-8") as f:
        prompt_dict = json.load(f)
    return PromptTemplate.from_template(prompt_dict[situation])