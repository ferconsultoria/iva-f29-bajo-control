def validar_numero_no_negativo(valor: float, nombre_campo: str) -> None:
    if valor < 0:
        raise ValueError(f"El campo '{nombre_campo}' no puede ser negativo.")