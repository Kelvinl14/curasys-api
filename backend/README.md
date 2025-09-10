# CuraSys API 🏥

API RESTful para gerenciamento de hospital (pacientes, médicos, consultas e exames).

---

## 🚀 Endpoints

### Pacientes
- `GET /pacientes` → lista pacientes
- `POST /pacientes` → cria paciente
- `GET /pacientes/:id` → detalha paciente
- `PUT /pacientes/:id` → atualiza paciente
- `DELETE /pacientes/:id` → remove paciente

### Médicos
- `GET /medicos`
- `POST /medicos`
- `GET /medicos/:id`
- `PUT /medicos/:id`
- `DELETE /medicos/:id`

### Consultas
- `GET /consultas?paciente_id=&medico_id=&data=`
- `POST /consultas`
- `PUT /consultas/:id`
- `DELETE /consultas/:id`

### Exames
- `GET /exames?paciente_id=`
- `POST /exames`
- `GET /exames/:id`

### Autenticação
- `POST /auth/login` → retorna token JWT fake (MVP)

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