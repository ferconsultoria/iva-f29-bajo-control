from models.resultado import ResultadoAnalisis
from services.calculadora_iva import (
    calcular_debito_fiscal,
    calcular_credito_fiscal,
    determinar_resultado_iva,
)
from services.calculadora_f29 import calcular_total_f29
from services.calculadora_caja import (
    calcular_iva_cobrado,
    calcular_iva_financiado,
    calcular_porcentaje_iva_financiado,
)
from services.alertas import generar_alertas
from services.semaforo import determinar_semaforo
from utils.validaciones import validar_numero_no_negativo
from utils.formateo import formatear_moneda, formatear_porcentaje


def pedir_float(mensaje: str) -> float:
    while True:
        try:
            valor = float(input(mensaje))
            return valor
        except ValueError:
            print("Error: debe ingresar un número válido.")


def main():
    print("\n=== IVA BAJO CONTROL ===")
    print("Inteligencia empresarial aplicada a los impuestos\n")

    try:
        ventas_netas_mes = pedir_float("Ingrese ventas netas del mes: ")
        compras_netas_mes = pedir_float("Ingrese compras netas del mes: ")
        ventas_cobradas_antes_f29 = pedir_float("Ingrese ventas netas cobradas antes del F29: ")
        remanente_anterior = pedir_float("Ingrese remanente de crédito fiscal anterior: ")
        iva_postergado_anterior = pedir_float("Ingrese IVA postergado anterior: ")
        ppm = pedir_float("Ingrese PPM del período: ")
        retencion_honorarios = pedir_float("Ingrese retención de honorarios: ")
        impuesto_unico = pedir_float("Ingrese impuesto único trabajadores: ")

        validar_numero_no_negativo(ventas_netas_mes, "ventas_netas_mes")
        validar_numero_no_negativo(compras_netas_mes, "compras_netas_mes")
        validar_numero_no_negativo(ventas_cobradas_antes_f29, "ventas_cobradas_antes_f29")
        validar_numero_no_negativo(remanente_anterior, "remanente_anterior")
        validar_numero_no_negativo(iva_postergado_anterior, "iva_postergado_anterior")
        validar_numero_no_negativo(ppm, "ppm")
        validar_numero_no_negativo(retencion_honorarios, "retencion_honorarios")
        validar_numero_no_negativo(impuesto_unico, "impuesto_unico")

        resultado = ResultadoAnalisis()

        resultado.debito_fiscal = calcular_debito_fiscal(ventas_netas_mes)
        resultado.credito_fiscal = calcular_credito_fiscal(compras_netas_mes)

        iva_resultado = determinar_resultado_iva(
            resultado.debito_fiscal,
            resultado.credito_fiscal,
            remanente_anterior
        )

        resultado.impuesto_por_pagar = iva_resultado["impuesto_por_pagar"]
        resultado.remanente_credito_fiscal = iva_resultado["remanente_credito_fiscal"]

        resultado.ppm = ppm
        resultado.retencion_honorarios = retencion_honorarios
        resultado.impuesto_unico = impuesto_unico
        resultado.iva_postergado_anterior = iva_postergado_anterior

        resultado.total_f29 = calcular_total_f29(
            resultado.impuesto_por_pagar,
            resultado.ppm,
            resultado.retencion_honorarios,
            resultado.impuesto_unico,
            resultado.iva_postergado_anterior
        )

        resultado.iva_cobrado = calcular_iva_cobrado(ventas_cobradas_antes_f29)
        resultado.iva_financiado = calcular_iva_financiado(
            resultado.debito_fiscal,
            resultado.iva_cobrado
        )
        resultado.porcentaje_iva_financiado = calcular_porcentaje_iva_financiado(
            resultado.debito_fiscal,
            resultado.iva_financiado
        )

        resultado.alertas = generar_alertas(
            resultado,
            ventas_netas_mes,
            compras_netas_mes
        )
        resultado.semaforo, resultado.comentario = determinar_semaforo(resultado)

        print("\n" + "=" * 50)
        print("RESULTADO DEL ANÁLISIS")
        print("=" * 50)

        print(f"Débito fiscal: {formatear_moneda(resultado.debito_fiscal)}")
        print(f"Crédito fiscal: {formatear_moneda(resultado.credito_fiscal)}")
        print(f"Impuesto por pagar: {formatear_moneda(resultado.impuesto_por_pagar)}")
        print(f"Remanente crédito fiscal: {formatear_moneda(resultado.remanente_credito_fiscal)}")
        print(f"PPM: {formatear_moneda(resultado.ppm)}")
        print(f"Retención honorarios: {formatear_moneda(resultado.retencion_honorarios)}")
        print(f"Impuesto único: {formatear_moneda(resultado.impuesto_unico)}")
        print(f"IVA postergado anterior: {formatear_moneda(resultado.iva_postergado_anterior)}")
        print(f"Total F29 estimado: {formatear_moneda(resultado.total_f29)}")

        print("\n--- CAPA DE CAJA ---")
        print(f"IVA cobrado antes del F29: {formatear_moneda(resultado.iva_cobrado)}")
        print(f"IVA financiado por la empresa: {formatear_moneda(resultado.iva_financiado)}")
        print(f"% IVA financiado: {formatear_porcentaje(resultado.porcentaje_iva_financiado)}")

        print("\n--- SEMÁFORO ---")
        print(f"Semáforo: {resultado.semaforo}")
        print(f"Comentario: {resultado.comentario}")

        print("\n--- ALERTAS ---")
        if resultado.alertas:
            for i, alerta in enumerate(resultado.alertas, start=1):
                print(f"{i}. {alerta}")
        else:
            print("Sin alertas relevantes en esta revisión básica.")

        print("\nAviso: este resultado es una estimación preventiva y no reemplaza la determinación tributaria final, determinada por un asesor.")

    except Exception as e:
        print(f"\nOcurrió un error: {e}")


if __name__ == "__main__":
    main()