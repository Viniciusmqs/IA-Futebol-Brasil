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


## 🛠️ Tecnologias Utilizadas

Linguagem: Python 3.10+ (testado em 3.13)

Dados: Pandas, NumPy

IA / ML: Scikit-learn

Backend: FastAPI, Uvicorn

Frontend: Streamlit, Plotly, Requests

Ambiente: VSCode, Jupyter Notebooks

## 📦 Pré-requisitos

Antes de começar, você precisa ter instalado:

Python 3.10+

Git

(Opcional) VSCode ou outro editor de código

⬇️ Clonando o repositório
git clone https://github.com/Viniciusmqs/IA-Futebol-Brasil.git
cd IA-Futebol-Brasil

## 🧬 Ambiente de Dados e Frontend (raiz)

Na raiz do projeto, crie e ative um ambiente virtual:

python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows (PowerShell)


Instale as dependências principais:

pip install -r requirements.txt
pip install streamlit requests plotly


Obs.: requirements.txt contém as bibliotecas base de dados e IA.
O comando extra garante as libs usadas no dashboard.

## 🗂️ Dados

O projeto espera encontrar os dados no diretório:

data/final/brasileirao_final.csv


Opcionalmente, você pode:

Colocar os dados brutos em data/raw/

Rodar os notebooks da pasta etl/ para recriar toda a pipeline de tratamento

Ou utilizar a base final já fornecida (se estiver versionada no repositório)

Por questões de tamanho e licença, arquivos de dados brutos podem não estar incluídos no repositório.

## 🌐 Rodando o Backend (API FastAPI)

O backend tem seu próprio ambiente virtual (recomendado).

cd backend
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows


Instale as dependências do backend:

pip install -r requirements.txt


Suba o servidor:

uvicorn app.main:app --reload


Por padrão, a API estará disponível em:

Swagger (documentação interativa):
## 👉 http://127.0.0.1:8000/docs

## 🖥️ Rodando o Frontend (Streamlit)

Com o ambiente virtual da raiz ativado:

cd IA-Futebol-Brasil        # se ainda não estiver na raiz
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows


Execute o app Streamlit:

streamlit run frontend/app.py


O dashboard ficará disponível em:

## 👉 http://localhost:8501

O que o usuário pode fazer no dashboard?

Selecionar dois times do Brasileirão

Ver estatísticas comparativas:

Jogos, vitórias, empates, derrotas

Médias de gols pró/contra

Perfil médio (chutes, escanteios, faltas, defesas)

Visualizar gráficos interativos:

Barras de gols pró/contra

Gráfico radar de desempenho

Simular uma partida com parâmetros ajustáveis:

ano, rodada, colocação na tabela

valor da equipe, idade média, capacidade do estádio

Obter a previsão de resultado com probabilidades (%) para:

vitória do mandante

empate

vitória do visitante

📊 Notebooks (ETL e Análises)

Na pasta notebooks/ e etl/ estão os arquivos usados para:

Coleta e limpeza dos dados

Criação de variáveis derivadas (resultado, flags de vitória/empate)

Tratamento de valores faltantes

Geração de análises exploratórias e gráficos (incluindo radar de times)

Treinamento e avaliação do modelo de IA

Esses notebooks são úteis para:

Entender passo a passo o pipeline de dados

Reproduzir experimentos

Apresentar o processo em contexto acadêmico

## 🔮 Próximos Passos

Testar modelos mais avançados (XGBoost, CatBoost, etc.)

Incluir variáveis contextuais: mando de campo mais detalhado, clima, deslocamento, retrospecto recente

Criar temas visuais mais “gamificados” para o dashboard

Publicar API + frontend em um serviço de nuvem (Render, Railway, etc.)

## 📚 Licença e Uso

Projeto desenvolvido para fins acadêmicos e de estudo.
Os dados utilizados são de campeonatos oficiais brasileiros e podem estar sujeitos a termos de uso das fontes originais.
