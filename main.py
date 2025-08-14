# model: 模型名字
# 目前只有 deepseek
model="deepseek"

# 模型温度
temperature = 0.3

# Embedding目录
embedding_model_path = "/home_data/public/ai/BAAI/bge-large-zh-v1___5"

# 知识库文件目录
knowledge_dir = "/home_data/public/ai/knowledge"

# chroma目录
persist_dir = "/home_data/public/ai/chroma"

# 提示词类型
prompt_type = "学习"


from app import ask_question
ask_question(model, temperature, embedding_model_path, knowledge_dir, persist_dir, prompt_type)