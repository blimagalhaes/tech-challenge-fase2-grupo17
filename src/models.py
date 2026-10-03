"""Definição e treino dos modelos.

Use no mínimo DOIS classificadores distintos.
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.config import RANDOM_STATE


def get_models() -> dict[str, Pipeline]:
    """Modelos candidatos, cada um encapsulado em um Pipeline.

    Usar Pipeline evita vazamento de dados: o scaler é ajustado apenas no fold
    de treino durante a validação cruzada.
    """
    return {
        "logistic_regression": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
        ]),
        "random_forest": Pipeline([
            ("clf", RandomForestClassifier(
                n_estimators=300,
                random_state=RANDOM_STATE,
                n_jobs=-1,
            )),
        ]),
        # PREENCHER: adicione outros candidatos (SVM, XGBoost, LightGBM...)
    }
