# 核物理知识问答系统

基于LangChain的本地化核物理知识问答系统，专为核物理研究者和学习者设计，提供高效的专业知识查询和科研服务。

## 核心特点

- **完全本地运行**：所有数据处理在本地完成
- **核物理专业问答**：针对专业领域优化
- **隐私保护**：敏感数据不会离开本地环境
- **来源追溯**：显示答案依据的知识条目和公式

## 技术栈

- **框架**：LangChain
- **嵌入模型**：sentence-transformers/all-MiniLM-L6-v2
- **语言模型**：HuggingFace GPT-2 / Flan-T5
- **向量数据库**：FAISS
- **前端界面**：Streamlit
- **数据处理**：JSONLoader, RecursiveCharacterTextSplitter

## 安装指南

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/siqinfan/Nuclear_questions_answer_system.git
cd Nuclear_question_answer_system
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **准备知识库**
```bash
mkdir your_knowledge_directory
# 将您的知识文件放入该目录，并在main.py中修改knowledge_dir参数
```

4. **下载模型**
```bash
# 更改download_model.py中存储路径
python download_model.py
```

## 使用说明

### 启动系统
```bash
python main.py
```

### 功能

1. **问题输入**：在文本框中输入核物理相关问题
2. **多种场景**：匹配多种科研场景
3. **专业回答**：系统基于知识库生成专业回答
4. **参考来源**：展示答案依据的知识条目
5. **历史记录**：查看所有历史问答

### 示例问题

- 什么是核裂变？

## 配置选项

### 模型选择

在```json/model_list.json```中添加想要使用的模型，并修改```main.py```中的```model```参数。

### 提示词选择

在```json/prompt.json```中选择想要的问答场景，也可根据自己的需求添加对应的提示词模板，并修改```main.py```中的```prompt_type```参数。

### 知识库配置

见knowledge_sample文件夹中的示例文件。

## 许可证

本项目采用 [Apache License 2.0](LICENSE)，本许可证允许商业用途，但须遵守其条款和条件。

---

**核物理研究 · 安全高效 · 知识管理**  
让核物理专业知识触手可及！
