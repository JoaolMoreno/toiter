# Toiter - Um Clone Simples do Twitter

## **1. Tema e Público-Alvo**
- **Tema**: A aplicação "Toiter" é um clone simplificado do Twitter, desenvolvido para simular uma plataforma de microblogging onde os usuários podem compartilhar e interagir com postagens em um formato de linha do tempo.
- **Público-Alvo**: O público-alvo do Toiter são usuários de redes sociais interessados em uma experiência de microblogging básica, onde possam criar postagens, responder, curtir, e visualizar conteúdos em uma estrutura organizada. Além disso, é voltada para estudantes e desenvolvedores iniciantes que buscam entender e construir uma aplicação web completa, utilizando tecnologias como Flask, SQL Server e Docker.

---

Toiter é uma versão simplificada do Twitter construída com Flask, SQL Server e Docker. Ele permite aos usuários:

- Criar uma conta apenas fornecendo um nome de usuário.
- Criar postagens com conteúdo de texto e mídia opcional (imagens ou vídeos).
- Responder a postagens, com respostas exibidas hierarquicamente.
- Curtir e descurtir postagens.
- Visualizar todas as postagens e respostas em um formato encadeado.
- Fazer upload de arquivos de mídia com validações de tamanho e tipo.

## **Índice**

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Executando o Aplicativo](#executando-o-aplicativo)
- [Uso](#uso)
- [Configuração](#configuração)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## **Estrutura do Projeto**

```
twitter_clone/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── database.sql
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── create_post.html
│   ├── reply.html
│   └── post.html
├── static/
│   └── styles.css
├── uploads/ (Este diretório é criado em tempo de execução)
```

- **app.py**: Arquivo principal do aplicativo Flask.
- **requirements.txt**: Dependências do Python.
- **Dockerfile**: Configuração Docker para o app Flask.
- **docker-compose.yml**: Configuração do Docker Compose para executar o app e o SQL Server.
- **database.sql**: Script SQL para inicializar o banco de dados.
- **templates/**: Templates HTML para as páginas da web.
- **static/**: Arquivos estáticos (CSS).
- **uploads/**: Diretório onde os arquivos de mídia carregados são armazenados.
- **README.md**: Documentação do projeto.
- **.gitignore**: Arquivo para ignorar arquivos no Git.

---

## **Funcionalidades**

- **Autenticação de Usuário**: Sistema simples de login usando nomes de usuário.
- **Criar Postagens**: Usuários podem criar postagens com texto e mídia opcional (imagens ou vídeos).
- **Respostas**: Usuários podem responder às postagens, exibidas de forma encadeada.
- **Curtidas**: Usuários podem curtir ou descurtir postagens.
- **Uploads de Mídia**: Suporte para upload de imagens e vídeos com validações.
- **Design Responsivo**: Estilização básica para simular o layout antigo do Twitter.

---

## **Pré-requisitos**

- **Docker**: Certifique-se de ter Docker e Docker Compose instalados.
- **Python 3.9**: Se desejar executar o aplicativo sem Docker.
- **Git**: Para clonar o repositório.

---

## **Instalação**

### **1. Clone o Repositório**

```bash
git clone https://github.com/yourusername/twitter_clone.git
cd twitter_clone
```

### **2. Configuração do Ambiente**

Se usar Docker, pule para a seção [Executando o Aplicativo](#executando-o-aplicativo).

Para executar localmente:

- **Crie um ambiente virtual**

  ```bash
  python -m venv venv
  source venv/bin/activate  # No Windows, use 'venv\Scripts\activate'
  ```

- **Instale as Dependências**

  ```bash
  pip install -r requirements.txt
  ```

- **Instale o SQL Server ou Ajuste para SQLite**

  O aplicativo está configurado para usar o SQL Server. Pode ser necessário ajustar as configurações de conexão ou usar SQLite para desenvolvimento local.

---

## **Executando o Aplicativo**

### **Usando Docker (Recomendado)**

**1. Construa e Execute com Docker Compose**

```bash
docker-compose up --build
```

**2. Acesse o Aplicativo**

Abra seu navegador e navegue para:

```
http://localhost:5000
```

### **Sem Docker**

**Nota**: É necessário ter o SQL Server instalado e configurado ou ajustar o aplicativo para usar SQLite.

**1. Inicialize o Banco de Dados**

```bash
# Certifique-se de que o SQL Server está em execução e acessível
# Execute o script SQL para criar o banco de dados e as tabelas
# Isso pode ser feito usando um cliente SQL ou uma ferramenta de linha de comando
```

**2. Execute o Aplicativo**

```bash
python app.py
```

---

## **Uso**

### **1. Login**

- Navegue até a página de login.
- Insira um nome de usuário para fazer login. Não é necessária senha.

### **2. Criar uma Postagem**

- Clique no botão circular "+" no canto inferior direito.
- Insira o conteúdo da sua postagem.
- Opcionalmente, carregue uma imagem ou vídeo (formatos suportados: PNG, JPG, JPEG, GIF, MP4, WebM).
- Clique em "Postar" para enviar.

### **3. Visualizar Postagens**

- As postagens são exibidas na página inicial.
- Respostas são mostradas encadeadas sob as postagens originais.

### **4. Responder a uma Postagem**

- Clique em "Responder" sob uma postagem.
- Você verá o conteúdo da postagem original.
- Insira sua resposta e, opcionalmente, carregue mídia.
- Clique em "Responder" para enviar.

### **5. Curtir/Descurtir uma Postagem**

- Clique em "Curtir" ou "Descurtir" para alternar seu status de curtida em uma postagem.

### **6. Sair**

- Clique em "Sair" no cabeçalho para deslogar.

---

## **Configuração**

### **Variáveis de Ambiente**

Você pode configurar certos aspectos do aplicativo usando variáveis de ambiente:

- **`SQL_SERVER_HOST`**: O nome do host do banco de dados SQL Server.
- **`SA_PASSWORD`**: A senha para o usuário `sa` do SQL Server.
- **`SECRET_KEY`**: Chave secreta do Flask para gerenciamento de sessões.

### **Uploads de Mídia**

- Arquivos de mídia carregados são armazenados no diretório `uploads/`.
- O tamanho máximo de upload é **50 MB**.
- Formatos de imagem permitidos: PNG, JPG, JPEG, GIF.
- Formatos de vídeo permitidos: MP4, WebM.

---

## **Tecnologias Utilizadas**

- **Backend**: Flask (Python)
- **Banco de Dados**: SQL Server
- **Frontend**: HTML, CSS (com templates do Flask)
- **Containers**: Docker, Docker Compose

---

## **Contribuição**

Contribuições são bem-vindas! Por favor, siga estes passos:

1. **Faça um Fork do Repositório**

   Clique no botão "Fork" no canto superior direito desta página para criar uma cópia do repositório em sua conta.

2. **Clone seu Fork**

   ```bash
   git clone https://github.com/yourusername/twitter_clone.git
   cd twitter_clone
   ```

3. **Crie um Branch**

   ```bash
   git checkout -b feature/nome-da-sua-feature
   ```

4. **Faça Alterações**

   Implemente sua feature ou correção de bug.

5. **Commit e Push**

   ```bash
   git add .
   git commit -m "Adicione sua mensagem de commit aqui"
   git push origin feature/nome-da-sua-feature
   ```

6. **Crie um Pull Request**

   Vá até o repositório original e clique em "Pull Requests" para enviar suas mudanças para revisão.

---

## **Licença**

Este projeto está licenciado sob a [Licença MIT](LICENSE).

---

## **Informações Adicionais**

### **Tratamento de Erros**

- O aplicativo usa mensagens `flash` para exibir erros, como tipos de arquivo inválidos ou uploads falhos.

### **Considerações de Segurança**

- **Autenticação**: Atualmente, os usuários fazem login apenas com um nome de usuário; não há autenticação por senha.
- **Validação de Entrada**: A validação básica é implementada, mas medidas de segurança adicionais devem ser adicionadas para uso em produção.
- **Uploads de Arquivos**: O aplicativo verifica tipos e tamanhos de arquivos, mas considere implementar verificações adicionais de segurança.

### **Possíveis Melhorias**

- Implementar autenticação por senha.
- Melhorar a interface com estilização e responsividade aprimoradas.
- Adicionar paginação para postagens e respostas.
- Implementar perfis de usuário e funcionalidade de seguir.
- Usar um serviço de armazenamento em nuvem para arquivos de mídia visando escalabilidade.

---

**Aproveite o Toiter!**