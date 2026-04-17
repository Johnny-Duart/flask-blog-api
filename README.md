# 🚀 Flask Blog API

API RESTful desenvolvida com Flask para gerenciamento de usuários, posts e permissões, com autenticação via JWT e controle de acesso baseado em roles (RBAC).

---

## 📌 Sobre o projeto

Este projeto é um backend completo que implementa:

* CRUD de usuários, posts e roles
* Autenticação com JWT
* Controle de acesso por tipo de usuário (RBAC)
* Documentação automática com Swagger/OpenAPI
* Estrutura organizada seguindo boas práticas

---

## 🧠 Tecnologias utilizadas

* **Python**
* **Flask**
* **Flask-JWT-Extended** (autenticação)
* **Flask-Bcrypt** (hash de senha)
* **Flask-SQLAlchemy** (ORM)
* **Flask-Migrate** (migrations)
* **Marshmallow** (serialização/validação)
* **APISpec / Swagger** (documentação)

---

## 🏗️ Arquitetura do projeto

O projeto segue uma separação em camadas:

```
├── controllers  # Rotas e regras de negócio
├── models       # Modelos do banco de dados
├── views        # Schemas e validações
├── config       # Configurações por ambiente
├── app.py       # Factory da aplicação
```

---

## 🔐 Autenticação e autorização

* Autenticação via **JWT**
* Senhas protegidas com **hash (bcrypt)**
* Controle de acesso com **roles**:

  * Exemplo: apenas usuários com role `admin` podem listar usuários

---

## 📡 Endpoints principais

### 🔑 Auth

* `POST /auth/login` → Login e geração de token

### 👤 Users

* `POST /users` → Criar usuário
* `GET /users` → Listar usuários (admin only)
* `PATCH /users/{id}` → Atualizar usuário
* `DELETE /users/{id}` → Deletar usuário

### 📝 Posts

* `POST /posts` → Criar post (requer login)
* `GET /posts` → Listar posts
* `PATCH /posts/{id}` → Atualizar post
* `DELETE /posts/{id}` → Deletar post

### 🛡️ Roles

* `POST /roles` → Criar role
* `GET /roles` → Listar roles

---

## 📄 Documentação da API

A documentação Swagger pode ser acessada em:

```
/swagger.json
```

---

## ⚙️ Como rodar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-user/flask-blog-api.git
cd flask-blog-api
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` ou configure:

```
ENVIRONMENT=development
SECRET_KEY=dev
JWT_SECRET_KEY=super-secret
DATABASE_URL=sqlite:///database.db
```

### 5. Rodar migrations

```bash
flask db upgrade
```

### 6. Executar o projeto

```bash
python app.py
```

---

## 🧪 Exemplo de uso (Login)

```json
POST /auth/login

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

---

## 🎯 Objetivo do projeto

Este projeto foi desenvolvido com foco em:

* Praticar desenvolvimento backend com Flask
* Implementar autenticação segura com JWT
* Aplicar conceitos de controle de acesso (RBAC)
* Estruturar APIs REST de forma profissional

---

## 👨‍💻 Autor

Desenvolvido por **Jonathan Duarte**

---

## 📌 Melhorias futuras

* [ ] Testes automatizados
* [ ] Deploy em produção
* [ ] Integração com frontend
* [ ] Paginação nos endpoints
* [ ] Filtros de busca

---

## ⭐ Contribuição

Sinta-se à vontade para contribuir ou sugerir melhorias!
