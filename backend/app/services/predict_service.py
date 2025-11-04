import pandas as pd
from app.utils.load_model import carregar_modelo

modelo = carregar_modelo()

def prever_partida(dados: dict):
    df = pd.DataFrame([dados])
    probs = modelo.predict_proba(df)[0]
    classes = modelo.classes_
    return dict(zip(classes, [float(p) for p in probs]))
