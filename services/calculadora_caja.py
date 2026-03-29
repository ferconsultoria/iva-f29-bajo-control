from config import TASA_IVA


def calcular_iva_cobrado(ventas_cobradas_antes_f29: float) -> float:
    """
    Asume que 'ventas_cobradas_antes_f29' es monto neto cobrado.
    """
    return ventas_cobradas_antes_f29 * TASA_IVA


def calcular_iva_financiado(debito_fiscal_total: float, iva_cobrado: float) -> float:
    """
    Si el IVA cobrado es menor al débito fiscal, la diferencia representa
    IVA financiado por la empresa.
    """
    diferencia = debito_fiscal_total - iva_cobrado
    return diferencia if diferencia > 0 else 0.0


def calcular_porcentaje_iva_financiado(
    debito_fiscal_total: float,
    iva_financiado: float
) -> float:
    if debito_fiscal_total <= 0:
        return 0.0
    return iva_financiado / debito_fiscal_total