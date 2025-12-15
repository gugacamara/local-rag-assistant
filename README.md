# 🤖 Local RAG Assistant

> **Assistente de Chat com IA Local usando RAG (Retrieval-Augmented Generation)**
> *Converse com seus PDFs sem enviar dados para a nuvem.*

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Backend-FastAPI-blue)
![Angular](https://img.shields.io/badge/Frontend-Angular_17+-red)
![Docker](https://img.shields.io/badge/Infra-Docker-2496ED)
![AI](https://img.shields.io/badge/AI-Ollama_Local-orange)

## 📖 Sobre o Projeto

O **Local RAG Assistant** é uma aplicação full-stack que permite aos usuários fazer upload de documentos PDF e conversar com eles usando Inteligência Artificial. 

Diferente de soluções baseadas em nuvem (como ChatGPT ou Claude), este projeto roda **100% localmente** utilizando o **Ollama**, garantindo total privacidade dos dados. Ele utiliza a técnica de **RAG (Retrieval-Augmented Generation)** para fornecer respostas precisas baseadas no contexto dos documentos enviados.

### 🚀 Principais Funcionalidades

*   **Privacidade Total**: Nenhum dado sai da sua máquina.
*   **Ingestão de Documentos**: Upload e processamento de PDFs com *chunking* inteligente.
*   **Busca Semântica**: Utiliza **ChromaDB** para armazenar e recuperar vetores de contexto.
*   **Chat Interativo**: Interface moderna em **Angular** com suporte a respostas em tempo real (streaming).
*   **Arquitetura Modular**: Backend desacoplado (FastAPI) e Frontend reativo (Angular Signals).
*   **Containerização**: Setup completo via **Docker Compose**.

---

## 🛠️ Tecnologias Utilizadas

### Backend
*   **Python 3.11+**
*   **FastAPI**: API REST de alta performance.
*   **LangChain**: Framework para orquestração de LLMs.
*   **ChromaDB**: Banco de dados vetorial para busca semântica.
*   **Ollama**: Executor local de modelos de linguagem (LLMs).
*   **Pytest**: Testes unitários e de integração.

### Frontend
*   **Angular (v17+)**: Framework SPA moderno.
*   **Signals**: Gerenciamento de estado reativo.
*   **Tailwind CSS / Custom CSS**: Estilização.

### Infraestrutura
*   **Docker & Docker Compose**: Orquestração de containers.
*   **NVIDIA Container Toolkit**: Suporte a aceleração por GPU (opcional).

---

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter instalado:
*   [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/install/).
*   *(Opcional)* Drivers NVIDIA e NVIDIA Container Toolkit para melhor performance do modelo.

---

## 🚀 Como Executar

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/local-rag-assistant.git
cd local-rag-assistant
```

### 2. Configuração de Ambiente
Crie um arquivo `.env` na raiz do projeto (ou renomeie um exemplo, se houver):

```env
# .env
OLLAMA_BASE_URL=http://ollama:11434
CHROMA_DB_DIR=/chroma_db
DATA_PDFS_DIR=/data/files
BACKEND_PORT=8000
FRONTEND_PORT=8080
```

### 3. Inicie os Containers
Execute o comando abaixo para construir e subir os serviços:

```bash
docker-compose up -d --build
```

### 4. Inicialize os Modelos de IA
O projeto inclui um script para baixar automaticamente os modelos necessários (`qwen2:0.5b` para chat e `all-minilm` para embeddings) dentro do container do Ollama:

```bash
chmod +x scripts/init_models.sh
./scripts/init_models.sh
```
> *Nota: O download pode levar alguns minutos dependendo da sua conexão.*

### 5. Acessar a Aplicação
*   **Frontend**: [http://localhost:8080](http://localhost:8080)
*   **API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Testes

O projeto segue boas práticas de desenvolvimento com testes automatizados.

### Backend (Pytest)
Os testes do backend utilizam *mocks* para simular o LLM, permitindo execução rápida sem carregar os modelos pesados.

```bash
# Executar testes dentro do container
docker exec rag_backend pytest -v
```

### Frontend (Karma/Jasmine)
Para rodar os testes unitários dos componentes Angular, é recomendado executar localmente, pois o container Docker de produção (Nginx) não possui as ferramentas de desenvolvimento.

```bash
# Na pasta frontend:
cd frontend
npm install
ng test
```

---

## 📂 Estrutura do Projeto

```
local-rag-assistant/
├── backend/                # API Python (FastAPI)
│   ├── app/
│   │   ├── main.py         # Entrypoint e Endpoints
│   │   └── ...
│   ├── tests/              # Testes automatizados (Pytest)
│   └── Dockerfile
├── frontend/               # Aplicação Angular
│   ├── src/app/
│   │   ├── components/     # Componentes (Chat, FileUpload)
│   │   ├── services/       # Comunicação com API
│   │   └── ...
│   └── Dockerfile
├── data/                   # Persistência de dados (PDFs, ChromaDB)
├── scripts/                # Scripts utilitários (init_models.sh)
└── docker-compose.yml      # Orquestração dos serviços
```

---

## 🔮 Melhorias Futuras

*   [ ] Adicionar suporte a múltiplos formatos de arquivo (.docx, .txt).
*   [ ] Implementar histórico de conversas persistente.
*   [ ] Melhorar a interface de feedback de upload.
*   [ ] Adicionar autenticação de usuário.

---

## 📝 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para contribuir!

---
Desenvolvido por **[Seu Nome]** 🚀
[LinkedIn](https://linkedin.com/in/seu-linkedin) | [GitHub](https://github.com/seu-github)
