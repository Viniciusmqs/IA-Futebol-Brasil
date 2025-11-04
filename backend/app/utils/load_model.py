import joblib
from pathlib import Path

def carregar_modelo():
    base_dir = Path(__file__).resolve().parents[2]
    modelo_path = base_dir / "app" / "models" / "modelo_basico.pkl"
    modelo = joblib.load(modelo_path)
    return modelo
