from dataclasses import dataclass, field


@dataclass
class ResultadoAnalisis:
    debito_fiscal: float = 0.0
    credito_fiscal: float = 0.0
    impuesto_por_pagar: float = 0.0
    remanente_credito_fiscal: float = 0.0

    ppm: float = 0.0
    retencion_honorarios: float = 0.0
    impuesto_unico: float = 0.0
    iva_postergado_anterior: float = 0.0

    total_f29: float = 0.0

    iva_cobrado: float = 0.0
    iva_financiado: float = 0.0
    porcentaje_iva_financiado: float = 0.0

    semaforo: str = ""
    comentario: str = ""
    alertas: list[str] = field(default_factory=list)