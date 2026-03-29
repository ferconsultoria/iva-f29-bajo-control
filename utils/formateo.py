def formatear_moneda(valor: float) -> str:
    return f"${valor:,.0f}"


def formatear_porcentaje(valor: float) -> str:
    return f"{valor * 100:.2f}%"