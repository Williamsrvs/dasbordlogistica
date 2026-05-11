import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import plotly.express as px
import plotly.graph_objects as go

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Torre de Controle · Logística",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS — DESIGN EDITORIAL INDUSTRIAL
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap');

/* ── BASE ── */
html, body, [class*="css"] {
    font-family: 'Instrument Sans', sans-serif;
}
.stApp {
    background-color: #F5F0E8;
    background-image:
        radial-gradient(circle at 20% 50%, rgba(210,185,145,0.15) 0%, transparent 50%),
        url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23C4B49A' fill-opacity='0.08'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background-color: #1A1A1A;
    border-right: 3px solid #E8C84A;
}
section[data-testid="stSidebar"] * {
    color: #F5F0E8 !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label {
    color: #A09880 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #2A2A2A !important;
    border-color: #3A3A3A !important;
    border-radius: 4px !important;
}

/* ── TÍTULOS PRINCIPAIS ── */
h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2.6rem !important;
    color: #1A1A1A !important;
    letter-spacing: -0.03em !important;
    line-height: 1.1 !important;
}
h2 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
    color: #1A1A1A !important;
    letter-spacing: -0.02em !important;
}
h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    color: #3A3530 !important;
    letter-spacing: -0.01em !important;
    text-transform: uppercase;
    font-size: 0.75rem !important;
    letter-spacing: 0.12em !important;
}

/* ── CARDS DE MÉTRICAS ── */
[data-testid="metric-container"] {
    background: #1E1C1A;
    border: 1.5px solid #3A3530;
    border-radius: 2px;
    padding: 20px 22px 18px 22px !important;
    box-shadow: 3px 3px 0px #3A3530;
    position: relative;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
[data-testid="metric-container"]:hover {
    transform: translate(-1px, -1px);
    box-shadow: 4px 4px 0px #B5860A;
    border-color: #B5860A;
}
[data-testid="metric-container"] label {
    color: #7A7060 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    font-weight: 500 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #F5F0E8 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.05em !important;
}

/* ── DIVISORES ── */
hr {
    border: none !important;
    border-top: 1.5px solid #D4C9B5 !important;
    margin: 1.5rem 0 !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1.5px solid #D4C9B5 !important;
    border-radius: 2px !important;
}

/* ── SEÇÃO LABEL ── */
.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #9A8E7A;
    margin-bottom: 4px;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.25rem;
    color: #1A1A1A;
    letter-spacing: -0.02em;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1.5px;
    background: #D4C9B5;
    display: inline-block;
}

/* ── AVISO ── */
.stAlert {
    border-radius: 2px !important;
    border-left: 4px solid #E8C84A !important;
}

/* ── PLOTLY ── */
.js-plotly-plot .plotly {
    border-radius: 2px;
}

/* ── CAPTION / RODAPÉ ── */
.stCaption {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important;
    color: #9A8E7A !important;
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PALETA — INDUSTRIAL / TIPOGRÁFICA
# ─────────────────────────────────────────────
CORES_STATUS = {
    "Finalizado":        "#2D6A3F",
    "Em trânsito":       "#1A4E8A",
    "Em Doca":           "#B5860A",
    "Carregando":        "#C45C2A",
    "Atrasado":          "#A32222",
    "Aguardando Pátio":  "#6B4C8A",
    "Agendado":          "#2A7AA8",
}
CORES_PRIORIDADE = {"Alta": "#A32222", "Média": "#B5860A", "Baixa": "#2D6A3F"}

PALETA = [
    "#1A4E8A", "#2D6A3F", "#B5860A", "#A32222", "#6B4C8A",
    "#C45C2A", "#2A7AA8", "#3D7A52", "#C48A1A", "#8A3A3A",
]

BG_PLOT    = "rgba(255,254,249,0)"
GRID_COLOR = "#E0D9CC"
FONT_COLOR = "#6A6055"
TITLE_COLOR= "#1A1A1A"
AXIS_COLOR = "#C4B49A"

def base_layout(**overrides):
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,254,249,0.6)",
        font=dict(color=FONT_COLOR, family="IBM Plex Mono, monospace", size=11),
        title_font=dict(color=TITLE_COLOR, size=13, family="Syne, sans-serif"),
        legend=dict(
            bgcolor="rgba(255,254,249,0.8)",
            bordercolor="#D4C9B5",
            borderwidth=1,
            font=dict(color=FONT_COLOR, size=10, family="IBM Plex Mono, monospace"),
        ),
        margin=dict(t=48, b=16, l=16, r=16),
        xaxis=dict(
            gridcolor=GRID_COLOR, linecolor=AXIS_COLOR, zeroline=False,
            tickfont=dict(color=FONT_COLOR, size=10),
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR, linecolor=AXIS_COLOR, zeroline=False,
            tickfont=dict(color=FONT_COLOR, size=10),
        ),
    )
    layout.update(overrides)
    return layout

