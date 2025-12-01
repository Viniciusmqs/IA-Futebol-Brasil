import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time
import unicodedata

# ==============================================================================
# 1. CONFIGURAÇÃO VISUAL "FIFA ULTIMATE TEAM"
# ==============================================================================
st.set_page_config(
    page_title="IA Futebol Brasil | Ultimate Engine",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = "http://127.0.0.1:8000"

# CSS Profissional: Glassmorphism, Fontes Tecnológicas e Hero Cards Dinâmicos
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;600&display=swap');

    /* Fundo Global com Gradiente Profundo */
    .stApp {
        background-color: #0b0c10;
        background-image: radial-gradient(circle at 50% 0%, #1f2833 0%, #0b0c10 80%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* Títulos */
    h1, h2, h3 {
        font-family: 'Rajdhani', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* --- HERO CARD (O ESTÁDIO) --- */
    .hero-card {
        position: relative;
        height: 400px;
        border-radius: 24px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 20px 60px rgba(0,0,0,0.8);
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: center;
        text-align: center;
        transition: all 0.5s ease;
        background-size: cover;
        background-position: center;
    }
    
    .hero-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 30px 80px rgba(0,0,0,0.9);
        border-color: rgba(255,255,255,0.4);
    }

    /* Camada escura sobre a foto do estádio para ler o texto */
    .hero-overlay {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(0deg, rgba(0,0,0,1) 0%, rgba(0,0,0,0.6) 50%, rgba(0,0,0,0.3) 100%);
        z-index: 1;
    }

    .hero-content {
        position: relative;
        z-index: 2;
        padding-bottom: 40px;
        width: 100%;
    }

    .team-logo-hero {
        width: 180px;
        height: 180px;
        filter: drop-shadow(0 0 30px rgba(0,0,0,0.7));
        margin-bottom: 15px;
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .team-logo-hero:hover { transform: scale(1.1); }

    .stadium-badge {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 8px 20px;
        border-radius: 30px;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 1px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        display: inline-block;
        margin-top: 15px;
        color: #ddd;
    }

    /* --- PAINEL DE CONTROLE (GLASSMORPHISM) --- */
    .control-panel {
        background: rgba(30, 35, 45, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 25px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }

    /* Botão Neon "Matador" */
    .stButton > button {
        background: linear-gradient(90deg, #00F260 0%, #0575E6 100%);
        color: #fff;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 800;
        font-size: 1.5rem;
        padding: 20px;
        border: none;
        border-radius: 12px;
        text-transform: uppercase;
        width: 100%;
        box-shadow: 0 0 30px rgba(5, 117, 230, 0.5);
        transition: all 0.4s ease;
        letter-spacing: 2px;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 60px rgba(5, 117, 230, 0.8);
        color: #fff;
    }

    /* Veredito Box (Resultado) */
    .veredito-box {
        background: rgba(20, 20, 30, 0.9);
        border-radius: 16px;
        padding: 30px;
        border-left: 10px solid; /* Cor dinâmica via Python */
        box-shadow: 0 20px 50px rgba(0,0,0,0.6);
        margin-top: 20px;
        animation: slideUp 0.8s cubic-bezier(0.165, 0.84, 0.44, 1);
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Ajuste de Métricas e Textos */
    [data-testid="stMetricValue"] {
        font-family: 'Rajdhani';
        font-size: 2.8rem;
        text-shadow: 0 0 20px rgba(255,255,255,0.2);
    }
    
    /* Inputs customizados */
    .stSelectbox label, .stSlider label {
        color: #66fcf1 !important;
        font-weight: 600;
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. MEGABASE DE DADOS (ESTÁDIOS E TIMES SEPARADOS)
# ==============================================================================

# Banco de Estádios com Capacidade e Imagem (URLs verificadas)
STADIUMS_DB = {
    "Maracanã (RJ)": {"capacity": 78838, "img": "https://pt.wikipedia.org/wiki/Est%C3%A1dio_Jornalista_M%C3%A1rio_Filho#/media/Ficheiro:Vis%C3%A3o_do_torcedor.JPG"},
    "Allianz Parque (SP)": {"capacity": 43713, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Allianz_Parque_Panorama_2015.jpg/1280px-Allianz_Parque_Panorama_2015.jpg"},
    "Neo Química Arena (SP)": {"capacity": 49205, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Arena_Corinthians_by_Diego_33.jpg/1280px-Arena_Corinthians_by_Diego_33.jpg"},
    "Morumbi (SP)": {"capacity": 66795, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Est%C3%A1dio_do_Morumbi_2017.jpg/1280px-Est%C3%A1dio_do_Morumbi_2017.jpg"},
    "Mineirão (MG)": {"capacity": 61846, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Arena_MRV_2023.jpg/1280px-Arena_MRV_2023.jpg"},
    "Beira-Rio (RS)": {"capacity": 50128, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Beira-Rio_aerial_view.jpg/1280px-Beira-Rio_aerial_view.jpg"},
    "Arena do Grêmio (RS)": {"capacity": 55662, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Arena_do_Gr%C3%AAmio_-_2012-12-08_-_007.jpg/1280px-Arena_do_Gr%C3%AAmio_-_2012-12-08_-_007.jpg"},
    "Nilton Santos (RJ)": {"capacity": 44661, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Engenh%C3%A3o_panorama_no_pelo.jpg/1280px-Engenh%C3%A3o_panorama_no_pelo.jpg"},
    "São Januário (RJ)": {"capacity": 21880, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/S%C3%A3o_Janu%C3%A1rio_-_Vasco_x_Coritiba.jpg/1280px-S%C3%A3o_Janu%C3%A1rio_-_Vasco_x_Coritiba.jpg"},
    "Vila Belmiro (SP)": {"capacity": 16068, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Vila_Belmiro_a%C3%A9rea.jpg/1280px-Vila_Belmiro_a%C3%A9rea.jpg"},
    "Arena Fonte Nova (BA)": {"capacity": 50025, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Arena_Fonte_Nova_2014.jpg/1280px-Arena_Fonte_Nova_2014.jpg"},
    "Arena Castelão (CE)": {"capacity": 63903, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Castel%C3%A3o_Arena_in_Fortaleza.jpg/1280px-Castel%C3%A3o_Arena_in_Fortaleza.jpg"},
    "Ligga Arena (PR)": {"capacity": 42372, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Arena_da_Baixada_2018.jpg/1280px-Arena_da_Baixada_2018.jpg"},
    "Nabi Abi Chedid (SP)": {"capacity": 17029, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Est%C3%A1dio_Nabi_Abi_Chedid.jpg/1280px-Est%C3%A1dio_Nabi_Abi_Chedid.jpg"},
    "Arena Pantanal (MT)": {"capacity": 44097, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Arena_Pantanal_2018.jpg/1280px-Arena_Pantanal_2018.jpg"},
    "Alfredo Jaconi (RS)": {"capacity": 19924, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Alfredo_Jaconi_2021.jpg/1280px-Alfredo_Jaconi_2021.jpg"},
    "Heriberto Hülse (SC)": {"capacity": 19225, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Est%C3%A1dio_Heriberto_H%C3%BClse.jpg/1280px-Est%C3%A1dio_Heriberto_H%C3%BClse.jpg"},
    "Barradão (BA)": {"capacity": 30618, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Barrad%C3%A3o_2019.jpg/1280px-Barrad%C3%A3o_2019.jpg"},
    "Antônio Accioly (GO)": {"capacity": 12500, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Est%C3%A1dio_Ant%C3%B4nio_Accioly.jpg/1280px-Est%C3%A1dio_Ant%C3%B4nio_Accioly.jpg"},
    "Genérico": {"capacity": 30000, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Soccer_Field_Transverse.svg/1280px-Soccer_Field_Transverse.svg.png"}
}

# Banco de Times (Cores e Logos) - Mapeamento para Chaves Normalizadas
TEAMS_DB = {
    # GIGANTES / SÉRIE A
    "flamengo": {"logo": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Flamengo_braz_logo.svg", "colors": ["#C3281E", "#000000"], "stadium": "Maracanã (RJ)"},
    "palmeiras": {"logo": "https://upload.wikimedia.org/wikipedia/commons/1/10/Palmeiras_logo.svg", "colors": ["#006437", "#FFFFFF"], "stadium": "Allianz Parque (SP)"},
    "sao paulo": {"logo": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Brasao_do_Sao_Paulo_Futebol_Clube.svg", "colors": ["#FE0000", "#FFFFFF"], "stadium": "Morumbi (SP)"},
    "corinthians": {"logo": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Sport_Club_Corinthians_Paulista_crest.svg", "colors": ["#111111", "#FFFFFF"], "stadium": "Neo Química Arena (SP)"},
    "atletico mineiro": {"logo": "https://upload.wikimedia.org/wikipedia/commons/2/27/Clube_Atl%C3%A9tico_Mineiro_logo.svg", "colors": ["#000000", "#FFFFFF"], "stadium": "Arena MRV (MG)"},
    "gremio": {"logo": "https://upload.wikimedia.org/wikipedia/commons/5/50/Gr%C3%AAmio_FBPA_logo.svg", "colors": ["#0D80BF", "#000000"], "stadium": "Arena do Grêmio (RS)"},
    "internacional": {"logo": "https://upload.wikimedia.org/wikipedia/commons/f/f1/Escudo_do_Sport_Club_Internacional.svg", "colors": ["#E5050F", "#FFFFFF"], "stadium": "Beira-Rio (RS)"},
    "botafogo": {"logo": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Botafogo_de_Futebol_e_Regatas_logo.svg", "colors": ["#000000", "#FFFFFF"], "stadium": "Nilton Santos (RJ)"},
    "fluminense": {"logo": "https://upload.wikimedia.org/wikipedia/commons/a/ad/Fluminense_FC_escudo.png", "colors": ["#9F022D", "#00913C"], "stadium": "Maracanã (RJ)"},
    "cruzeiro": {"logo": "https://upload.wikimedia.org/wikipedia/commons/b/b8/Cruzeiro_Esporte_Clube_%28logo%29.svg", "colors": ["#005CA9", "#FFFFFF"], "stadium": "Mineirão (MG)"},
    "vasco": {"logo": "https://upload.wikimedia.org/wikipedia/commons/6/67/Vasco_da_Gama_logo.svg", "colors": ["#000000", "#FFFFFF"], "stadium": "São Januário (RJ)"},
    "bahia": {"logo": "https://upload.wikimedia.org/wikipedia/commons/2/2c/Esporte_Clube_Bahia_logo.svg", "colors": ["#009CA6", "#EC1C24"], "stadium": "Arena Fonte Nova (BA)"},
    "fortaleza": {"logo": "https://upload.wikimedia.org/wikipedia/commons/4/42/Crest_of_Fortaleza_Esporte_Clube.svg", "colors": ["#12207B", "#C8102E"], "stadium": "Arena Castelão (CE)"},
    "athletico": {"logo": "https://upload.wikimedia.org/wikipedia/commons/c/cb/Club_Athl%C3%A9tico_Paranaense_2019.svg", "colors": ["#C8102E", "#000000"], "stadium": "Ligga Arena (PR)"},
    "bragantino": {"logo": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Red_Bull_Bragantino.svg", "colors": ["#FFFFFF", "#D30F16"], "stadium": "Nabi Abi Chedid (SP)"},
    "cuiaba": {"logo": "https://upload.wikimedia.org/wikipedia/commons/1/1d/Cuiab%C3%A1_Esporte_Clube_logo.svg", "colors": ["#01592E", "#F4E409"], "stadium": "Arena Pantanal (MT)"},
    "atletico goianiense": {"logo": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Atl%C3%A9tico_Clube_Goianiense_logo.svg", "colors": ["#EC1C24", "#000000"], "stadium": "Antônio Accioly (GO)"},
    "juventude": {"logo": "https://upload.wikimedia.org/wikipedia/commons/5/52/Juventude_logo.svg", "colors": ["#00913C", "#FFFFFF"], "stadium": "Alfredo Jaconi (RS)"},
    "criciuma": {"logo": "https://upload.wikimedia.org/wikipedia/commons/8/87/Crici%C3%BAma_Esporte_Clube_logo.svg", "colors": ["#FDD116", "#000000"], "stadium": "Heriberto Hülse (SC)"},
    "vitoria": {"logo": "https://upload.wikimedia.org/wikipedia/commons/8/80/Esporte_Clube_Vit%C3%B3ria_logo.svg", "colors": ["#EC1C24", "#000000"], "stadium": "Barradão (BA)"},
    
    # OUTROS / SÉRIE B (Para não faltar escudo)
    "santos": {"logo": "https://upload.wikimedia.org/wikipedia/commons/1/15/Santos_Logo.png", "colors": ["#FFFFFF", "#000000"], "stadium": "Vila Belmiro (SP)"},
    "sport": {"logo": "https://upload.wikimedia.org/wikipedia/commons/a/a2/Sport_Club_do_Recife.svg", "colors": ["#EC1C24", "#000000"], "stadium": "Ilha do Retiro (PE)"},
    "ceara": {"logo": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Cear%C3%A1_Sporting_Club_logo.svg", "colors": ["#000000", "#FFFFFF"], "stadium": "Arena Castelão (CE)"},
    "goias": {"logo": "https://upload.wikimedia.org/wikipedia/commons/b/bb/Goi%C3%A1s_Esporte_Clube_logo.svg", "colors": ["#006437", "#FFFFFF"], "stadium": "Serrinha (GO)"},
    "america mineiro": {"logo": "https://upload.wikimedia.org/wikipedia/commons/a/ac/Am%C3%A9rica_Futebol_Clube_%28MG%29_logo.svg", "colors": ["#01592E", "#000000"], "stadium": "Independência (MG)"},
    "avai": {"logo": "https://upload.wikimedia.org/wikipedia/commons/f/fe/Ava%C3%AD_Futebol_Clube_logo.svg", "colors": ["#005CA9", "#FFFFFF"], "stadium": "Ressacada (SC)"},
    "coritiba": {"logo": "https://upload.wikimedia.org/wikipedia/commons/6/60/Coritiba_FBC_%282024%29_-_Crest.svg", "colors": ["#00522B", "#FFFFFF"], "stadium": "Couto Pereira (PR)"},
    
    # Fallback
    "generic": {"logo": "https://cdn-icons-png.flaticon.com/512/53/53283.png", "colors": ["#333333", "#666666"], "stadium": "Genérico"}
}

# Função de busca ultra-robusta e DEBUG
def get_team_assets(name, debug=False):
    # Remove acentos e joga pra minúsculo
    nfkd_form = unicodedata.normalize('NFKD', str(name))
    clean_name = "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()
    
    # Dicionário de sinônimos
    mapa = {
        "atletico-mg": "atletico mineiro", "cam": "atletico mineiro", "galo": "atletico mineiro",
        "athletico-pr": "athletico", "cap": "athletico", "furacao": "athletico", "athletico paranaense": "athletico",
        "vasco da gama": "vasco", "gigante": "vasco",
        "sport club do recife": "sport", "sport recife": "sport",
        "sao paulo fc": "sao paulo",
        "atletico-go": "atletico goianiense", "dragao": "atletico goianiense",
        "bragantino": "bragantino", "red bull bragantino": "bragantino", "rb bragantino": "bragantino",
        "america-mg": "america mineiro", "america mineiro": "generic"
    }
    
    match_key = clean_name
    if clean_name in mapa:
        match_key = mapa[clean_name]
    
    if debug:
        st.sidebar.markdown(f"**Debug Asset:** `{name}` -> `{clean_name}` -> Key: `{match_key}`")

    for key in TEAMS_DB:
        if key in match_key: # Procura a chave do DB dentro do nome normalizado
            return TEAMS_DB[key]
            
    return TEAMS_DB["generic"]

# ==============================================================================
# 3. LÓGICA DE INTELIGÊNCIA TÁTICA (MODIFICADORES REAIS)
# ==============================================================================
def calcular_modificadores(dados_originais, config):
    """
    Aplica penalidades e bônus MATEMÁTICOS aos dados antes de enviar para a IA.
    """
    novos_dados = dados_originais.copy()
    
    # 1. FATOR CLIMA E GRAMADO
    fator_tecnico = 1.0
    if config['clima'] == "Chuva Intensa / Tempestade":
        fator_tecnico -= 0.15
    if config['gramado'] == "Ruim / Irregular":
        fator_tecnico -= 0.20
    if config['clima'] == "Calor Extremo (40ºC)":
        novos_dados['idade_media_titular_mandante'] += 3
        novos_dados['idade_media_titular_visitante'] += 3

    if novos_dados['valor_equipe_titular_mandante'] > novos_dados['valor_equipe_titular_visitante']:
        novos_dados['valor_equipe_titular_mandante'] *= fator_tecnico
    else:
        novos_dados['valor_equipe_titular_visitante'] *= fator_tecnico

    # 2. FATOR HUMANO
    if config['arbitragem'] == "Caseiro (Pressionável)":
        novos_dados['publico_max'] *= 1.5
    elif config['arbitragem'] == "Rigoroso (Visitante Protegido)":
        novos_dados['publico_max'] *= 0.7

    # 3. CONTEXTO DO JOGO
    if config['tipo_jogo'] == "Final de Campeonato":
        novos_dados['rodada'] = 38
    elif config['tipo_jogo'] == "Clássico Estadual":
        media = (novos_dados['valor_equipe_titular_mandante'] + novos_dados['valor_equipe_titular_visitante']) / 2
        novos_dados['valor_equipe_titular_mandante'] = (novos_dados['valor_equipe_titular_mandante'] + media) / 2
        novos_dados['valor_equipe_titular_visitante'] = (novos_dados['valor_equipe_titular_visitante'] + media) / 2

    # 4. DESFALQUES
    if config['desfalques'] == "Principal Craque Fora":
        novos_dados['valor_equipe_titular_mandante'] *= 0.70

    return novos_dados

def gerar_narrativa_premium(probs, t_home, t_away, config, dados_finais):
    p_h = probs['mandante']
    p_a = probs['visitante']
    diff = p_h - p_a
    
    res = {"titulo": "", "texto": "", "cor": ""}
    motivos = []

    if diff > 0.10:
        res['titulo'] = f"VITÓRIA PROVÁVEL DO {t_home.upper()}"
        res['cor'] = "#00FF00"
    elif diff < -0.10:
        res['titulo'] = f"VITÓRIA PROVÁVEL DO {t_away.upper()}"
        res['cor'] = "#FF0055"
    elif diff > 0:
        res['titulo'] = f"LEVE VANTAGEM PARA O {t_home.upper()}"
        res['cor'] = "#CCFF00"
    else:
        res['titulo'] = "JOGO TRUNCADO / ALTO RISCO DE EMPATE"
        res['cor'] = "#FFAA00"

    val_diff = dados_finais['valor_equipe_titular_mandante'] - dados_finais['valor_equipe_titular_visitante']
    if abs(val_diff) > 50_000_000:
        rico = t_home if val_diff > 0 else t_away
        motivos.append(f"💎 **Abismo Técnico:** O elenco do {rico} vale muito mais (R$ {abs(val_diff)/1_000_000:.0f}M a mais), garantindo superioridade individual.")

    if config['clima'] == "Chuva Intensa / Tempestade":
        motivos.append("🌧️ **Efeito Chuva:** O gramado pesado nivelou o jogo por baixo, reduzindo a vantagem técnica.")
    elif config['clima'] == "Calor Extremo (40ºC)":
        motivos.append("☀️ **Desgaste Físico:** O calor extremo penalizou a intensidade, aumentando a chance de gols no final.")

    if config['arbitragem'] == "Caseiro (Pressionável)" and dados_finais['publico_max'] > 40000:
        motivos.append(f"📢 **Pressão Total:** A combinação de estádio lotado com arbitragem caseira aumentou a probabilidade do mandante.")
    
    if config['tipo_jogo'] == "Clássico Estadual" and abs(diff) < 0.1:
        motivos.append("⚔️ **Fator Clássico:** A rivalidade histórica anulou as diferenças financeiras, criando um cenário de puro equilíbrio emocional.")
        
    if config['desfalques'] == "Principal Craque Fora":
        motivos.append(f"🚑 **Desfalque de Peso:** A ausência do craque do {t_home} reduziu drasticamente o poder ofensivo.")

    if not motivos:
        motivos.append("A IA identificou um equilíbrio de forças onde detalhes táticos decidirão o placar.")

    res['texto'] = "\n\n".join(motivos)
    return res

# ==============================================================================
# 4. ENGINE DE DADOS (CONEXÃO BACKEND)
# ==============================================================================
@st.cache_data
def get_times_list():
    try:
        resp = requests.get(f"{API_URL}/times")
        return sorted(resp.json()["times"])
    except:
        return []

@st.cache_data
def get_history(t1, t2):
    try:
        return requests.get(f"{API_URL}/comparar-times", params={"time_a": t1, "time_b": t2}).json()
    except:
        return None

# ==============================================================================
# 5. APLICAÇÃO PRINCIPAL (INTERFACE)
# ==============================================================================

times_list = get_times_list()

# --- HEADER (STATUS E TÍTULO) ---
c1, c2 = st.columns([0.8, 0.2])
with c1:
    st.markdown("# 🧠 IA FUTEBOL BRASIL PRO")
    st.markdown("**SISTEMA PREDITIVO DE ALTA PERFORMANCE | 2025**")
with c2:
    if times_list:
        st.markdown("<div style='text-align:right; color:#00FF00; font-weight:bold; font-size:1.2rem; padding:10px'>● ONLINE</div>", unsafe_allow_html=True)
    else:
        st.error("● OFFLINE")
        st.stop()

# --- BARRA LATERAL PARA DEBUG ---
st.sidebar.title("Configurações")
debug_mode = st.sidebar.checkbox("🛠️ Modo Desenvolvedor (Debug)", value=False)

st.markdown("---")

# --- SELEÇÃO DE TIMES (HERO SECTION IMERSIVA) ---
col_home, col_vs, col_away = st.columns([1, 0.2, 1])

with col_home:
    st.markdown("### MANDANTE")
    idx_h = times_list.index("Flamengo") if "Flamengo" in times_list else 0
    t_home = st.selectbox("Selecione Mandante", times_list, index=idx_h, key="sel_h", label_visibility="collapsed")
    
    # Busca Assets (Logo e Estádio Padrão)
    assets_h = get_team_assets(t_home, debug=debug_mode)
    
    # SELETOR DE ESTÁDIO DO MANDANTE
    # Pega o estádio padrão do time e permite trocar
    default_stadium_h = assets_h.get('default_stadium', "Maracanã (RJ)")
    # Se o padrão não estiver na lista de estádios, usa genérico
    if default_stadium_h not in STADIUMS_DB: default_stadium_h = "Genérico"
    
    st.markdown("**Local do Jogo:**")
    selected_stadium_name = st.selectbox("Estádio", list(STADIUMS_DB.keys()), index=list(STADIUMS_DB.keys()).index(default_stadium_h), label_visibility="collapsed")
    
    # Pega dados do estádio selecionado
    stadium_data_h = STADIUMS_DB[selected_stadium_name]
    stadium_img_url_h = stadium_data_h['img']
    stadium_capacity_h = stadium_data_h['capacity']

    # Renderiza Card
    st.markdown(f"""
    <div class="hero-card" style="background-image: url('{stadium_img_url_h}'); border-color: {assets_h['colors'][0]}">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <img src="{assets_h['logo']}" class="team-logo-hero">
            <h1 style="margin:0; text-shadow: 0 0 20px black; font-size: 2.8rem; color: white;">{t_home}</h1>
            <div class="stadium-badge">🏟️ {selected_stadium_name}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_vs:
    st.markdown("<br><br><br><br><h1 style='text-align:center; font-size: 4rem; opacity: 0.5'>X</h1>", unsafe_allow_html=True)

with col_away:
    st.markdown("### VISITANTE")
    idx_a = times_list.index("Palmeiras") if "Palmeiras" in times_list else 1
    t_away = st.selectbox("Selecione Visitante", times_list, index=idx_a, key="sel_a", label_visibility="collapsed")
    
    # Busca Assets Visitante
    assets_a = get_team_assets(t_away, debug=debug_mode)
    
    # Para o visitante, usamos o estádio padrão dele APENAS PARA A FOTO DE FUNDO DO CARD DELE
    # Não afeta o local do jogo (que é o do mandante)
    default_stadium_a = assets_a.get('default_stadium', "Genérico")
    if default_stadium_a not in STADIUMS_DB: default_stadium_a = "Genérico"
    stadium_data_a = STADIUMS_DB[default_stadium_a]
    stadium_img_url_a = stadium_data_a['img']
    
    st.markdown("<br><br>", unsafe_allow_html=True) # Espaçamento para alinhar com o seletor extra do mandante
    st.markdown(f"""
    <div class="hero-card" style="background-image: url('{stadium_img_url_a}'); border-color: {assets_a['colors'][0]}">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <img src="{assets_a['logo']}" class="team-logo-hero">
            <h1 style="margin:0; text-shadow: 0 0 20px black; font-size: 2.8rem; color: white;">{t_away}</h1>
            <div class="stadium-badge">✈️ Visitante</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- SISTEMA DE ABAS (SIMULADOR / ESTATÍSTICAS) ---
tab_sim, tab_stat, tab_metodo = st.tabs(["🎮 SIMULADOR DE CENÁRIOS", "📊 ESTATÍSTICAS HISTÓRICAS", "🧠 NEURAL ENGINE"])

# >>> ABA 1: O SIMULADOR TÁTICO
with tab_sim:
    # Layout de Controle
    c_input_env, c_input_team, c_exec = st.columns([1, 1, 1.2])
    
    with c_input_env:
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        st.markdown("### 1. AMBIENTE & CLIMA")
        i_jogo = st.selectbox("Tipo de Jogo", ["Rodada Comum", "Clássico Estadual", "Final de Campeonato", "Jogo Decisivo (G4/Z4)"])
        i_clima = st.selectbox("Condição do Tempo", ["Tempo Bom (Ideal)", "Chuva Intensa / Tempestade", "Calor Extremo (40ºC)", "Frio/Neve"])
        i_gramado = st.selectbox("Estado do Gramado", ["Tapete (Perfeito)", "Ruim / Irregular", "Sintético"])
        st.markdown('</div>', unsafe_allow_html=True)

    with c_input_team:
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        st.markdown("### 2. FATOR HUMANO")
        
        # Slider de Público usa a capacidade do estádio selecionado no HERO
        i_publico_label = st.select_slider("Ocupação do Estádio", ["Portões Fechados", "Público Baixo", "Médio", "Cheio", "Caldeirão (Lotado)"])
        
        # Calcula número para mostrar ao usuário
        mapa_pub_visual = {"Portões Fechados": 0, "Público Baixo": 0.2, "Médio": 0.5, "Cheio": 0.8, "Caldeirão (Lotado)": 1.0}
        publico_real_show = int(stadium_capacity_h * mapa_pub_visual[i_publico_label])
        
        st.caption(f"👥 Público Estimado: **{publico_real_show:,}** (Base: {selected_stadium_name})")

        i_juiz = st.selectbox("Arbitragem", ["Neutro (Padrão)", "Caseiro (Pressionável)", "Rigoroso (Visitante Protegido)", "Liberal (Deixa Jogar)"])
        i_desfalque = st.selectbox("Desfalques Mandante", ["Elenco Completo", "Principal Craque Fora", "Vários Titulares Fora"])
        st.markdown('</div>', unsafe_allow_html=True)

    with c_exec:
        st.markdown("### 3. FORÇA DOS ELENCOS")
        st.caption("Ajuste o Momento Financeiro/Técnico Atual:")
        val_h = st.select_slider(f"💰 Elenco {t_home}", ["Crise", "Base", "Médio", "Forte", "Galáctico"], value="Forte")
        val_a = st.select_slider(f"💰 Elenco {t_away}", ["Crise", "Base", "Médio", "Forte", "Galáctico"], value="Forte")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 CALCULAR PREVISÃO FINAL"):
            with st.spinner(f"Simulando partida no {selected_stadium_name}... Aplicando {i_clima} e {i_juiz}..."):
                time.sleep(1.2)
                
                # 1. Tradução dos Sliders
                mapa_val = {"Crise": 5e6, "Base": 20e6, "Médio": 60e6, "Forte": 120e6, "Galáctico": 250e6}
                publico_final = float(publico_real_show)
                
                # Rodada Base
                rodada_base = 20
                if "Final" in i_jogo: rodada_base = 38
                
                # 2. Montagem do Payload Bruto
                raw_payload = {
                    "ano_campeonato": 2025,
                    "rodada": rodada_base,
                    "colocacao_mandante": 3,
                    "colocacao_visitante": 4,
                    "valor_equipe_titular_mandante": mapa_val[val_h],
                    "valor_equipe_titular_visitante": mapa_val[val_a],
                    "idade_media_titular_mandante": 27.5,
                    "idade_media_titular_visitante": 27.5,
                    "publico_max": publico_final
                }
                
                # 3. Configuração para Modificadores
                config_vars = {
                    "clima": i_clima, "gramado": i_gramado, 
                    "arbitragem": i_juiz, "tipo_jogo": i_jogo, 
                    "desfalques": i_desfalque
                }
                
                # 4. APLICAÇÃO DA INTELIGÊNCIA TÁTICA
                final_payload = calcular_modificadores(raw_payload, config_vars)
                
                # 5. Chamada à API
                try:
                    resp = requests.post(f"{API_URL}/prever", json=final_payload)
                    resultado = resp.json()["probabilidades"]
                    
                    st.session_state['resultado'] = resultado
                    st.session_state['config'] = config_vars
                    st.session_state['payload'] = final_payload
                    
                except Exception as e:
                    st.error(f"Erro de conexão com o cérebro da IA: {e}")

        # EXIBIÇÃO DO RESULTADO (VEREDITO)
        if 'resultado' in st.session_state:
            probs = st.session_state['resultado']
            config = st.session_state['config']
            dados = st.session_state['payload']
            
            narrativa = gerar_narrativa_premium(probs, t_home, t_away, config, dados)
            
            st.markdown(f"""
            <div class="veredito-box" style="border-color: {narrativa['cor']}">
                <h2 style="margin:0; color:{narrativa['cor']}; text-shadow: 0 0 15px {narrativa['cor']}; letter-spacing: 2px;">{narrativa['titulo']}</h2>
                <div style="margin-top:20px; font-size:1.2rem; line-height:1.6; color:#EEE">
                    {narrativa['texto'].replace('\n', '<br>')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            df_chart = pd.DataFrame({
                "Time": [t_home, "Empate", t_away],
                "Probabilidade": [probs['mandante'], probs['empate'], probs['visitante']],
                "Cor": [assets_h['colors'][0], "#888888", assets_a['colors'][0]]
            })
            
            fig = px.bar(df_chart, x="Probabilidade", y="Time", orientation='h', text_auto='.1%', 
                         color="Time", color_discrete_sequence=df_chart["Cor"].tolist())
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=16),
                showlegend=False,
                margin=dict(l=0, r=0, t=20, b=0),
                height=300,
                xaxis=dict(showgrid=False, range=[0, 1])
            )
            st.plotly_chart(fig, use_container_width=True)

# >>> ABA 2: ESTATÍSTICAS HISTÓRICAS
with tab_stat:
    if st.button("📥 CARREGAR DOSSIÊ DE CONFRONTO (HISTÓRICO)"):
        dados_hist = get_history(t_home, t_away)
        
        if dados_hist:
            stats = dados_hist['estatisticas']
            st.markdown("### 📜 Histórico Recente (Base 2003-2024)")
            
            col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
            col_kpi1.metric(f"Vitórias {t_home}", stats[t_home]['vitorias'], delta="Mandante")
            col_kpi2.metric("Empates", dados_hist['empates_totais'])
            col_kpi3.metric(f"Vitórias {t_away}", stats[t_away]['vitorias'], delta="Visitante", delta_color="inverse")
            
            st.markdown("---")
            
            # Gráfico Radar
            c_radar, c_table = st.columns([1, 1])
            
            with c_radar:
                st.markdown("### 🕸️ Comparativo de DNA")
                cat = ['Gols Pró', 'Gols Contra', 'Vitórias', 'Jogos']
                fig_r = go.Figure()
                
                fig_r.add_trace(go.Scatterpolar(
                    r=[stats[t_home]['gols_pro'], stats[t_home]['gols_contra'], stats[t_home]['vitorias']/10, 1],
                    theta=cat, fill='toself', name=t_home, line_color=assets_h['colors'][0]
                ))
                fig_r.add_trace(go.Scatterpolar(
                    r=[stats[t_away]['gols_pro'], stats[t_away]['gols_contra'], stats[t_away]['vitorias']/10, 1],
                    theta=cat, fill='toself', name=t_away, line_color=assets_a['colors'][0]
                ))
                fig_r.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, showticklabels=False),
                        bgcolor='rgba(0,0,0,0.3)'
                    ), 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    font=dict(color='white'),
                    margin=dict(l=40, r=40, t=40, b=40)
                )
                st.plotly_chart(fig_r, use_container_width=True)
            
            with c_table:
                st.markdown("### 📋 Tabela Detalhada")
                df_stats = pd.DataFrame({
                    "Métrica": ["Gols Marcados", "Gols Sofridos", "Saldo de Gols", "Derrotas"],
                    t_home: [
                        f"{stats[t_home]['gols_pro']:.2f}", 
                        f"{stats[t_home]['gols_contra']:.2f}",
                        f"{stats[t_home]['gols_pro'] - stats[t_home]['gols_contra']:.2f}",
                        stats[t_home]['derrotas']
                    ],
                    t_away: [
                        f"{stats[t_away]['gols_pro']:.2f}", 
                        f"{stats[t_away]['gols_contra']:.2f}",
                        f"{stats[t_away]['gols_pro'] - stats[t_away]['gols_contra']:.2f}",
                        stats[t_away]['derrotas']
                    ]
                })
                st.dataframe(df_stats, use_container_width=True, hide_index=True)
            
        else:
            st.warning("Dados históricos insuficientes para este confronto.")

# >>> ABA 3: METODOLOGIA
with tab_metodo:
    st.markdown("### 🧠 Como Funciona a Neural Engine?")
    st.info("""
    Este sistema utiliza um modelo de **Machine Learning (Random Forest)** treinado com mais de 7.000 partidas do Brasileirão (2003-2024).
    
    A "Camada Tática" (Frontend) atua como um pré-processador inteligente:
    1.  **Inputs do Usuário:** Clima, Juiz, Público.
    2.  **Tradução Matemática:** O código converte "Chuva" em penalidade técnica (-15%).
    3.  **Predição:** O modelo calcula a probabilidade com os dados ajustados.
    4.  **Narrativa:** O sistema gera texto explicativo baseado nas variáveis alteradas.
    """)