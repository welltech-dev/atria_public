# PURGE_AND_REBOOT_PRIMEZA.md

## Contexto

Este documento existe para servir como:
- âncora técnica
- ponto de clareza
- referência arquitetural

Ele marca o momento em que o projeto Primeza deixa de ser apenas
"algo que funciona" e passa a ser um sistema consciente, limpo
e preparado para evoluir.

Objetivo explícito:
> Remover lixo mental, estrutural e técnico antes de escalar.

---

## Visão Geral do Sistema

O Primeza é um sistema modular, orientado a segurança, automação
e integração bancária.

Ele é composto por quatro camadas principais:

1. Interface (Frontend)
2. Lógica e Orquestração (Backend)
3. Automação Inteligente (bot_primeza)
4. Segurança e Segredos (Secrets Layer)

Cada camada deve e pode evoluir sem acoplar e comprometer as demais, porém quando precisar ter modulação clara e eficiente.

---

## 1. Frontend (Interface)

Responsabilidade:
- Coletar dados
- Apresentar informações de forma clara
- Nunca conter e/ou reter lógica sensível ou segredos dentro do sistema.

Princípios:
- Simplicidade > Estética exagerada
- Clareza > Promessa vazias
- Confiança > Impacto visual

O frontend NÃO:
- acessa APIs bancárias diretamente
- armazena tokens
- toma decisões críticas

Ele apenas inicia fluxos.

---

## 2. Backend (Orquestração)

Responsabilidade:
- Validar dados
- Orquestrar fluxos
- Mediar comunicação entre frontend, bot e serviços internos e/ou externos

Aqui vivem:
- regras de negócio
- validações
- controle de estados
- logs e rastreabilidade

O backend é o "cérebro operacional",
mas não deve conhecer segredos em texto puro.

---

## 3. bot_primeza (Automação)

Responsabilidade:
- Executar ações automatizadas
- Interagir com APIs internas e externas
- Responder eventos do sistema e anomalias dentro dele indicando arquivo, index and columns.

O bot_primeza:
- NÃO possui interface pública
- NÃO recebe input direto do usuário final
- Age somente por comandos internos controlados

Ele deve ser:
- previsível
- auditável
- isolado

---

## 4. Segurança e Segredos (Secrets Layer)

Todos os segredos do sistema vivem fora do código.

Inclui:
- credenciais bancárias
- tokens de API
- chaves sensíveis

Princípios:
- Segredo nunca em repositório
- Segredo nunca em frontend
- Segredo nunca em log

Ferramenta base:
- Arquivo KDBX (KeePass)

O sistema acessa segredos apenas quando necessário
e apenas pelo componente autorizado.

---

## Integrações Externas (APIs Bancárias)

As APIs bancárias:
- nunca são chamadas diretamente pelo frontend
- passam sempre pelo backend e por avaliação de recaptch

Ambiente:
- Sandbox primeiro
- Produção apenas com contrato, validação e rastreabilidade

Toda integração deve assumir:
> a falha é esperada, o erro deve ser controlado.

---

## O que é considerado "lixo" neste projeto

Deve ser removido sem apego:
- código duplicado
- lógica misturada
- variáveis sem propósito claro
- funcionalidades sem uso real
- complexidade que só impressiona o autor

Regra simples:
> Se não serve ao sistema descarte, ego não escala.

---

## Diretriz de Evolução

Antes de adicionar algo novo, responder:

1. Isso quebra isolamento?
2. Isso adiciona risco?
3. Isso pode ser feito mais simples?
4. Isso serve ao usuário ou só ao desenvolvedor?

Se não houver clareza, NÃO evoluir.

---

## Nota Final

Este documento não é marketing.
Não é apresentação.
Não é justificativa.

É um compromisso técnico.

Sempre que o sistema parecer confuso,
retornar aqui e limpar antes de crescer.
