---
title: ML System
type: concept
status: draft
created: 2026-05-21
updated: 2026-05-21
domain: machine-learning
tags: [type/concept, domain/machine-learning, topic/mlops]
aliases: ["machine learning system", "sistema de ML"]
source_count: 1
related: ["[[mlops]]", "[[ml-project-lifecycle]]"]
---

# ML System

## Definicao formal

ML System e o conjunto de infraestrutura, dados, codigo, modelos, processos, cultura, ownership e operacao que leva um projeto de ML de uma ideia ate um ativo autoscalado gerando predicoes.

## Intuicao

O modelo e uma parte pequena do sistema. O sistema inclui como dados chegam, como features sao criadas, como experimentos viram codigo, como pipelines executam, como modelos sao publicados, como incidentes sao tratados e como mudancas retornam ao ciclo de desenvolvimento.

## Variantes e extensoes

- Sistema batch: previsoes sao geradas em jobs programados.
- Sistema online: modelo responde requests em tempo real.
- Sistema hibrido: features e predicoes combinam batch, streaming e serving online.
- Sistema com human in the loop: decisoes ou correcao de labels dependem de revisao humana.

## Procedimento de aplicacao

1. Mapear entradas de dados e contratos.
2. Mapear transformacoes e features.
3. Mapear training pipeline e artifact storage.
4. Mapear serving, APIs e consumidores.
5. Mapear monitoring, alerting, runbooks e ownership.
6. Registrar dependencies e pontos de rollback.

## Exemplo concreto

Um recommender system inclui coleta de eventos, ETL, feature store, treino periodico, experiment tracking, registry, serviço de inferencia, A/B testing, dashboards, alertas e processo de rollback. Sem esses componentes, existe apenas um modelo treinado, nao um ML System robusto.

## Armadilhas e erros comuns

- Desenhar arquitetura apenas ao redor do modelo.
- Ignorar contratos de dados.
- Nao documentar owners por componente.
- Nao tratar dados stateful como parte de disaster recovery.

## Sources relacionadas

- [[a-guide-to-implementing-mlops-from-data-to-operations]]

---
[[wiki/index|Voltar ao Indice]]

