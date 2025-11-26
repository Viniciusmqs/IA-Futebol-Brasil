import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

API_URL = "http://127.0.0.1:8000"

PRIMARY_COLOR = "#FFFFFF"
SECONDARY_COLOR = "#1E293B"
ACCENT_COLOR = "#00FF41"    # Neon green for key highlights
ACCENT_CYAN = "#00D9FF"     # Cyan for secondary accents
ACCENT_PINK = "#FF006E"     # Pink for warnings/danger
BACKGROUND_DARK = "#0A0E27" # Ultra dark background
BACKGROUND_CARD = "#1A1F3A" # Dark card background
BORDER_COLOR = "#2D3748"    # Dark borders
TEXT_LIGHT = "#E2E8F0"      # Light text for contrast
TEXT_SECONDARY = "#94A3B8"  # Secondary text gray

st.set_page_config(
    page_title="IA Futebol Brasil | Análise Tática Avançada ⚽",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@600;700&display=swap');

    /* Base styling - Dark mode */
    html, body, [data-testid="stAppViewContainer"] {{
        background: linear-gradient(135deg, {BACKGROUND_DARK} 0%, #0F1424 100%);
        background-attachment: fixed;
        color: {TEXT_LIGHT};
        font-family: 'Inter', sans-serif;
    }}

    /* Main container */
    [data-testid="stApp"] {{
        background: linear-gradient(135deg, {BACKGROUND_CARD} 0%, #22273A 100%);
        border-radius: 28px;
        box-shadow: 0 12px 48px rgba(0, 255, 65, 0.08), 0 2px 6px rgba(0, 0, 0, 0.4);
        padding: 40px;
        margin: 50px auto;
        max-width: 1550px;
        border: 1.5px solid {ACCENT_COLOR}30;
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {BACKGROUND_CARD} 0%, #1A1F3A 100%);
        border-right: 3px solid {ACCENT_COLOR}40;
        border-radius: 24px;
        box-shadow: 3px 0 24px rgba(0, 255, 65, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }}

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: {TEXT_LIGHT};
        font-family: 'Sora', sans-serif;
        font-weight: 700;
        letter-spacing: -0.8px;
    }}

    /* Heading styles */
    h1, h2, h3 {{
        color: {TEXT_LIGHT};
        font-family: 'Sora', sans-serif;
        font-weight: 700;
        letter-spacing: -0.8px;
    }}

    h1 {{
        color:{ACCENT_COLOR };
        font-size: 3.2em;
        display: flex;
        align-items: center;
        gap: 15px;
    }}

    h2 {{
        font-size: 1.9em;
        color: {TEXT_LIGHT};
        margin-top: 32px;
        margin-bottom: 16px;
        border-bottom: 4px solid {ACCENT_COLOR};
        padding-bottom: 12px;
        display: inline-block;
        box-shadow: 0 4px 12px {ACCENT_COLOR}20;
    }}

    h3 {{
        font-size: 1.35em;
        color: {TEXT_LIGHT};
        font-weight: 600;
    }}

    /* Caption styling */
    .st-emotion-cache-nahz7x p {{
        color: {TEXT_SECONDARY};
        font-size: 1.05em;
        line-height: 1.6;
    }}

    /* Button styling with neon glow */
    .stButton>button {{
        border: 2px solid {ACCENT_COLOR};
        color: #0A0E27;
        background: transparent;
        border-radius: 14px;
        font-weight: 700;
        transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        text-transform: uppercase;
        letter-spacing: 1.8px;
        font-size: 0.82em;
        padding: 14px 28px !important;
        box-shadow: 0 6px 20px {ACCENT_COLOR}50, 0 0 15px {ACCENT_COLOR}30;
        position: relative;
        overflow: hidden;
    }}

    .stButton>button::before {{
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }}

    .stButton>button:hover {{
        background: {ACCENT_COLOR};
        box-shadow: 0 12px 40px {ACCENT_COLOR}70, 0 0 30px {ACCENT_COLOR}60;
        transform: translateY(-4px);
        border-color: {ACCENT_COLOR};
        text-color: black !important;
    }}

    .stButton>button:active {{
        transform: translateY(-1px);
        box-shadow: 0 4px 15px {ACCENT_COLOR}40;
    }}

    /* Metric styling */
    [data-testid="stMetricValue"] {{
        color: {ACCENT_COLOR};
        font-size: 2.6rem;
        font-weight: 800;
        font-family: 'Sora', sans-serif;
        text-shadow: 0 2px 8px {ACCENT_COLOR}30;
    }}

    [data-testid="stMetricLabel"] {{
        color: {TEXT_SECONDARY};
        font-size: 0.95em;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}

    /* Metric container */
    [data-testid="stMetric"] {{
        background: linear-gradient(135deg, {BACKGROUND_CARD} 0%, #1F2639 100%);
        border: 1.5px solid {ACCENT_COLOR}20;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 4px 16px rgba(0, 255, 65, 0.05), 0 1px 3px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
        position: relative;
    }}

    [data-testid="stMetric"]::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, {ACCENT_COLOR}15, transparent);
        transition: left 0.6s ease;
    }}

    [data-testid="stMetric"]:hover {{
        border-color: {ACCENT_COLOR}40;
        box-shadow: 0 16px 32px {ACCENT_COLOR}15, 0 2px 6px rgba(0, 0, 0, 0.4);
        transform: translateY(-6px);
    }}

    [data-testid="stMetric"]:hover::before {{
        left: 100%;
    }}

    /* Container styling */
    .st-emotion-cache-1pxpx8z {{
        background: linear-gradient(135deg, {BACKGROUND_CARD} 0%, #1F2639 100%);
        border: 1.5px solid {BORDER_COLOR};
        border-radius: 18px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px rgba(0, 255, 65, 0.04);
    }}

    /* Expander styling */
    .st-expander {{
        background: {BACKGROUND_CARD};
        border: 1.5px solid {BORDER_COLOR};
        border-radius: 18px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
        overflow: hidden;
        margin-bottom: 18px;
        transition: all 0.3s ease;
    }}

    .st-expander:hover {{
        border-color: {ACCENT_COLOR}35;
        box-shadow: 0 8px 24px {ACCENT_COLOR}12;
    }}

    .st-expander details summary {{
        color: {TEXT_LIGHT};
        font-weight: 700;
        padding: 20px 24px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1.1em;
        border-left: 5px solid transparent;
        background: linear-gradient(90deg, {ACCENT_COLOR}08 0%, transparent 100%);
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .st-expander details summary:hover {{
        background: linear-gradient(90deg, {ACCENT_COLOR}12 0%, transparent 100%);
        border-left-color: {ACCENT_COLOR};
        padding-left: 20px;
    }}

    .st-expander details[open] summary {{
        background: linear-gradient(90deg, {ACCENT_COLOR}12 0%, transparent 100%);
        border-left-color: {ACCENT_COLOR};
        box-shadow: inset 0 4px 12px {ACCENT_COLOR}10;
    }}

    /* Input styling */
    .st-emotion-cache-rnrmy {{
        color: {TEXT_LIGHT};
        font-weight: 600;
        font-size: 0.95em;
    }}

    .st-emotion-cache-ue6h4q {{
        background: {BACKGROUND_CARD};
        border: 2px solid {BORDER_COLOR} !important;
        border-radius: 12px;
        color: {TEXT_LIGHT};
        transition: all 0.3s ease;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    }}

    .st-emotion-cache-ue6h4q:focus-within {{
        border-color: {ACCENT_COLOR} !important;
        box-shadow: 0 0 0 4px {ACCENT_COLOR}20, 0 4px 12px {ACCENT_COLOR}25;
    }}

    /* Alert styling */
    [data-testid="stAlert"] {{
        border-radius: 14px;
        background: {BACKGROUND_CARD};
        border-left: 6px solid {ACCENT_COLOR};
        border: 1.5px solid {BORDER_COLOR};
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }}

    [data-testid="stAlert"] div[data-testid="stMarkdownContainer"] p {{
        color: {TEXT_LIGHT};
        font-size: 0.95em;
        line-height: 1.6;
    }}

    /* Markdown styling */
    [data-testid="stMarkdownContainer"] {{
        color: {TEXT_LIGHT};
    }}

    p {{
        color: {TEXT_LIGHT};
        line-height: 1.6;
    }}

    /* Link styling */
    a {{
        color: {ACCENT_COLOR};
        text-decoration: none;
        font-weight: 700;
        transition: all 0.3s ease;
    }}

    a:hover {{
        color: {ACCENT_CYAN};
        text-decoration: underline;
    }}

    /* Number input */
    input[type="number"] {{
        background: {PRIMARY_COLOR} !important;
        border: 2px solid {BORDER_COLOR} !important;
        color: {BACKGROUND_DARK } !important;
        border-radius: 12px;
        font-weight: 500;
    }}

    /* Column styling */
    .st-emotion-cache-ocqkz7 {{
        background: linear-gradient(135deg, {BACKGROUND_CARD} 0%, #1F2639 100%);
        border-radius: 18px;
        padding: 24px;
        border: 1.5px solid {BORDER_COLOR};
        transition: all 0.4s ease;
    }}

    .st-emotion-cache-ocqkz7:hover {{
        border-color: {ACCENT_COLOR}30;
        box-shadow: 0 12px 32px {ACCENT_COLOR}12;
        transform: translateY(-4px);
    }}

    /* Added bouncing ball animation */
    @keyframes bounce-ball {{
        0%, 100% {{ transform: translateY(0) scale(1); }}
        50% {{ transform: translateY(-20px) scale(1.05); }}
    }}

    @keyframes glow-pulse {{
        0%, 100% {{ filter: drop-shadow(0 0 8px {ACCENT_COLOR}60); }}
        50% {{ filter: drop-shadow(0 0 16px {ACCENT_COLOR}100); }}
    }}

    .bouncing-ball {{
        display: inline-block;
        animation: bounce-ball 0.8s ease-in-out infinite, glow-pulse 1.2s ease-in-out infinite;
        font-size: 1.5em;
        margin-left: 10px;
    }}

    .st-emotion-cache-oteskg:hover{{
        background: {ACCENT_COLOR} !important;
        color: {BACKGROUND_DARK} !important;
        border-radius: 8px;
    }}

    .st-emotion-cache-oteskg:selected{{
        background: {ACCENT_COLOR} !important;
        color: {BACKGROUND_DARK} !important;
        border-radius: 8px;
    }}

    .st-emotion-cache-oteskg:hover:enabled, 
    .st-emotion-cache-oteskg:focus:enabled {{
    color: rgb(255, 255, 255);
    background-color: #00FF41;;
    transition: none;
    outline: none;
}}

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 15px;">
        <span> IA FUTEBOL BRASIL</span>
        <span class="bouncing-ball">⚽⚽⚽⚽</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("Projeção Tática Avançada")
st.caption(f"🚀 Análise e Predição de Confrontos do Brasileirão Série A | **Impulsionado por IA com Tecnologia de Última Geração**")


@st.cache_data
def get_times():
    try:
        resp = requests.get(f"{API_URL}/times")
        resp.raise_for_status()
        return resp.json()["times"]
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Erro de Conexão: Não foi possível conectar-se à API em {API_URL}. Verifique se o backend está rodando.")
        return ["Erro de Conexão"]

@st.cache_data
def get_perfil_time(time: str):
    try:
        resp = requests.get(f"{API_URL}/perfil-time", params={"time": time})
        resp.raise_for_status()
        return resp.json()["perfil"]
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro ao buscar perfil do time {time}: {e}")
        return {}

def get_comparacao(time_a: str, time_b: str):
    try:
        resp = requests.get(
            f"{API_URL}/comparar-times",
            params={"time_a": time_a, "time_b": time_b},
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro ao comparar times {time_a} vs {time_b}: {e}")
        return None

def prever_partida(payload: dict):
    try:
        resp = requests.post(f"{API_URL}/prever", json=payload)
        resp.raise_for_status()
        return resp.json()["probabilidades"]
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro ao prever partida: {e}")
        return None

# ========== Sidebar (Painel de Controle) ==========

st.sidebar.markdown(f"## ⚙️ **Parâmetros da Análise**")

times = get_times()
if "Erro de Conexão" in times:
    st.sidebar.warning("⚠️ Seleção de times indisponível devido a erro de conexão com a API.")
    time_a = "Time A (Indisponível)"
    time_b = "Time B (Indisponível)"
else:
    time_a = st.sidebar.selectbox("**Time da Casa (Mandante)**", options=times, index=times.index("Flamengo") if "Flamengo" in times else 0)
    time_b = st.sidebar.selectbox("**Time Visitante**", options=times, index=times.index("Palmeiras") if "Palmeiras" in times else 1)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 **Dados da Partida**")

with st.sidebar.expander("Detalhes do Campeonato", expanded=False):
    ano = st.number_input("Ano da Temporada", min_value=2003, max_value=2025, value=2024, help="Ano em que a partida será disputada ou foi simulada.")
    rodada = st.number_input("Rodada do Campeonato", min_value=1, max_value=38, value=10, help="Número da rodada dentro do campeonato.")
    publico_max = st.number_input("Capacidade do Estádio (Público Máx)", value=40000.0, step=1000.0, help="Capacidade máxima de público do estádio.")

st.sidebar.markdown("**Posicionamento Atual:**")

col_pos1, col_pos2 = st.sidebar.columns(2)
with col_pos1:
    col_mand = st.number_input(f"Pos. {time_a[:6]}", min_value=1, max_value=20, value=3, help=f"Ranking")
with col_pos2:
    col_visit = st.number_input(f"Pos. {time_b[:6]}", min_value=1, max_value=20, value=7, help=f"Ranking")

st.sidebar.markdown("**Valor e Idade do Elenco:**")

col_val1, col_val2 = st.sidebar.columns(2)
with col_val1:
    valor_mand = st.number_input(f"Valor {time_a[:8]} (M)", value=25.0, step=1.0, format="%.2f", help=f"Valor em milhões (R$)")
with col_val2:
    valor_visit = st.number_input(f"Valor {time_b[:8]} (M)", value=18.0, step=1.0, format="%.2f", help=f"Valor em milhões (R$)")

col_age1, col_age2 = st.sidebar.columns(2)
with col_age1:
    idade_mand = st.number_input(f"Idade {time_a[:6]}", value=26.5, step=0.1, help=f"Média etária")
with col_age2:
    idade_visit = st.number_input(f"Idade {time_b[:6]}", value=27.1, step=0.1, help=f"Média etária")

st.sidebar.markdown("---")
if "Erro de Conexão" not in times:
    btn_comparar = st.sidebar.button("Iniciar Análise Comparativa", use_container_width=True)
    btn_prever = st.sidebar.button("Gerar Projeção de Resultado", use_container_width=True)
else:
    st.sidebar.button(" Iniciar Análise Comparativa", use_container_width=True, disabled=True)
    st.sidebar.button(" Gerar Projeção de Resultado", use_container_width=True, disabled=True)

# ========== Layout principal ==========

st.markdown("### **Confronto em Destaque**")
col_esq, col_meio, col_dir = st.columns([1, 0.3, 1])

with col_esq:
    st.markdown(f"<h3 style='text-align: left; color: {TEXT_LIGHT}; border-bottom: 4px solid {ACCENT_COLOR}; padding-bottom: 10px;'> {time_a}</h3>", unsafe_allow_html=True)

with col_meio:
    st.markdown(f"<h3 style='text-align: center; color: {ACCENT_CYAN}; font-size: 1.5em;'> vs </h3>", unsafe_allow_html=True)

with col_dir:
    st.markdown(f"<h3 style='text-align: right; color: {TEXT_LIGHT}; border-bottom: 4px solid {ACCENT_COLOR}; padding-bottom: 10px;'> {time_b}</h3>", unsafe_allow_html=True)

st.markdown("---")

if not btn_comparar and not btn_prever:
    st.info(" Utilize o **Painel de Parâmetros** ao lado para configurar a análise ou previsão da partida.")

# ========== 1) Comparação de times ==========

if btn_comparar and "Erro de Conexão" not in times:
    comparacao = get_comparacao(time_a, time_b)
    if comparacao:
        stats = comparacao["estatisticas"]

        st.markdown(f"## 📊 **Relatório Tático de Confronto Direto**")
        st.markdown(f"O histórico geral registra **{comparacao['empates_totais']}** empates em partidas anteriores entre as equipes.")

        with st.expander("📈 **Estatísticas Gerais da Carreira**", expanded=True):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### **Dados de Performance - {time_a}**")
                st.metric("Total de Jogos", stats[time_a]["jogos"])
                st.metric("Vitórias", stats[time_a]["vitorias"])
                st.metric("Média de Gols Pró", f"{stats[time_a]['gols_pro']:.2f}", delta_color="normal")
                st.metric("Média de Gols Contra", f"{stats[time_a]['gols_contra']:.2f}", delta_color="inverse")

            with col2:
                st.markdown(f"### **Dados de Performance - {time_b}**")
                st.metric("Total de Jogos", stats[time_b]["jogos"])
                st.metric("Vitórias", stats[time_b]["vitorias"])
                st.metric("Média de Gols Pró", f"{stats[time_b]['gols_pro']:.2f}", delta_color="normal")
                st.metric("Média de Gols Contra", f"{stats[time_b]['gols_contra']:.2f}", delta_color="inverse")

        st.markdown("---")

        with st.expander(" **Dinâmica de Gols (Média por Partida)**", expanded=True):
            st.markdown(f"### 🎯 Gols Marcados vs Sofridos")
            df_gols = pd.DataFrame({
                "Time": [time_a, time_a, time_b, time_b],
                "Tipo de Gol": ["Pró", "Contra", "Pró", "Contra"],
                "Valor": [
                    stats[time_a]["gols_pro"],
                    stats[time_a]["gols_contra"],
                    stats[time_b]["gols_pro"],
                    stats[time_b]["gols_contra"],
                ]
            })
            
            fig_bar = px.bar(
                df_gols, 
                x="Time", 
                y="Valor", 
                color="Tipo de Gol", 
                barmode="group", 
                text_auto=".2f",
                title="Média de Gols por Tipo",
                color_discrete_map={
                    "Pró": ACCENT_COLOR, 
                    "Contra": ACCENT_PINK
                },
                template="plotly"
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(248, 250, 252, 0)', 
                plot_bgcolor='rgba(248, 250, 252, 0)',
                font=dict(color=TEXT_LIGHT, size=12, family="Inter"),
                legend_title_text='Tipo de Gol',
                hovermode='x unified',
                margin=dict(l=0, r=0, t=40, b=0),
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor='rgba(0, 255, 65, 0.12)')
            )
            fig_bar.update_traces(
                marker=dict(line=dict(width=2, color='rgba(255,255,255,0.6)')),
                hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y:.2f}<extra></extra>'
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")

        with st.expander(" **Radar de Atributos Táticos**", expanded=True):
            st.markdown("### 📊 Comparativo de Perfil de Jogo")

            perfil_a = get_perfil_time(time_a)
            perfil_b = get_perfil_time(time_b)
            
            if perfil_a and perfil_b:
                campos = [
                    "gols_pro", "gols_contra", "chutes_pro", "escanteios_pro",
                    "faltas_pro", "defesas_pro", "taxa_vitorias", "taxa_empates", "taxa_derrotas",
                ]

                df_radar = pd.DataFrame({
                    "Métrica": campos,
                    time_a: [perfil_a.get(c, 0) for c in campos],
                    time_b: [perfil_b.get(c, 0) for c in campos],
                })

                for col in [time_a, time_b]:
                    max_val = df_radar[col].max()
                    if max_val > 0:
                        df_radar[col] = df_radar[col] / max_val
                
                melted_df = df_radar.melt(id_vars="Métrica", var_name="Time", value_name="Valor")
                
                fig_radar = px.line_polar(
                    melted_df,
                    r="Valor",
                    theta="Métrica",
                    color="Time",
                    line_close=True,
                    color_discrete_map={
                        time_a: ACCENT_COLOR,
                        time_b: ACCENT_CYAN,
                    },
                    template="plotly",
                    title="Desempenho Relativo por Métrica"
                )
                fig_radar.update_traces(
                    fill="toself", 
                    opacity=0.35, 
                    line=dict(width=3),
                    hovertemplate='<b>%{theta}</b><br>%{fullData.name}<br>Valor: %{r:.2f}<extra></extra>'
                )
                fig_radar.update_layout(
                    paper_bgcolor='rgba(248, 250, 252, 0)', 
                    plot_bgcolor='rgba(248, 250, 252, 0)',
                    font=dict(color=TEXT_LIGHT, family="Inter"),
                    polar=dict(
                        radialaxis=dict(
                            visible=True, 
                            range=[0, 1], 
                            showticklabels=True,
                            gridcolor='rgba(0, 255, 65, 0.15)',
                            tickcolor=ACCENT_COLOR
                        ),
                        angularaxis=dict(
                            rotation=90, 
                            direction='clockwise', 
                            tickfont=dict(size=11, color=TEXT_LIGHT)
                        ),
                        bgcolor='rgba(0, 255, 65, 0.02)'
                    ),
                    margin=dict(l=80, r=80, t=80, b=80)
                )
                st.plotly_chart(fig_radar, use_container_width=True)
            else:
                st.warning("⚠️ Não foi possível carregar o perfil completo de um ou ambos os times para o radar.")

# ========== 2) Previsão de resultado ==========

if btn_prever and "Erro de Conexão" not in times:
    payload = {
        "ano_campeonato": int(ano),
        "rodada": int(rodada),
        "colocacao_mandante": float(col_mand),
        "colocacao_visitante": float(col_visit),
        "valor_equipe_titular_mandante": float(valor_mand * 1_000_000),
        "valor_equipe_titular_visitante": float(valor_visit * 1_000_000),
        "idade_media_titular_mandante": float(idade_mand),
        "idade_media_titular_visitante": float(idade_visit),
        "publico_max": float(publico_max),
    }

    probs = prever_partida(payload)

    if probs:
        st.markdown(f"## **Projeção Preditiva: Resultado da Partida**")
        
        with st.container(border=True):
            st.markdown(f"### 📈 **Probabilidades Calculadas pela IA**")
            st.markdown(f"**Mandante:** **{time_a}** | **Visitante:** **{time_b}**")

            col_p1, col_p2, col_p3 = st.columns(3)
            
            col_p1.metric(f"Vitória {time_a}", f"{probs['mandante'] * 100:.1f}%", delta_color="normal")
            col_p2.metric("Empate", f"{probs['empate'] * 100:.1f}%", delta_color="off")
            col_p3.metric(f"Vitória {time_b}", f"{probs['visitante'] * 100:.1f}%", delta_color="inverse")

        df_probs = pd.DataFrame({
            "Resultado": [f"Vitória {time_a}", "Empate", f"Vitória {time_b}"],
            "Probabilidade": [
                probs["mandante"],
                probs["empate"],
                probs["visitante"],
            ],
        })

        fig_prob = px.bar(
            df_probs, 
            x="Resultado", 
            y="Probabilidade", 
            text_auto=".1%",
            title="Distribuição de Probabilidades do Modelo Preditivo",
            color="Resultado",
            color_discrete_map={
                f"Vitória {time_a}": ACCENT_COLOR,
                "Empate": ACCENT_CYAN,
                f"Vitória {time_b}": ACCENT_PINK,
            },
            template="plotly"
        )
        fig_prob.update_yaxes(
            tickformat=".0%", 
            range=[0, df_probs['Probabilidade'].max() * 1.2 if df_probs['Probabilidade'].max() > 0.0 else 1.0],
            gridcolor='rgba(0, 255, 65, 0.12)'
        )
        fig_prob.update_xaxes(showgrid=False)
        fig_prob.update_layout(
            paper_bgcolor='rgba(248, 250, 252, 0)', 
            plot_bgcolor='rgba(248, 250, 252, 0)',
            font=dict(color=TEXT_LIGHT, family="Inter"),
            hovermode='x unified',
            margin=dict(l=0, r=0, t=40, b=0),
        )
        fig_prob.update_traces(
            marker=dict(line=dict(width=2, color='rgba(255,255,255,0.6)')),
            hovertemplate='<b>%{x}</b><br>Probabilidade: %{y:.1%}<extra></extra>'
        )
        st.plotly_chart(fig_prob, use_container_width=True)
