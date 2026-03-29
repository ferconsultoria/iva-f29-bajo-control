import streamlit as st

# ===============================
# CONFIGURACIÓN GENERAL
# ===============================
st.set_page_config(
    page_title="Flujo de Caja Tributario",
    page_icon="⚠️",
    layout="wide"
)

# ===============================
# FUNCIONES
# ===============================
def formatear_miles(valor):
    return f"{int(round(valor)):,}".replace(",", ".")


def calcular_ppm(ventas, tasa):
    return ventas * tasa


def limpiar_formulario():
    claves = [
        "ventas",
        "ventas_cobradas",
        "compras",
        "remanente",
        "tasa_ppm_porcentaje",
        "honorarios",
        "impuesto_unico",
        "iva_postergado_1",
        "iva_postergado_2",
        "iva_vencido_impago"
    ]
    for clave in claves:
        if clave in st.session_state:
            del st.session_state[clave]


# ===============================
# ENCABEZADO
# ===============================
st.title("Flujo de Caja Tributario")
st.subheader("Control mensual del F29, IVA acumulado y riesgo de caja")

st.markdown("""
**Muchas empresas no se complican por falta de ventas, sino por no entender cuánto impuesto generan, cuánto arrastran y cuánto están financiando con su propio capital de trabajo.**
""")

st.markdown("""
Esta herramienta le ayuda a visualizar:
- cuánto IVA genera su negocio este mes,
- cuánto puede recuperar por sus compras,
- cuánto realmente debe pagar ahora,
- cuánto IVA viene arrastrando,
- y cuál es su exposición tributaria total a la fecha.
""")

col_boton_1, col_boton_2, col_boton_3 = st.columns([1, 1, 4])
with col_boton_1:
    st.button("Limpiar formulario", on_click=limpiar_formulario)

# ===============================
# BLOQUE 1: VENTAS
# ===============================
st.markdown("## 1) Ventas e IVA de ventas")

col1, col2 = st.columns(2)

with col1:
    ventas = st.number_input(
        "Ventas netas del mes",
        min_value=0,
        step=100000,
        key="ventas"
    )

with col2:
    ventas_cobradas = st.number_input(
        "Ventas cobradas antes del F29",
        min_value=0,
        step=100000,
        key="ventas_cobradas"
    )

# ===============================
# BLOQUE 2: COMPRAS
# ===============================
st.markdown("## 2) Compras e IVA de compras")

col1, col2 = st.columns(2)

with col1:
    compras = st.number_input(
        "Compras netas del mes",
        min_value=0,
        step=100000,
        key="compras"
    )

with col2:
    remanente = st.number_input(
        "Remanente de crédito fiscal anterior",
        min_value=0,
        step=100000,
        key="remanente"
    )

# ===============================
# BLOQUE 3: PPM Y OTROS IMPUESTOS
# ===============================
st.markdown("## 3) Carga tributaria del mes")

col1, col2 = st.columns(2)

with col1:
    tasa_ppm_porcentaje = st.number_input(
        "Tasa PPM (%)",
        min_value=0.0,
        value=1.0,
        step=0.1,
        key="tasa_ppm_porcentaje"
    )
    tasa_ppm = tasa_ppm_porcentaje / 100
    ppm = calcular_ppm(ventas, tasa_ppm)

with col2:
    st.info(f"PPM estimado del mes: ${formatear_miles(ppm)}")

col1, col2 = st.columns(2)

with col1:
    honorarios = st.number_input(
        "Retención de honorarios del mes",
        min_value=0,
        step=100000,
        key="honorarios"
    )

with col2:
    impuesto_unico = st.number_input(
        "Impuesto único trabajadores del mes",
        min_value=0,
        step=100000,
        key="impuesto_unico"
    )

# ===============================
# BLOQUE 4: DEUDA ACUMULADA IVA
# ===============================
st.markdown("## 4) Deuda acumulada por IVA")

col1, col2, col3 = st.columns(3)

