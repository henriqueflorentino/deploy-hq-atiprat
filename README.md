# PRATILEIRA - Aplicação Web com Deploy Automatizado 📦

Este é um projeto de aplicação web desenvolvido em **Python** com **Flask**, que implementa operações CRUD (Criar, Ler, Atualizar, Deletar) para gerenciar "itens" quaisquer em um banco de dados **MySQL**.

A aplicação é totalmente containerizada com **Docker** e possui um pipeline de CI/CD automatizado no **GitHub Actions** para gerenciar o build, a análise de qualidade de código com **SonarQube** e o deploy contínuo em um servidor remoto.


---

## 🚀 URL de Acesso da Aplicação Deploiada

Após um deploy bem-sucedido, a aplicação estará acessível no servidor remoto.

**Endereço:** `http://201.23.3.86:8134`


---

## 🎯 Objetivo

O principal objetivo deste projeto é demonstrar um fluxo de trabalho de desenvolvimento web moderno e automatizado, abrangendo:

* Desenvolvimento de uma aplicação web com interface de usuário básica e persistência de dados.
* Containerização de todos os serviços com Docker.
* Versionamento de código com Git/GitHub.
* Implementação de um pipeline de CI/CD para automação de build, análise de qualidade (SonarQube) e deploy remoto.

---

## 🛠️ Requisitos Técnicos

### 1. Aplicação

* **Backend**: Desenvolvido em **Python** utilizando o framework **Flask**.
    * Funcionalidades: CRUD completo para a entidade "Item".
* **Interface Gráfica**: Uma interface de usuário simples e responsiva para interação com os dados.
* **Banco de Dados**: **MySQL** relacional, configurado para rodar em uma porta específica (`8135` no servidor remoto).
* **Containerização**: A aplicação Flask e o banco de dados MySQL rodam em contêineres Docker distintos, comunicando-se através de uma rede Docker customizada.

### 2. Repositório GitHub

O código-fonte está versionado no GitHub e inclui:
* `app/`: Código-fonte da aplicação Flask.
* `init_db.py`: Script de inicialização do banco de dados.
* `Dockerfile`: Para construir a imagem Docker da aplicação Flask.
* `.github/workflows/deploy.yml`: Define o pipeline de CI/CD com GitHub Actions.

### 3. CI/CD com GitHub Actions ⚙️

O processo de integração e entrega contínua é acionado automaticamente a cada `push` para a branch `main`. O fluxo de trabalho executa os seguintes passos:

1.  **Build e Push da Imagem Docker**: A imagem Docker da aplicação Flask é construída e enviada para o Docker Hub.
2.  **Análise de Qualidade com SonarQube**:
    * O pipeline conecta-se ao servidor remoto (`201.23.3.86`) via SSH.
    * Um contêiner do SonarQube é iniciado temporariamente no servidor na porta `8138`.
    * A análise do código-fonte é executada.
    * **Gate de Qualidade**: O pipeline **falhará** se o código não atender aos critérios de qualidade definidos no SonarQube.
    * Após a análise, o contêiner do SonarQube é finalizado e removido do servidor.
3.  **Deploy Remoto Automatizado**:
    * **Condicional**: Este passo só é executado se a análise do SonarQube for bem-sucedida.
    * Conexão ao servidor remoto (`201.23.3.86`).
    * Remoção de contêineres antigos da aplicação e do banco de dados.
    * As novas imagens são baixadas do Docker Hub.
    * Novos contêineres são iniciados para o MySQL (porta `8135`) e para a aplicação Flask (porta `8134`), tornando a aplicação publicamente acessível.

---

## 💻 Como Executar Localmente (Docker Compose)

Para rodar a aplicação localmente com Docker Compose:

1.  Clone o repositório.
2.  No diretório raiz do projeto, execute:
    ```bash
    docker-compose up --build
    ```
    Isso iniciará o MySQL na porta `3307` e a aplicação Flask na porta `8134`.

3.  Acesse a aplicação no seu navegador: `http://localhost:8134`
