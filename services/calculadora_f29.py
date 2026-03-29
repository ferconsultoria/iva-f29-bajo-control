def calcular_total_f29(
    impuesto_por_pagar: float,
    ppm: float,
    retencion_honorarios: float,
    impuesto_unico: float,
    iva_postergado_anterior: float = 0.0
) -> float:
    return (
        impuesto_por_pagar
        + ppm
        + retencion_honorarios
        + impuesto_unico
        + iva_postergado_anterior
    )