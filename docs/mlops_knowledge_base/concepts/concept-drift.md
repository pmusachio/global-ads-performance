---
title: Concept Drift
type: concept
status: active
created: 2026-05-22
updated: 2026-05-22
domain: machine-learning
tags: [type/concept, domain/machine-learning, topic/mlops, topic/monitoring]
aliases: ["Deriva de Conceito"]
source_count: 1
related: ["[[mlops]]", "[[model-monitoring]]"]
---

# Concept Drift (Deriva de Conceito)

O **Concept Drift** refere-se ao fenômeno em que as propriedades estatísticas da variável alvo, que o modelo está tentando prever, mudam ao longo do tempo de maneiras imprevistas.

## Impacto
O drift faz com que as predições do modelo deixem de fazer sentido ou percam acurácia drasticamente, pois o modelo foi treinado em uma realidade (dados históricos) que não representa mais o presente.

## Causas Comuns
- Mudanças sazonais ou súbitas no comportamento do consumidor (ex: Pandemia).
- Alterações em processos externos (ex: novas leis ou sensores trocados).

## Mitigação no MLOps
Dentro de um pipeline de **[[mlops]]**, a detecção de concept drift é um gatilho essencial para:
1.  Alertar a equipe técnica.
2.  Disparar o processo automático de **retreinamento** do modelo com dados mais recentes.

## Fontes Relacionadas

- [[puc-engenharia-sistemas-inteligentes]]

---
[[wiki/index|Voltar ao Indice]]
