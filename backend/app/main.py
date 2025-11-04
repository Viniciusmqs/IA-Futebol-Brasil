from fastapi import FastAPI, HTTPException
from app.models.partida_model import PartidaEntrada
from app.services.predict_service import prever_partida
from app.services.times_service import listar_times, comparar_times, perfil_time

app = FastAPI(
    title="IA Futebol Brasil",
    description="API de previsão de resultados do Brasileirão baseada em dados estatísticos.",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "API IA Futebol Brasil - Online"}

@app.post("/prever")
def prever(entrada: PartidaEntrada):
    resultado = prever_partida(entrada.dict())
    return {"probabilidades": resultado}

@app.get("/times")
def get_times():
    """
    Retorna a lista de todos os times presentes na base do Brasileirão.
    """
    return {"times": listar_times()}

@app.get("/comparar-times")
def get_comparacao_times(time_a: str, time_b: str):
    """
    Compara estatísticas gerais entre dois times (gols, vitórias, empates, etc.).
    """
    try:
        comparacao = comparar_times(time_a, time_b)
        return comparacao
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/perfil-time")
def get_perfil_time(time: str):
    """
    Retorna o perfil estatístico médio de um time (para gráfico de radar).
    """
    try:
        perfil = perfil_time(time)
        return {"time": time, "perfil": perfil}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
