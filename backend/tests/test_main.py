from fastapi.testclient import TestClient
from langchain_core.language_models.fake import FakeListLLM
from langchain_community.embeddings import FakeEmbeddings
from app.main import app, get_llm, get_embeddings

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "running", "model": "qwen2:0.5b"}

def test_chat_endpoint():
    # Arrange: Configura IA falsa e embeddings falsos
    fake_llm = FakeListLLM(responses=["Olá, sou um teste!"])
    fake_embeddings = FakeEmbeddings(size=384) 

    # Substitui as dependências reais pelas falsas
    app.dependency_overrides[get_llm] = lambda: fake_llm
    app.dependency_overrides[get_embeddings] = lambda: fake_embeddings

    # Act: Chama o endpoint de chat
    response = client.post("/chat?query=Oi")
    
    # Assert: Verifica a resposta
    assert response.status_code == 200
    assert "Olá, sou um teste!" in response.text
    
    # Limpa os overrides das dependências
    app.dependency_overrides = {}
