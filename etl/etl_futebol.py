# etl/etl_futebol.py

"""
ETL dos dados de Brasileirão Série A e Copa do Brasil.

Fluxo geral:
- Leitura dos arquivos .csv.gz em data/raw
- Limpeza e padronização de tipos
- Criação de colunas derivadas básicas (resultado, pontos, flags)
- Gravação de arquivos tratados em data/processed
"""

from pathlib import Path
import pandas as pd


# Caminhos base
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


# Nomes dos arquivos de origem
BRASILEIRAO_RAW = "mundo_transfermarkt_competicoes_brasileirao_serie_a.csv.gz"
COPA_RAW = "mundo_transfermarkt_competicoes_copa_brasil.csv.gz"


def to_numeric_safe(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Converte colunas para numéricas de forma segura.
    Se a coluna não existir, ignora.
    """
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def add_resultado_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria colunas de resultado e pontos a partir de gols_mandante e gols_visitante.

    - resultado: "mandante", "empate", "visitante"
    - pontos_mandante, pontos_visitante: 3, 1 ou 0
    """
    if "gols_mandante" not in df.columns or "gols_visitante" not in df.columns:
        return df

    df["resultado"] = None

    mandante_vence = df["gols_mandante"] > df["gols_visitante"]
    visitante_vence = df["gols_mandante"] < df["gols_visitante"]
    empate = df["gols_mandante"] == df["gols_visitante"]

    df.loc[mandante_vence, "resultado"] = "mandante"
    df.loc[visitante_vence, "resultado"] = "visitante"
    df.loc[empate, "resultado"] = "empate"

    # Pontos na lógica padrão de 3 pontos
    df["pontos_mandante"] = 0
    df["pontos_visitante"] = 0

    df.loc[mandante_vence, "pontos_mandante"] = 3
    df.loc[visitante_vence, "pontos_visitante"] = 3
    df.loc[empate, ["pontos_mandante", "pontos_visitante"]] = 1

    # Flags numéricas úteis para modelos
    df["mandante_venceu"] = mandante_vence.astype(int)
    df["visitante_venceu"] = visitante_vence.astype(int)
    df["empate_flag"] = empate.astype(int)

    return df


def clean_common_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpeza comum para ambos os campeonatos:
    - data em formato datetime
    - ano_campeonato numérico
    - conversão de colunas numéricas básicas
    """
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce", dayfirst=True)

    if "ano_campeonato" in df.columns:
        df["ano_campeonato"] = pd.to_numeric(df["ano_campeonato"], errors="coerce").astype("Int64")

    # Colunas numéricas comuns
    numeric_common = [
        "publico",
        "publico_max",
        "gols_mandante",
        "gols_visitante",
        "gols_1_tempo_mandante",
        "gols_1_tempo_visitante",
        "escanteios_mandante",
        "escanteios_visitante",
        "faltas_mandante",
        "faltas_visitante",
        "chutes_bola_parada_mandante",
        "chutes_bola_parada_visitante",
        "defesas_mandante",
        "defesas_visitante",
        "impedimentos_mandante",
        "impedimentos_visitante",
        "chutes_mandante",
        "chutes_visitante",
        "chutes_fora_mandante",
        "chutes_fora_visitante",
        "valor_equipe_titular_mandante",
        "valor_equipe_titular_visitante",
        "idade_media_titular_mandante",
        "idade_media_titular_visitante",
    ]

    df = to_numeric_safe(df, numeric_common)

    return df


def etl_brasileirao() -> pd.DataFrame:
    """
    Faz o ETL específico do Brasileirão Série A.
    Retorna o DataFrame tratado.
    """
    path = RAW_DIR / BRASILEIRAO_RAW
    print(f"Lendo Brasileirão de {path}...")
    df = pd.read_csv(path, compression="gzip")

    # Limpeza comum
    df = clean_common_columns(df)

    # Colunas numéricas específicas do Brasileirão
    numeric_brasileirao = [
        "rodada",
        "colocacao_mandante",
        "colocacao_visitante",
    ]
    df = to_numeric_safe(df, numeric_brasileirao)

    # Resultado e pontos
    df = add_resultado_columns(df)

    # Ordenação básica por ano, rodada, data
    sort_cols = [c for c in ["ano_campeonato", "rodada", "data"] if c in df.columns]
    if sort_cols:
        df = df.sort_values(sort_cols).reset_index(drop=True)

    # Salva versão tratada
    out_path = PROCESSED_DIR / "brasileirao_serie_a_clean.csv"
    df.to_csv(out_path, index=False)
    print(f"Brasileirão tratado salvo em {out_path}")

    return df


def etl_copa_brasil() -> pd.DataFrame:
    """
    Faz o ETL específico da Copa do Brasil.
    Retorna o DataFrame tratado.
    """
    path = RAW_DIR / COPA_RAW
    print(f"Lendo Copa do Brasil de {path}...")
    df = pd.read_csv(path, compression="gzip")

    # Limpeza comum
    df = clean_common_columns(df)

    # Colunas numéricas específicas da Copa do Brasil
    numeric_copa = [
        "penalti",
        "gols_penalti_mandante",
        "gols_penalti_visitante",
    ]
    df = to_numeric_safe(df, numeric_copa)

    # Resultado e pontos
    df = add_resultado_columns(df)

    # Ordenação básica por ano, fase, data
    sort_cols = [c for c in ["ano_campeonato", "fase", "data"] if c in df.columns]
    if sort_cols:
        df = df.sort_values(sort_cols).reset_index(drop=True)

    # Salva versão tratada
    out_path = PROCESSED_DIR / "copa_brasil_clean.csv"
    df.to_csv(out_path, index=False)
    print(f"Copa do Brasil tratada salva em {out_path}")

    return df


def run_all_etl() -> None:
    """
    Executa o ETL para todos os campeonatos.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df_brasileirao = etl_brasileirao()
    df_copa = etl_copa_brasil()

    print()
    print("Resumo rápido:")
    print(f"Brasileirão Série A: {len(df_brasileirao)} partidas tratadas")
    print(f"Copa do Brasil: {len(df_copa)} partidas tratadas")


if __name__ == "__main__":
    run_all_etl()
