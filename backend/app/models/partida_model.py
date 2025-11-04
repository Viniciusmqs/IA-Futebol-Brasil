from pydantic import BaseModel

class PartidaEntrada(BaseModel):
    ano_campeonato: int
    rodada: int
    colocacao_mandante: float
    colocacao_visitante: float
    valor_equipe_titular_mandante: float
    valor_equipe_titular_visitante: float
    idade_media_titular_mandante: float
    idade_media_titular_visitante: float
    publico_max: float
