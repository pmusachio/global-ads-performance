---
title: MLOps
type: concept
status: draft
created: 2026-05-21
updated: 2026-05-21
domain: machine-learning
tags: [type/concept, domain/machine-learning, topic/mlops]
aliases: ["machine learning operations", "ML operations"]
source_count: 1
related: ["[[ml-system]]", "[[ml-project-lifecycle]]", "[[model-monitoring]]"]
---

# MLOps

## Definicao formal

MLOps e o conjunto de praticas, processos e plataformas que conecta desenvolvimento de modelos de machine learning a operacao confiavel em producao, combinando DevOps, software engineering, data engineering, model evaluation, deployment, monitoring e retraining.

## Intuicao

Um modelo treinado e apenas um artefato. Um produto de ML precisa de dados versionados, codigo testado, pipeline reproduzivel, deploy controlado, observabilidade, rollback, ownership e processo de atualizacao. MLOps e a disciplina que torna esse conjunto operavel.

## Metricas de Maturidade Operacional

Para avaliar a saude de uma iniciativa de MLOps, utilize os seguintes indicadores extraidos do Capítulo 3 de Mishra:

| Categoria | Metrica | Descricao |
| :--- | :--- | :--- |
| **Velocidade** | *Average Time to Production* | Tempo medio da ideia ate o primeiro serving real. |
| **Velocidade** | *Experiment Iteration Time* | Tempo gasto em cada ciclo de experimentacao. |
| **Estabilidade** | *Workflow Failures per Month* | Numero de falhas em pipelines de treino/deploy. |
| **Estabilidade** | *Time to Recover from Disaster* | Tempo de recuperacao em caso de falha critica. |
| **Eficiencia** | *Resource Reuse Rate* | Proporcao de componentes e dados reutilizados. |
| **Eficiencia** | *Time to start EDA* | Tempo para iniciar analise com novos dados. |

## Golden ML Template (Estrutura Recomendada)

Um template padronizado reduz o *time-to-market* e garante conformidade. Estrutura tipica de repositorio:

```text
project-root/
├── src/                # Codigo fonte modular (nao apenas notebooks)
├── notebooks/          # Experimentacao e EDA (limpar antes de commit)
├── pipelines/          # Definicao de DAGs (Kubeflow, Airflow, Vertex)
├── components/         # Componentes de pipeline reutilizaveis
├── manifests/          # Configuracoes K8s/GitOps
├── infra/              # Terraform/IaC para recursos especificos
├── tests/              # Testes unitarios e de integracao
├── Dockerfile          # Multi-stage build otimizado
├── requirements.txt    # Gestao de dependencias
└── .pre-commit-config.yaml # Linting e seguranca automatizada
```

## Componentes tecnicos

- Version control para codigo, dados, modelos, features e configuracoes.
- Automation para preprocessing, training, deployment, retraining e maintenance.
- Testing para unidade, integracao, smoke, edge cases e readiness.
- [[model-monitoring]] para performance, drift, saude de servico e alertas.
- Collaboration entre data scientists, ML engineers, software engineers, SREs e negocio.
- Scalability vertical e horizontal para dados, treinamento e inferencia.

## Procedimento de aplicacao

1. Classificar o projeto dentro de um [[ml-project-lifecycle]].
2. Definir ownership tecnico e de negocio.
3. Versionar entradas, transformacoes, modelos e artefatos.
4. Automatizar treinamento, testes, build, deploy e rollback.
5. Monitorar metricas de servico e metricas de modelo.
6. Criar gatilhos de retraining e runbooks de incidente.
7. Revisar maturidade continuamente.

## Exemplo concreto

Em um sistema de predicao de churn, MLOps exige que a equipe saiba qual versao do dataset gerou a versao atual do modelo, quais features foram usadas, como o modelo foi validado, qual pipeline fez deploy, quais dashboards indicam drift e quem atua quando a taxa de falsos positivos cresce.

## Armadilhas e erros comuns

- Usar MLflow, Kubeflow ou Airflow sem definir processo e ownership.
- Fazer deploy de modelo sem monitoring de dados e performance.
- Versionar apenas codigo, deixando dados e modelos sem lineage.
- Misturar experimentacao de notebook com codigo de producao sem revisao.
- Medir sucesso apenas por metrica offline.

## Quando usar

- Modelos precisam ir para producao e receber trafego real.
- Ha necessidade de compliance, reproducibility, rollback ou auditoria.
- Dados mudam com frequencia e exigem retraining.
- Varias equipes colaboram no mesmo produto de ML.

## Quando evitar

- Experimentos exploratorios sem intencao de producao.
- Prototipos descartaveis onde custo operacional nao se justifica.
- Analises pontuais que nao geram modelo servindo previsoes.

## Sources relacionadas

- [[a-guide-to-implementing-mlops-from-data-to-operations]]
- [[capitulo-01-understanding-mlops]]

---
[[wiki/index|Voltar ao Indice]]

