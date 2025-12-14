import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI(title="Personal Chat RAG")

# Liberar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, troque "*" pela URL do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
CHROMA_PATH = os.getenv("CHROMA_DB_DIR", "/chroma_db")
DATA_PATH = os.getenv("DATA_PDFS_DIR", "/data/files")

# Usando o Qwen 2 (0.5B)
llm = OllamaLLM(base_url=OLLAMA_URL, model="qwen2:0.5b") 
embeddings = OllamaEmbeddings(base_url=OLLAMA_URL, model="all-minilm")

os.makedirs(DATA_PATH, exist_ok=True)

@app.get("/")
def health_check():
    return {"status": "running", "model": "qwen2:0.5b"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(DATA_PATH, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        
        # Atualizar Vector DB
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
        db.add_documents(splits)
        
        return {"filename": file.filename, "status": "uploaded and ingested", "chunks": len(splits)}
    except Exception as e:
        return {"filename": file.filename, "status": "error", "detail": str(e)}

@app.post("/chat")
async def chat_endpoint(query: str):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    # Busca contexto (Retrieval)
    docs = db.similarity_search(query, k=2)
    context_text = "\n\n".join([d.page_content for d in docs]) if docs else "Sem contexto adicional."

    # --- PROMPT ---
    template = """Você é um assistente de IA prestativo e inteligente.
    Responda à pergunta do usuário usando o contexto fornecido abaixo.
    Se a resposta não estiver no contexto, use seu conhecimento para responder da melhor forma possível em Português.
    
    Contexto:
    {context}
    
    Pergunta do Usuário:
    {question}
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    async def response_generator():
        async for chunk in chain.astream({"context": context_text, "question": query}):
            yield chunk

    return StreamingResponse(response_generator(), media_type="text/plain")