# ─────────────────────────────────────────────
# DADOS
# ─────────────────────────────────────────────
@st.cache_data
def carregar_dados():
    df = pd.read_excel("torre_controle.xlsx")
    df["DATA_REGISTRO"]    = pd.to_datetime(df["DATA_REGISTRO"])
    df["DATA_AGENDAMENTO"] = pd.to_datetime(df["DATA_AGENDAMENTO"])
    df["CHEGADA_REAL"]     = pd.to_datetime(df["CHEGADA_REAL"])
    df["MES"]              = df["DATA_REGISTRO"].dt.month
    df["MES_NOME"]         = df["DATA_REGISTRO"].dt.strftime("%b/%Y")
    df["ANO"]              = df["DATA_REGISTRO"].dt.year
    df["DIA_SEMANA"]       = df["DATA_REGISTRO"].dt.day_name()
    df["HORA"]             = df["DATA_REGISTRO"].dt.hour
    df["ATRASO_CHEGADA"]   = (df["CHEGADA_REAL"] - df["DATA_AGENDAMENTO"]).dt.total_seconds() / 60
    df["SLA_OK"]           = df["TEMPO_TOTAL_MIN"] <= 240
    return df

df_base = carregar_dados()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 24px 0;">
        <div style="font-family: 'IBM Plex Mono', monospace; font-size: 9px; letter-spacing: 0.2em;
                    color: #E8C84A; text-transform: uppercase; margin-bottom: 6px;">
            Sistema de Monitoramento
        </div>
        <div style="font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.4rem;
                    color: #F5F0E8; letter-spacing: -0.02em; line-height: 1.2;">
            Torre de<br>Controle
        </div>
        <div style="font-family: 'Instrument Sans', sans-serif; font-size: 12px;
                    color: #8A8070; margin-top: 8px; font-style: italic;">
            Visibilidade ponta a ponta
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family: 'IBM Plex Mono', monospace; font-size: 9px; letter-spacing: 0.18em;
                color: #E8C84A; text-transform: uppercase; border-top: 1px solid #3A3A3A;
                padding-top: 16px; margin-bottom: 12px;">
        Filtros ativos
    </div>
    """, unsafe_allow_html=True)

    anos_disponiveis = sorted(df_base["ANO"].unique())
    clientes_lista   = ["Todos"] + sorted(df_base["CLIENTE"].unique())
    transport_lista  = ["Todas"] + sorted(df_base["TRANSPORTADORA"].unique())
    status_lista     = ["Todos"] + sorted(df_base["STATUS"].unique())
    prioridade_lista = ["Todas"] + sorted(df_base["PRIORIDADE"].unique())
    operacao_lista   = ["Todas"] + sorted(df_base["OPERACAO"].unique())

    sel_anos       = st.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)
    sel_cliente    = st.selectbox("Cliente", clientes_lista)
    sel_transport  = st.selectbox("Transportadora", transport_lista)
    sel_status     = st.selectbox("Status", status_lista)
    sel_prioridade = st.selectbox("Prioridade", prioridade_lista)
    sel_operacao   = st.selectbox("Operação", operacao_lista)

    st.markdown("""
    <div style="border-top: 1px solid #3A3A3A; margin-top: 24px; padding-top: 16px;
                font-family: 'IBM Plex Mono', monospace; font-size: 9px;
                color: #5A5550; letter-spacing: 0.1em;">
        v2.1 · dados atualizados<br>automaticamente
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILTROS
# ─────────────────────────────────────────────
df = df_base.copy()
if sel_anos:                   df = df[df["ANO"].isin(sel_anos)]
if sel_cliente    != "Todos":  df = df[df["CLIENTE"] == sel_cliente]
if sel_transport  != "Todas":  df = df[df["TRANSPORTADORA"] == sel_transport]
if sel_status     != "Todos":  df = df[df["STATUS"] == sel_status]
if sel_prioridade != "Todas":  df = df[df["PRIORIDADE"] == sel_prioridade]
if sel_operacao   != "Todas":  df = df[df["OPERACAO"] == sel_operacao]