with col1:
    iva_postergado_1 = st.number_input(
        "IVA postergado vigente - período 1",
        min_value=0,
        step=100000,
        key="iva_postergado_1"
    )

with col2:
    iva_postergado_2 = st.number_input(
        "IVA postergado vigente - período 2",
        min_value=0,
        step=100000,
        key="iva_postergado_2"
    )

with col3:
    iva_vencido_impago = st.number_input(
        "IVA vencido e impago",
        min_value=0,
        step=100000,
        key="iva_vencido_impago"
    )

# ===============================
# BOTÓN PRINCIPAL
# ===============================
if st.button("Analizar flujo de caja tributario"):

    # ===============================
    # CÁLCULOS BASE
    # ===============================
    iva_ventas = ventas * 0.19
    iva_compras = compras * 0.19

    iva_neto_mes = iva_ventas - iva_compras - remanente
    iva_neto_mes = max(0, iva_neto_mes)

    carga_tributaria_inmediata = iva_neto_mes + ppm + honorarios + impuesto_unico

    deuda_acumulada_iva = iva_postergado_1 + iva_postergado_2 + iva_vencido_impago

    exposicion_tributaria_total = carga_tributaria_inmediata + deuda_acumulada_iva

    iva_cobrado = ventas_cobradas * 0.19
    iva_cubierto_con_caja = max(0, iva_neto_mes - iva_cobrado)
    porcentaje_no_cobrado = (iva_cubierto_con_caja / iva_neto_mes * 100) if iva_neto_mes > 0 else 0

    # ===============================
    # SEMÁFORO
    # ===============================
    if porcentaje_no_cobrado < 20:
        semaforo = "VERDE"
        mensaje_semaforo = "Tu empresa está cubriendo razonablemente el IVA del mes con cobros reales."
    elif porcentaje_no_cobrado < 50:
        semaforo = "AMARILLO"
        mensaje_semaforo = "Atención: una parte relevante del IVA del mes aún no ha sido cobrada."
    else:
        semaforo = "ROJO"
        mensaje_semaforo = "Riesgo alto: tu empresa está pagando IVA con su capital de trabajo."

    # ===============================
    # RESULTADO
    # ===============================
    st.markdown("---")
    st.markdown("# Tu diagnóstico tributario del mes")

    # IVA del período
    st.markdown("## 1) IVA del período")
    a1, a2, a3 = st.columns(3)
    a1.metric("IVA generado por tus ventas", f"${formatear_miles(iva_ventas)}")
    a2.metric("IVA recuperable por tus compras", f"${formatear_miles(iva_compras)}")
    a3.metric("IVA neto del mes", f"${formatear_miles(iva_neto_mes)}")

    # Carga tributaria inmediata
    st.markdown("## 2) Carga tributaria inmediata del mes")
    st.markdown(f"""
<div style="background-color:#1E293B; padding:18px; border-radius:12px; border:1px solid #334155;">
    <p style="margin:6px 0;"><strong>IVA neto del mes</strong>: ${formatear_miles(iva_neto_mes)}</p>
    <p style="margin:6px 0;"><strong>+ PPM del mes</strong>: ${formatear_miles(ppm)}</p>
    <p style="margin:6px 0;"><strong>+ Retención de honorarios del mes</strong>: ${formatear_miles(honorarios)}</p>
    <p style="margin:6px 0;"><strong>+ Impuesto único trabajadores del mes</strong>: ${formatear_miles(impuesto_unico)}</p>
    <hr style="border:1px solid #475569;">
    <p style="margin:6px 0; font-size:22px;"><strong>CARGA TRIBUTARIA INMEDIATA DEL MES</strong>: ${formatear_miles(carga_tributaria_inmediata)}</p>
</div>
""", unsafe_allow_html=True)

    # Deuda acumulada por IVA
    st.markdown("## 3) Deuda acumulada por IVA")
    st.markdown(f"""
<div style="background-color:#1E293B; padding:18px; border-radius:12px; border:1px solid #334155;">
    <p style="margin:6px 0;"><strong>IVA postergado vigente - período 1</strong>: ${formatear_miles(iva_postergado_1)}</p>
    <p style="margin:6px 0;"><strong>IVA postergado vigente - período 2</strong>: ${formatear_miles(iva_postergado_2)}</p>
    <p style="margin:6px 0;"><strong>IVA vencido e impago</strong>: ${formatear_miles(iva_vencido_impago)}</p>
    <hr style="border:1px solid #475569;">
    <p style="margin:6px 0; font-size:22px;"><strong>DEUDA ACUMULADA POR IVA</strong>: ${formatear_miles(deuda_acumulada_iva)}</p>
</div>
""", unsafe_allow_html=True)

    # Exposición tributaria total
    st.markdown("## 4) Exposición tributaria total a la fecha")
    e1, e2 = st.columns(2)
    e1.metric("Carga tributaria inmediata del mes", f"${formatear_miles(carga_tributaria_inmediata)}")
    e2.metric("Exposición tributaria total a la fecha", f"${formatear_miles(exposicion_tributaria_total)}")

    # Riesgo de caja tributaria
    st.markdown("## 5) Riesgo de caja tributaria")
    b1, b2, b3 = st.columns(3)
    b1.metric("IVA ya cobrado a tus clientes", f"${formatear_miles(iva_cobrado)}")
    b2.metric("IVA que estás cubriendo con tu capital de trabajo", f"${formatear_miles(iva_cubierto_con_caja)}")
    b3.metric("% del IVA del mes que aún no has cobrado", f"{int(porcentaje_no_cobrado)}%")

    # Explicación simple
    st.markdown("## 6) ¿Qué significa esto en simple?")
    st.markdown(f"""
<div style="background-color:#0F172A; padding:18px; border-radius:12px; border:1px solid #334155;">
    <p style="margin:6px 0;">
        Este mes tu negocio generó <strong>${formatear_miles(iva_ventas)}</strong> de IVA por ventas.
    </p>
    <p style="margin:6px 0;">
        Tus compras te ayudan a descontar <strong>${formatear_miles(iva_compras)}</strong>.
    </p>
    <p style="margin:6px 0;">
        Por eso, tu <strong>IVA neto del mes</strong> es <strong>${formatear_miles(iva_neto_mes)}</strong>.
    </p>
    <p style="margin:6px 0;">
        La <strong>carga tributaria inmediata del mes</strong> asciende a <strong>${formatear_miles(carga_tributaria_inmediata)}</strong>.
    </p>
    <p style="margin:6px 0;">
        Además, mantienes una <strong>deuda acumulada por IVA</strong> de <strong>${formatear_miles(deuda_acumulada_iva)}</strong>.
    </p>
    <p style="margin:6px 0;">
        En total, tu <strong>exposición tributaria a la fecha</strong> llega a <strong>${formatear_miles(exposicion_tributaria_total)}</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

    # Semáforo
    st.markdown("## 7) Diagnóstico ejecutivo")
    if semaforo == "VERDE":
        st.success(f"🟢 {semaforo}: {mensaje_semaforo}")
    elif semaforo == "AMARILLO":
        st.warning(f"🟡 {semaforo}: {mensaje_semaforo}")
    else:
        st.error(f"🔴 {semaforo}: {mensaje_semaforo} (capital de trabajo)")

    # Recomendación
    st.markdown("## 8) Recomendación práctica")
    if semaforo == "VERDE":
        st.info("Tu nivel de riesgo se ve controlado. Aun así, monitorea cada mes la relación entre cobro, IVA del período y deuda acumulada.")
    elif semaforo == "AMARILLO":
        st.info("Conviene revisar plazos de cobro, provisión de impuestos y acumulación de IVA postergado antes de que se transforme en un problema mayor.")
    else:
        st.info("Tu empresa está financiando IVA con caja propia y además puede estar acumulando deuda tributaria. Revisa de inmediato tu flujo de cobro, provisión mensual y riesgo frente a Tesorería.")

    # Información legal
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