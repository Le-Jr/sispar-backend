# Backend - Sispar

![Screenshot](./assets/swagger.png)

## Descrição

Este é o backend do projeto **Sispar**, desenvolvido com **Flask** e utilizando o banco de dados **MySQL**. O backend fornece as APIs para gerenciar **Colaboradores** e solicitações de **Reembolsos**, incluindo funcionalidades de criação, leitura, atualização e exclusão (CRUD).

A documentação da API está disponível através do **Swagger** na rota `/apidocs` após a inicialização da aplicação.

---

## Tecnologias Utilizadas

[![My Skills](https://skillicons.dev/icons?i=flask&theme=light)](https://skillicons.dev) - **Flask**: Framework Python para a construção de APIs escaláveis e de fácil manutenção.

[![My Skills](https://skillicons.dev/icons?i=mysql&theme=light)](https://skillicons.dev)- **MySQL**: Banco de dados relacional utilizado para armazenar as informações de produtos e categorias.

[![My Skills](https://skillicons.dev/icons?i=sqlalchemy&theme=light)](https://skillicons.dev)- **SQLAlchemy**: ORM para interagir com o banco de dados.

---

## Estrutura do Projeto

```bash
API/
├── src/
│   ├── controller/
│   │   ├── colaborador_controller.py
│   │   └── reembolso_controller.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── colaborador_model.py
│   │   └── reembolso_model.py
│   ├── security/
│   │   └── security.py
│   ├── app.py
├── docs/
│   ├── colaborador/
│   └── reembolso/
├── tests/
├── venv/
├── .env
├── .gitignore
├── config.py
├── Procfile
├── requirements.txt
├── run.py
├── assets/
│   └── swagger.png
└── README.md


```

---

## Como Rodar o projeto ✅

### 1. Localmente 🖥️

1. **Clonar o repositório**:

   ```bash
   git clone https://github.com/Le-Jr/sispar-backend.git
   cd sispar-backend
   ```

2. **Instalar as dependências**

   ```bash
     pip install -r requirements.txt
   ```

3. **Configurar o banco de dados (MySQL):** Certifique-se de que o banco de dados MySQL esteja configurado corretamente e acessível. As credenciais do banco de dados podem ser configuradas no arquivo .env(exemplo abaixo)

   ```bash
   URL_DATABASE_DEV="mysql://USER:PASSWORD@localhost:3306/mydb"
   ```

4. **Rodar a aplicação**: Para rodar o backend no ambiente de desenvolvimento, use o seguinte comando:

   ```bash
   python run.py
   ```

   Isso irá iniciar o servidor na porta 5000 por padrão.

5. **Acessar o Swagger**: A documentação da API gerada pelo Swagger estará disponível na rota /apidocs após a aplicação ser inicializada. Você pode acessar a documentação visitando:

   ```bash
     http://localhost:5000/apidocs
   ```

## Endpoints 🎖️

O backend fornece os seguintes endpoints:

## Colaborador

- **PUT** /colaborador/atualizar/{id}

  - Função: Atualiza os dados de um colaborador existente pelo id.

  - Campos atualizáveis: name, email, password, job, salary (via corpo da requisição).

- **POST** /colaborador/criar

  - Função: Cria um novo colaborador no banco de dados.

  - Campos obrigatórios: name, email, password, job, salary (via corpo da requisição).

- **POST** /colaborador/login

  - Função: Autentica um colaborador usando email e password.

  - Retorno: Credenciais básicas (via to_dict(), que retorna apenas email e password).

- **GET** /colaborador/todos-colaboradores

  - Função: Lista todos os colaboradores cadastrados.

  - Retorno: Lista de colaboradores com todos os dados (via all_data()).

## Reembolso

- **POST** /reembolso/solicita-reembolso

  - Função: Cria uma nova solicitação de reembolso.

  - Retorno: Dados completos da solicitação (via to_dict()).

- **GET** /reembolso/ver-reembolso/(installment_num)

  - Função: Busca reembolsos pelo número de prestação (installment_num).

  - Retorno: Lista de reembolsos filtrados por prestação.

### Observações 🔍

Relacionamento entre as tabelas:

O campo **id_employee** na tabela Refund é uma chave estrangeira que referencia o id da tabela **Employee**.

Isso permite vincular **cada reembolso a um colaborador** específico.

---

### Swagger 📚

A documentação da API gerada pelo Swagger está disponível no endpoint /api. Para acessar a documentação interativa, basta inicializar a aplicação e navegar até:

```bash

http://localhost:3000/apidocs

```

Essa interface permite testar os endpoints diretamente, visualizar os modelos de dados e obter uma visão geral de todos os recursos da API.