# ─────────────────────────────────────────────
# CABEÇALHO
# ─────────────────────────────────────────────
col_title, col_sub = st.columns([3, 1])
with col_title:
    st.markdown("""
    <div style="padding: 8px 0 0 0;">
        <span style="font-family: 'IBM Plex Mono', monospace; font-size: 16px;
                    color: #9A8E7A; letter-spacing: 0.15em; text-transform: uppercase;">
            Cadeia de suprimentos · monitoramento em tempo real
        </span>
        <h1 style="font-family: 'Syne', sans-serif; font-weight: 800; font-size: 2.4rem;
                color: #1A1A1A; letter-spacing: -0.03em; margin: 4px 0 0 0; line-height: 1.1;">
            Torre de Controle<br>
            <span style="color: #B5860A;">Logístico</span>
        </h1>
    </div>
    """, unsafe_allow_html=True)
with col_sub:
    if not df.empty:
        st.markdown(f"""
        <div style="text-align: right; padding-top: 24px;">
            <span style="font-family: 'IBM Plex Mono', monospace; font-size: 14px;
                        color: #9A8E7A; letter-spacing: 0.1em; text-transform: uppercase;">
                registros carregados
            </span><br>
            <span style="font-family: 'Syne', sans-serif; font-weight: 800; font-size: 2rem;
                        color: #1A1A1A; letter-spacing: -0.04em;">
                {len(df):,}
            </span>
        </div>
        """, unsafe_allow_html=True)

st.divider()

if df.empty:
    st.warning("Nenhum registro encontrado com os filtros selecionados.")
    st.stop()

# ─────────────────────────────────────────────
# SEÇÃO 1 — KPIs
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-label">desempenho geral</div>
<div class="section-title">Indicadores principais</div>
""", unsafe_allow_html=True)

total        = len(df)
atrasados    = len(df[df["STATUS"] == "Atrasado"])
perc_atraso  = atrasados / total * 100 if total else 0
sla_ok       = df["SLA_OK"].sum()
perc_sla     = sla_ok / total * 100 if total else 0
tempo_medio  = df["TEMPO_TOTAL_MIN"].mean()
valor_total  = df["VALOR_CARGA"].sum()
peso_total   = df["PESO_KG"].sum()
ocorrencias  = len(df[df["OCORRENCIA"] != "Sem ocorrência"])
perc_ocorr   = ocorrencias / total * 100 if total else 0
tempo_espera = df["TEMPO_ESPERA_MIN"].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total de viagens",        f"{total:,}".replace(",", "."))
c2.metric("Viagens atrasadas",        f"{atrasados:,}".replace(",", "."),
        f"−{perc_atraso:.1f}% do total", delta_color="inverse")
c3.metric("SLA cumprido  ≤ 240 min",  f"{perc_sla:.1f}%",
        f"{sla_ok:,} viagens".replace(",", "."))
c4.metric("Ocorrências registradas",  f"{ocorrencias:,}".replace(",", "."),
        f"{perc_ocorr:.1f}% do total", delta_color="inverse")

st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)

c5, c6, c7, c8 = st.columns(4)
c5.metric("Tempo médio total",        f"{tempo_medio:.0f} min")
c6.metric("Espera média no pátio",    f"{tempo_espera:.0f} min")
c7.metric("Valor total das cargas",   f"R$ {valor_total/1e6:.1f} M")
c8.metric("Peso total transportado",  f"{peso_total/1e6:.1f} M kg")

st.divider()

# ─────────────────────────────────────────────
# SEÇÃO 2 — STATUS E PRIORIDADE
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-label">composição operacional</div>
<div class="section-title">Status e prioridade das viagens</div>
""", unsafe_allow_html=True)

col_a, col_b = st.columns([1.5, 1])

