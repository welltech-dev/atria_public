# Arquitetura Modular em Flask — Refatoração e Organização do Projeto #

# Projeto Flask — Arquitetura Modular

## Visão Geral

Este projeto passou por um processo de refatoração com foco em:

* Separação de responsabilidades
* Redução de acoplamento
* Eliminação de importações circulares
* Organização modular escalável

O objetivo principal foi transformar o `app.py` de um **monolito funcional** em um **orquestrador da aplicação**.

---

## Problema Inicial

O `app.py` concentrava múltiplas responsabilidades:

* Rotas (HTTP)
* Segurança (login_required, CSRF)
* Banco de dados
* Regras de negócio
* Configuração da aplicação

Isso resultava em:

* Código difícil de manter
* Alto acoplamento
* Risco de erros estruturais
* Baixa escalabilidade

---

## Estrutura Atual do Projeto

```
/core
│
├── config/
│   └── config.py              # conexão com banco
│
├── security/
│   └── security.py            # autenticação e CSRF
│
├── services/
│   └── payment_service.py     # regras de negócio
│
├── routes/
│   ├── auth_routes/
│   │   └── auth_routes.py     # login, register, logout
│   │
│   └── system_routes.py       # captcha, salvar_cliente
│
app.py                         # bootstrap da aplicação
```

---

## Separação de Responsabilidades

### Segurança

Arquivo: `core/security/security.py`

Responsável por:

* `login_required`
* Proteção CSRF
* Validação de requisições POST
* Injeção de token CSRF nos templates

---

### 🗄️ Banco de Dados

Arquivo: `core/config/config.py`

Responsável por:

* `get_connection`
* `get_tenant_connection`

---

### ⚙️ Regras de Negócio

Arquivo: `core/services/payment_service.py`

Responsável por:

* `process_payment`

Regra aplicada:

> Tudo que não é rota nem infraestrutura → vira service

---

### 🌐 Rotas

#### `auth_routes.py`

* `/login`
* `/register`
* `/logout`

#### `system_routes.py`

* `/captcha`
* `/captcha-verify`
* `/salvar_cliente`

---

## app.py (Estado Atual)

O `app.py` agora é responsável apenas por:

* Criar a aplicação Flask
* Configurar sessão
* Registrar blueprints
* Registrar hooks globais (CSRF)

### Exemplo simplificado:

```python
from flask import Flask
from datetime import timedelta

from core.routes.auth_routes import auth_routes
from core.routes.system_routes import system_bp
from core.security.security import csrf_protect, inject_csrf

app = Flask(__name__)
app.secret_key = SECRET_KEY

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=2)

app.register_blueprint(auth_routes.auth_bp)
app.register_blueprint(system_bp)

app.before_request(csrf_protect)
app.context_processor(inject_csrf)
```

---

## Limpeza Realizada

Removido do `app.py`:

* ❌ Lógica de segurança
* ❌ Conexão com banco
* ❌ Regras de negócio
* ❌ Rotas secundárias
* ❌ Código duplicado (`app` recriado)

Mantido:

* ✅ Inicialização
* ✅ Configuração
* ✅ Registro de módulos

---

## Problemas Corrigidos

### Instância duplicada do Flask

```python
app = Flask(__name__)
...
app = Flask(__name__)  # removido
```

---

### Blueprint duplicado

```python
auth_bp = Blueprint("auth", __name__)  # removido do app.py
```

---

### Uso incorreto de @app.route fora do app

* Problema: dependência direta da instância `app`
* Solução correta: uso de **Blueprints**

---

## Decisões Técnicas

### CAPTCHA

* Mantido dentro de `routes`
* Não transformado em service

Motivo:

* Lógica simples
* Não reutilizável
* Sem complexidade suficiente

---

## Padrões Adotados

### Separação por camadas

| Camada   | Responsabilidade        |
| -------- | ----------------------- |
| routes   | entrada HTTP            |
| services | regras de negócio       |
| config   | infraestrutura          |
| security | autenticação e proteção |

---

### Boas práticas aplicadas

* Single Responsibility Principle (SRP)
* Modularização por domínio
* Evitar import circular
* Código desacoplado
* Organização escalável

---

## Estado Atual

* Aplicação funcional
* Sem erros estruturais
* Código modularizado
* Base pronta para crescimento

---

## Próximos Passos

* Externalizar configurações (`.env`)
* Modularizar extensões (Limiter)
* Implementar logging estruturado
* Evoluir CAPTCHA (expiração, tentativas)

---

## Conclusão

O projeto evoluiu de um modelo monolítico para uma arquitetura modular.

O `app.py` agora atua como:

> Orquestrador da aplicação

Isso proporciona:

* Melhor manutenção
* Maior clareza
* Facilidade de expansão
* Estrutura profissional


Belo Horizonte-MG 25 de Março de 2026
welltech-dev