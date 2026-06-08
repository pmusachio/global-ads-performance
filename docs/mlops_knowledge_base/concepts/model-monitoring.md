---
title: Model Monitoring
type: concept
status: draft
created: 2026-05-21
updated: 2026-05-21
domain: machine-learning
tags: [type/concept, domain/machine-learning, topic/monitoring]
aliases: ["monitoring de modelos", "ML monitoring"]
source_count: 1
related: ["[[mlops]]", "[[ml-system]]"]
---

# Model Monitoring

## Definicao formal

Model Monitoring e a observabilidade continua de modelos de machine learning em producao, cobrindo metricas de servico, metricas de modelo, drift de dados, degradacao de performance, erros de pipeline e gatilhos de retraining.

## Intuicao

Um modelo pode continuar respondendo requests e ainda assim estar errado. Monitoring de modelo existe para detectar quando a distribuicao de entrada, a relacao entre features e target ou a qualidade de predicao mudou.

## Metricas e sinais

- Latencia, throughput, erros, disponibilidade e saturacao.
- Distribuicao de features e outliers.
- Data drift e concept drift.
- Performance supervisionada quando labels chegam depois.
- Taxa de fallback, rejeicao, alerta humano ou override.
- Integridade de pipeline e freshness de dados.

## Procedimento de aplicacao

1. Definir metricas offline usadas no treinamento.
2. Definir proxies online quando labels atrasam.
3. Criar dashboards para servico, dados e modelo.
4. Definir thresholds e alertas acionaveis.
5. Linkar cada alerta a runbook e owner.
6. Registrar quando o alerta deve gerar rollback, retraining ou investigacao.

## Exemplo concreto

Em fraud detection, drift pode aparecer quando fraudadores mudam padrao de transacao. O modelo ainda responde em baixa latencia, mas recall cai. O monitoring precisa capturar mudanca de distribuicao, atraso de labels, aumento de falsos negativos e necessidade de retreinar.

## Armadilhas e erros comuns

- Monitorar apenas infraestrutura.
- Criar alertas sem owner.
- Usar thresholds estaticos sem considerar sazonalidade.
- Acionar retraining automatico sem validacao de dados.
- Nao registrar runbooks.

## Sources relacionadas

- [[a-guide-to-implementing-mlops-from-data-to-operations]]
- [[capitulo-01-understanding-mlops]]

---
[[wiki/index|Voltar ao Indice]]