with col_a:
    status_count = df["STATUS"].value_counts().reset_index()
    status_count.columns = ["STATUS", "QTD"]
    status_count["COR"] = status_count["STATUS"].map(CORES_STATUS)

    fig = go.Figure(go.Bar(
        x=status_count["QTD"],
        y=status_count["STATUS"],
        orientation="h",
        marker_color=status_count["COR"],
        marker_line_color="rgba(0,0,0,0)",
        text=status_count["QTD"],
        textposition="outside",
        textfont=dict(color=FONT_COLOR, size=11, family="IBM Plex Mono, monospace"),
    ))
    fig.update_layout(
        **base_layout(
            title="Distribuição por status atual",
            height=330,
            xaxis_title="",
            yaxis_title="",
        )
    )
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    prio_count = df["PRIORIDADE"].value_counts().reset_index()
    prio_count.columns = ["PRIORIDADE", "QTD"]
    cores_prio = [CORES_PRIORIDADE.get(p, "#888") for p in prio_count["PRIORIDADE"]]

    fig2 = go.Figure(go.Pie(
        labels=prio_count["PRIORIDADE"],
        values=prio_count["QTD"],
        marker=dict(colors=cores_prio, line=dict(color="#F5F0E8", width=3)),
        hole=0.6,
        textinfo="label+percent",
        textfont=dict(color=FONT_COLOR, size=10, family="IBM Plex Mono, monospace"),
        insidetextorientation="radial",
    ))
    fig2.update_layout(
        **base_layout(
            title="Prioridade das cargas",
            height=330,
            showlegend=False,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
        )
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
# SEÇÃO 3 — ANÁLISE TEMPORAL
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-label">evolução histórica</div>
<div class="section-title">Volume e atrasos por período</div>
""", unsafe_allow_html=True)

df_mensal = (
    df.groupby(["ANO", "MES", "MES_NOME"])
    .agg(
        VIAGENS=("ID_VIAGEM", "count"),
        ATRASADOS=("STATUS", lambda x: (x == "Atrasado").sum()),
        TEMPO_MEDIO=("TEMPO_TOTAL_MIN", "mean"),
        VALOR=("VALOR_CARGA", "sum"),
    )
    .reset_index()
    .sort_values(["ANO", "MES"])
)
df_mensal["PERC_ATRASO"] = df_mensal["ATRASADOS"] / df_mensal["VIAGENS"] * 100

fig_tempo = make_subplots(specs=[[{"secondary_y": True}]])
fig_tempo.add_trace(go.Bar(
    x=df_mensal["MES_NOME"], y=df_mensal["VIAGENS"],
    name="Viagens",
    marker=dict(color=PALETA[0], opacity=0.75, line=dict(color="rgba(0,0,0,0)")),
), secondary_y=False)
fig_tempo.add_trace(go.Scatter(
    x=df_mensal["MES_NOME"], y=df_mensal["PERC_ATRASO"],
    name="% de atrasos",
    mode="lines+markers",
    line=dict(color=CORES_STATUS["Atrasado"], width=2),
    marker=dict(size=5, color=CORES_STATUS["Atrasado"], symbol="circle"),
), secondary_y=True)

layout_tempo = base_layout(
    title="Viagens mensais e percentual de atrasos",
    height=330,
    legend=dict(
        orientation="h", y=1.08, x=0,
        bgcolor="rgba(0,0,0,0)",
        font=dict(color=FONT_COLOR, size=10, family="IBM Plex Mono, monospace"),
    ),
)
fig_tempo.update_layout(**layout_tempo)
fig_tempo.update_yaxes(
    title_text="Viagens", secondary_y=False,
    gridcolor=GRID_COLOR, tickfont=dict(color=FONT_COLOR, size=10),
    title_font=dict(color=FONT_COLOR, size=10),
)
fig_tempo.update_yaxes(
    title_text="% Atrasos", secondary_y=True,
    gridcolor="rgba(0,0,0,0)",
    tickfont=dict(color=CORES_STATUS["Atrasado"], size=10),
    title_font=dict(color=CORES_STATUS["Atrasado"], size=10),
)
st.plotly_chart(fig_tempo, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
# SEÇÃO 4 — TEMPOS OPERACIONAIS
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-label">eficiência operacional</div>
<div class="section-title">Análise de tempos por parceiro</div>
""", unsafe_allow_html=True)

col_c, col_d = st.columns(2)

