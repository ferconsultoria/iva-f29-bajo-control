import streamlit as st

# ===============================
# CONFIGURACIÓN GENERAL
# ===============================
st.set_page_config(page_title="IVA – F29 Bajo Control", layout="wide")

# ===============================
# FUNCIONES
# ===============================
def formatear_miles(valor):
    return f"{int(valor):,}".replace(",", ".")

def calcular_ppm(ventas, tasa):
    return ventas * tasa

# ===============================
# TÍTULO
# ===============================
st.title("IVA – F29 Bajo Control")
st.subheader("Inteligencia empresarial aplicada a los impuestos")

st.write("""
Descubra cuánto IVA podría pagar, cuánto ya cobró y cuánto está financiando con su propia caja.
""")

# ===============================
# BLOQUE 1: VENTAS / DÉBITO
# ===============================
st.markdown("### Ventas y Débito Fiscal")

col1, col2 = st.columns(2)

ventas = col1.number_input("Ventas netas del mes", min_value=0, step=100000)
ventas_cobradas = col2.number_input("Ventas cobradas antes del F29", min_value=0, step=100000)

# ===============================
# BLOQUE 2: COMPRAS / CRÉDITO
# ===============================
st.markdown("### Compras y Crédito Fiscal")

col1, col2 = st.columns(2)

compras = col1.number_input("Compras netas del mes", min_value=0, step=100000)
remanente = col2.number_input("Remanente crédito fiscal anterior", min_value=0, step=100000)

# ===============================
# BLOQUE 3: PPM AUTOMÁTICO
# ===============================
st.markdown("### PPM")

tasa_ppm = st.number_input("Tasa PPM (%)", min_value=0.0, value=1.0) / 100
ppm = calcular_ppm(ventas, tasa_ppm)

st.info(f"PPM estimado: ${formatear_miles(ppm)}")

# ===============================
# BLOQUE 4: OTROS IMPUESTOS
# ===============================
st.markdown("### Otros impuestos F29")

col1, col2 = st.columns(2)

honorarios = col1.number_input("Retención de honorarios", min_value=0, step=100000)
impuesto_unico = col2.number_input("Impuesto único trabajadores", min_value=0, step=100000)

iva_postergado = st.number_input("IVA postergado anterior", min_value=0, step=100000)

