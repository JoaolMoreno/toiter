# Use uma imagem oficial do Python
FROM python:3.9-slim

# Instala as dependências do sistema para o pyodbc, o driver ODBC do SQL Server e libmagic
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    curl \
    gnupg \
    libmagic1 \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de dependências e instala as dependências do Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia todos os arquivos da aplicação para o diretório de trabalho no container
COPY . .

# Exponha a porta do Flask
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]