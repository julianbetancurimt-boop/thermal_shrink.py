import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="R&D Materials Optimizer", layout="wide")

# CSS para apariencia sofisticada (Dark Mode Enterprise)
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); }
    div[data-testid="stMetricValue"] { color: #38bdf8 !important; font-size: 32px; font-weight: bold; }
    .report-card { background-color: #1e293b; padding: 20px; border-radius: 12px; border-left: 5px solid #3b82f6; margin-bottom: 20px; }
    h1, h2, h3 { color: #f1f5f9; }
    </style>
    """, unsafe_allow_html=True)

# --- MODELOS MATEMÁTICOS ---
def modelo_logistico(T, L, k, T0):
    return L / (1 + np.exp(-k * (T - T0)))

# --- TÍTULO ---
st.title("🛡️ Materials Innovation Engine")
st.markdown("*Optimización de Películas Termoencogibles de Alto Desempeño*")
st.markdown("---")

# --- BARRA LATERAL: ENTRADAS DINÁMICAS ---
with st.sidebar:
    st.header("⚙️ Parámetros de Diseño")
    
    with st.expander("📦 Configuración de Paca", expanded=True):
        peso_paca = st.number_input("Peso Total de la Paca (kg)", value=18.0, step=0.5)
        l_paca = st.number_input("Largo de Paca (mm)", value=400)
        a_paca = st.number_input("Ancho de Paca (mm)", value=200)

    with st.expander("🧪 Propiedades de Material", expanded=True):
        costo_pcr = st.number_input("Costo PCR ($/kg)", value=6400)
        costo_vir = st.number_input("Costo Virgen + mLLDPE ($/kg)", value=7800)
        sig_pcr = st.slider("Fluencia PCR (MPa)", 8.0, 15.0, 12.0)
        sig_vir = st.slider("Fluencia Virgen (MPa)", 18.0, 35.0, 24.0)
    
    with st.expander("🏭 Proceso de Extrusión", expanded=True):
        gap = st.number_input("Gap del Dado (mm)", value=1.2)
        bur = st.slider("BUR (Soplado)", 1.5, 4.5, 3.0)
        cal_actual = st.number_input("Calibre Actual PCR (µm)", value=60)
        vol_mensual = st.number_input("Producción Mensual (kg)", value=25000)

# --- LÓGICA DE INGENIERÍA ---
f_pcr = sig_pcr * (cal_actual / 1000)
cal_target = (f_pcr / sig_vir) * 1000
ahorro_masa_porc = ((cal_actual - cal_target) / cal_actual) * 100

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs(["🌎 Sostenibilidad", "🏗️ Mecánica", "🔥 Cinética", "💰 ROI Financiero"])

# TAB 1: SOSTENIBILIDAD
with tab1:
    st.markdown('<div class="report-card"><h3>Impacto Ambiental y Eficiencia</h3></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Espesor Objetivo", f"{cal_target:.1f} µm", f"-{ahorro_masa_porc:.1f}%")
    kg_evitados = (vol_mensual * ahorro_masa_porc / 100)
    c2.metric("Plástico Evitado", f"{kg_evitados:,.0f} kg/mes")
    c3.metric("Huella CO2 Evitada", f"{(kg_evitados * 2.1):,.0f} kg", "Impacto Verde")

# TAB 2: MECÁNICA Y ESTABILIDAD
with tab2:
    st.markdown('<div class="report-card"><h3>Validación Estructural y de Proceso</h3></div>', unsafe_allow_html=True)
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("📦 Integridad de Carga")
        # Esfuerzo inducido por la paca dinámica
        # Factor dinámico de transporte (0.22G)
        esfuerzo_real = (peso_paca * 9.81 * 0.22) / (2 * a_paca)
        resistencia_material = sig_vir * (cal_target / 1000)
        fs = resistencia_material / esfuerzo_real
        
        st.write(f"**Carga Dinámica Estada:** {esfuerzo_real:.3f} N/mm")
        if fs > 1.2:
            st.success(f"Factor de Seguridad: {fs:.2f} (CUMPLE)")
        else:
            st.error(f"Factor de Seguridad: {fs:.2f} (RIESGO DE RUPTURA)")
        st.caption("Un FS > 1.2 asegura que la paca no se abra durante el transporte.")

    with col_r:
        st.subheader("🫧 Procesabilidad (Burbuja)")
        ddr = gap / ((cal_target/1000) * bur)
        st.write(f"**Draw-Down Ratio (DDR):** {ddr:.1f}")
        if ddr < 45:
            st.info("Estado: Estable (Proceso Robusto)")
        elif ddr < 55:
            st.warning("Estado: Crítico (Riesgo de Oscilación)")
        else:
            st.error("Estado: Inestable (Burbuja muy delgada)")

# TAB 3: CINÉTICA TÉRMICA
with tab3:
    st.markdown('<div class="report-card"><h3>Curvas de Contracción del Material</h3></div>', unsafe_allow_html=True)
    c_dat, c_plt = st.columns([1,2])
    with c_dat:
        st.write("Datos de Horno (°C vs %)")
        df_lab = pd.DataFrame({"Temp": [90, 100, 110, 120, 130, 140, 150], "Shrink": [2, 8, 26, 48, 58, 62, 64]})
        new_data = st.data_editor(df_lab, num_rows="dynamic")
    with c_plt:
        try:
            popt, _ = curve_fit(modelo_logistico, new_data["Temp"], new_data["Shrink"], p0=[65, 0.1, 115])
            tr = np.linspace(80, 160, 100)
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(6,3)); ax.plot(tr, modelo_logistico(tr, *popt), color='#38bdf8', lw=2)
            ax.scatter(new_data["Temp"], new_data["Shrink"], color='red', s=40)
            ax.set_yaxis_title("% Contracción TD"); ax.grid(alpha=0.2)
            st.pyplot(fig)
        except: st.warning("Ingrese datos válidos para el ajuste.")

# TAB 4: FINANCIERO (COP)
with tab4:
    st.markdown('<div class="report-card"><h3>Evaluación de Rentabilidad (Pesos Colombianos)</h3></div>', unsafe_allow_html=True)
    
    costo_mes_pcr = vol_mensual * costo_pcr
    # Calculamos cuántos kg de virgen se necesitan para cubrir los mismos metros lineales
    kg_vir_necesarios = vol_mensual * (1 - ahorro_masa_porc/100)
    costo_mes_vir = kg_vir_necesarios * costo_vir
    ahorro_mes = costo_mes_pcr - costo_mes_vir
    
    f1, f2, f3 = st.columns(3)
    f1.metric("Costo Mensual PCR", f"$ {costo_mes_pcr:,.0f}")
    f2.metric("Costo Virgen Optimizado", f"$ {costo_mes_vir:,.0f}", f"- $ {ahorro_mes:,.0f}")
    f3.metric("AHORRO ANUAL ESTIMADO", f"$ {(ahorro_mes * 12):,.0f}")
    
    st.divider()
    if ahorro_mes > 0:
        st.success(f"PROYECTO VIABLE: El ahorro en masa compensa el mayor costo por kg en un **{((ahorro_mes/costo_mes_pcr)*100):.1f}%** del presupuesto.")
    else:
        st.error("PROYECTO NO RENTABLE: El costo de la resina virgen supera los ahorros por reducción de calibre.")