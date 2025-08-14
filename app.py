from setup_model import setup_llm,setup_embedding
from store_vector import setup_vectorstore
from prompt import get_prompt_template
from pathlib import Path
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

def ask_question(model, temperature, embedding_model_path, knowledge_dir, persist_dir, prompt_type):

    llm = setup_llm(model_name=model, temperature=temperature)
    embedding_model = setup_embedding(embedding_model_path)
    # 检查知识库目录
    knowledge_file_dir = Path(knowledge_dir)
    if not knowledge_file_dir.exists() or not any(knowledge_file_dir.iterdir()):
        raise FileNotFoundError(f"知识库目录 {knowledge_file_dir} 不存在或为空")

    vector_store = setup_vectorstore(
        load_knowledge_dir=knowledge_file_dir,
        persist_dir=persist_dir,
        embedding_model=embedding_model,
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    prompt_template = get_prompt_template(prompt_type)
    
    chain = (
        RunnableParallel({
            "context": itemgetter("question") | retriever | format_docs,
            "question": RunnablePassthrough()
        })
        | prompt_template
        | llm
        | StrOutputParser()
    )

    question = input("请输入问题: ")
    while question not in ["exit", "Exit", "quit", "Quit", "q", "Q"]:
        print("============================================================")
        response = chain.invoke({"question": question})
        print("\n回答:")
        print(response)
        print("============================================================\n")
        question = input("请输入问题: ")

# 格式化检索结果
def format_docs(docs):
    formatted = []
    for i, doc in enumerate(docs, 1):
        source = Path(doc.metadata['source']).name
        content = doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
        formatted.append(f"[知识片段 #{i} - 来源: {source}]\n{content}")
    return "\n\n".join(formatted)