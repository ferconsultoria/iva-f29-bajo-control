from config import TASA_IVA


def calcular_debito_fiscal(ventas_netas_mes: float) -> float:
    return ventas_netas_mes * TASA_IVA


def calcular_credito_fiscal(compras_netas_mes: float) -> float:
    return compras_netas_mes * TASA_IVA


def determinar_resultado_iva(
    debito_fiscal: float,
    credito_fiscal: float,
    remanente_anterior: float = 0.0
) -> dict:
    """
    En esta versión 1, el remanente anterior se suma al crédito fiscal disponible.
    """
    credito_total_disponible = credito_fiscal + remanente_anterior

    if debito_fiscal > credito_total_disponible:
        impuesto_por_pagar = debito_fiscal - credito_total_disponible
        remanente_credito_fiscal = 0.0
    elif credito_total_disponible > debito_fiscal:
        impuesto_por_pagar = 0.0
        remanente_credito_fiscal = credito_total_disponible - debito_fiscal
    else:
        impuesto_por_pagar = 0.0
        remanente_credito_fiscal = 0.0

    return {
        "impuesto_por_pagar": impuesto_por_pagar,
        "remanente_credito_fiscal": remanente_credito_fiscal,
    }