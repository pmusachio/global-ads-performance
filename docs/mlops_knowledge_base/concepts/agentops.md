---
title: AgentOps
type: concept
status: active
created: 2026-05-22
updated: 2026-05-22
domain: artificial-intelligence
tags: [type/concept, domain/artificial-intelligence, topic/agents, topic/mlops]
aliases: ["Agent Operations"]
source_count: 1
related: ["[[mlops]]", "[[ai-agent]]", "[[agent-development-kit]]"]
---

# AgentOps

**AgentOps** (Agent Operations) refere-se ao conjunto de práticas, processos e ferramentas voltados para o ciclo de vida completo de agentes de inteligência artificial, desde o desenvolvimento e teste até o deploy, monitoramento e melhoria contínua.

## Ciclo de Vida do AgentOps

De acordo com o framework do [[agent-development-kit]], o AgentOps abrange as seguintes dimensões:

### 1. Customização (Customization)
- **Segurança:** Implementação de guardrails e políticas de segurança.
- **Grounding (Aterramento):** Conectar o agente a fontes de dados proprietárias para reduzir alucinações.

### 2. Avaliação (Evaluation)
- **Dataset Generation:** Criação de cenários de teste sintéticos ou baseados em dados reais.
- **Performance Measurement:** Uso de métricas como `tool_trajectory` (corretude do fluxo) e `response_match` (qualidade semântica da resposta).

### 3. Deploy (Deployment)
- **CI/CD & Testing:** Integração de testes automatizados no pipeline de entrega.
- **Infrastructure:** Gestão do runtime (ex: [[vertex-ai-agent-engine]], Cloud Run, GKE).
- **UI Integration:** Disponibilização do agente em interfaces de usuário (Agent Starter Pack).

### 4. Observabilidade (Observability)
- Monitoramento de logs, traces e métricas de custo e latência.
- Análise do raciocínio interno do agente para depuração e otimização.

## Relação com MLOps
Enquanto o [[mlops]] foca na gestão de modelos e dados, o AgentOps estende esses conceitos para lidar com a complexidade de sistemas compostos por modelos, ferramentas e fluxos de decisão dinâmicos.

## Fontes Relacionadas

- [[techub-agent-sdk-v2]]

---
[[wiki/index|Voltar ao Indice]]