with col_c:
    fig_box = px.box(
        df, x="TRANSPORTADORA", y="TEMPO_TOTAL_MIN",
        color="TRANSPORTADORA",
        color_discrete_sequence=PALETA,
        title="Tempo total por transportadora",
    )
    fig_box.update_traces(
        marker=dict(outliercolor=FONT_COLOR, size=3),
        line=dict(width=1.5),
    )
    fig_box.update_layout(
        **base_layout(height=360, showlegend=False,
                    xaxis_tickangle=-20, xaxis_title="", yaxis_title="Minutos")
    )
    st.plotly_chart(fig_box, use_container_width=True)

with col_d:
    tempo_cliente = df.groupby("CLIENTE").agg(
        ESPERA=("TEMPO_ESPERA_MIN", "mean"),
        DOCA=("TEMPO_DOCA_MIN", "mean"),
    ).reset_index().sort_values("ESPERA", ascending=True)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=tempo_cliente["ESPERA"], y=tempo_cliente["CLIENTE"],
        orientation="h", name="Espera no pátio",
        marker=dict(color=PALETA[0], opacity=0.85, line=dict(color="rgba(0,0,0,0)")),
    ))
    fig_bar.add_trace(go.Bar(
        x=tempo_cliente["DOCA"], y=tempo_cliente["CLIENTE"],
        orientation="h", name="Tempo em doca",
        marker=dict(color="#B5860A", opacity=0.85, line=dict(color="rgba(0,0,0,0)")),
    ))
    fig_bar.update_layout(
        **base_layout(
            showlegend=True, barmode="stack", height=360,
            title="Espera + doca por cliente (min)",
            xaxis_title="Minutos", yaxis_title="",
        )
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
# SEÇÃO 5 — OCORRÊNCIAS
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-label">gestão de riscos</div>
<div class="section-title">Ocorrências e desvios operacionais</div>
""", unsafe_allow_html=True)

col_e, col_f = st.columns([1, 1.4])

with col_e:
    ocorr_count = (
        df[df["OCORRENCIA"] != "Sem ocorrência"]["OCORRENCIA"]
        .value_counts().reset_index()
    )
    ocorr_count.columns = ["OCORRENCIA", "QTD"]

    cores_ocorr = ["#A32222", "#B5860A", "#C45C2A", "#6B4C8A"]

    fig_ocorr = go.Figure(go.Pie(
        labels=ocorr_count["OCORRENCIA"], values=ocorr_count["QTD"],
        marker=dict(colors=cores_ocorr, line=dict(color="#F5F0E8", width=3)),
        hole=0.5,
        textinfo="label+percent",
        textfont=dict(color=FONT_COLOR, size=10, family="IBM Plex Mono, monospace"),
    ))
    fig_ocorr.update_layout(
        **base_layout(
            title="Tipos de ocorrência",
            height=350,
            showlegend=False,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
        )
    )
    st.plotly_chart(fig_ocorr, use_container_width=True)

with col_f:
    ocorr_cliente = (
        df[df["OCORRENCIA"] != "Sem ocorrência"]
        .groupby(["CLIENTE", "OCORRENCIA"])
        .size().reset_index(name="QTD")
    )
    fig_heat = px.bar(
        ocorr_cliente, x="CLIENTE", y="QTD", color="OCORRENCIA",
        barmode="stack",
        color_discrete_sequence=cores_ocorr,
        title="Ocorrências acumuladas por cliente",
    )
    fig_heat.update_layout(
        **base_layout(height=350, xaxis_title="", yaxis_title="Ocorrências", xaxis_tickangle=-20)
    )
    st.plotly_chart(fig_heat, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
# SEÇÃO 6 — FLUXO ORIGEM → DESTINO
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-label">mapeamento de rotas</div>
<div class="section-title">Fluxo de cargas por origem e destino</div>
""", unsafe_allow_html=True)

fluxo = (
    df.groupby(["UF_ORIGEM", "UF_DESTINO"])
    .agg(QTD=("ID_VIAGEM", "count"), VALOR=("VALOR_CARGA", "sum"))
    .reset_index().sort_values("QTD", ascending=False).head(20)
)

