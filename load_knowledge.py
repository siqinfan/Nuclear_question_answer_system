
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import json

# 自定义加载器类，解决编码问题
class EncodingAwareTextLoader(TextLoader):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.file_path = file_path
        
    def load(self):
        """
        通过自动编码检测加载文档
        """
        encodings_to_try = ['utf-8', 'gbk', 'latin-1']
        for encoding in encodings_to_try:
            try:
                with open(self.file_path, 'r', encoding=encoding) as f:
                    text = f.read()
                metadata = {"source": self.file_path}
                return [{"page_content": text, "metadata": metadata}]
            except UnicodeDecodeError:
                continue
        # 如果所有编码都失败，尝试二进制模式
        try:
            with open(self.file_path, 'rb') as f:
                raw_data = f.read()
                # 尝试解码为UTF-8并忽略错误
                text = raw_data.decode('utf-8', errors='ignore')
            metadata = {"source": self.file_path}
            return [{"page_content": text, "metadata": metadata}]
        except Exception as e:
            print(f"无法加载文件 {self.file_path}: {str(e)}")
            return []
        
# 加载并处理文档
def load_and_process_documents(knowledge_file_dir: Path):
    print("正在加载知识库文件...")
    # 加载文档 - 支持多种文件类型
    all_files = []
    for ext in ['*.json', '*.txt', '*.md']:
        all_files.extend(knowledge_file_dir.glob(ext))
    if not all_files:
        raise FileNotFoundError(f"在 {knowledge_file_dir} 中没有找到任何知识文件")
    print(f"找到 {len(all_files)} 个知识文件")
    docs = []
    for file_path in all_files:
        try:
            loader = EncodingAwareTextLoader(str(file_path))
            file_docs = loader.load()
            if file_docs:
                docs.extend(file_docs)
        except Exception as e:
            print(f"加载文件 {file_path} 时出错: {str(e)}")
    
    if not docs:
        raise RuntimeError("成功加载的知识文件数量为0")
    
    print(f"成功加载 {len(docs)} 个文档")
    
    # 处理文档内容
    processed_docs = []
    for doc in docs:
        source_path = Path(doc['metadata']['source'])
        
        # 根据文件类型处理内容
        if source_path.suffix.lower() == '.json':
            try:
                data = json.loads(doc['page_content'])
                title = data.get('title', '无标题')
                content = data.get('content', '')
                tags = data.get('tags', [])
                
                formatted_content = f"标题: {title}\n"
                if tags:
                    formatted_content += f"标签: {', '.join(tags)}\n"
                formatted_content += f"内容: {content}"
                
                doc['page_content'] = formatted_content
                processed_docs.append(doc)
            except json.JSONDecodeError:
                print(f"JSON解析失败: {source_path}")
                continue
        else:  # .txt 或 .md 文件
            # 使用文件名作为标题
            title = source_path.stem
            content = doc['page_content']
            doc['page_content'] = f"标题: {title}\n内容: {content}"
            processed_docs.append(doc)
    
    # 分割文本
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", "。", "！", "？", "；"]
    )
    splits = text_splitter.split_documents(processed_docs)
    print(f"文档分割为 {len(splits)} 个片段")
    return splits