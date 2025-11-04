# etl/etl_tratamento_nulos.py

"""
Tratamento de valores ausentes (NaN) nos datasets de futebol.

Objetivos:
- Analisar colunas com muitos NaN
- Preencher valores ausentes com estratégias seguras
- Gerar uma versão refinada dos datasets em data/processed_refined
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
REFINED_DIR = DATA_DIR / "processed_refined"
REFINED_DIR.mkdir(exist_ok=True)

# Caminhos
BR_PATH = PROCESSED_DIR / "brasileirao_serie_a_clean.csv"
CB_PATH = PROCESSED_DIR / "copa_brasil_clean.csv"

# Carregar
df_brasileirao = pd.read_csv(BR_PATH)
df_copa = pd.read_csv(CB_PATH)


def fill_brasileirao(df: pd.DataFrame) -> pd.DataFrame:
    """Preenche valores ausentes do Brasileirão com base em lógicas simples."""

    # 1. Datas: preenche datas faltantes aproximando pela rodada
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["data"] = df.groupby("ano_campeonato")["data"].transform(
        lambda x: x.fillna(method="ffill").fillna(method="bfill")
    )

    # 2. Públicos: substitui nulos por mediana do ano
    for col in ["publico", "publico_max"]:
        df[col] = df.groupby("ano_campeonato")[col].transform(lambda x: x.fillna(x.median()))

    # 3. Técnicos e árbitros: mantém nulos (não interfere na IA)
    # 4. Estatísticas técnicas: substitui por 0 (jogo sem registro, não significa zero real)
    cols_estat = [
        "escanteios_mandante", "escanteios_visitante", "faltas_mandante", "faltas_visitante",
        "chutes_bola_parada_mandante", "chutes_bola_parada_visitante", "defesas_mandante",
        "defesas_visitante", "impedimentos_mandante", "impedimentos_visitante",
        "chutes_mandante", "chutes_visitante", "chutes_fora_mandante", "chutes_fora_visitante"
    ]
    df[cols_estat] = df[cols_estat].fillna(0)

    return df


def fill_copa(df: pd.DataFrame) -> pd.DataFrame:
    """Preenche valores ausentes da Copa do Brasil."""
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["data"] = df.groupby("ano_campeonato")["data"].transform(
        lambda x: x.fillna(method="ffill").fillna(method="bfill")
    )

    for col in ["publico", "publico_max"]:
        df[col] = df.groupby("ano_campeonato")[col].transform(lambda x: x.fillna(x.median()))

    estat = [
        "escanteios_mandante", "escanteios_visitante", "faltas_mandante", "faltas_visitante",
        "defesas_mandante", "defesas_visitante", "chutes_mandante", "chutes_visitante"
    ]
    df[estat] = df[estat].fillna(0)

    return df


# Executar tratamento
df_brasileirao_ref = fill_brasileirao(df_brasileirao)
df_copa_ref = fill_copa(df_copa)

# Salvar versões refinadas
df_brasileirao_ref.to_csv(REFINED_DIR / "brasileirao_refinado.csv", index=False)
df_copa_ref.to_csv(REFINED_DIR / "copa_brasil_refinado.csv", index=False)

print("Tratamento concluído!")
print(f"→ {REFINED_DIR / 'brasileirao_refinado.csv'}")
print(f"→ {REFINED_DIR / 'copa_brasil_refinado.csv'}")