labels_sankey = sorted(set(fluxo["UF_ORIGEM"].tolist() + fluxo["UF_DESTINO"].tolist()))
fig_sankey = go.Figure(data=[dict(
    type="sankey",
    node=dict(
        pad=18, thickness=16,
        line=dict(color="#D4C9B5", width=0.8),
        color=PALETA[0],
        label=labels_sankey,
        hovertemplate="%{label}<extra></extra>",
    ),
    link=dict(
        source=[labels_sankey.index(o) for o in fluxo["UF_ORIGEM"]],
        target=[labels_sankey.index(d) for d in fluxo["UF_DESTINO"]],
        value=fluxo["QTD"].tolist(),
        color="rgba(26,78,138,0.18)",
        hovertemplate="%{source.label} → %{target.label}<br>%{value} viagens<extra></extra>",
    ),
)])
fig_sankey.update_layout(
    **base_layout(title="Top 20 rotas · volume de viagens", height=430)
)
st.plotly_chart(fig_sankey, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
# SEÇÃO 7 — FROTA
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-label">gestão de frota</div>
<div class="section-title">Análise por tipo de veículo</div>
""", unsafe_allow_html=True)

col_g, col_h = st.columns(2)

with col_g:
    veiculo_status = df.groupby(["TIPO_VEICULO", "STATUS"]).size().reset_index(name="QTD")
    fig_vei = px.bar(
        veiculo_status, x="TIPO_VEICULO", y="QTD", color="STATUS",
        color_discrete_map=CORES_STATUS, barmode="stack",
        title="Status das viagens por tipo de veículo",
    )
    fig_vei.update_layout(
        **base_layout(height=330, xaxis_title="", yaxis_title="Viagens")
    )
    st.plotly_chart(fig_vei, use_container_width=True)

with col_h:
    peso_veiculo = df.groupby("TIPO_VEICULO").agg(
        PESO_MEDIO=("PESO_KG", "mean"),
        VALOR_MEDIO=("VALOR_CARGA", "mean"),
    ).reset_index()

    fig_scatter = px.scatter(
        peso_veiculo, x="PESO_MEDIO", y="VALOR_MEDIO", text="TIPO_VEICULO",
        size="PESO_MEDIO", color="TIPO_VEICULO",
        color_discrete_sequence=PALETA,
        title="Peso médio × valor médio por tipo de veículo",
    )
    fig_scatter.update_traces(
        textposition="top center",
        textfont=dict(color=FONT_COLOR, size=10, family="IBM Plex Mono, monospace"),
        marker=dict(opacity=0.85, line=dict(color="#F5F0E8", width=1.5)),
    )
    fig_scatter.update_layout(
        **base_layout(height=330, xaxis_title="Peso médio (kg)", yaxis_title="Valor médio (R$)", showlegend=False)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
# SEÇÃO 8 — DOCAS E HEATMAP HORÁRIO
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-label">utilização de infraestrutura</div>
<div class="section-title">Docas e distribuição horária</div>
""", unsafe_allow_html=True)

col_i, col_j = st.columns(2)

with col_i:
    doca_uso = (
        df.groupby("DOCA")
        .agg(VIAGENS=("ID_VIAGEM", "count"), TEMPO_MEDIO=("TEMPO_DOCA_MIN", "mean"))
        .reset_index().sort_values("VIAGENS", ascending=False).head(15)
    )

    fig_doca = go.Figure(go.Bar(
        x=doca_uso["DOCA"], y=doca_uso["VIAGENS"],
        marker=dict(color=PALETA[0], opacity=0.8, line=dict(color="rgba(0,0,0,0)")),
        text=doca_uso["VIAGENS"], textposition="outside",
        textfont=dict(color=FONT_COLOR, size=10, family="IBM Plex Mono, monospace"),
    ))
    fig_doca.update_layout(
        **base_layout(title="Top 15 docas por volume", height=330,
                    xaxis_title="", yaxis_title="Viagens", xaxis_tickangle=-45)
    )
    st.plotly_chart(fig_doca, use_container_width=True)

