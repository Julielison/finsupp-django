# FinSupp - Monólito Django (Módulo de Autenticação)

Este projeto é um monólito fullstack utilizando Django, refatorado de uma arquitetura anterior Spring/Next.js. Este módulo foca na base de autenticação robusta utilizando sessões nativas do Django.

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para configurar o ambiente e iniciar a aplicação.

### 1. Pré-requisitos
* Python 3.12+
* No Ubuntu, é necessário o pacote `python3-venv`:
  ```bash
  sudo apt update && sudo apt install python3.12-venv -y
  ```

### 2. Configuração do Ambiente Virtual
Crie e ative o ambiente para isolar as dependências:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalação de Dependências
Instale o Django e as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

### 4. Configuração do Banco de Dados
Gere e aplique as migrações (incluindo o Custom User Model):
```bash
cd finsupp
python manage.py makemigrations accounts
python manage.py migrate
```

### 5. Criação de Superusuário (Admin)
Crie um usuário para acessar o painel administrativo:
```bash
python manage.py createsuperuser
```
*Lembre-se: O login utiliza **E-mail** em vez de username.*

### 6. Iniciando o Servidor
```bash
python manage.py runserver
```
Acesse em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔐 Módulo de Autenticação (`accounts`)

O projeto utiliza um fluxo de autenticação customizado:
- **Custom User Model:** Login via `email`.
- **Session Auth:** Autenticação baseada em sessões (substituindo JWT).
- **Redirecionamentos:** Configurados no `settings.py` (`LOGIN_REDIRECT_URL`).
- **Templates:** As views esperam templates em `accounts/` (ex: `login.html`, `signup.html`).

## 🛠️ Comandos Úteis
- **Acessar Admin:** `/admin`

### 🧪 Executando Testes
Os testes da aplicação foram separados por conceito em diretórios específicos:
- **Testes Unitários:** Concentram-se na validação de *Models*, *Services*, *Serializers* e *Forms*.
- **Testes de Integração:** Concentram-se na validação dos *Views*, chamadas ao banco de dados e fluxos de navegação.

Para rodar **todos os testes**, na raiz do projeto ou dentro de `finsupp/`:
```bash
pytest
```

Para rodar **apenas os testes unitários**:
```bash
pytest finsupp/*/tests/unit/
```

Para rodar **apenas os testes de integração**:
```bash
pytest finsupp/*/tests/integration/
```