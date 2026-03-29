from config import (
    UMBRAL_IVA_FINANCIADO_AMARILLO,
    UMBRAL_IVA_FINANCIADO_ROJO,
)


def determinar_semaforo(resultado) -> tuple[str, str]:
    """
    Reglas simples para versión 1.
    """

    if resultado.total_f29 <= 0 and resultado.remanente_credito_fiscal > 0:
        return (
            "AMARILLO",
            "Existe remanente de crédito fiscal. La situación requiere revisión preventiva."
        )

    if resultado.porcentaje_iva_financiado >= UMBRAL_IVA_FINANCIADO_ROJO:
        return (
            "ROJO",
            "La empresa financia una parte crítica del IVA con su propia caja."
        )

    if resultado.porcentaje_iva_financiado >= UMBRAL_IVA_FINANCIADO_AMARILLO:
        return (
            "AMARILLO",
            "Existe tensión de caja: una parte relevante del IVA aún no ha sido cobrada."
        )

    if resultado.impuesto_por_pagar > 0 and resultado.iva_financiado > 0:
        return (
            "AMARILLO",
            "Existe impuesto por pagar y parte de ese IVA está siendo financiado por la empresa."
        )

    return (
        "VERDE",
        "La estructura tributaria y de caja luce razonable en esta revisión básica."
    )