with col_j:
    hora_uso = df.groupby("HORA").size().reset_index(name="QTD")
    pico = lambda h: (6 <= h <= 9) or (17 <= h <= 20)
    cores_hora = [CORES_STATUS["Atrasado"] if pico(h) else PALETA[0] for h in hora_uso["HORA"]]

    fig_hora = go.Figure(go.Bar(
        x=hora_uso["HORA"], y=hora_uso["QTD"],
        marker=dict(color=cores_hora, opacity=0.85, line=dict(color="rgba(0,0,0,0)")),
        text=hora_uso["QTD"], textposition="outside",
        textfont=dict(color=FONT_COLOR, size=9, family="IBM Plex Mono, monospace"),
    ))
    fig_hora.update_layout(
        **base_layout(
            title="Registros por hora  ·  vermelho = horário de pico",
            height=330, xaxis_title="Hora", yaxis_title="Viagens",
            xaxis=dict(dtick=1, gridcolor=GRID_COLOR, tickfont=dict(color=FONT_COLOR, size=10)),
        )
    )
    st.plotly_chart(fig_hora, use_container_width=True)

st.divider()

# ─────────────────────────────────────────────
# SEÇÃO 9 — RANKING TRANSPORTADORAS
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-label">ranking de parceiros</div>
<div class="section-title">Performance das transportadoras</div>
""", unsafe_allow_html=True)

rank = df.groupby("TRANSPORTADORA").agg(
    VIAGENS=("ID_VIAGEM", "count"),
    TEMPO_MEDIO=("TEMPO_TOTAL_MIN", "mean"),
    ESPERA_MEDIA=("TEMPO_ESPERA_MIN", "mean"),
    PESO_TOTAL=("PESO_KG", "sum"),
    VALOR_TOTAL=("VALOR_CARGA", "sum"),
    ATRASOS=("STATUS", lambda x: (x == "Atrasado").sum()),
    OCORRENCIAS=("OCORRENCIA", lambda x: (x != "Sem ocorrência").sum()),
).reset_index()
rank["% Atraso"]     = (rank["ATRASOS"] / rank["VIAGENS"] * 100).round(1)
rank["% Ocorrência"] = (rank["OCORRENCIAS"] / rank["VIAGENS"] * 100).round(1)
rank["Valor (R$ M)"] = (rank["VALOR_TOTAL"] / 1e6).round(2)
rank["Tempo (min)"]  = rank["TEMPO_MEDIO"].round(0).astype(int)
rank["Espera (min)"] = rank["ESPERA_MEDIA"].round(0).astype(int)
rank = rank.sort_values("VIAGENS", ascending=False).reset_index(drop=True)
rank.index += 1

st.dataframe(
    rank[["TRANSPORTADORA", "VIAGENS", "Tempo (min)", "Espera (min)",
        "% Atraso", "% Ocorrência", "Valor (R$ M)"]].rename(
        columns={"TRANSPORTADORA": "Transportadora", "VIAGENS": "Viagens"}
    ),
    use_container_width=True, height=290,
)

st.divider()

# ─────────────────────────────────────────────
# SEÇÃO 10 — TABELA DE VIAGENS RECENTES
# ─────────────────────────────────────────────
st.markdown("""
<div class="section-label">detalhe operacional</div>
<div class="section-title">Últimas 100 viagens registradas</div>
""", unsafe_allow_html=True)

cols_exibir = [
    "ID_VIAGEM", "CLIENTE", "TRANSPORTADORA", "TIPO_VEICULO",
    "OPERACAO", "STATUS", "PRIORIDADE", "OCORRENCIA",
    "TEMPO_TOTAL_MIN", "VALOR_CARGA", "UF_ORIGEM", "UF_DESTINO",
]
df_recentes = (
    df[cols_exibir]
    .sort_values("TEMPO_TOTAL_MIN", ascending=False)
    .head(100)
    .rename(columns={
        "ID_VIAGEM": "ID", "TIPO_VEICULO": "Veículo", "OPERACAO": "Operação",
        "OCORRENCIA": "Ocorrência", "TEMPO_TOTAL_MIN": "Tempo (min)",
        "VALOR_CARGA": "Valor (R$)", "UF_ORIGEM": "Origem", "UF_DESTINO": "Destino",
    })
)
st.dataframe(df_recentes, use_container_width=True, height=380)

# ─────────────────────────────────────────────
# RODAPÉ
# ─────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center;
            font-family: 'IBM Plex Mono', monospace; font-size: 16px; color: #9A8E7A;
            letter-spacing: 0.08em;">
    <span>Torre de Controle Logístico · v2.1</span>
    <span>Date Analytics - Williams Rodrigues 2026</span>   
</div>
""", unsafe_allow_html=True)