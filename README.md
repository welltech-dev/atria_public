# Atria – Multi-Tenant Financial Backend

A backend system designed with real market vision, focused on building secure, modular and scalable financial operations in a multi-tenant environment.

This project demonstrates how to structure a complete backend from scratch, applying architecture principles, security practices and real-world problem solving beyond basic CRUD applications.

Atria simulates a financial system capable of handling multiple tenants, processing transaction flows and maintaining data integrity with a clear separation of responsibilities across the codebase.

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
