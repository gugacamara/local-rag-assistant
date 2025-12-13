#!/bin/bash
echo "⏳ Aguardando o serviço Ollama iniciar..."
sleep 5

echo "⬇️ Baixando modelo Qwen 2 (1.5B)... (Isso pode demorar uns minutos)"
docker exec rag_ollama ollama pull qwen2:0.5b

echo "⬇️ Baixando modelo de Embeddings..."
docker exec rag_ollama ollama pull all-minilm

echo "✅ Modelos prontos! Pode usar o chat."