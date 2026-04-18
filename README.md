# Átria – Multi-Tenant Financial Backend

Sistema backend modular com arquitetura multi-tenant, foco em segurança e simulação de fluxo financeiro completo.

---

## 🇧🇷 Português

### Visão geral

O Átria é um backend desenvolvido com foco em cenários reais de mercado, projetado para suportar múltiplos clientes (multi-tenant), com arquitetura escalável, segura e organizada.

O projeto vai além de aplicações CRUD simples, simulando fluxos financeiros completos e aplicando boas práticas de engenharia de software desde a base.

---

### Principais características

* Arquitetura multi-tenant com conexão dinâmica por cliente
* Simulação de fluxo de pagamentos com estados controlados
* Processamento determinístico e auditável
* Estrutura modular inspirada em clean architecture
* Integração entre backend e frontend para validação de fluxo

---

### Segurança

* Proteção contra CSRF
* Validação de entradas
* Prevenção contra SQL Injection
* Uso de CAPTCHA contra força bruta
* Centralização das regras de segurança

---

### Estrutura do projeto

```
core/
 ├── adapters      # integrações externas (simulação de banco, gateways)
 ├── automation    # lógica de automação
 ├── config        # configuração da aplicação
 ├── db            # conexões e multi-tenant
 ├── models        # entidades de domínio
 ├── repositories  # acesso a dados
 ├── routes        # endpoints HTTP
 ├── security      # segurança centralizada
 ├── services      # regras de negócio
 └── utils         # utilitários
```

---

### Simulação de fluxo

O sistema simula um ciclo completo de transações financeiras, incluindo:

* aprovação
* rejeição
* comportamento suspeito
* timeout

As respostas são estruturadas em JSON, representando integrações externas reais.

---

### Tecnologias

* Python
* Flask
* PostgreSQL (em uso real)
* JavaScript (Vanilla)
* HTML / CSS
* Linux

---

### O que este projeto demonstra

* Construção de backend escalável
* Implementação de multi-tenant
* Aplicação de segurança em múltiplas camadas
* Organização de código para manutenção e crescimento
* Tradução de regras de negócio em arquitetura

---

### Como executar

> Nota: versão pública simplificada. Algumas configurações foram abstraídas.

---

### Autor

Wellington Pereira da Silva
Desenvolvedor com foco em backend, arquitetura, segurança e sistemas escaláveis.

---

## 🇺🇸 English

# Átria – Multi-Tenant Financial Backend

A backend system designed with real market vision, focused on building secure, modular and scalable financial operations in a multi-tenant environment.

This project demonstrates how to structure a complete backend from scratch, applying architecture principles, security practices and real-world problem solving beyond basic CRUD applications.

Átria simulates a financial system capable of handling multiple tenants, processing transaction flows and maintaining data integrity with a clear separation of responsibilities across the codebase.

The system was built with a strong focus on:

- Multi-tenant architecture using dynamic database connections
- Payment flow simulation with controlled transaction states
- Security-first design (CSRF protection, input validation, CAPTCHA, SQL injection prevention)
- Modular structure inspired by clean architecture principles
- Deterministic and auditable processing
- Full backend and frontend integration for flow validation

The project structure is organized to reflect real production patterns:

core/
- adapters: external integrations (bank simulation, gateways)
- automation: messaging and automation logic
- config: application configuration
- db: connection handling and tenant management
- models: domain entities
- repositories: data access layer
- routes: HTTP endpoints
- security: centralized security logic
- services: business rules and processing
- utils: shared utilities

The application simulates a full transaction lifecycle, including scenarios such as approval, rejection, suspicious behavior and timeout, using structured JSON responses to represent external systems.

Technologies used:

- Python
- Flask
- PostgreSQL (architecture-ready)
- JavaScript (Vanilla)
- HTML / CSS
- Linux environment

This repository represents a public version of a larger private system and is intended to showcase technical decision-making, system design and implementation strategy.

It highlights the ability to:

- Design scalable backend systems
- Implement multi-tenant solutions
- Apply security best practices
- Structure maintainable and extensible codebases
- Translate real-world problems into modular solutions

To run locally:

git clone https://github.com/welltech-dev/atria_public.git
cd atria_public
pip install -r requirements.txt
python app.py

Note: This is a simplified public version. Some environment-specific configurations are intentionally abstracted.

Author:

Wellington Pereira da Silva

Backend-focused developer with emphasis on architecture, security and scalable system design.
