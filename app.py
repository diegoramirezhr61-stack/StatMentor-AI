"""
StatMentor - Asistente Virtual de Estadística Aplicada
Universidad Mariano Gálvez de Guatemala - Facultad de Ingeniería
"""
import math
import random
import re
from collections import Counter
import traceback
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from scipy import stats

# ===================== DATOS DEL EQUIPO (EDÍTALOS) =====================
INTEGRANTES = ["Diego Alejandro Ramirez Aquino (2990-25-12692)", "Cristel Marleny Caná Regino (2990-25-12719)"]
ASIGNATURA = "Estadística Aplicada"
SECCION = "Sección A"
# ========================================================================

st.set_page_config(page_title="StatMentor", page_icon="📊", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }
.stApp { background: #F7F6FB; }
.block-container { padding-top: 1.2rem; max-width: 1100px; }
header[data-testid="stHeader"] { background: transparent; }

/* ---------- Barra lateral ---------- */
section[data-testid="stSidebar"] { background: linear-gradient(180deg,#1B0F3B 0%,#2A1465 100%); }
section[data-testid="stSidebar"] * { color: #F3EEFF !important; }
section[data-testid="stSidebar"] [role="radiogroup"] label { padding: 8px 12px; border-radius: 10px; width: 100%; }
section[data-testid="stSidebar"] [role="radiogroup"] label:hover { background: rgba(255,255,255,.10); }
section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) { background: linear-gradient(90deg,#7D2AE8,#4F6BF0); }
section[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display: none; }

/* ---------- Banner ---------- */
.hero { background: linear-gradient(100deg,#7D2AE8 0%,#4F6BF0 55%,#00C4CC 100%);
        border-radius: 18px; padding: 20px 26px; color: #fff; margin-bottom: 14px; }
.hero h1 { color:#fff; margin:0; font-size: 1.7rem; font-weight: 700; letter-spacing:-.5px; }
.hero p { color: rgba(255,255,255,.9); margin: 4px 0 0; font-size: .92rem; }
.legend { display:flex; gap:10px; flex-wrap:wrap; margin: 0 0 16px; font-size:.78rem; }
.legend span { padding:5px 12px; border-radius:999px; font-weight:600; }
.lg-d { background:#F1EAFE; color:#5B1FB5; border:1.5px solid #CDB4F7; }
.lg-p { background:#fff; color:#000; border:1.5px solid #111; }
.lg-r { background:#EFEDE8; color:#2B2A27; border:1.5px solid #C9C3B6; }

h2 { color:#111; font-weight:700 !important; letter-spacing:-.4px; }

/* ---------- DATOS (entradas): lavanda ---------- */
div[data-baseweb="textarea"], div[data-baseweb="input"], div[data-baseweb="base-input"],
div[data-baseweb="select"] > div, div[data-baseweb="textarea"] textarea, div[data-baseweb="base-input"] input {
    background: #F1EAFE !important; color: #1B0F3B !important; }
div[data-baseweb="textarea"], div[data-baseweb="input"], div[data-baseweb="select"] > div {
    border: 1.5px solid #CDB4F7 !important; border-radius: 12px !important; }
.stTextArea label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stRadio label p, .stCheckbox label p {
    font-weight: 600; color: #5B1FB5; }

/* ---------- Botones ---------- */
.stButton > button[kind="primary"] { background: linear-gradient(90deg,#7D2AE8,#4F6BF0); color:#fff; border:0;
    border-radius: 12px; padding: .55rem 1.6rem; font-weight:600; }
.stButton > button[kind="primary"]:hover { filter: brightness(1.08); }
.stButton > button[kind="secondary"] { border-radius: 12px; border: 1.5px solid #CDB4F7; font-weight:600; }


/* ---------- PROCEDIMIENTO: tarjetas claras y legibles ---------- */
div[class*="st-key-proc_"] {
    background: #FFFFFF !important;
    border: 1px solid #D9CCFA !important;
    border-left: 5px solid #4F6BF0 !important;
    border-radius: 14px !important;
    padding: 20px 24px !important;
    margin-top: 14px;
    margin-bottom: 16px;
    box-shadow: 0 3px 12px rgba(63, 35, 120, 0.06);
}

div[class*="st-key-proc_"] * {
    color: #292638 !important;
}

div[class*="st-key-proc_"] h1,
div[class*="st-key-proc_"] h2,
div[class*="st-key-proc_"] h3,
div[class*="st-key-proc_"] h4 {
    color: #4F46A5 !important;
    font-weight: 700 !important;
}

div[class*="st-key-proc_"] .tag {
    color: #4F6BF0 !important;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.2px;
    margin-bottom: 10px;
}

div[class*="st-key-proc_"] p,
div[class*="st-key-proc_"] li {
    line-height: 1.75;
}

div[class*="st-key-proc_"] code {
    background: #F1EAFE !important;
    color: #5B1FB5 !important;
    border-radius: 5px;
    padding: 3px 6px;
}

/* ---------- RESULTADOS: tarjetas modernas ---------- */
div[class*="st-key-res_"] {
    background: linear-gradient(135deg, #FFFFFF 0%, #F3EEFF 100%);
    border: 1px solid #D9CCFA;
    border-left: 5px solid #7D2AE8;
    border-radius: 14px;
    padding: 18px 22px;
    margin: 16px 0;
    box-shadow: 0 3px 12px rgba(63, 35, 120, 0.08);
}

div[class*="st-key-res_"] * {
    color: #292638 !important;
}

div[class*="st-key-res_"] .tag {
    color: #6D28D9 !important;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.2px;
    margin-bottom: 8px;
}

div[class*="st-key-res_"] p {
    font-size: 1.02rem;
    line-height: 1.7;
}


/* ---------- Notas / interpretación ---------- */
div[class*="st-key-note_"] { background:#fff; border:1px dashed #A9A39A; border-radius:14px; padding:12px 18px; margin:10px 0; }
div[class*="st-key-note_"] * { color:#4A4843 !important; }

.tag { font-size:.68rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:4px; }
div[class*="st-key-proc_"] .tag { color:#000 !important; }
div[class*="st-key-res_"] .tag { color:#6B665C !important; }
div[class*="st-key-note_"] .tag { color:#8A857B !important; }


/* ---------- CORRECCIÓN DE CONTRASTE GENERAL ---------- */
.stApp {
    background: #F7F6FB !important;
    color: #292638 !important;
}

/* Títulos de los módulos */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6 {
    color: #292638 !important;
}

/* Texto normal, párrafos y listas */
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li,
.stApp [data-testid="stMarkdownContainer"] strong,
.stApp [data-testid="stMarkdownContainer"] em {
    color: #343044;
}

/* Tablas de los módulos */
.stApp [data-testid="stTable"] th,
.stApp [data-testid="stTable"] td {
    color: #292638 !important;
}

/* Mantener blanco el texto del banner superior */
.stApp .hero h1,
.stApp .hero p {
    color: #FFFFFF !important;
}


/* ---------- TEXTO EN CAMPOS OSCUROS ---------- */

/* Áreas de texto */
.stApp div[data-baseweb="textarea"] textarea {
    background-color: #262630 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    caret-color: #FFFFFF !important;
}

/* Campos de texto */
.stApp div[data-baseweb="input"] input,
.stApp div[data-baseweb="base-input"] input {
    background-color: #262630 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    caret-color: #FFFFFF !important;
}

/* Texto que aparece al escribir o seleccionar */
.stApp textarea::placeholder,
.stApp input::placeholder {
    color: #C5C5D0 !important;
    -webkit-text-fill-color: #C5C5D0 !important;
    opacity: 1 !important;
}

/* Corrección definitiva de áreas de texto */
.stApp textarea,
.stApp textarea.st-ae,
.stApp [data-testid="stTextArea"] textarea,
.stApp [data-baseweb="textarea"] textarea {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    background: #262630 !important;
    caret-color: #FFFFFF !important;
    opacity: 1 !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    text-shadow: none !important;
}

/* Evitar que el texto seleccionado desaparezca */
.stApp textarea::selection {
    color: #FFFFFF !important;
    background: #5B3AAE !important;
    -webkit-text-fill-color: #FFFFFF !important;
}


/* =========================================
   STATMENTOR AI - INTERACCIONES Y ANIMACIONES
   ========================================= */

/* Transiciones generales */
.stApp button,
.stApp a,
.stApp input,
.stApp textarea,
.stApp select,
.stApp [data-testid="stMetric"],
.stApp [data-testid="stExpander"],
.stApp [data-testid="stDataFrame"],
.stApp [data-testid="stTable"] {
    transition:
        background-color 0.22s ease,
        color 0.22s ease,
        border-color 0.22s ease,
        box-shadow 0.22s ease,
        transform 0.22s ease;
}

/* Botones principales */
.stApp button[kind="primary"] {
    border: 1px solid transparent !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(108, 77, 230, 0.16);
}

/* Efecto al pasar el cursor */
@media (hover: hover) and (pointer: fine) {
    .stApp button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 18px rgba(80, 55, 150, 0.17);
        border-color: #8B72EB !important;
    }

    .stApp button[kind="primary"]:hover {
        filter: brightness(1.07);
        box-shadow: 0 8px 20px rgba(108, 77, 230, 0.28);
    }

    /* Tarjetas de métricas */
    .stApp [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 22px rgba(80, 55, 150, 0.10);
        border-radius: 12px;
    }

    /* Paneles desplegables */
    .stApp [data-testid="stExpander"]:hover {
        border-color: #A99AE8;
    }

    /* Opciones del menú lateral */
    [data-testid="stSidebar"] button:hover {
        background-color: rgba(255, 255, 255, 0.13) !important;
        transform: translateX(3px);
    }
}

/* Campos de entrada */
.stApp input:focus,
.stApp textarea:focus,
.stApp [data-baseweb="select"]:focus-within,
.stApp [data-baseweb="input"]:focus-within,
.stApp [data-baseweb="textarea"]:focus-within {
    border-color: #8B72EB !important;
    box-shadow: 0 0 0 2px rgba(139, 114, 235, 0.22) !important;
}

/* Pestañas de navegación */
.stApp button[data-baseweb="tab"] {
    border-radius: 10px 10px 0 0 !important;
}

.stApp button[data-baseweb="tab"][aria-selected="true"] {
    font-weight: 700 !important;
}

/* Tablas: resaltado suave de filas */
.stApp [data-testid="stTable"] tbody tr,
.stApp [data-testid="stDataFrame"] {
    transition: background-color 0.2s ease;
}

/* Aparición suave del contenido principal */
@keyframes statmentorEntrada {
    from {
        opacity: 0.88;
        transform: translateY(5px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.stApp [data-testid="stMainBlockContainer"] {
    animation: statmentorEntrada 0.35s ease-out;
}

/* Accesibilidad: respetar preferencia de reducir movimiento */
@media (prefers-reduced-motion: reduce) {
    .stApp *,
    .stApp *::before,
    .stApp *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
        transform: none !important;
    }
}


/* ===== MENÚ LATERAL STATMENTOR ===== */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #292044 0%,
        #39275F 55%,
        #493078 100%
    ) !important;
    border-right: 1px solid rgba(255,255,255,0.10);
}

/* Texto general del menú */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] .stCaption {
    color: #F2EEFF !important;
}

/* Marca */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 4px 24px;
}

.sidebar-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 46px;
    height: 46px;
    flex-shrink: 0;
    border-radius: 15px;
    color: white;
    font-size: 25px;
    font-weight: 800;
    background: linear-gradient(135deg, #A78BFA, #6C4DE6);
    box-shadow: 0 5px 18px rgba(167,139,250,0.3);
}

.sidebar-brand-title {
    color: white;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.sidebar-brand-subtitle {
    color: #C9BDF4;
    font-size: 12px;
    margin-top: 2px;
}

.sidebar-section-label {
    color: #C9BDF4;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin: 8px 0 12px;
}

/* Opciones del radio: mantener legible el texto */
[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 7px;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: 10px 12px;
    border-radius: 11px;
    border: 1px solid transparent;
    transition: background-color 0.2s ease,
                transform 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
}

/* Hover de cada módulo */
@media (hover: hover) and (pointer: fine) {
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(255,255,255,0.10);
        border-color: rgba(210,195,255,0.25);
        transform: translateX(4px);
    }
}

/* Módulo seleccionado */
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(
        100deg,
        rgba(167,139,250,0.28),
        rgba(108,77,230,0.20)
    );
    border-color: rgba(196,181,253,0.60);
    box-shadow: inset 3px 0 0 #C4B5FD;
}

/* Indicador de selección */
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* Separador */
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15);
    margin: 20px 0;
}

/* Información del curso */
.sidebar-info {
    padding: 14px;
    margin: 10px 0 20px;
    border-radius: 13px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
}

.sidebar-info-label {
    color: #C9BDF4;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 5px;
}

.sidebar-info-value {
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 600;
    overflow-wrap: anywhere;
    margin-bottom: 12px;
}

.sidebar-info-value:last-child {
    margin-bottom: 0;
}

/* Respetar la preferencia de reducir movimiento */
@media (prefers-reduced-motion: reduce) {
    [data-testid="stSidebar"] * {
        transition: none !important;
        animation: none !important;
    }
}


/* Botón para usar la pregunta seleccionada */
div.st-key-pregunta_ia button,
.stButton > button {
    background: linear-gradient(135deg, #7046E8, #3977F6) !important;
    color: #FFFFFF !important;
    border: 1px solid #7046E8 !important;
    border-radius: 12px !important;
    transition: all 0.25s ease !important;
}

/* Mantener texto blanco al pasar el mouse */
div.st-key-pregunta_ia button:hover,
.stButton > button:hover {
    background: linear-gradient(135deg, #5932C4, #285ACB) !important;
    color: #FFFFFF !important;
    border-color: #5932C4 !important;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(112, 70, 232, 0.25);
}

/* Evitar que el texto cambie de color */
.stButton > button p,
.stButton > button span {
    color: #FFFFFF !important;
}


/* Flecha para contraer o expandir la barra lateral */
[data-testid="stSidebarCollapseButton"] button,
[data-testid="stExpandSidebarButton"] button {
    color: #BFA7FF !important;
}

/* Color del icono de la flecha */
[data-testid="stSidebarCollapseButton"] button svg,
[data-testid="stExpandSidebarButton"] button svg {
    color: #BFA7FF !important;
    fill: #BFA7FF !important;
    stroke: #BFA7FF !important;
}

/* Efecto al pasar el cursor */
[data-testid="stSidebarCollapseButton"] button:hover,
[data-testid="stExpandSidebarButton"] button:hover {
    background-color: rgba(191, 167, 255, 0.18) !important;
    color: #FFFFFF !important;
}


/* Flechas y botones de la barra superior de Streamlit */
.stApp button[kind="header"],
.stApp button[data-testid="stBaseButton-header"] {
    color: #D6C5FF !important;
}

/* Icono SVG de la flecha */
.stApp button[kind="header"] svg,
.stApp button[data-testid="stBaseButton-header"] svg {
    color: #D6C5FF !important;
    fill: #D6C5FF !important;
    stroke: #D6C5FF !important;
}

/* Mejor visibilidad al pasar el cursor */
.stApp button[kind="header"]:hover,
.stApp button[data-testid="stBaseButton-header"]:hover {
    background-color: rgba(214, 197, 255, 0.2) !important;
}


/* Cambiar el color de los iconos de la barra superior */
[data-testid="stAppViewContainer"] header button svg,
[data-testid="stHeader"] button svg,
[data-testid="stSidebarCollapsedControl"] button svg,
[data-testid="stSidebarCollapseButton"] svg {
    color: #D6C5FF !important;
    fill: #D6C5FF !important;
    stroke: #D6C5FF !important;
}

/* Color del botón al pasar el cursor */
[data-testid="stAppViewContainer"] header button:hover,
[data-testid="stHeader"] button:hover,
[data-testid="stSidebarCollapsedControl"] button:hover {
    background-color: rgba(214, 197, 255, 0.2) !important;
}

/* Flecha de la barra lateral: color más intenso */
[data-testid="stIconMaterial"] {
    color: #B18AFF !important;
    opacity: 1 !important;
    font-weight: bold !important;
}

/* Al pasar el cursor, la flecha resalta más */
[data-testid="stIconMaterial"]:hover {
    color: #FFFFFF !important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

_ctr = [0]
_depth = [0]



def resultado(txt):
    _ctr[0] += 1

    with st.container(key=f"res_{_ctr[0]}"):
        st.markdown(
            '<div class="tag">✦ RESULTADO</div>',
            unsafe_allow_html=True
        )

        st.markdown(txt)



def nota(txt):
    _ctr[0] += 1
    with st.container(key=f"note_{_ctr[0]}"):
        st.markdown('<div class="tag">Interpretación / nota</div>', unsafe_allow_html=True)
        st.markdown(txt)


def procedimiento(f):
    """Envuelve una función de cálculo en la tarjeta blanca 'Procedimiento'."""
    def wrapper(*a, **k):
        if _depth[0] > 0:          # evita tarjetas anidadas
            return f(*a, **k)
        _ctr[0] += 1
        _depth[0] += 1
        try:
            with st.container(key=f"proc_{_ctr[0]}"):
                st.markdown('<div class="tag">Procedimiento</div>', unsafe_allow_html=True)
                return f(*a, **k)
        finally:
            _depth[0] -= 1
    return wrapper


# ----------------------------- UTILIDADES -----------------------------
def fmt(v, d=4):
    return f"{v:.{d}f}"


def parse_numbers(text, nombre="los datos"):
    """Convierte texto en lista de floats. Devuelve None si hay error."""
    tokens = [t for t in re.split(r"[,;\s]+", text.strip()) if t]
    if not tokens:
        st.warning(f"Faltan datos: ingresa {nombre} separados por coma, espacio o salto de línea.")
        return None
    nums, bad = [], []
    for t in tokens:
        try:
            v = float(t)
            if not math.isfinite(v):
                raise ValueError
            nums.append(v)
        except ValueError:
            bad.append(t)
    if bad:
        st.error(f"Valores no numéricos en {nombre}: {', '.join(bad)}. "
                 "Usa punto como separador decimal (ej. 2.5).")
        return None
    return nums


def sum_txt(vals, maxn=10):
    s = [fmt(v) for v in vals]
    if len(s) <= maxn:
        return " + ".join(s)
    return " + ".join(s[:4]) + r" + \cdots + " + s[-1]


def pasos(titulo):
    st.markdown(f"#### {titulo}")


# ------------------------- ESTADÍSTICA DESCRIPTIVA ---------------------
def render_desc(data, sample=True, unit=""):
    x = np.array(data, float)
    n = len(x)
    u = f" {unit}" if unit else ""
    mean = x.mean()

    pasos("1. Media aritmética")
    st.latex(r"\bar{x}=\frac{\sum x_i}{n}")
    st.latex(rf"\bar{{x}}=\frac{{{sum_txt(x)}}}{{{n}}}=\frac{{{fmt(x.sum())}}}{{{n}}}={fmt(mean)}")

    pasos("2. Mediana")
    xs = np.sort(x)
    med = float(np.median(x))
    st.write("Datos ordenados:", ", ".join(fmt(v, 3).rstrip("0").rstrip(".") for v in xs))
    if n % 2 == 1:
        st.write(f"n = {n} es impar → la mediana es el dato central (posición {(n + 1) // 2}) = **{fmt(med)}**")
    else:
        a, b = xs[n // 2 - 1], xs[n // 2]
        st.latex(rf"Me=\frac{{{fmt(a)}+{fmt(b)}}}{{2}}={fmt(med)}")

    pasos("3. Moda")
    cnt = Counter(np.round(x, 10))
    mx = max(cnt.values())
    if mx == 1:
        modas_txt = "No hay moda (todos los valores aparecen una sola vez)"
    else:
        modas = sorted(k for k, c in cnt.items() if c == mx)
        modas_txt = f"Moda = {', '.join(fmt(m, 3) for m in modas)} (aparece {mx} veces)"
    st.write(modas_txt)

    pasos("4. Rango")
    st.latex(rf"R=x_{{max}}-x_{{min}}={fmt(x.max())}-{fmt(x.min())}={fmt(x.max() - x.min())}")

    if n < 2:
        st.warning("Con un solo dato no se puede calcular varianza ni desviación estándar.")
        return

    pasos("5. Varianza y desviación estándar")
    ss = float(((x - mean) ** 2).sum())
    if n <= 15:
        st.dataframe(pd.DataFrame({
            "xᵢ": x, "xᵢ − x̄": x - mean, "(xᵢ − x̄)²": (x - mean) ** 2}).round(4),
            hide_index=True)
    st.write(f"Σ(xᵢ − x̄)² = **{fmt(ss)}**")
    var_s, var_p = ss / (n - 1), ss / n
    sd_s, sd_p = math.sqrt(var_s), math.sqrt(var_p)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Muestral (divide entre n − 1)**")
        st.latex(r"s^2=\frac{\sum (x_i-\bar{x})^2}{n-1}")
        st.latex(rf"s^2=\frac{{{fmt(ss)}}}{{{n - 1}}}={fmt(var_s)}")
        st.latex(rf"s=\sqrt{{{fmt(var_s)}}}={fmt(sd_s)}")
    with c2:
        st.markdown("**Poblacional (divide entre n)**")
        st.latex(r"\sigma^2=\frac{\sum (x_i-\mu)^2}{N}")
        st.latex(rf"\sigma^2=\frac{{{fmt(ss)}}}{{{n}}}={fmt(var_p)}")
        st.latex(rf"\sigma=\sqrt{{{fmt(var_p)}}}={fmt(sd_p)}")

    pasos("6. Coeficiente de variación y cuartiles")
    if mean != 0:
        cv = sd_s / abs(mean) * 100
        st.latex(rf"CV=\frac{{s}}{{|\bar{{x}}|}}\times100={fmt(cv, 2)}\%")
    else:
        cv = None
        st.warning("La media es 0: el coeficiente de variación no está definido.")
    q1, q3 = np.percentile(x, [25, 75])
    st.write(f"Q1 = {fmt(q1)}, Q3 = {fmt(q3)}, RIC = Q3 − Q1 = {fmt(q3 - q1)} "
             "(método de interpolación lineal)")

    sd_sel, lab = (sd_s, "muestral s") if sample else (sd_p, "poblacional σ")
    resultado(f"**Resultado final:** media = {fmt(mean)}{u}; mediana = {fmt(med)}{u}; "
               f"desviación estándar {lab} = {fmt(sd_sel)}{u}; rango = {fmt(x.max() - x.min())}{u}.")

    pasos("Interpretación")
    txt = (f"En promedio, los datos se alejan unos {fmt(sd_sel, 3)}{u} de la media ({fmt(mean, 3)}{u}). ")
    if cv is not None:
        nivel = "baja" if cv < 10 else "moderada" if cv < 30 else "alta"
        txt += f"El CV de {fmt(cv, 1)}% indica una variabilidad relativa **{nivel}**. "
    if abs(mean - med) > 0.1 * (sd_s or 1):
        txt += "La media y la mediana difieren notablemente: puede haber asimetría o valores atípicos."
    else:
        txt += "La media y la mediana son parecidas: la distribución es aproximadamente simétrica."
    nota(txt)
    st.caption("Se usa la desviación **muestral** cuando los datos son una muestra de un conjunto mayor "
               "(caso típico de mediciones); la **poblacional** cuando se tienen todos los datos del universo.")


# --------------------------- DATOS EXPERIMENTALES ----------------------
UNITS = {
    "Corriente": {"A": 1, "mA": 1e-3, "µA": 1e-6},
    "Voltaje": {"V": 1, "mV": 1e-3, "kV": 1e3},
    "Longitud": {"m": 1, "cm": 1e-2, "mm": 1e-3, "km": 1e3},
    "Masa": {"kg": 1, "g": 1e-3, "mg": 1e-6},
    "Tiempo": {"s": 1, "ms": 1e-3, "min": 60, "h": 3600},
    "Sin conversión": {"(sin unidad)": 1},
}


def render_exp(data, mag, u_in, u_out, resol=0.0):
    x = np.array(data, float)
    n = len(x)
    if u_in != u_out:
        f = UNITS[mag][u_in] / UNITS[mag][u_out]
        st.write(f"Conversión: 1 {u_in} = {f:g} {u_out}")
        x = x * f
        st.write("Datos convertidos:", ", ".join(fmt(v) for v in x), u_out)
    unit = "" if u_out == "(sin unidad)" else u_out
    if n < 2:
        st.warning("Se necesitan al menos 2 mediciones para estimar la incertidumbre.")
        return
    mean, s = x.mean(), x.std(ddof=1)
    uA = s / math.sqrt(n)
    pasos("Media, desviación y error estándar")
    st.latex(rf"\bar{{x}}={fmt(mean)},\quad s={fmt(s)}")
    st.latex(rf"u_A=\frac{{s}}{{\sqrt{{n}}}}=\frac{{{fmt(s)}}}{{\sqrt{{{n}}}}}={fmt(uA)}")
    u_tot = uA
    if resol and resol > 0:
        uB = resol / (2 * math.sqrt(3))
        u_tot = math.sqrt(uA ** 2 + uB ** 2)
        st.latex(rf"u_B=\frac{{\text{{resolución}}}}{{2\sqrt3}}={fmt(uB)},\quad "
                 rf"u_c=\sqrt{{u_A^2+u_B^2}}={fmt(u_tot)}")
    resultado(f"**Resultado:** x = ({fmt(mean, 3)} ± {fmt(u_tot, 3)}) {unit}  "
               f"(media ± incertidumbre estándar, n = {n})")
    nota(f"Error relativo: {fmt(u_tot / abs(mean) * 100, 2) if mean else '—'} %. "
            "Una incertidumbre pequeña respecto a la media indica mediciones precisas y repetibles.")
    render_desc(x.tolist(), True, unit)



# ----------------------------- TABLAS Y GRÁFICAS -----------------------
def render_freq(data, k=None):
    x = np.array(data, float)
    n = len(x)

    if n < 5:
        st.warning("Se recomiendan al menos 5 datos para una tabla de frecuencias.")
        return

    R = x.max() - x.min()

    if R == 0:
        st.error("Todos los datos son iguales; no se puede agrupar en clases.")
        return

    pasos("Número de clases (regla de Sturges) y amplitud")

    k_st = math.ceil(1 + 3.322 * math.log10(n))
    st.latex(
        rf"k=1+3.322\log_{{10}}(n)=1+3.322\log_{{10}}({n})"
        rf"\approx {k_st}"
    )

    k = k or k_st
    w = R / k

    st.latex(
        rf"R={fmt(x.max())}-{fmt(x.min())}={fmt(R)},\quad "
        rf"A=\frac{{R}}{{k}}=\frac{{{fmt(R)}}}{{{k}}}={fmt(w)}"
    )

    edges = np.linspace(x.min(), x.max(), k + 1)
    fi, _ = np.histogram(x, bins=edges)
    marca = (edges[:-1] + edges[1:]) / 2

    clases = [
        f"[{edges[i]:.3f} , {edges[i + 1]:.3f}"
        + (")" if i < k - 1 else "]")
        for i in range(k)
    ]

    df = pd.DataFrame({
        "Clase": clases,
        "Marca": marca.round(3),
        "fᵢ": fi,
        "fr": (fi / n).round(4),
        "fr %": (fi / n * 100).round(2),
        "Fᵢ": np.cumsum(fi),
        "Fr %": (np.cumsum(fi) / n * 100).round(2)
    })

    st.markdown("### 📋 Tabla de frecuencias")
    st.caption(f"Total de observaciones: {n} · Número de clases: {k}")

    st.dataframe(
        df,
        hide_index=True,
        width="stretch"
    )

    # Histograma con diseño mejorado
    st.markdown("### 📊 Distribución de los datos")

    fig, ax = plt.subplots(figsize=(10, 5))

    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FAF9FF")

    ax.hist(
        x,
        bins=edges,
        color="#6C4DE6",
        edgecolor="#FFFFFF",
        linewidth=2,
        alpha=0.95
    )

    ax.set_xlabel("Valor", fontsize=11, color="#292638", labelpad=10)
    ax.set_ylabel("Frecuencia", fontsize=11, color="#292638", labelpad=10)
    ax.set_title(
        "Histograma de frecuencias",
        fontsize=16,
        fontweight="bold",
        color="#292638",
        pad=16
    )

    ax.grid(axis="y", linestyle="--", alpha=0.25, color="#777777")
    ax.set_axisbelow(True)

    ax.tick_params(axis="both", colors="#343044", labelsize=10)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#D8D4E8")
    ax.spines["bottom"].set_color("#D8D4E8")

    fig.tight_layout(pad=2.0)

    st.pyplot(fig, width="stretch")
    plt.close(fig)

    indice = int(np.argmax(fi))

    nota(
        f"La clase más frecuente es {clases[indice]} "
        f"con {fi[indice]} datos ({fi[indice] / n * 100:.1f}%)."
    )


# ------------------------------- PROBABILIDAD --------------------------
def plot_normal(mu, sigma, lo, hi):
    xs = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 400)
    ys = stats.norm.pdf(xs, mu, sigma)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(xs, ys)
    m = (xs >= lo) & (xs <= hi)
    ax.fill_between(xs[m], ys[m], alpha=0.4)
    ax.set_xlabel("x"); ax.set_title("Distribución normal")
    st.pyplot(fig); plt.close(fig)


def render_normal(mu, sigma, kind, a, b=None):
    if sigma <= 0:
        st.error("σ debe ser mayor que 0.")
        return
    st.latex(r"Z=\frac{X-\mu}{\sigma}")
    if kind == "P(X < a)":
        z = (a - mu) / sigma
        p = stats.norm.cdf(z)
        st.latex(rf"Z=\frac{{{fmt(a, 3)}-{fmt(mu, 3)}}}{{{fmt(sigma, 3)}}}={fmt(z, 3)}")
        st.latex(rf"P(X<{a:g})=P(Z<{z:.2f})=\Phi({z:.2f})={fmt(p)}")
        plot_normal(mu, sigma, -np.inf, a)
        resultado(f"**Respuesta:** P(X < {a:g}) = {fmt(p)} ({p * 100:.2f}%)")
    elif kind == "P(X > a)":
        z = (a - mu) / sigma
        p = 1 - stats.norm.cdf(z)
        st.latex(rf"Z={fmt(z, 3)};\quad P(X>{a:g})=1-\Phi({z:.2f})=1-{fmt(stats.norm.cdf(z))}={fmt(p)}")
        plot_normal(mu, sigma, a, np.inf)
        resultado(f"**Respuesta:** P(X > {a:g}) = {fmt(p)} ({p * 100:.2f}%)")
    elif kind == "P(a < X < b)":
        if b is None or a >= b:
            st.error("Error: se requiere a < b.")
            return
        z1, z2 = (a - mu) / sigma, (b - mu) / sigma
        p = stats.norm.cdf(z2) - stats.norm.cdf(z1)
        st.latex(rf"Z_1={fmt(z1, 3)},\ Z_2={fmt(z2, 3)}")
        st.latex(rf"P=\Phi({z2:.2f})-\Phi({z1:.2f})={fmt(stats.norm.cdf(z2))}-{fmt(stats.norm.cdf(z1))}={fmt(p)}")
        plot_normal(mu, sigma, a, b)
        resultado(f"**Respuesta:** P({a:g} < X < {b:g}) = {fmt(p)} ({p * 100:.2f}%)")
    else:  # percentil
        if not 0 < a < 1:
            st.error("La probabilidad debe estar entre 0 y 1 (excluyendo los extremos).")
            return
        z = stats.norm.ppf(a)
        x = mu + z * sigma
        st.latex(rf"Z=\Phi^{{-1}}({a:g})={fmt(z, 3)};\quad x=\mu+Z\sigma={fmt(mu, 3)}+({fmt(z, 3)})({fmt(sigma, 3)})={fmt(x)}")
        plot_normal(mu, sigma, -np.inf, x)
        resultado(f"**Respuesta:** el valor con P(X < x) = {a:g} es x = {fmt(x)}")


def render_binom(n, p, k, kind):
    if n != int(n) or n < 1 or k != int(k) or not 0 <= k <= n:
        st.error("n debe ser entero ≥ 1 y k un entero entre 0 y n.")
        return
    if not 0 <= p <= 1:
        st.error("p debe estar entre 0 y 1.")
        return
    n, k = int(n), int(k)
    st.latex(r"P(X=k)=\binom{n}{k}p^k(1-p)^{n-k}")
    pk = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
    st.latex(rf"P(X={k})=\binom{{{n}}}{{{k}}}({p:g})^{{{k}}}({1 - p:g})^{{{n - k}}}={fmt(pk)}")
    if kind == "P(X = k)":
        res, txt = pk, f"P(X = {k})"
    elif kind == "P(X ≤ k)":
        res, txt = stats.binom.cdf(k, n, p), f"P(X ≤ {k})"
        st.write("Se suman las probabilidades de 0 hasta k.")
    else:
        res, txt = stats.binom.sf(k - 1, n, p), f"P(X ≥ {k})"
        st.write("P(X ≥ k) = 1 − P(X ≤ k − 1).")
    resultado(f"**Respuesta:** {txt} = {fmt(res)}  |  Media = np = {n * p:.3f}, "
               f"desv. = √(np(1−p)) = {math.sqrt(n * p * (1 - p)):.3f}")


def render_clasica(fav, tot, pa, pb, pab):
    if tot is not None:
        if tot <= 0 or fav < 0 or fav > tot:
            st.error("Casos favorables deben estar entre 0 y los casos posibles (>0).")
            return
        st.latex(rf"P(A)=\frac{{\text{{favorables}}}}{{\text{{posibles}}}}=\frac{{{fav:g}}}{{{tot:g}}}={fmt(fav / tot)}")
        resultado(f"**Respuesta:** P(A) = {fmt(fav / tot)}")
    if pa is not None:
        if not all(0 <= v <= 1 for v in (pa, pb, pab)) or pab > min(pa, pb):
            st.error("Valores inconsistentes: deben estar en [0,1] y P(A∩B) ≤ mín(P(A),P(B)).")
            return
        u = pa + pb - pab
        st.latex(rf"P(A\cup B)=P(A)+P(B)-P(A\cap B)={pa:g}+{pb:g}-{pab:g}={fmt(u)}")
        msg = f"**Respuesta:** P(A∪B) = {fmt(u)}"
        if pb > 0:
            msg += f";  P(A|B) = P(A∩B)/P(B) = {fmt(pab / pb)}"
        resultado(msg)
        st.caption("Independientes si P(A∩B) = P(A)·P(B): "
                   + ("sí lo son." if math.isclose(pab, pa * pb, abs_tol=1e-9) else "no lo son."))


# --------------------------- CORRELACIÓN Y REGRESIÓN -------------------
def render_reg(x, y, x0=None, xl="x", yl="y"):
    if x is None or y is None:
        return
    if len(x) != len(y):
        st.error(f"Error: {xl} tiene {len(x)} datos e {yl} tiene {len(y)}. Deben ser la misma cantidad.")
        return
    n = len(x)
    if n < 3:
        st.warning("Se necesitan al menos 3 pares de datos.")
        return
    x, y = np.array(x, float), np.array(y, float)
    mx, my = x.mean(), y.mean()
    sxx, syy = ((x - mx) ** 2).sum(), ((y - my) ** 2).sum()
    sxy = ((x - mx) * (y - my)).sum()
    if sxx == 0 or syy == 0:
        st.error("Una de las variables es constante (varianza 0): no se puede calcular r ni la regresión.")
        return
    r = sxy / math.sqrt(sxx * syy)
    b = sxy / sxx
    a = my - b * mx
    pasos("Sumas necesarias")
    st.latex(rf"\bar{{x}}={fmt(mx)},\ \bar{{y}}={fmt(my)},\ S_{{xx}}={fmt(sxx)},\ S_{{yy}}={fmt(syy)},\ S_{{xy}}={fmt(sxy)}")
    pasos("Coeficiente de correlación")
    st.latex(r"r=\frac{S_{xy}}{\sqrt{S_{xx}S_{yy}}}")
    st.latex(rf"r=\frac{{{fmt(sxy)}}}{{\sqrt{{({fmt(sxx)})({fmt(syy)})}}}}={fmt(r)},\quad r^2={fmt(r * r)}")
    pasos("Recta de regresión  ŷ = a + b·x")
    st.latex(rf"b=\frac{{S_{{xy}}}}{{S_{{xx}}}}=\frac{{{fmt(sxy)}}}{{{fmt(sxx)}}}={fmt(b)}")
    st.latex(rf"a=\bar{{y}}-b\bar{{x}}={fmt(my)}-({fmt(b)})({fmt(mx)})={fmt(a)}")
    resultado(f"**Recta:** ŷ = {fmt(a)} + {fmt(b)}·x   |   r = {fmt(r)}   |   r² = {fmt(r * r)}")
    fuerza = ("muy fuerte" if abs(r) >= 0.9 else "fuerte" if abs(r) >= 0.7
              else "moderada" if abs(r) >= 0.4 else "débil" if abs(r) >= 0.2 else "casi nula")
    sentido = "positiva (al aumentar x, y tiende a aumentar)" if r > 0 else "negativa (al aumentar x, y tiende a disminuir)"
    nota(f"Correlación lineal **{fuerza}** y {sentido}. "
            f"El {r * r * 100:.1f}% de la variación de y se explica por la relación lineal con x. "
            f"Por cada unidad que aumenta x, y cambia en promedio {fmt(b, 3)}. "
            "Recuerda: correlación no implica causalidad.")
    
    # Gráfica de correlación y regresión
    fig, ax = plt.subplots(figsize=(10, 5))

    # Fondo de la gráfica
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FAF9FF")

    # Puntos de los datos
    ax.scatter(
        x, y,
        color="#6C4DE6",
        edgecolors="white",
        linewidths=1.5,
        s=90,
        label="Datos observados",
        zorder=3
    )

    # Línea de regresión
    xx = np.linspace(x.min(), x.max(), 100)
    ax.plot(
        xx, a + b * xx,
        color="#E0528A",
        linewidth=2.5,
        label="Recta de regresión",
        zorder=2
    )

    # Punto de predicción, si se ingresó un valor
    if x0 is not None:
        yp = a + b * x0
        ax.scatter(
            [x0], [yp],
            color="#159D78",
            edgecolors="white",
            linewidths=1.5,
            marker="*",
            s=250,
            label="Predicción",
            zorder=4
        )

    # Títulos y etiquetas
    ax.set_xlabel(xl, fontsize=12, fontweight="bold", color="#29243D")
    ax.set_ylabel(yl, fontsize=12, fontweight="bold", color="#29243D")
    ax.set_title(
        "Diagrama de dispersión y recta de regresión",
        fontsize=14,
        fontweight="bold",
        color="#29243D",
        pad=15
    )

    # Cuadrícula y bordes
    ax.grid(True, linestyle="--", alpha=0.25, color="#8A7BAE")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#D6D0E5")
    ax.spines["bottom"].set_color("#D6D0E5")
    ax.tick_params(colors="#39334D")

    # Leyenda
    ax.legend(
        frameon=True,
        facecolor="white",
        edgecolor="#E2DCEF",
        fontsize=10
    )

    fig.tight_layout(pad=2)
    st.pyplot(fig, width="stretch")
    plt.close(fig)

    if x0 is not None:
        yp = a + b * x0
        st.latex(rf"\hat{{y}}({x0:g})={fmt(a)}+({fmt(b)})({x0:g})={fmt(yp)}")
        if x0 < x.min() or x0 > x.max():
            st.warning("⚠️ Extrapolación: x queda fuera del rango de los datos; la predicción es poco confiable.")


render_desc = procedimiento(render_desc)
render_exp = procedimiento(render_exp)
render_freq = procedimiento(render_freq)
render_normal = procedimiento(render_normal)
render_binom = procedimiento(render_binom)
render_clasica = procedimiento(render_clasica)
render_reg = procedimiento(render_reg)


# ------------------------------- EJEMPLOS ------------------------------
EJEMPLOS = [
    ("Corriente eléctrica (ejemplo de prueba)",
     "Mediciones de corriente (A): 2.1, 2.3, 2.2, 2.4 y 2.0. Calcula media, desviación estándar muestral e interpreta.",
     lambda: render_desc([2.1, 2.3, 2.2, 2.4, 2.0], True, "A")),
    ("Tiempo de caída",
     "Tiempos (s) de caída de una esfera: 0.52, 0.49, 0.51, 0.50, 0.53, 0.48. Resolución del cronómetro 0.01 s. Reporta x ± u.",
     lambda: render_exp([0.52, 0.49, 0.51, 0.50, 0.53, 0.48], "Tiempo", "s", "s", 0.01)),
    ("Conversión de unidades",
     "Longitudes en mm: 152, 150, 153, 151, 149. Exprésalas en cm y calcula la media y la incertidumbre.",
     lambda: render_exp([152, 150, 153, 151, 149], "Longitud", "mm", "cm", 1)),
    ("Notas: poblacional vs muestral",
     "Notas de 6 estudiantes: 70, 85, 90, 65, 80, 75. Calcula σ si son toda la población.",
     lambda: render_desc([70, 85, 90, 65, 80, 75], False)),
    ("Moda y dispersión",
     "Datos: 4, 5, 5, 6, 7, 5, 8, 6, 9. Calcula todas las medidas descriptivas.",
     lambda: render_desc([4, 5, 5, 6, 7, 5, 8, 6, 9], True)),
    ("Tabla de frecuencias e histograma",
     "Estaturas (cm) de 24 personas. Construye la tabla de frecuencias y el histograma.",
     lambda: render_freq([158, 162, 165, 170, 172, 168, 175, 160, 163, 167, 169, 171,
                          174, 178, 166, 164, 161, 173, 169, 170, 177, 159, 168, 172])),
    ("Normal: P(X < x)",
     "La resistencia de una pieza sigue N(μ=70, σ=10). Calcula P(X < 85).",
     lambda: render_normal(70, 10, "P(X < a)", 85)),
    ("Normal: entre dos valores",
     "X ~ N(70, 10). Calcula P(60 < X < 80).",
     lambda: render_normal(70, 10, "P(a < X < b)", 60, 80)),
    ("Normal: percentil",
     "X ~ N(100, 15). ¿Qué valor deja a la izquierda el 90% de los datos?",
     lambda: render_normal(100, 15, "Percentil (hallar x)", 0.90)),
    ("Binomial",
     "Se lanza una moneda 10 veces. Probabilidad de obtener exactamente 3 caras.",
     lambda: render_binom(10, 0.5, 3, "P(X = k)")),
    ("Unión y condicional",
     "P(A)=0.5, P(B)=0.4, P(A∩B)=0.2. Calcula P(A∪B) y P(A|B).",
     lambda: render_clasica(None, None, 0.5, 0.4, 0.2)),
    ("Ley de Ohm: regresión",
     "Voltaje (V) 1,2,3,4,5 y corriente (A) 0.21, 0.40, 0.62, 0.79, 1.02. Ajusta la recta y predice para 6 V.",
     lambda: render_reg([1, 2, 3, 4, 5], [0.21, 0.40, 0.62, 0.79, 1.02], 6, "Voltaje (V)", "Corriente (A)")),
]


# -------------------------------- PRÁCTICA -----------------------------
TIPOS = ["Media", "Mediana", "Desviación estándar muestral",
         "Probabilidad normal P(X < x)", "Probabilidad binomial P(X = k)", "Coeficiente de correlación r"]


def gen_question(kind):
    q = {"kind": kind, "alt": None}
    if kind in ("Media", "Mediana", "Desviación estándar muestral"):
        d = [random.randint(10, 50) for _ in range(random.randint(5, 7))]
        if kind == "Media":
            q.update(ans=float(np.mean(d)), tol=0.01,
                     sol=f"Media = {sum(d)} / {len(d)} = {np.mean(d):.4f}")
        elif kind == "Mediana":
            q.update(ans=float(np.median(d)), tol=0.01,
                     sol=f"Ordenados: {sorted(d)} → mediana = {np.median(d):.4f}")
        else:
            q.update(ans=float(np.std(d, ddof=1)), tol=0.01, alt=float(np.std(d, ddof=0)),
                     sol=f"x̄ = {np.mean(d):.4f}; Σ(xᵢ−x̄)² = {((np.array(d) - np.mean(d)) ** 2).sum():.4f}; "
                         f"s = √(Σ/(n−1)) = {np.std(d, ddof=1):.4f}")
        q["text"] = f"Calcula la **{kind.lower()}** de: {d} (redondea a 2 decimales)."
    elif kind.startswith("Probabilidad normal"):
        mu, sg = random.choice([50, 60, 70, 100]), random.choice([5, 8, 10, 15])
        x = mu + random.choice([-1, -0.5, 0.5, 1, 1.5, 2]) * sg
        z = (x - mu) / sg
        q.update(ans=float(stats.norm.cdf(z)), tol=0.005,
                 text=f"X ~ N(μ={mu}, σ={sg}). Calcula P(X < {x:g}) (4 decimales).",
                 sol=f"z = ({x:g} − {mu})/{sg} = {z:.2f}; P = Φ({z:.2f}) = {stats.norm.cdf(z):.4f}")
    elif kind.startswith("Probabilidad binomial"):
        n, p = random.randint(5, 10), random.choice([0.3, 0.5, 0.6])
        k = random.randint(0, n)
        ans = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
        q.update(ans=ans, tol=0.002,
                 text=f"X ~ Binomial(n={n}, p={p}). Calcula P(X = {k}) (4 decimales).",
                 sol=f"C({n},{k})·{p}^{k}·{1 - p:.1f}^{n - k} = {ans:.4f}")
    else:
        x = list(range(1, 6))
        y = [round(2 * v + random.uniform(-2, 2), 1) for v in x]
        r = float(np.corrcoef(x, y)[0, 1])
        q.update(ans=r, tol=0.01,
                 text=f"Con x = {x} e y = {y}, calcula r (2 decimales).",
                 sol=f"r = Sxy / √(Sxx·Syy) = {r:.4f}")
    return q



def page_practica():
    st.markdown("""
    <div style="
        background: linear-gradient(120deg, #30204F, #6544B5, #8B5CF6);
        padding: 28px;
        border-radius: 20px;
        margin-bottom: 22px;
        box-shadow: 0 10px 25px rgba(76,48,130,0.16);
    ">
        <div style="
            color: #E9DFFF;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 10px;
        ">MÓDULO 07 · PON A PRUEBA TUS CONOCIMIENTOS</div>
        <h1 style="
            color: #FFFFFF !important;
            background: transparent !important;
            font-size: 30px;
            margin: 0 0 10px 0;
        ">🎯 Práctica interactiva</h1>
        <p style="
            color: #F0EAFE !important;
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        ">Resuelve preguntas de estadística, comprueba tus respuestas
        y aprende de cada intento mediante retroalimentación.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧠 Configura tu práctica")

    kind = st.selectbox(
        "Tema del ejercicio",
        TIPOS,
        key="practica_tipo"
    )

    if "q" not in st.session_state or st.session_state.q["kind"] != kind:
        st.session_state.q = gen_question(kind)
        st.session_state.setdefault("score", [0, 0])

    q = st.session_state.q

    st.markdown("""
    <div style="
        background: #F0EAFE;
        border: 1px solid #D9CCFA;
        border-radius: 12px;
        padding: 12px;
        color: #4C367D;
        font-size: 13px;
        line-height: 1.7;
        margin: 10px 0 16px 0;
    ">
        <b>📌 Instrucciones</b><br>
        Lee el problema, realiza tus cálculos e introduce una respuesta
        numérica. Puedes usar punto o coma para separar los decimales.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📝 Tu ejercicio")

    st.markdown(
        f"""
        <div style="
            background: #FFFFFF;
            border: 1px solid #DDD2F8;
            border-left: 5px solid #7950D9;
            border-radius: 16px;
            padding: 22px;
            margin: 8px 0 18px 0;
            box-shadow: 0 5px 16px rgba(76,48,130,0.07);
            color: #30204F;
            font-size: 16px;
            line-height: 1.8;
        ">
            {q["text"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    resp = st.text_input(
        "Tu respuesta numérica",
        placeholder="Ej. 0.8413",
        key="resp_" + str(id(q))
    )

    c1, c2 = st.columns(2)

    with c1:
        verificar = st.button(
            "✅ Verificar respuesta",
            type="primary",
            width="stretch",
            key="btn_verificar_practica"
        )

    with c2:
        nueva = st.button(
            "🔄 Nueva pregunta",
            width="stretch",
            key="btn_nueva_practica"
        )

    if verificar:
        try:
            val = float(resp.replace(",", ".").strip())
        except ValueError:
            st.warning("Escribe un número válido, por ejemplo: 0.8413.")
            return

        st.session_state.score[1] += 1

        if abs(val - q["ans"]) <= q["tol"]:
            st.session_state.score[0] += 1
            resultado(
                f"✅ ¡Correcto! La respuesta es {q['ans']:.4f}."
            )
        else:
            st.error(
                f"❌ La respuesta no coincide. "
                f"La respuesta correcta es {q['ans']:.4f}."
            )

            if (
                q["alt"] is not None
                and abs(val - q["alt"]) <= q["tol"]
            ):
                st.warning(
                    "Parece que dividiste entre n en lugar de n − 1 "
                    "(desviación poblacional)."
                )

        nota("**Procedimiento:** " + q["sol"])

    if nueva:
        st.session_state.q = gen_question(kind)
        st.rerun()

    a, t = st.session_state.get("score", [0, 0])
    porcentaje = (a / t * 100) if t > 0 else 0

    st.markdown("---")
    st.markdown("### 🏆 Tu progreso")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Aciertos", a)

    with c2:
        st.metric("Intentos", t)

    with c3:
        st.metric("Porcentaje de aciertos", f"{porcentaje:.1f}%")

    if t > 0:
        st.progress(porcentaje / 100)
        st.caption(
            "¡Sigue practicando! Cada ejercicio te ayuda a dominar "
            "los conceptos de Estadística Aplicada."
        )
    else:
        st.caption(
            "Tu progreso aparecerá aquí cuando respondas tu primer ejercicio."
        )

def page_inicio():
    st.markdown("""
    <div style="
        background: linear-gradient(120deg, #30204F, #6544B5, #8B5CF6);
        padding: 32px;
        border-radius: 22px;
        color: #FFFFFF;
        margin-bottom: 20px;
        box-shadow: 0 12px 30px rgba(76, 48, 130, 0.20);
    ">
        <div style="
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
            color: #E9DFFF;
            margin-bottom: 12px;
        ">PLATAFORMA ACADÉMICA</div>
        <h1 style="
            color: #FFFFFF !important;
            background: transparent !important;
            margin: 0 0 12px 0;
            padding: 0;
            font-size: 32px;
        ">¡Bienvenido a StatMentor AI!</h1>
        <p style="
            color: #F0EAFE !important;
            background: transparent !important;
            font-size: 15px;
            line-height: 1.7;
            margin-bottom: 20px;
        ">Aprende estadística paso a paso, analiza tus datos
        y comprende cada resultado.</p>
        <div style="
            display: inline-block;
            padding: 8px 12px;
            border-radius: 9px;
            background: rgba(255,255,255,0.15);
            color: #FFFFFF;
            font-size: 12px;
        ">Fórmula → Procedimiento → Resultado → Interpretación</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid #E8E0F8;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 24px;
        color: #292638;
    ">
        <div style="font-size: 18px; font-weight: 800; color: #39265F;">
            🎓 Universidad Mariano Gálvez de Guatemala
        </div>
        <p style="color: #6B6480; margin-bottom: 8px;">
            Facultad de Ingeniería · {ASIGNATURA} · {SECCION}
        </p>
        <p style="color: #6B6480; margin-bottom: 0;">
            <b>Integrantes:</b><br>
            {INTEGRANTES[0]}<br>
            {INTEGRANTES[1]}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Explora tus herramientas")
    st.caption("Selecciona un módulo desde el menú lateral para comenzar.")

    modulos = [
        ("📊", "Estadística descriptiva",
         "Media, mediana, moda, varianza y desviación estándar."),
        ("🔬", "Datos experimentales",
         "Mediciones, unidades, conversiones e incertidumbre."),
        ("📈", "Tablas y gráficas",
         "Tablas de frecuencias e histogramas."),
        ("🎲", "Probabilidad",
         "Probabilidad clásica, binomial y distribución normal."),
        ("📉", "Correlación y regresión",
         "Relaciones entre variables y predicciones."),
        ("📚", "Ejercicios de ejemplo",
         "Ejercicios resueltos paso a paso."),
        ("🎯", "Práctica",
         "Resuelve ejercicios y revisa tus respuestas."),
        ("💡", "Interpretación",
         "Comprende los resultados estadísticos."),
        ("🤖", "Asistente IA",
         "Resuelve dudas con explicaciones de estadística.")
    ]

    columnas = st.columns(3)

    for i, (icono, titulo, descripcion) in enumerate(modulos):
        with columnas[i % 3]:
            st.markdown(f"""
            <div style="
                background: #FFFFFF;
                border: 1px solid #E5DDF5;
                border-radius: 16px;
                padding: 20px;
                min-height: 165px;
                margin-bottom: 16px;
                box-shadow: 0 4px 12px rgba(48,32,79,0.06);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            ">
                <div style="font-size: 28px; margin-bottom: 12px;">
                    {icono}
                </div>
                <div style="
                    color: #39265F;
                    font-size: 15px;
                    font-weight: 800;
                    margin-bottom: 8px;
                ">{titulo}</div>
                <div style="
                    color: #716A81;
                    font-size: 12px;
                    line-height: 1.7;
                ">{descripcion}</div>
            </div>
            """, unsafe_allow_html=True)

    st.caption("StatMentor AI · Comprende los datos. Aprende haciendo.")



def page_desc():
    st.markdown("""
    <div style="
        background: linear-gradient(120deg, #30204F, #6544B5, #8B5CF6);
        padding: 28px;
        border-radius: 20px;
        margin-bottom: 22px;
        box-shadow: 0 10px 25px rgba(76,48,130,0.16);
    ">
        <div style="
            color: #E9DFFF;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 10px;
        ">MÓDULO 01 · ANÁLISIS DE DATOS</div>
        <h1 style="
            color: #FFFFFF !important;
            background: transparent !important;
            font-size: 30px;
            margin: 0 0 10px 0;
        ">📊 Estadística descriptiva</h1>
        <p style="
            color: #F0EAFE !important;
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        ">Resume tus datos, identifica sus características principales
        y comprende los resultados mediante fórmulas y procedimientos.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📝 Ingresa tus datos")
    st.caption(
        "Escribe números separados por comas, espacios o saltos de línea. "
        "Utiliza punto para los decimales."
    )

    txt = st.text_area(
        "Datos numéricos",
        "2.1, 2.3, 2.2, 2.4, 2.0",
        height=120,
        key="desc_datos"
    )

    col1, col2 = st.columns(2)

    with col1:
        tipo = st.radio(
            "Tipo de datos",
            ["Muestra (s, n−1)", "Población (σ, n)"],
            horizontal=False,
            key="desc_tipo"
        )

    with col2:
        unit = st.text_input(
            "Unidad de medida (opcional)",
            placeholder="Ej. cm, kg, segundos",
            key="desc_unidad"
        )

        st.markdown("""
        <div style="
            background: #F0EAFE;
            border: 1px solid #D9CCFA;
            border-radius: 12px;
            padding: 12px;
            color: #4C367D;
            font-size: 12px;
            line-height: 1.7;
        ">
            <b>💡 Recuerda</b><br>
            Muestra: utiliza n − 1 para calcular la varianza muestral.<br>
            Población: utiliza n para calcular la varianza poblacional.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    if st.button(
        "📐 Calcular estadísticas",
        type="primary",
        width="stretch",
        key="btn_calcular_desc"
    ):
        d = parse_numbers(txt)

        if d:
            render_desc(
                d,
                tipo.startswith("Muestra"),
                unit
            )
        else:
            st.warning(
                "Ingresa al menos un dato numérico válido para continuar."
            )




def page_exp():
    st.markdown("""
    <div style="
        background: linear-gradient(120deg, #30204F, #6544B5, #8B5CF6);
        padding: 28px;
        border-radius: 20px;
        margin-bottom: 22px;
        box-shadow: 0 10px 25px rgba(76,48,130,0.16);
    ">
        <div style="
            color: #E9DFFF;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 10px;
        ">MÓDULO 02 · MEDICIONES</div>
        <h1 style="
            color: #FFFFFF !important;
            background: transparent !important;
            font-size: 30px;
            margin: 0 0 10px 0;
        ">🧪 Datos experimentales</h1>
        <p style="
            color: #F0EAFE !important;
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        ">Registra mediciones, selecciona sus unidades y considera
        la resolución del instrumento para analizar tus resultados.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📝 Ingresa tus mediciones")
    st.caption(
        "Escribe los valores separados por comas, espacios "
        "o saltos de línea. Utiliza punto para los decimales."
    )

    txt = st.text_area(
        "Valores medidos",
        "2.1, 2.3, 2.2, 2.4, 2.0",
        height=120,
        key="exp_mediciones"
    )

    st.markdown("### ⚙️ Configuración del experimento")

    mag = st.selectbox(
        "Magnitud física",
        list(UNITS),
        key="exp_magnitud"
    )

    c1, c2 = st.columns(2)

    with c1:
        u_in = st.selectbox(
            "Unidad de los datos",
            list(UNITS[mag]),
            key="exp_unidad_entrada"
        )

    with c2:
        u_out = st.selectbox(
            "Unidad de salida",
            list(UNITS[mag]),
            key="exp_unidad_salida"
        )

    res = st.number_input(
        "Resolución del instrumento (0 = no aplicar)",
        min_value=0.0,
        value=0.0,
        format="%.4f",
        help="Introduce la resolución del instrumento de medición si deseas considerarla.",
        key="exp_resolucion"
    )

    st.markdown("""
    <div style="
        background: #F0EAFE;
        border: 1px solid #D9CCFA;
        border-radius: 12px;
        padding: 14px;
        color: #4C367D;
        font-size: 13px;
        line-height: 1.7;
        margin: 10px 0 18px 0;
    ">
        <b>💡 Antes de procesar</b><br>
        Verifica que todos los datos correspondan a la misma magnitud.
        Selecciona las unidades correctas para convertir los resultados
        de forma adecuada.
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "🧪 Procesar mediciones",
        type="primary",
        width="stretch",
        key="btn_procesar_exp"
    ):
        d = parse_numbers(txt, "las mediciones")

        if d:
            render_exp(d, mag, u_in, u_out, res)
        else:
            st.warning(
                "Ingresa al menos una medición numérica válida para continuar."
            )




def page_tablas():
    st.markdown("""
    <div style="
        background: linear-gradient(120deg, #30204F, #6544B5, #8B5CF6);
        padding: 28px;
        border-radius: 20px;
        margin-bottom: 22px;
        box-shadow: 0 10px 25px rgba(76,48,130,0.16);
    ">
        <div style="
            color: #E9DFFF;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 10px;
        ">MÓDULO 03 · ORGANIZACIÓN VISUAL</div>
        <h1 style="
            color: #FFFFFF !important;
            background: transparent !important;
            font-size: 30px;
            margin: 0 0 10px 0;
        ">📈 Tablas y gráficas</h1>
        <p style="
            color: #F0EAFE !important;
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        ">Organiza tus datos en una tabla de frecuencias y representa
        su distribución mediante un histograma para identificar patrones.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📝 Ingresa los datos")
    st.caption(
        "Escribe los valores separados por comas, espacios "
        "o saltos de línea. Utiliza punto para los decimales."
    )

    txt = st.text_area(
        "Datos numéricos",
        "158 162 165 170 172 168 175 160 163 167 169 171 174 178 166 164",
        height=120,
        key="tab_datos"
    )

    st.markdown("### ⚙️ Configuración de frecuencias")

    manual = st.checkbox(
        "Elegir el número de clases manualmente",
        key="tab_manual"
    )

    if manual:
        k = st.number_input(
            "Número de clases",
            min_value=2,
            max_value=30,
            value=5,
            step=1,
            help="Selecciona entre 2 y 30 intervalos para agrupar los datos.",
            key="tab_clases"
        )
    else:
        k = None
        st.info(
            "El número de clases se determinará automáticamente "
            "según los datos ingresados."
        )

    st.markdown("""
    <div style="
        background: #F0EAFE;
        border: 1px solid #D9CCFA;
        border-radius: 12px;
        padding: 14px;
        color: #4C367D;
        font-size: 13px;
        line-height: 1.7;
        margin: 10px 0 18px 0;
    ">
        <b>💡 ¿Qué obtendrás?</b><br>
        Una tabla de frecuencias para organizar los datos y un histograma
        para visualizar cómo se distribuyen los valores.
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "📊 Construir tabla y gráfica",
        type="primary",
        width="stretch",
        key="btn_construir_tab"
    ):
        d = parse_numbers(txt)

        if d:
            render_freq(d, int(k) if k is not None else None)
        else:
            st.warning(
                "Ingresa al menos un dato numérico válido para continuar."
            )



def page_prob():
    st.markdown("""
    <div style="
        background: linear-gradient(120deg, #30204F, #6544B5, #8B5CF6);
        padding: 28px;
        border-radius: 20px;
        margin-bottom: 22px;
        box-shadow: 0 10px 25px rgba(76,48,130,0.16);
    ">
        <div style="
            color: #E9DFFF;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 10px;
        ">MÓDULO 04 · AZAR Y DISTRIBUCIONES</div>
        <h1 style="
            color: #FFFFFF !important;
            background: transparent !important;
            font-size: 30px;
            margin: 0 0 10px 0;
        ">🎲 Probabilidad</h1>
        <p style="
            color: #F0EAFE !important;
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        ">Resuelve problemas de probabilidad con distribuciones,
        eventos y modelos estadísticos mediante procedimientos guiados.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧠 Selecciona el tema")

    tipo = st.radio(
        "Tipo de problema",
        [
            "Distribución normal",
            "Binomial",
            "Clásica / unión / condicional"
        ],
        horizontal=True,
        key="prob_tipo"
    )

    st.markdown("")

    if tipo == "Distribución normal":
        st.markdown("### 📈 Distribución normal")
        st.caption(
            "Calcula probabilidades o encuentra un valor a partir "
            "de la media y la desviación estándar."
        )

        c1, c2 = st.columns(2)

        with c1:
            mu = st.number_input(
                "Media (μ)",
                value=70.0,
                key="prob_normal_mu"
            )

        with c2:
            sg = st.number_input(
                "Desviación estándar (σ)",
                min_value=0.0,
                value=10.0,
                key="prob_normal_sigma"
            )

        kind = st.selectbox(
            "¿Qué deseas calcular?",
            [
                "P(X < a)",
                "P(X > a)",
                "P(a < X < b)",
                "Percentil (hallar x)"
            ],
            key="prob_normal_tipo"
        )

        if kind == "Percentil (hallar x)":
            a = st.number_input(
                "Probabilidad del percentil (entre 0 y 1)",
                min_value=0.0,
                max_value=1.0,
                value=0.85,
                key="prob_normal_percentil"
            )
            st.caption(
                "Ejemplo: 0.85 corresponde al percentil 85."
            )
        else:
            a = st.number_input(
                "Valor a",
                value=85.0,
                key="prob_normal_a"
            )

        b = None

        if kind == "P(a < X < b)":
            b = st.number_input(
                "Valor b",
                value=95.0,
                key="prob_normal_b"
            )

        st.markdown("""
        <div style="
            background: #F0EAFE;
            border: 1px solid #D9CCFA;
            border-radius: 12px;
            padding: 12px;
            color: #4C367D;
            font-size: 13px;
            line-height: 1.7;
            margin: 10px 0 18px 0;
        ">
            <b>💡 Recuerda</b><br>
            La desviación estándar debe ser mayor que cero.
            La puntuación estándar se calcula como z = (x − μ) / σ.
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "📐 Resolver distribución normal",
            type="primary",
            width="stretch",
            key="btn_prob_normal"
        ):
            if sg <= 0:
                st.warning(
                    "La desviación estándar debe ser mayor que cero."
                )
            elif kind == "P(a < X < b)" and a >= b:
                st.warning(
                    "El valor a debe ser menor que el valor b."
                )
            else:
                render_normal(mu, sg, kind, a, b)

    elif tipo == "Binomial":
        st.markdown("### 🎯 Distribución binomial")
        st.caption(
            "Modela el número de éxitos en una cantidad fija de "
            "ensayos independientes con probabilidad constante."
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            n = st.number_input(
                "Ensayos (n)",
                min_value=1,
                max_value=1000,
                value=10,
                step=1,
                key="prob_binom_n"
            )

        with c2:
            p = st.number_input(
                "Probabilidad de éxito (p)",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.05,
                key="prob_binom_p"
            )

        with c3:
            k = st.number_input(
                "Número de éxitos (k)",
                min_value=0,
                max_value=1000,
                value=3,
                step=1,
                key="prob_binom_k"
            )

        kind = st.selectbox(
            "¿Qué deseas calcular?",
            ["P(X = k)", "P(X ≤ k)", "P(X ≥ k)"],
            key="prob_binom_tipo"
        )

        st.markdown("""
        <div style="
            background: #F0EAFE;
            border: 1px solid #D9CCFA;
            border-radius: 12px;
            padding: 12px;
            color: #4C367D;
            font-size: 13px;
            line-height: 1.7;
            margin: 10px 0 18px 0;
        ">
            <b>💡 Fórmula binomial</b><br>
            P(X = k) = C(n, k) · pᵏ · (1 − p)ⁿ⁻ᵏ<br>
            El número de éxitos k no puede superar el número de ensayos n.
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "🎲 Resolver distribución binomial",
            type="primary",
            width="stretch",
            key="btn_prob_binom"
        ):
            if k > n:
                st.warning(
                    "El número de éxitos k no puede ser mayor que n."
                )
            else:
                render_binom(int(n), p, int(k), kind)

    else:
        st.markdown("### 🎲 Probabilidad clásica")
        st.caption(
            "Introduce los casos favorables y posibles para calcular "
            "la probabilidad de un evento."
        )

        c1, c2 = st.columns(2)

        with c1:
            fav = st.number_input(
                "Casos favorables",
                min_value=0.0,
                value=1.0,
                key="prob_favorables"
            )

        with c2:
            tot = st.number_input(
                "Casos posibles",
                min_value=0.0,
                value=6.0,
                key="prob_totales"
            )

        st.markdown("---")
        st.markdown("### 🔗 Unión y probabilidad condicional")
        st.caption(
            "Indica las probabilidades de los eventos A y B "
            "y su intersección."
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            pa = st.number_input(
                "P(A)",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                key="prob_pa"
            )

        with c2:
            pb = st.number_input(
                "P(B)",
                min_value=0.0,
                max_value=1.0,
                value=0.4,
                key="prob_pb"
            )

        with c3:
            pab = st.number_input(
                "P(A ∩ B)",
                min_value=0.0,
                max_value=1.0,
                value=0.2,
                key="prob_pab"
            )

        st.markdown("""
        <div style="
            background: #F0EAFE;
            border: 1px solid #D9CCFA;
            border-radius: 12px;
            padding: 12px;
            color: #4C367D;
            font-size: 13px;
            line-height: 1.7;
            margin: 10px 0 18px 0;
        ">
            <b>💡 Fórmulas importantes</b><br>
            Probabilidad clásica: P(A) = casos favorables / casos posibles.<br>
            Unión: P(A ∪ B) = P(A) + P(B) − P(A ∩ B).<br>
            Condicional: P(A | B) = P(A ∩ B) / P(B), cuando P(B) &gt; 0.
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "📊 Resolver probabilidades",
            type="primary",
            width="stretch",
            key="btn_prob_clasica"
        ):
            if tot <= 0:
                st.warning(
                    "Los casos posibles deben ser mayores que cero."
                )
            elif fav > tot:
                st.warning(
                    "Los casos favorables no pueden superar los casos posibles."
                )
            elif pab > min(pa, pb):
                st.warning(
                    "La intersección P(A ∩ B) no puede superar P(A) ni P(B)."
                )
            else:
                render_clasica(fav, tot, pa, pb, pab)




def page_reg():
    st.markdown("""
    <div style="
        background: linear-gradient(120deg, #30204F, #6544B5, #8B5CF6);
        padding: 28px;
        border-radius: 20px;
        margin-bottom: 22px;
        box-shadow: 0 10px 25px rgba(76,48,130,0.16);
    ">
        <div style="
            color: #E9DFFF;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 10px;
        ">MÓDULO 05 · RELACIÓN ENTRE VARIABLES</div>
        <h1 style="
            color: #FFFFFF !important;
            background: transparent !important;
            font-size: 30px;
            margin: 0 0 10px 0;
        ">📉 Correlación y regresión</h1>
        <p style="
            color: #F0EAFE !important;
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        ">Explora la relación entre dos variables, calcula su correlación
        y utiliza la regresión lineal para estimar valores.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📝 Ingresa tus datos")
    st.caption(
        "Cada valor de x debe corresponder al valor de y que aparece "
        "en la misma posición. Separa los números con espacios, comas "
        "o saltos de línea."
    )

    c1, c2 = st.columns(2)

    with c1:
        tx = st.text_area(
            "Valores de la variable X",
            "1 2 3 4 5",
            height=130,
            key="reg_datos_x"
        )

    with c2:
        ty = st.text_area(
            "Valores de la variable Y",
            "0.21 0.40 0.62 0.79 1.02",
            height=130,
            key="reg_datos_y"
        )

    st.markdown("### ⚙️ Personaliza el análisis")

    c3, c4 = st.columns(2)

    with c3:
        xl = st.text_input(
            "Nombre de la variable X",
            "x",
            key="reg_nombre_x"
        )

    with c4:
        yl = st.text_input(
            "Nombre de la variable Y",
            "y",
            key="reg_nombre_y"
        )

    x0 = st.text_input(
        "Valor de X para realizar una predicción (opcional)",
        placeholder="Ej. 6",
        key="reg_prediccion"
    )

    st.markdown("""
    <div style="
        background: #F0EAFE;
        border: 1px solid #D9CCFA;
        border-radius: 12px;
        padding: 14px;
        color: #4C367D;
        font-size: 13px;
        line-height: 1.7;
        margin: 10px 0 18px 0;
    ">
        <b>💡 ¿Qué analizarás?</b><br>
        • Coeficiente de correlación: indica la dirección y la intensidad
        de la relación lineal.<br>
        • Recta de regresión: permite estimar Y a partir de X.<br>
        • Gráfica de dispersión: ayuda a visualizar el patrón de los datos.
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "📊 Calcular correlación y regresión",
        type="primary",
        width="stretch",
        key="btn_calcular_reg"
    ):
        x = parse_numbers(tx, "x")
        y = parse_numbers(ty, "y")

        if not x or not y:
            st.warning(
                "Ingresa valores numéricos válidos para ambas variables."
            )
            return

        if len(x) != len(y):
            st.error(
                f"Las variables deben tener la misma cantidad de datos. "
                f"X tiene {len(x)} y Y tiene {len(y)}."
            )
            return

        if len(x) < 3:
            st.warning(
                "Ingresa al menos tres pares de datos para realizar "
                "el análisis."
            )
            return

        xv = None

        if x0.strip():
            try:
                xv = float(x0.strip())
            except ValueError:
                st.error(
                    "El valor de predicción debe ser un número válido."
                )
                return

        if not xl.strip() or not yl.strip():
            st.warning(
                "Escribe un nombre para cada variable antes de continuar."
            )
            return

        render_reg(x, y, xv, xl.strip(), yl.strip())




def page_ejemplos():
    st.markdown("""
    <div style="
        background: linear-gradient(120deg, #30204F, #6544B5, #8B5CF6);
        padding: 28px;
        border-radius: 20px;
        margin-bottom: 22px;
        box-shadow: 0 10px 25px rgba(76,48,130,0.16);
    ">
        <div style="
            color: #E9DFFF;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 10px;
        ">MÓDULO 06 · APRENDIZAJE GUIADO</div>
        <h1 style="
            color: #FFFFFF !important;
            background: transparent !important;
            font-size: 30px;
            margin: 0 0 10px 0;
        ">📚 Ejercicios de ejemplo</h1>
        <p style="
            color: #F0EAFE !important;
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        ">Aprende estadística aplicada mediante ejercicios resueltos
        y procedimientos que te ayudan a comprender cada resultado.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧠 Selecciona un ejercicio")

    nombres = [
        f"{i + 1:02d} · {e[0]}"
        for i, e in enumerate(EJEMPLOS)
    ]

    seleccionado = st.selectbox(
        "Ejercicios disponibles",
        range(len(EJEMPLOS)),
        format_func=lambda i: nombres[i],
        key="ejemplo_seleccionado"
    )

    ejercicio = EJEMPLOS[seleccionado]

    st.markdown(f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid #DDD2F8;
        border-left: 5px solid #7950D9;
        border-radius: 16px;
        padding: 22px;
        margin: 12px 0 18px 0;
        box-shadow: 0 5px 16px rgba(76,48,130,0.07);
    ">
        <div style="
            color: #7950D9;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.5px;
            margin-bottom: 10px;
        ">ENUNCIADO DEL EJERCICIO</div>
        <h3 style="
            color: #30204F !important;
            margin: 0 0 12px 0;
            font-size: 20px;
        ">{ejercicio[0]}</h3>
        <p style="
            color: #48405A !important;
            font-size: 15px;
            line-height: 1.8;
            margin: 0;
        ">{ejercicio[1]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: #F0EAFE;
        border: 1px solid #D9CCFA;
        border-radius: 12px;
        padding: 13px;
        color: #4C367D;
        font-size: 13px;
        line-height: 1.7;
        margin-bottom: 16px;
    ">
        <b>💡 Consejo de estudio</b><br>
        Lee primero el enunciado e intenta identificar los datos
        y la fórmula que necesitas. Después, resuelve el ejemplo
        para comparar tu razonamiento.
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "🧮 Resolver ejercicio seleccionado",
        type="primary",
        width="stretch",
        key="btn_resolver_ejemplo"
    ):
        ejercicio[2]()




def page_interp():
    st.markdown("""
    <div style="
        background: linear-gradient(120deg, #30204F, #6544B5, #8B5CF6);
        padding: 28px;
        border-radius: 20px;
        margin-bottom: 22px;
        box-shadow: 0 10px 25px rgba(76,48,130,0.16);
    ">
        <div style="
            color: #E9DFFF;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 10px;
        ">MÓDULO 08 · COMPRENSIÓN DE RESULTADOS</div>
        <h1 style="
            color: #FFFFFF !important;
            background: transparent !important;
            font-size: 30px;
            margin: 0 0 10px 0;
        ">📖 Guía de interpretación estadística</h1>
        <p style="
            color: #F0EAFE !important;
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        ">Aprende a interpretar la dispersión, la correlación y
        el coeficiente de variación para comprender mejor tus datos.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 1. Desviación estándar")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div style="
            background: #FFFFFF;
            border: 1px solid #DDD2F8;
            border-top: 5px solid #7950D9;
            border-radius: 15px;
            padding: 20px;
            min-height: 180px;
        ">
            <h3 style="color:#4C367D !important;">σ Poblacional</h3>
            <p style="color:#48405A !important;line-height:1.7;">
                Se utiliza cuando se dispone de todos los datos
                de la población.
            </p>
            <div style="
                background:#F0EAFE;padding:10px;border-radius:9px;
                color:#4C367D;text-align:center;font-weight:600;
            ">Divisor: N</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style="
            background: #FFFFFF;
            border: 1px solid #DDD2F8;
            border-top: 5px solid #00A6A6;
            border-radius: 15px;
            padding: 20px;
            min-height: 180px;
        ">
            <h3 style="color:#087F83 !important;">s Muestral</h3>
            <p style="color:#48405A !important;line-height:1.7;">
                Se utiliza cuando los datos representan una muestra.
                El divisor n − 1 ayuda a corregir la subestimación
                de la variabilidad poblacional.
            </p>
            <div style="
                background:#E1F7F5;padding:10px;border-radius:9px;
                color:#087F83;text-align:center;font-weight:600;
            ">Divisor: n − 1</div>
        </div>
        """, unsafe_allow_html=True)

    st.info(
        "Con muestras grandes, ambas desviaciones suelen ser parecidas. "
        "Con muestras pequeñas, la diferencia puede ser más notable."
    )

    st.markdown("---")
    st.markdown("### 📉 2. Interpretación de la correlación")

    st.markdown("""
    La correlación **r** indica la dirección y la intensidad de una
    relación lineal. El signo indica su dirección y el valor absoluto
    indica su intensidad aproximada.
    """)

    niveles = [
        ("Muy fuerte", "|r| ≥ 0.90", "#27845B"),
        ("Fuerte", "0.70 ≤ |r| < 0.90", "#4777D5"),
        ("Moderada", "0.40 ≤ |r| < 0.70", "#C18422"),
        ("Débil", "|r| < 0.40", "#B95A68"),
    ]

    for nombre, rango, color in niveles:
        st.markdown(f"""
        <div style="
            display:flex;align-items:center;gap:12px;
            background:#FFFFFF;border:1px solid #E7E0F4;
            border-radius:10px;padding:12px 15px;margin:7px 0;
        ">
            <div style="
                width:5px;align-self:stretch;
                background:{color};border-radius:5px;
            "></div>
            <div style="flex:1;color:#30204F;font-weight:600;">
                {nombre}
            </div>
            <div style="color:#655A78;font-size:13px;">
                {rango}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background:#F0EAFE;border:1px solid #D9CCFA;
        border-radius:12px;padding:15px;color:#4C367D;
        line-height:1.8;margin-top:14px;
    ">
        <b>¿Qué significa r²?</b><br>
        Es el coeficiente de determinación y, en regresión lineal simple,
        representa la proporción de la variabilidad de Y explicada por
        el modelo lineal con X.<br><br>
        <b>Importante:</b> correlación no implica causalidad.
        Dos variables relacionadas no necesariamente hacen que una
        provoque cambios en la otra.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📐 3. Coeficiente de variación")

    st.markdown(r"""
    El coeficiente de variación permite comparar la variabilidad
    relativa de conjuntos de datos con diferentes escalas o unidades.

    \[
    CV = \frac{s}{|\bar{x}|}\times 100\%
    \]
    """)

    st.caption(
        "Esta expresión utiliza la desviación estándar muestral. "
        "Si trabajas con toda la población, puedes usar σ en lugar de s. "
        "Cuando la media es cero o muy cercana a cero, el CV puede "
        "no estar definido o resultar poco informativo."
    )

    st.markdown("---")
    st.markdown("### 🧪 4. Prueba con tus propios datos")

    txt = st.text_area(
        "Datos numéricos",
        "2.1 2.3 2.2 2.4 2.0",
        height=110,
        key="interp_datos"
    )

    if st.button(
        "🔍 Analizar e interpretar",
        type="primary",
        width="stretch",
        key="btn_interp"
    ):
        d = parse_numbers(txt)

        if not d or len(d) < 2:
            st.warning(
                "Ingresa al menos dos datos numéricos válidos."
            )
        else:
            media = float(np.mean(d))
            s = float(np.std(d, ddof=1))
            sigma = float(np.std(d, ddof=0))

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("Cantidad de datos (n)", len(d))

            with c2:
                st.metric("Media", f"{media:.4f}")

            with c3:
                st.metric("Diferencia entre s y σ", f"{s - sigma:.4f}")

            st.markdown("#### Resultados de dispersión")

            c1, c2 = st.columns(2)

            with c1:
                st.metric("s · Muestral", f"{s:.4f}")

            with c2:
                st.metric("σ · Poblacional", f"{sigma:.4f}")

            if abs(s - sigma) < 1e-10:
                st.success(
                    "Ambos resultados son prácticamente iguales "
                    "para estos datos."
                )
            else:
                st.write(
                    f"La desviación muestral es {s:.4f}, mientras que "
                    f"la poblacional es {sigma:.4f}. "
                    "La diferencia se debe al divisor utilizado."
                )

            if abs(media) > 1e-12:
                cv = s / abs(media) * 100
                st.metric(
                    "Coeficiente de variación muestral",
                    f"{cv:.2f}%"
                )

                st.caption(
                    "El CV expresa la desviación estándar muestral "
                    "como porcentaje del valor absoluto de la media."
                )
            else:
                st.warning(
                    "No se calcula el coeficiente de variación porque "
                    "la media es cero o demasiado cercana a cero."
                )

            with st.expander("📘 Ver el procedimiento"):
                st.write(f"Datos ingresados: {d}")
                st.write(f"Media: {media:.4f}")
                st.write(
                    f"Desviación muestral: s = {s:.4f} "
                    "(divisor n − 1)."
                )
                st.write(
                    f"Desviación poblacional: σ = {sigma:.4f} "
                    "(divisor n)."
                )
                st.write(
                    "La desviación estándar mide cuánto se dispersan "
                    "los datos alrededor de la media."
                )


import re


import re

def limpiar_respuesta_ia(texto):
    """Convierte comandos matemáticos frecuentes a texto legible."""

    texto = str(texto)

    # Quitar delimitadores matemáticos.
    for marca in (r"\(", r"\)", r"\[", r"\]"):
        texto = texto.replace(marca, "")

    texto = texto.replace("$$", "").replace("$", "")

    # Simplificar comandos frecuentes.
    reemplazos = {
        r"\displaystyle": "",
        r"\displaystylesuma": "suma",
        r"\sum_{i=1}^{n}": "suma de los datos",
        r"\sum\_{i=1}^{n}": "suma de los datos",
        r"\sum x_i": "suma de los datos",
        r"\bar{x}": "media",
        r"\boxed{": "",
        r"\text{": "",
        r"\mathrm{": "",
        r"\begin{aligned}": "",
        r"\end{aligned}": "",
        r"\begin{array}": "",
        r"\end{array}": "",
        r"\,": " ",
        r"\;": " ",
        r"\quad": " ",
        r"\qquad": " ",
        r"\times": "×",
        r"\cdot": "·",
        "&=": "=",
        r"\\": "\n",
    }

    for original, nuevo in reemplazos.items():
        texto = texto.replace(original, nuevo)

    # Convertir fracciones sencillas.
    texto = re.sub(
        r"\\frac\{([^{}]+)\}\{([^{}]+)\}",
        r"(\1) / (\2)",
        texto
    )

    # Eliminar llaves que hayan quedado de comandos simples.
    texto = texto.replace("{", "").replace("}", "")

    # Quitar espacios sobrantes y líneas vacías excesivas.
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)

    return texto.strip()



def page_ai():
    from ai_groq import consultar_groq
    import ai_groq
    st.caption(ai_groq.__file__)
    import html

    # Estilos del asistente
    st.markdown("""
        <style>
        .ai-banner {
            background: linear-gradient(120deg, #35116B, #7046E8, #3977F6);
            padding: 28px;
            border-radius: 20px;
            color: white;
            margin-bottom: 22px;
            box-shadow: 0 8px 25px rgba(82, 55, 170, 0.18);
        }

        .ai-banner h1 {
            color: white !important;
            margin: 0 0 10px 0;
            font-size: 30px;
        }

        .ai-banner p {
            color: #F1EDFF !important;
            margin: 0;
            font-size: 15px;
        }

        .ai-info {
            background: #F0EAFF;
            padding: 15px;
            border-radius: 12px;
            border-left: 4px solid #8052E8;
            color: #332052;
            margin: 12px 0 20px 0;
        }

        .ai-response {
            background: #172033;
            color: #F1F5F9;
            padding: 22px;
            border-radius: 14px;
            line-height: 1.8;
            border: 1px solid #35415A;
            overflow-wrap: anywhere;
        }

        .ai-response h1, .ai-response h2, .ai-response h3 {
            color: #C4B5FD !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Banner principal
    st.markdown("""
        <div class="ai-banner">
            <h1>🤖 StatMentor AI</h1>
            <p>
                Tu tutor virtual de Estadística Aplicada.
                Pregunta, aprende y comprende cada procedimiento paso a paso.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Preguntas sugeridas
    st.subheader("💡 ¿Qué quieres aprender?")

    preguntas = [
        "¿Cómo se calcula la desviación estándar muestral?",
        "¿Qué diferencia hay entre media, mediana y moda?",
        "Explícame cómo calcular la probabilidad de un evento.",
        "¿Cómo se interpreta el coeficiente de correlación?",
        "Explícame la fórmula de la distribución normal.",
        "¿Cómo se calcula una ecuación de regresión lineal?"
    ]

    ejemplo = st.selectbox(
        "Selecciona una pregunta de ejemplo:",
        ["Elige una pregunta..."] + preguntas,
        key="ejemplo_ia"
    )

    if st.button("📌 Usar pregunta seleccionada", width="stretch"):
        if ejemplo != "Elige una pregunta...":
            st.session_state["pregunta_ia"] = ejemplo
            st.rerun()
        else:
            st.warning("Primero selecciona una pregunta de ejemplo.")

    st.markdown("""
        <div class="ai-info">
            <strong>📚 Consejo:</strong> Puedes pedir fórmulas,
            ejemplos resueltos, sustitución de datos e interpretación
            de resultados. También puedes escribir tu propio ejercicio.
        </div>
    """, unsafe_allow_html=True)

    # Entrada de la pregunta
    pregunta = st.text_area(
        "✍️ Escribe tu pregunta o ejercicio:",
        placeholder=(
            "Ejemplo: Tengo los datos 5, 8, 10, 12 y 15. "
            "Explícame cómo calcular la media y la desviación estándar."
        ),
        height=140,
        key="pregunta_ia"
    )

    # Botón de consulta
    consultar = st.button(
    "✨ Consultar a StatMentor AI",
    type="primary",
    width="stretch"
)

    if consultar:
        if not pregunta.strip():
            st.warning("Escribe una pregunta antes de consultar.")
        else:
            try:
                with st.spinner(
                    "🧠 StatMentor está preparando tu explicación..."
                ):
                    respuesta = consultar_groq(pregunta)

                if respuesta:
                    st.markdown("### 📖 Respuesta del asistente")

                    respuesta_limpia = limpiar_respuesta_ia(respuesta)

                    with st.container(border=True):
                        st.markdown(respuesta_limpia)
                    st.caption(
                        "💜 Revisa los pasos y verifica los cálculos "
                        "antes de utilizar los resultados."
                    )
                else:
                    st.warning(
                        "No se recibió una respuesta. "
                        "Intenta nuevamente con otra pregunta."
                    )

            except Exception as e:
                st.error(
                    "No se pudo completar la consulta. "
                    "Verifica tu conexión y la configuración de Groq."
                )
                with st.expander("Ver detalles del error"):
                    st.code(traceback.format_exc())


# ---------------------------------- MAIN ------------------------------
PAGES = {
    "🏠 Inicio": page_inicio,
    "📈 Estadística descriptiva": page_desc,
    "🔬 Datos experimentales": page_exp,
    "📋 Tablas y gráficas": page_tablas,
    "🎲 Probabilidad": page_prob,
    "📉 Correlación y regresión": page_reg,
    "📚 Ejercicios de ejemplo": page_ejemplos,
    "🎯 Práctica": page_practica,
    "💡 Interpretación": page_interp,
    "🤖 Asistente IA": page_ai,
}


with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">S</div>
            <div>
                <div class="sidebar-brand-title">StatMentor</div>
                <div class="sidebar-brand-subtitle">AI · Estadística</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section-label">NAVEGACIÓN</div>',
        unsafe_allow_html=True
    )

    sel = st.radio(
        "Módulos",
        list(PAGES),
        label_visibility="collapsed",
        key="menu_statmentor"
    )

    st.divider()

    st.markdown(
        f"""
        <div class="sidebar-info">
            <div class="sidebar-info-label">ASIGNATURA</div>
            <div class="sidebar-info-value">{ASIGNATURA}</div>
            <div class="sidebar-info-label">SECCIÓN</div>
            <div class="sidebar-info-value">{SECCION}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section-label">INTEGRANTES</div>',
        unsafe_allow_html=True
    )

    for i in INTEGRANTES:
        st.caption(i)
try:
    PAGES[sel]()
except Exception as e:  # red de seguridad para entradas inesperadas
    st.error(f"No pude resolver este caso: {e}. Revisa los datos ingresados.")
