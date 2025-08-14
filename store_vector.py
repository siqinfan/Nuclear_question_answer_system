from langchain_chroma import Chroma
from pathlib import Path
from load_knowledge import load_and_process_documents
# 2. 创建或加载向量数据库
def setup_vectorstore(load_knowledge_dir: Path, persist_dir: str, embedding_model):
    # 检查向量库是否已存在
    if Path(persist_dir).exists() and any(Path(persist_dir).iterdir()):
        print("加载已有向量数据库...")
        return Chroma(persist_directory=persist_dir, embedding_function=embedding_model)
    else:
        print("创建新向量数据库...")
        splits = load_and_process_documents(load_knowledge_dir)
        vector_store = Chroma.from_documents(
            documents=splits,
            embedding=embedding_model,
            persist_directory=persist_dir
        )
        print(f"向量数据库已创建，包含 {len(splits)} 个文档片段")
        return vector_store