# ===============================
# BOTÓN
# ===============================
if st.button("Analizar mi F29"):

    # ===============================
    # CÁLCULOS
    # ===============================
    iva_debito = ventas * 0.19
    iva_credito = compras * 0.19

    iva_neto = iva_debito - iva_credito - remanente
    iva_a_pagar = max(0, iva_neto)

    total_f29 = iva_a_pagar + ppm + honorarios + impuesto_unico + iva_postergado

    iva_cobrado = ventas_cobradas * 0.19
    iva_puesto_por_la_empresa = max(0, iva_a_pagar - iva_cobrado)

    porcentaje_financiado = (iva_puesto_por_la_empresa / iva_a_pagar * 100) if iva_a_pagar > 0 else 0

    # ===============================
    # SEMÁFORO
    # ===============================
    if porcentaje_financiado < 20:
        semaforo = "VERDE"
        mensaje_semaforo = "Tu empresa está cubriendo razonablemente el IVA del mes con cobros reales."
    elif porcentaje_financiado < 50:
        semaforo = "AMARILLO"
        mensaje_semaforo = "Atención: una parte relevante del IVA del mes aún no ha sido cobrada."
    else:
        semaforo = "ROJO"
        mensaje_semaforo = "Riesgo alto: tu empresa está pagando IVA con su capital de trabajo."

    # ===============================
    # RESULTADO VISUAL PRO
    # ===============================
    st.markdown("---")
    st.markdown("## Tu diagnóstico tributario del mes")

    st.markdown("### 1) IVA del período")
    a1, a2, a3 = st.columns(3)
    a1.metric("IVA generado por tus ventas", f"${formatear_miles(iva_debito)}")
    a2.metric("IVA recuperable por tus compras", f"${formatear_miles(iva_credito)}")
    a3.metric("IVA neto a pagar este mes", f"${formatear_miles(iva_a_pagar)}")

    st.markdown("### 2) ¿Cómo se forma tu F29?")
    st.markdown(f"""
<div style="background-color:#1E293B; padding:18px; border-radius:12px; border:1px solid #334155;">
    <p style="margin:6px 0;"><strong>IVA neto a pagar</strong>: ${formatear_miles(iva_a_pagar)}</p>
    <p style="margin:6px 0;"><strong>+ PPM</strong>: ${formatear_miles(ppm)}</p>
    <p style="margin:6px 0;"><strong>+ Retención de honorarios</strong>: ${formatear_miles(honorarios)}</p>
    <p style="margin:6px 0;"><strong>+ Impuesto único trabajadores</strong>: ${formatear_miles(impuesto_unico)}</p>
    <p style="margin:6px 0;"><strong>+ IVA postergado anterior</strong>: ${formatear_miles(iva_postergado)}</p>
    <hr style="border:1px solid #475569;">
    <p style="margin:6px 0; font-size:22px;"><strong>TOTAL ESTIMADO F29</strong>: ${formatear_miles(total_f29)}</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("### 3) Descalce financiero del IVA")
    b1, b2, b3 = st.columns(3)
    b1.metric("IVA ya cobrado a tus clientes", f"${formatear_miles(iva_cobrado)}")
    b2.metric("IVA que estás poniendo de tu bolsillo", f"${formatear_miles(iva_puesto_por_la_empresa)}")
    b3.metric("% del IVA que aún no has cobrado", f"{int(porcentaje_financiado)}%")

    st.markdown("### 4) ¿Qué significa esto en simple?")
    st.markdown(f"""
<div style="background-color:#0F172A; padding:18px; border-radius:12px; border:1px solid #334155;">
    <p style="margin:6px 0;">
        Este mes tu negocio generó <strong>${formatear_miles(iva_debito)}</strong> de IVA por ventas.
    </p>
    <p style="margin:6px 0;">
        Tus compras te ayudan a descontar <strong>${formatear_miles(iva_credito)}</strong>.
    </p>
    <p style="margin:6px 0;">
        Por eso, tu <strong>IVA neto a pagar</strong> es <strong>${formatear_miles(iva_a_pagar)}</strong>.
    </p>
    <p style="margin:6px 0;">
        Pero antes del F29 solo has cobrado <strong>${formatear_miles(iva_cobrado)}</strong> de ese IVA.
    </p>
    <p style="margin:6px 0;">
        Eso significa que hoy estás poniendo con tu propia caja <strong>${formatear_miles(iva_puesto_por_la_empresa)}</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

    st.markdown("### 5) Diagnóstico ejecutivo")
    if semaforo == "VERDE":
        st.success(f"🟢 {semaforo}: {mensaje_semaforo}")
    elif semaforo == "AMARILLO":
        st.warning(f"🟡 {semaforo}: {mensaje_semaforo}")
    else:
        st.error(f"🔴 {semaforo}: {mensaje_semaforo} (capital de trabajo)")

    st.markdown("### 6) Recomendación práctica")
    if semaforo == "VERDE":
        st.info("Tu nivel de riesgo es controlado. Aun así, monitorea mensualmente cobros, IVA y capital de trabajo.")
    elif semaforo == "AMARILLO":
        st.info("Conviene revisar plazos de cobro, anticipos y provisión de impuestos para evitar que el problema crezca.")
    else:
        st.info("Tu empresa está financiando IVA antes de cobrarlo. Revisa de inmediato plazos de pago de clientes, provisión mensual y riesgo de atraso ante Tesorería.")

    # ===============================
    # INFORMACIÓN LEGAL CORREGIDA
    # ===============================
    st.markdown("---")
    st.markdown("## Información legal importante")

    st.info("""
- El Formulario 29 debe presentarse mensualmente, incluso sin movimiento.
- Con pago por Internet: vence el día 20 del mes siguiente.
- Sin pago por Internet, incluido sin movimiento: vence el día 28 del mes siguiente.
- Si el vencimiento cae en sábado, domingo, festivo o en el caso especial que corresponda, se prorroga al día hábil siguiente.
- Declarar o pagar fuera de plazo genera multas, intereses y reajustes.
""")

    st.markdown("""
**Normativa relevante**
- Art. 97 N° 2 del Código Tributario.
- Art. 97 N° 11 del Código Tributario.
""")

    st.caption("""
Referencia rápida:
- Art. 97 N° 2: multa de 1 UTM a 1 UTA.
- Art. 97 N° 11: multa de 10% sobre el impuesto adeudado, más 2% por cada mes o fracción de mes de atraso, con tope de 30%.
  Si la omisión es detectada por el Servicio, la multa base sube a 20%, más 2% por mes o fracción, con tope de 60%.
""")

    st.markdown("""
⚠️ Esta herramienta es preventiva y no reemplaza una asesoría profesional.
""")