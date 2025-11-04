from typing import List, Dict
import numpy as np
from app.utils.data_loader import (
    carregar_df_times,
    carregar_metricas_times,
)

def listar_times() -> List[str]:
    df_times = carregar_df_times()
    times = sorted(df_times["time"].unique())
    return times

def comparar_times(time_a: str, time_b: str) -> Dict:
    df_times = carregar_df_times()

    subset = df_times[df_times["time"].isin([time_a, time_b])]

    if subset.empty:
        raise ValueError("Nenhum dado encontrado para esses times.")

    stats = {}

    for t in [time_a, time_b]:
        jogos_time = subset[subset["time"] == t]
        stats[t] = {
            "jogos": int(jogos_time.shape[0]),
            "gols_pro": float(jogos_time["gols_pro"].mean()),
            "gols_contra": float(jogos_time["gols_contra"].mean()),
            "vitorias": int(jogos_time["vitoria"].sum()),
            "empates": int(jogos_time["empate"].sum()),
            "derrotas": int(jogos_time["derrota"].sum()),
        }

    total_empates = int(subset["empate"].sum())

    return {
        "time_a": time_a,
        "time_b": time_b,
        "estatisticas": stats,
        "empates_totais": total_empates,
    }

def perfil_time(time: str) -> Dict:
    metricas = carregar_metricas_times()

    if time not in metricas.index:
        raise ValueError("Time não encontrado.")

    linha = metricas.loc[time]

    # transforma em dict com floats
    perfil = {k: float(v) for k, v in linha.to_dict().items()}
    return perfil
