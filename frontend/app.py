import requests
import streamlit as st
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="IA Futebol Brasil",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ IA Futebol Brasil")
st.caption("Comparador de times e previsão de resultados com dados do Brasileirão Série A")

# ========== Funções auxiliares ==========

@st.cache_data
def get_times():
    resp = requests.get(f"{API_URL}/times")
    resp.raise_for_status()
    return resp.json()["times"]

@st.cache_data
def get_perfil_time(time: str):
    resp = requests.get(f"{API_URL}/perfil-time", params={"time": time})
    resp.raise_for_status()
    return resp.json()["perfil"]

def get_comparacao(time_a: str, time_b: str):
    resp = requests.get(
        f"{API_URL}/comparar-times",
        params={"time_a": time_a, "time_b": time_b},
    )
    resp.raise_for_status()
    return resp.json()

def prever_partida(payload: dict):
    resp = requests.post(f"{API_URL}/prever", json=payload)
    resp.raise_for_status()
    return resp.json()["probabilidades"]

# ========== Sidebar ==========

st.sidebar.header("⚙️ Configurações")

times = get_times()

time_a = st.sidebar.selectbox("Time A", options=times, index=times.index("Flamengo") if "Flamengo" in times else 0)
time_b = st.sidebar.selectbox("Time B", options=times, index=times.index("Palmeiras") if "Palmeiras" in times else 1)

st.sidebar.markdown("---")
st.sidebar.subheader("Parâmetros da partida (para previsão)")
ano = st.sidebar.number_input("Ano do campeonato", min_value=2003, max_value=2025, value=2024)
rodada = st.sidebar.number_input("Rodada", min_value=1, max_value=38, value=10)
col_mand = st.sidebar.number_input("Colocação mandante", min_value=1, max_value=20, value=3)
col_visit = st.sidebar.number_input("Colocação visitante", min_value=1, max_value=20, value=7)
valor_mand = st.sidebar.number_input("Valor equipe mandante (R$)", value=25000000.0, step=1_000_000.0)
valor_visit = st.sidebar.number_input("Valor equipe visitante (R$)", value=18000000.0, step=1_000_000.0)
idade_mand = st.sidebar.number_input("Idade média mandante", value=26.5)
idade_visit = st.sidebar.number_input("Idade média visitante", value=27.1)
publico_max = st.sidebar.number_input("Capacidade do estádio", value=40000.0, step=1000.0)

st.sidebar.markdown("---")
btn_comparar = st.sidebar.button("🔍 Comparar Times")
btn_prever = st.sidebar.button("🎯 Prever Resultado")

# ========== Layout principal ==========

col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader(f"Time A: {time_a}")

with col_dir:
    st.subheader(f"Time B: {time_b}")

# ========== 1) Comparação de times ==========

if btn_comparar:
    try:
        comparacao = get_comparacao(time_a, time_b)
        stats = comparacao["estatisticas"]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### 📊 Estatísticas gerais – {time_a}")
            st.metric("Jogos", stats[time_a]["jogos"])
            st.metric("Vitórias", stats[time_a]["vitorias"])
            st.metric("Empates", stats[time_a]["empates"])
            st.metric("Derrotas", stats[time_a]["derrotas"])
            st.metric("Gols pró (média)", f"{stats[time_a]['gols_pro']:.2f}")
            st.metric("Gols contra (média)", f"{stats[time_a]['gols_contra']:.2f}")

        with col2:
            st.markdown(f"### 📊 Estatísticas gerais – {time_b}")
            st.metric("Jogos", stats[time_b]["jogos"])
            st.metric("Vitórias", stats[time_b]["vitorias"])
            st.metric("Empates", stats[time_b]["empates"])
            st.metric("Derrotas", stats[time_b]["derrotas"])
            st.metric("Gols pró (média)", f"{stats[time_b]['gols_pro']:.2f}")
            st.metric("Gols contra (média)", f"{stats[time_b]['gols_contra']:.2f}")

        st.markdown(f"🟡 **Empates entre eles:** {comparacao['empates_totais']}")

        st.markdown("### ⚽ Gols Pró x Gols Contra (média)")
        df_gols = pd.DataFrame({
            "Time": [time_a, time_a, time_b, time_b],
            "Tipo": ["Gols pró", "Gols contra", "Gols pró", "Gols contra"],
            "Valor": [
                stats[time_a]["gols_pro"],
                stats[time_a]["gols_contra"],
                stats[time_b]["gols_pro"],
                stats[time_b]["gols_contra"],
            ]
        })
        fig_bar = px.bar(df_gols, x="Time", y="Valor", color="Tipo", barmode="group", text_auto=".2f")
        st.plotly_chart(fig_bar, use_container_width=True)

        # RADAR
        st.markdown("### 🧭 Radar de desempenho geral")

        perfil_a = get_perfil_time(time_a)
        perfil_b = get_perfil_time(time_b)

        # Escolhe algumas métricas para o radar
        campos = [
            "gols_pro",
            "gols_contra",
            "chutes_pro",
            "escanteios_pro",
            "faltas_pro",
            "defesas_pro",
            "taxa_vitorias",
            "taxa_empates",
            "taxa_derrotas",
        ]

        df_radar = pd.DataFrame({
            "Métrica": campos,
            time_a: [perfil_a[c] for c in campos],
            time_b: [perfil_b[c] for c in campos],
        })

        # normaliza para 0–1 pra ficar mais bonito
        for col in [time_a, time_b]:
            max_val = df_radar[col].max()
            if max_val > 0:
                df_radar[col] = df_radar[col] / max_val

        fig_radar = px.line_polar(
            df_radar.melt(id_vars="Métrica", var_name="Time", value_name="Valor"),
            r="Valor",
            theta="Métrica",
            color="Time",
            line_close=True,
        )
        fig_radar.update_traces(fill="toself")
        st.plotly_chart(fig_radar, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao buscar dados de comparação: {e}")

# ========== 2) Previsão de resultado ==========

if btn_prever:
    payload = {
        "ano_campeonato": int(ano),
        "rodada": int(rodada),
        "colocacao_mandante": float(col_mand),
        "colocacao_visitante": float(col_visit),
        "valor_equipe_titular_mandante": float(valor_mand),
        "valor_equipe_titular_visitante": float(valor_visit),
        "idade_media_titular_mandante": float(idade_mand),
        "idade_media_titular_visitante": float(idade_visit),
        "publico_max": float(publico_max),
    }

    try:
        probs = prever_partida(payload)

        st.markdown("## 🎯 Previsão da partida")
        st.write(f"**Mandante:** {time_a}")
        st.write(f"**Visitante:** {time_b}")

        col_p1, col_p2, col_p3 = st.columns(3)
        col_p1.metric("Vitória mandante", f"{probs['mandante'] * 100:.1f}%")
        col_p2.metric("Empate", f"{probs['empate'] * 100:.1f}%")
        col_p3.metric("Vitória visitante", f"{probs['visitante'] * 100:.1f}%")

        df_probs = pd.DataFrame({
            "Resultado": ["Mandante", "Empate", "Visitante"],
            "Probabilidade": [
                probs["mandante"],
                probs["empate"],
                probs["visitante"],
            ],
        })

        fig_prob = px.bar(df_probs, x="Resultado", y="Probabilidade", text_auto=".1%")
        fig_prob.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig_prob, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao prever resultado: {e}")
