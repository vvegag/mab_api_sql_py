FROM python:3.11-slim

WORKDIR /app

# Evita arquivos temporários de bytecode e mantém logs sem buffer.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala as dependências da API e do cálculo estatístico.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte para dentro do container.
COPY . .

EXPOSE 8000

# Sobe a aplicação principal da solução.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
