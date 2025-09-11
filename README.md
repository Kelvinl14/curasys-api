# CuraSys API 🏥

API RESTful para gerenciamento de hospital (pacientes, médicos, consultas e exames).

---

## 🚀 Endpoints

### 🔑 Autenticação
- `POST /auth/login` → autentica usuário e retorna JWT
- `GET /auth/secure-jwt` → rota protegida com JWT
- `GET /auth/secure-apikey` → rota protegida com API Key

> **Headers:**
> - JWT → `Authorization: <token>`
> - API Key → `x-api-key: 1234567890abcdef`

---

### 👤 Pacientes
- `GET /pacientes` → lista pacientes
- `POST /pacientes` → cria paciente
- `GET /pacientes/:id` → detalha paciente
- `PUT /pacientes/:id` → atualiza paciente
- `DELETE /pacientes/:id` → remove paciente

---

### 🧑‍⚕️ Médicos
- `GET /medicos` → lista médicos
- `POST /medicos` → cria médico
- `GET /medicos/:id` → detalha médico
- `PUT /medicos/:id` → atualiza médico
- `DELETE /medicos/:id` → remove médico

---

### 📅 Consultas
- `GET /consultas` → lista consultas
- `POST /consultas` → cria consulta
- `GET /consultas/:id` → detalha consulta
- `PUT /consultas/:id` → atualiza consulta
- `DELETE /consultas/:id` → remove consulta
- `GET /consultas/paciente/:id_paciente` → lista consultas de um paciente
- `GET /consultas/medico/:id_medico` → lista consultas de um médico

---

### 🧾 Exames
- `GET /exames` → lista exames
- `POST /exames` → cria exame
- `GET /exames/:id` → detalha exame
- `PUT /exames/:id` → atualiza exame
- `DELETE /exames/:id` → remove exame

---

### 👥 Usuários
- `GET /usuarios` → lista usuários
- `POST /usuarios` → cria usuário
- `GET /usuarios/:id` → detalha usuário
- `PUT /usuarios/:id` → atualiza usuário
- `DELETE /usuarios/:id` → remove usuário


---

## 🛠 Como rodar a API

Instale as dependências:
```bash
pip install -r requirements.txt
python -m backend.app
```
API disponível em:
- http://127.0.0.1:5000

___

## 💾 Banco de Dados
Inicializar o banco:
```bash
python backend/init_db.py
```
Resetar o banco (apaga e recria)
```bash
python backend/reset_db.py
```

___

## 🧪 Testes Automatizados (pytest)
Os testes validam POST, GET, PUT e DELETE para pacientes, médicos e consultas.

Rodar todos os testes:
```bash
pytest -v
```

Rodar apenas um módulo de teste:
```bash
pytest backend/tests/test_api/test_pacientes.py -v
```

Se quiser garantir banco limpo antes de rodar os testes:
```bash
python backend/reset_db.py && pytest -v
```

___

## 📂 Estrutura do projeto

```bash
CuraSys/
backend/
│── app.py                # Ponto de entrada principal da aplicação
│── database.py           # Conexão com o banco de dados
│── init_db.py            # Script para inicializar o banco
│── reset_db.py           # Script para resetar o banco
│── hospital.db           # Banco SQLite
│── requirements.txt      # Dependências
│── README.md             # Documentação
│── __init__.py
│
├── src/
│   ├── blueprints/
│   │   └── routes/       # Rotas organizadas por domínio
│   │       ├── auth.py
│   │       ├── consultas.py
│   │       ├── exames.py
│   │       ├── medicos.py
│   │       ├── pacientes.py
│   │       ├── usuarios.py
│   │       └── __init__.py
│   │
│   ├── models/           # Modelos (ainda vazio)
│   │   └── __init__.py
│   │
│   ├── utils/
│   │   ├── logs.py       # Utilitário para logging
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── tests/
│   ├── conftest.py
│   ├── test_api/         # Testes separados por domínio
│   │   ├── test_consultas.py
│   │   ├── test_exames.py
│   │   ├── test_medicos.py
│   │   ├── test_pacientes.py
│   │   ├── test_usuarios.py
│   │   └── __init__.py
│   └── __init__.py


```
___

## 📌 Exemplos de requisições (curl)
### 🔹 Pacientes
Criar paciente:

```bash
bash

curl -X POST http://127.0.0.1:5000/pacientes \
-H "Content-Type: application/json" \
-d '{
  "nome": "João Silva",
  "data_nascimento": "1980-05-01",
  "cpf": "12345678900",
  "telefone": "(85) 99999-9999",
  "email": "joao@email.com"
}'
```

Listar pacientes:
```bash
bash

curl http://127.0.0.1:5000/pacientes
```

Atualizar paciente (id=1):
```bash
bash 

curl -X PUT http://127.0.0.1:5000/pacientes/1 \
-H "Content-Type: application/json" \
-d '{
  "nome": "João Silva Atualizado",
  "data_nascimento": "1980-05-01",
  "cpf": "98765432100",
  "telefone": "(85) 98888-8888",
  "email": "joao.novo@email.com"
}'
```
Deletar paciente (id=1):
```bash
bash 

curl -X DELETE http://127.0.0.1:5000/pacientes/1
```

___
