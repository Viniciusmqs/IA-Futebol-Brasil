from functools import lru_cache
from pathlib import Path
import pandas as pd

def _get_root_dir() -> Path:
    # este arquivo está em backend/app/utils
    backend_dir = Path(__file__).resolve().parents[2]  # .../backend
    root_dir = backend_dir.parent                      # .../ia-futebol-brasil
    return root_dir

@lru_cache
def carregar_df_brasileirao() -> pd.DataFrame:
    root_dir = _get_root_dir()
    data_path = root_dir / "data" / "final" / "brasileirao_final.csv"
    df = pd.read_csv(data_path)
    return df

def _construir_base_times(df: pd.DataFrame) -> pd.DataFrame:
    # mesma lógica do notebook 05
    mandante = pd.DataFrame({
        "time": df["time_mandante"],
        "adversario": df["time_visitante"],
        "casa_fora": "casa",
        "ano_campeonato": df["ano_campeonato"],
        "gols_pro": df["gols_mandante"],
        "gols_contra": df["gols_visitante"],
        "chutes_pro": df["chutes_mandante"],
        "chutes_contra": df["chutes_visitante"],
        "escanteios_pro": df["escanteios_mandante"],
        "escanteios_contra": df["escanteios_visitante"],
        "faltas_pro": df["faltas_mandante"],
        "faltas_contra": df["faltas_visitante"],
        "defesas_pro": df["defesas_mandante"],
        "defesas_contra": df["defesas_visitante"],
        "vitoria": (df["mandante_venceu"] == 1).astype(int),
        "empate": (df["empate_flag"] == 1).astype(int),
        "derrota": (df["visitante_venceu"] == 1).astype(int),
    })

    visitante = pd.DataFrame({
        "time": df["time_visitante"],
        "adversario": df["time_mandante"],
        "casa_fora": "fora",
        "ano_campeonato": df["ano_campeonato"],
        "gols_pro": df["gols_visitante"],
        "gols_contra": df["gols_mandante"],
        "chutes_pro": df["chutes_visitante"],
        "chutes_contra": df["chutes_mandante"],
        "escanteios_pro": df["escanteios_visitante"],
        "escanteios_contra": df["escanteios_mandante"],
        "faltas_pro": df["faltas_visitante"],
        "faltas_contra": df["faltas_mandante"],
        "defesas_pro": df["defesas_visitante"],
        "defesas_contra": df["defesas_mandante"],
        "vitoria": (df["visitante_venceu"] == 1).astype(int),
        "empate": (df["empate_flag"] == 1).astype(int),
        "derrota": (df["mandante_venceu"] == 1).astype(int),
    })

    df_times = pd.concat([mandante, visitante], ignore_index=True)
    return df_times

@lru_cache
def carregar_df_times() -> pd.DataFrame:
    df = carregar_df_brasileirao()
    return _construir_base_times(df)

@lru_cache
def carregar_metricas_times() -> pd.DataFrame:
    df_times = carregar_df_times()
    agrupado = df_times.groupby("time").agg(
        jogos=("time", "count"),
        gols_pro=("gols_pro", "mean"),
        gols_contra=("gols_contra", "mean"),
        chutes_pro=("chutes_pro", "mean"),
        chutes_contra=("chutes_contra", "mean"),
        escanteios_pro=("escanteios_pro", "mean"),
        faltas_pro=("faltas_pro", "mean"),
        defesas_pro=("defesas_pro", "mean"),
        taxa_vitorias=("vitoria", "mean"),
        taxa_empates=("empate", "mean"),
        taxa_derrotas=("derrota", "mean"),
    )
    return agrupado
