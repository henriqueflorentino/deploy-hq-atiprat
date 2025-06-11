FROM python:3.11-slim

# Instala as dependências de sistema necessárias
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copia templates (aparentemente redundante, pois o COPY . . já cobre isso)
# Você pode manter se quiser garantir que os templates estão sempre no lugar certo
COPY app/templates/ /app/app/templates/

# Expõe a porta da aplicação Flask
EXPOSE 5000

# Inicia o Gunicorn na porta 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
