FROM python:3.10-slim

WORKDIR /app

# Instala dependências de sistema necessárias
RUN apt-get update && apt-get install -y build-essential curl

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando para rodar em modo dev
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]