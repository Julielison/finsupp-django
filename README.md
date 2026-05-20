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

## 📁 Estrutura de Diretórios
```text
finsupp-django/
├── requirements.txt         # Dependências do projeto
├── README.md                # Documentação
└── finsupp/                 # Raiz da aplicação Django
    ├── manage.py            # CLI do Django
    ├── pytest.ini           # Configuração de Testes (pytest)
    ├── finsupp/             # Configurações globais do projeto (settings, asgi, wsgi, urls)
    ├── accounts/            # App responsável por Autenticação, Usuários, etc.
    │   ├── forms.py
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   └── tests/           # Testes divididos por contexto
    │       ├── integration/ # Testes de fluxos e Views
    │       └── unit/        # Testes de Forms, Models e regras de negócio
    ├── categories/          # App para gerenciar categorias financeiras
    │   ├── forms.py
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   └── tests/
    │       ├── integration/
    │       └── unit/
    ├── core/                # App central / domínios principais da aplicação
    │   ├── models.py
    │   ├── views.py
    │   └── tests/
    │       ├── integration/
    │       └── unit/
    └── templates/           # Arquivos de front-end / Tailwind
        ├── auth/            # Telas do fluxo de autenticação (login, register...)
        ├── categories/      # Telas do CRUD de categorias (listagem, formulário, exclusão)
        └── core/            # Telas principais da aplicação (ex: home)
```

---

## �🔐 Módulo de Autenticação (`accounts`)

O projeto utiliza um fluxo de autenticação customizado:
- **Custom User Model:** Login via `email`.
- **Session Auth:** Autenticação baseada em sessões (substituindo JWT).
- **Redirecionamentos:** Configurados no `settings.py` (`LOGIN_REDIRECT_URL`).
- **Templates:** As views esperam templates em `accounts/` (ex: `login.html`, `signup.html`).

## 🗂️ Módulo de Categorias (`categories`)

Gerenciamento das categorias de itens financeiros.
- **CRUD Completo:** Views baseadas em classes (CreateView, ListView, UpdateView, DeleteView).
- **Associação de Usuário:** Cada usuário gerencia e visualiza apenas as suas categorias.
- **Templates:** Estão estruturados em `templates/categories/` (`category_list.html`, `category_form.html`, `category_confirm_delete.html`).
- **Navegação Integrada:** As funções estão acessíveis na home e as restrições de acesso (LoginRequiredMixin) estão implementadas.

## 🏦 Módulo de Contas Bancárias (`bank_accounts`)

Gerenciamento das contas bancárias dos usuários.
- **Campos Detalhados:** Configuração do nome da conta, banco (select predefinido), tipo (corrente, poupança, investimento), e saldo inicial.
- **Dias de Fechamento e Vencimento:** Suporte a datas de vencimento configuráveis pelo usuário (1 a 31).
- **Isolamento de Dados:** Cada usuário visualiza exclusivamente suas próprias contas.
- **CRUD Visual:** Interface elegante em Tailwind contendo lista interativa e modais consistentes com o resto da aplicação.

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

### 📊 Relatório de Cobertura (Coverage)
O projeto utiliza o pacote `pytest-cov` para analisar o percentual de código coberto pelos testes. 

Você pode rodar os testes e acompanhar no próprio terminal as linhas não cobertas:
```bash
pytest --cov=. --cov-report=term-missing
```

Ou, gerar um relatório visual HTML interativo:
```bash
pytest --cov=. --cov-report=html
```
Um diretório `htmlcov/` será criado com um arquivo `index.html`. Abra-o no navegador e veja detalhadamente todos os arquivos e linhas de códigos que estão ou não cobertos.