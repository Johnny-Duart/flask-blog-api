# 🚀 Flask Blog API

API RESTful desenvolvida com Flask para gerenciamento de usuários, posts e permissões, com autenticação via JWT e controle de acesso baseado em roles (RBAC).

## 📌 Sobre o projeto

Este projeto é um backend completo que implementa:

- CRUD de usuários, posts e roles
- Autenticação com JWT
- Controle de acesso por tipo de usuário (RBAC)
- Documentação automática com Swagger/OpenAPI
- Estrutura organizada seguindo boas práticas (controllers, models, views)
- Testes automatizados (unitários e de integração) com pytest

## 🧠 Tecnologias utilizadas

- Python (3.10–3.11)
- Flask
- Flask-JWT-Extended (autenticação)
- Flask-Bcrypt (hash de senha)
- Flask-SQLAlchemy (ORM)
- Flask-Migrate / Alembic (migrations)
- Marshmallow / Flask-Marshmallow (serialização/validação)
- APISpec + APISpec-Webframeworks (documentação Swagger/OpenAPI)
- Pytest + Pytest-Mock (testes)
- Gunicorn / Waitress (servidor WSGI em produção)

## 🏗️ Arquitetura do projeto

O projeto segue uma separação em camadas dentro do pacote `flask_blog_api`:

```
flask_blog_api/
├── flask_blog_api/
│   ├── controllers/   # Rotas e regras de negócio (blueprints)
│   ├── models/        # Modelos do banco de dados (SQLAlchemy)
│   ├── views/         # Schemas de serialização/validação (Marshmallow)
│   ├── config.py       # Configurações por ambiente (Development/Testing/Production)
│   └── app.py          # Application factory (create_app)
├── migrations/         # Migrações geradas pelo Alembic/Flask-Migrate
├── tests/
│   ├── unit/           # Testes unitários (ex: utils)
│   └── integration/     # Testes de integração (rotas e controllers)
├── Procfile             # Entrypoint para deploy (gunicorn)
├── pyproject.toml / poetry.lock
└── requirements.txt
```

## 🔐 Autenticação e autorização

- Autenticação via JWT (`Flask-JWT-Extended`)
- Senhas protegidas com hash (`bcrypt`) — nunca armazenadas em texto puro
- Controle de acesso com roles:
  - Exemplo: apenas usuários com role `admin` podem listar usuários (`@requires_role("admin")`)
  - Rotas sensíveis (criação/edição/remoção de posts e roles) exigem token válido (`@jwt_required()`)

## 📡 Endpoints principais

### 🔑 Auth
- `POST /auth/login` → Login e geração de token JWT

### 👤 Users
- `POST /users/` → Criar usuário
- `GET /users/` → Listar usuários (admin only)
- `PATCH /users/{id}` → Atualizar usuário (username e/ou senha)
- `DELETE /users/{id}` → Deletar usuário

### 📝 Posts
- `POST /posts/` → Criar post (requer login)
- `GET /posts/` → Listar posts
- `PATCH /posts/{id}` → Atualizar post (requer login)
- `DELETE /posts/{id}` → Deletar post (requer login)

### 🛡️ Roles
- `POST /roles/` → Criar role (requer login)
- `GET /roles/` → Listar roles (requer login)

## 📄 Documentação da API

A documentação Swagger/OpenAPI é gerada automaticamente e pode ser acessada em:

```
/swagger.json
```

## ⚙️ Como rodar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-user/flask-blog-api.git
cd flask-blog-api
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

> Se preferir usar Poetry, basta rodar `poetry install` (o `pyproject.toml` e o `poetry.lock` já estão configurados).

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto (ou exporte as variáveis no terminal):

```env
ENVIRONMENT=development
SECRET_KEY=dev
JWT_SECRET_KEY=super-secret
DATABASE_URL=sqlite:///dio_bank.sqlite
```

> A variável `ENVIRONMENT` define qual classe de configuração será usada (`DevelopmentConfig`, `TestingConfig` ou `ProductionConfig`, em `flask_blog_api/config.py`).

### 5. Rodar as migrations

```bash
export FLASK_APP="flask_blog_api.app:create_app"   # Linux/Mac
set FLASK_APP=flask_blog_api.app:create_app        # Windows

flask db upgrade
```

### 6. Executar o projeto

```bash
python -m flask_blog_api.app
```

A API estará disponível em `http://localhost:5000`.

## 🧪 Como rodar os testes

```bash
pytest
```

Os testes de integração usam um banco SQLite em memória configurado via `TestingConfig`, então não é necessário ter o banco de desenvolvimento rodando para executá-los.

## 🧪 Exemplo de uso (Login)

```http
POST /auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "123456"
}
```

Resposta:

```json
{
  "access_token": "seu_token_jwt"
}
```

## 🎯 Objetivo do projeto

Este projeto foi desenvolvido com foco em:

- Praticar desenvolvimento backend com Flask
- Implementar autenticação segura com JWT
- Aplicar conceitos de controle de acesso (RBAC)
- Estruturar APIs REST de forma profissional, com testes e documentação automática

## 👨‍💻 Autor

Desenvolvido por **Jonathan Duarte**

## ⭐ Contribuição

Sinta-se à vontade para contribuir ou sugerir melhorias!