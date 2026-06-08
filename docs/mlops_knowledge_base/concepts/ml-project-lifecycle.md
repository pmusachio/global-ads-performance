---
title: ML Project Lifecycle
type: concept
status: draft
created: 2026-05-21
updated: 2026-05-21
domain: machine-learning
tags: [type/concept, domain/machine-learning, topic/mlops]
aliases: ["machine learning project lifecycle", "ciclo de vida de projeto ML", "Helix ML lifecycle"]
source_count: 1
related: ["[[mlops]]", "[[ml-system]]"]
---

# ML Project Lifecycle

## Definicao formal

ML Project Lifecycle e a classificacao operacional dos estados pelos quais um projeto de machine learning passa, com expectativas e automacoes diferentes em cada etapa.

## Intuicao

A pergunta "em que estagio esta o projeto?" muda a decisao tecnica correta. Um projeto em exploratory data analysis precisa de liberdade; um modelo em production precisa de testes, alertas, runbooks, ownership e controles de mudanca.

## Estados identificados na fonte

- Exploratory Data Analysis.
- Under Development.
- Deployed in Development Environment.
- Deployed in Production Environment.
- Under Maintenance.
- Archived.

## Procedimento de aplicacao

1. Registrar o estado do projeto em metadado versionado, por exemplo um arquivo `.mlops`.
2. Associar automacoes a cada estado.
3. Bloquear mudancas incompativeis com o estado atual.
4. Revisar estado em cada decisao de arquitetura, deploy e retraining.

## Exemplo concreto

Durante EDA, notebooks podem ser sincronizados diariamente e usados para iteracao. Em producao, o mesmo projeto precisa de unit tests, integration tests, dashboards, alertas, runbooks e production readiness review.

## Armadilhas e erros comuns

- Aplicar rigor de producao cedo demais e matar exploracao.
- Levar codigo exploratorio diretamente para deploy.
- Tratar manutencao como fim do projeto, quando retraining inicia novo ciclo.
- Arquivar sistema removendo recursos stateless sem preservar artefatos stateful necessarios para lineage.

## Sources relacionadas

- [[a-guide-to-implementing-mlops-from-data-to-operations]]
- [[capitulo-01-understanding-mlops]]

---
[[wiki/index|Voltar ao Indice]]

