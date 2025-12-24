import os
import shutil
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma
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
os.makedirs(DATA_PATH, exist_ok=True)

# Funções de dependência
def get_llm():
    """
    Cria e retorna uma instância do modelo de linguagem OllamaLLM.
    Utiliza a URL e o modelo definidos nas variáveis de ambiente.
    Returns:
        OllamaLLM: Instância configurada do modelo de linguagem.
    """
    return OllamaLLM(base_url=OLLAMA_URL, model="qwen2:0.5b")

def get_embeddings():
    """
    Cria e retorna uma instância de embeddings OllamaEmbeddings.
    Utiliza a URL e o modelo definidos nas variáveis de ambiente.
    Returns:
        OllamaEmbeddings: Instância configurada de embeddings.
    """
    return OllamaEmbeddings(base_url=OLLAMA_URL, model="all-minilm")

@app.get("/")
def health_check(): # Not implemented
    """
    Endpoint de verificação de saúde da API.
    Retorna o status de execução e o modelo de linguagem em uso.
    Returns:
        dict: Status e modelo atual.
    """
    return {"status": "running", "model": "qwen2:0.5b"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), embeddings=Depends(get_embeddings)):
    """
    Endpoint para upload e ingestão de arquivos PDF.
    Salva o arquivo enviado, realiza a extração e divisão do texto em chunks,
    e atualiza o banco vetorial ChromaDB com os embeddings gerados.

    Parameters:
        file (UploadFile): Arquivo PDF enviado pelo usuário.
        embeddings: Função de dependência para geração de embeddings.

    Returns:
        dict: Status do upload, nome do arquivo, quantidade de chunks ou detalhes do erro.
    """
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
        return JSONResponse(
            status_code=201,
            content={
                "filename": file.filename,
                "status": "uploaded and ingested",
                "chunks": len(splits)
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "filename": file.filename,
                "status": "error",
                "detail": str(e)
            }
        )

@app.post("/chat")
async def chat_endpoint(query: str, llm=Depends(get_llm), embeddings=Depends(get_embeddings)):
    """
    Endpoint de chat para responder perguntas do usuário com base nos PDFs enviados.
    Realiza busca semântica no banco vetorial, monta o prompt e retorna a resposta do LLM via streaming.

    Parameters:
        query (str): Pergunta do usuário.
        llm: Função de dependência para o modelo de linguagem.
        embeddings: Função de dependência para embeddings.

    Returns:
        StreamingResponse: Resposta do modelo em tempo real (streaming).
    """
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