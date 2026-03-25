
# 💳 API Bancária com FastAPI

API simples de operações bancárias desenvolvida com **FastAPI**, utilizando autenticação JWT, banco de dados PostgreSQL e migrações com Alembic.

---

## 🚀 Funcionalidades

* 🔐 Registro de usuário
* 🔑 Login com autenticação JWT
* 💰 Depósito
* 💸 Saque
* 📄 Extrato de transações

---

## 🛠️ Tecnologias utilizadas

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* JWT (JSON Web Token)

---

## 📁 Estrutura do projeto

```
app/
│
├── models/        # Modelos do banco de dados
├── schemas/       # Schemas (Pydantic)
├── routes/        # Rotas da API
├── database/      # Conexão com o banco
├── core/          # Segurança (JWT, hash)
│
alembic/           # Migrações do banco
```

---

## ⚙️ Como rodar o projeto

### 1. Clonar o repositório

---

### 2. Criar ambiente virtual

```bash
python -m venv venv
```

Ativar:

```bash
# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configurar banco de dados

No arquivo `alembic.ini`, configure:

```ini
sqlalchemy.url = postgresql://usuario:senha@localhost:5432/seubanco
```

---

### 5. Rodar migrations

```bash
alembic upgrade head
```

---

### 6. Rodar o servidor

```bash
uvicorn app.main:app --reload
```

---

## 📚 Documentação da API

Acesse:

```
http://127.0.0.1:8000/docs
```

Interface interativa com Swagger.

---

## 🔐 Autenticação

Para acessar rotas protegidas:

1. Faça login
2. Copie o token JWT
3. No Swagger, clique em **Authorize**
4. Insira:

```
Bearer SEU_TOKEN
```

---

## ⚠️ Observações

* Os valores monetários utilizam `Decimal` para evitar problemas de precisão
* Migrações são controladas com Alembic
* Projeto desenvolvido com foco educacional (desafio DIO)

---

## 📌 Melhorias futuras (V3)

* Transferência entre contas
* Validação de saldo insuficiente
* Testes automatizados
* Logs estruturados

---

## 👨‍💻 Autor

Desenvolvido por **Raimundo Jr**

---

Se quiser, posso adaptar esse README pra ficar mais chamativo (com badges, prints do Swagger, etc.) ou no estilo que recrutador gosta.
