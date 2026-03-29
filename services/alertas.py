def generar_alertas(resultado, ventas_netas_mes: float, compras_netas_mes: float) -> list[str]:
    alertas = []

    if ventas_netas_mes <= 0:
        alertas.append("La empresa no registra ventas netas en el período.")

    if compras_netas_mes >= ventas_netas_mes and ventas_netas_mes > 0:
        alertas.append(
            "Las compras son iguales o superiores a las ventas. Revise margen y coherencia comercial."
        )

    if resultado.impuesto_por_pagar > 0 and resultado.iva_financiado > 0:
        alertas.append(
            "Debe pagar IVA antes de haber cobrado completamente sus ventas."
        )

    if resultado.iva_financiado > 0:
        alertas.append(
            "Está financiando IVA con capital de trabajo de la empresa."
        )

    if resultado.iva_postergado_anterior > 0 and resultado.impuesto_por_pagar > 0:
        alertas.append(
            "Existe efecto bola de nieve: mantiene IVA postergado anterior y además nuevo IVA por pagar."
        )

    if resultado.remanente_credito_fiscal > 0:
        alertas.append(
            "Existe remanente de crédito fiscal. Revise si responde a una situación normal del negocio."
        )

    if resultado.total_f29 > 0 and resultado.iva_cobrado < resultado.impuesto_por_pagar:
        alertas.append(
            "El IVA efectivamente cobrado no alcanza para cubrir el IVA del período."
        )

    return alertas