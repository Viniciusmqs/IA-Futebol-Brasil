# ⚽ IA Futebol Brasil

Sistema de **análise estatística** e **previsão de resultados** do Campeonato Brasileiro Série A, utilizando **dados históricos reais**, **modelos de Machine Learning** e uma interface interativa para comparação entre times e simulação de partidas.

Projeto desenvolvido para a disciplina de **Inteligência Artificial**, com foco em aplicação prática de ciência de dados, aprendizado de máquina e desenvolvimento web.

---

## 🚀 Visão Geral

O IA Futebol Brasil é composto por três grandes camadas:

1. **ETL & Dados**  
   - Coleta, limpeza e transformação de dados históricos do Brasileirão (2003–2024).
   - Geração de uma base consolidada e refinada para uso em IA.

2. **Inteligência Artificial (Machine Learning)**  
   - Modelo de classificação que prevê o resultado da partida:
     - Vitória do mandante
     - Empate
     - Vitória do visitante

3. **Aplicação (API + Dashboard)**  
   - API REST em **FastAPI** para servir o modelo.
   - Dashboard interativo em **Streamlit**, onde o usuário escolhe times, vê estatísticas e simula resultados.

---

## 🧱 Arquitetura do Projeto

```text
ia-futebol-brasil/
│
├── data/
│   ├── raw/           # dados brutos (CSV originais)
│   ├── processed/     # dados intermediários
│   └── final/         # base refinada pronta para a IA (brasileirao_final.csv)
│
├── etl/               # notebooks de tratamento e análise de dados
│
├── backend/           # API FastAPI
│   └── app/
│       ├── main.py        # ponto de entrada da API
│       ├── models/        # modelos Pydantic (schemas de entrada/saída)
│       ├── services/      # regras de negócio (previsão, comparação de times)
│       └── utils/         # carregamento de modelo e dados
│
├── frontend/
│   └── app.py         # dashboard em Streamlit
│
├── notebooks/         # exploração e experimentação (dados/IA)
├── requirements.txt   # dependências do ambiente principal (dados + frontend)
└── README.md
