# 🚀 Market Intelligence & Data Engine (2024-2026)

## 📋 Sobre o Projeto
Este sistema é um ecossistema de análise financeira projetado para operar em ambientes com restrições de hardware (Debian GNU/Linux 12). O projeto evoluiu de um simples script de consulta para um **Pipeline de Dados (ETL)** completo, integrando análise fundamentalista, técnica e sentimento de mercado através de uma arquitetura resiliente.

## 🏗️ Arquitetura e Decisões de Engenharia

### 1. Camada de Ingestão (Python & APIs)
- **O quê:** Integração com Alpha Vantage para dados em tempo real.
- **Por que:** Implementamos um sistema de *throttling* (pausas controladas de 15s-35s) para respeitar o limite de 5 requisições por minuto da API gratuita, garantindo a estabilidade do pipeline sem bloqueios de credenciais.

### 2. Camada de Armazenamento (SQLite3)
- **O quê:** Banco de dados relacional leve (Serverless).
- **Por que:** Em vez de arquivos CSV voláteis, utilizamos **SQL**. Isso permitiu a persistência de dados históricos e cálculos de médias móveis, ocupando o mínimo de espaço em disco — uma restrição crítica do ambiente de desenvolvimento.

### 3. Camada de BI (Business Intelligence)
- **O quê:** Dashboard dinâmico com Chart.js.
- **Por que:** O sistema gera um comparativo visual de **Lucro Líquido vs. Custos Operacionais** (2024-2025), permitindo identificar não apenas a variação de preço, mas a eficiência real das Big Techs analisadas.



## ⚠️ Limitações Técnicas e Desafios
Como todo projeto de engenharia real, trabalhamos sob restrições:
- **API Rate Limit:** Resiliência programada para lidar com o limite de 500 chamadas diárias.
- **Granularidade Histórica:** Devido às restrições da API gratuita para dados fundamentais profundos, implementamos um motor de "conhecimento prévio" para os anos de 2024 e 2025.
- **Hardware-Friendly:** Otimizado para rodar em containers ou sistemas Linux com baixo armazenamento, evitando dependências pesadas de Machine Learning e focando em estatística aplicada.

## 🛠️ Como Operar
1. **Configuração:** Insira sua API Key no arquivo `data_engine.py`.
2. **Coleta (ETL):** Execute `python3 data_engine.py` para alimentar o banco de dados SQL.
3. **Dashboard:** Execute `python3 analise_bi.py` para gerar o arquivo `index.html` com os insights.

---
**Projeto desenvolvido para demonstração de competências em Engenharia de Dados, SQL e Automação Linux.**
