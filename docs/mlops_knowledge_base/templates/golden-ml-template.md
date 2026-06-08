---
title: Snippet: Golden ML Template
type: code-snippet
status: active
created: 2026-05-21
domain: machine-learning
source: "[[a-guide-to-implementing-mlops-from-data-to-operations]]"
source_id: SRC-0001
---

# 🏗️ Golden ML Template Structure

Extraído de *A Guide to Implementing MLOps* (Mishra, 2025, pág. 131). Este template representa uma estrutura "utópica" para projetos de Machine Learning visando reprodutibilidade e escalabilidade.

```text
.
├── .github/
│   ├── pull_request_template.md
│   ├── scripts/
│   └── workflows/
│       ├── start-training.yaml
│       └── deploy-server.yaml
├── .mlops                # Arquivo de metadados do estágio do projeto
├── .gitignore
├── .pre-commit-config.yaml
├── Makefile              # Automação de tarefas (sync, test, build)
├── README.md
├── infra-terraform/      # IaC para provisionamento de recursos
│   └── {{ app_name_snake }}.tf
├── notebooks/            # Apenas para EDA (Exploratory Data Analysis)
│   └── .gitkeep
├── .dockerignore
├── Dockerfile            # Multi-stage build com foco em caching
├── docker-compose.yaml
├── k8s-manifests/        # Manifestos Kubernetes (ArgoCD/Kustomize)
│   └── {{ app_name_dash }}/
│       ├── base/
│       └── overlays/
├── pyproject.toml        # Gerenciamento de dependências (Poetry/Pipenv)
├── src/                  # Pacote Python principal (importável)
│   └── {{ app_name_snake }}/
│       ├── app.py
│       └── settings.py
├── tests/                # Testes unitários e de integração
│   └── test_app.py
├── components/           # Componentes reutilizáveis de pipeline (YAML)
│   ├── preprocess-component.yaml
│   ├── train-component.yaml
│   ├── evaluation-component.yaml
│   └── data-validation-component.yaml
└── pipelines/            # Definição de DAGs (Kubeflow/Airflow)
    └── train-pipeline.py
```

## 💡 Princípios do Template
1. **Namespace Único:** Cada projeto deve ter seu próprio repositório para evitar colisões e facilitar o versionamento.
2. **Dockerfile Multi-stage:** Garantir que a imagem final seja enxuta e que os testes passem antes da geração do artefato.
3. **Metadados (.mlops):** O arquivo `.mlops` permite que o CI se comporte de forma diferente dependendo do estágio (ex: EDA vs. Produção).
4. **Notebooks como Artefatos:** Notebooks devem ser convertidos em módulos (`src/`) assim que a lógica de pré-processamento for finalizada.

---
[[wiki/outputs/code/README|Voltar ao Índice de Código]]
