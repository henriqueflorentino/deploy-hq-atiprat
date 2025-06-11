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

COPY app/templates/ /app/app/templates/

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]