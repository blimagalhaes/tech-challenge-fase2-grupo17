"""Definição e treino dos modelos.

Três classificadores são comparados:
1. Regressão Logística: baseline interpretável, bom para entender o sinal.
2. Random Forest: modelo não-linear, robusto a outliers, não exige escala.
3. XGBoost: gradient boosting, tipicamente forte em dados tabulares.

Todos são encapsulados em Pipeline para evitar vazamento de dados: o scaler
(quando aplicável) é ajustado apenas no fold de treino durante a validação
cruzada.
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from src.config import RANDOM_STATE


def get_logistic_regression() -> Pipeline:
    """Regressão Logística com imputação e padronização.

    O SimpleImputer(strategy="median") é necessário porque a coluna
    cad_anos_emprego tem NaN para clientes desempregados.
    O StandardScaler é necessário porque a Regressão Logística é sensível
    à escala das variáveis de entrada.
    O class_weight="balanced" compensa o desbalanceamento sem alterar os
    dados de treino.
    """
    return Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(
            max_iter=3000,
            class_weight="balanced",
            C=0.3,
            random_state=RANDOM_STATE,
        )),
    ])


def get_random_forest() -> Pipeline:
    """Random Forest com imputação.

    O SimpleImputer é necessário pela mesma razão da Regressão Logística:
    a coluna cad_anos_emprego tem NaN. Diferente da Regressão Logística,
    o RandomForest não precisa de StandardScaler (é invariante à escala).
    O class_weight="balanced_subsample" repondera cada árvore pela
    frequência das classes na subamostra bootstrap.
    """
    return Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("clf", RandomForestClassifier(
            n_estimators=400,
            min_samples_leaf=30,
            max_features=0.3,
            class_weight="balanced_subsample",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )),
    ])


def get_xgboost(scale_pos_weight: float) -> Pipeline:
    """XGBoost com regularização para evitar overfitting em classe rara.

    Parâmetros:
    - scale_pos_weight: razão negativos/positivos no treino, dividida por 3
      para evitar overcompensação (o valor puro tende a inflar o recall
      artificialmente). Precisa ser calculado a partir do y_train.
    - reg_lambda: regularização L2, aumenta a penalização em folhas profundas.
    - min_child_weight: mínimo de amostras por folha, evita overfitting.
    - max_depth baixo (3) + learning_rate baixo (0.03): modelo mais estável.
    """
    return Pipeline([
        ("clf", XGBClassifier(
            n_estimators=400,
            max_depth=3,
            learning_rate=0.03,
            subsample=0.8,
            colsample_bytree=0.7,
            min_child_weight=20,
            reg_lambda=10,
            scale_pos_weight=scale_pos_weight / 3,
            eval_metric="aucpr",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )),
    ])


def get_models(scale_pos_weight: float) -> dict[str, Pipeline]:
    """Devolve o dicionário com os três modelos candidatos.

    O parâmetro scale_pos_weight precisa ser calculado a partir do y_train
    (razão entre a classe majoritária e a minoritária). Exemplo:

        spw = (y_train == 0).sum() / y_train.sum()
        modelos = get_models(spw)
    """
    return {
        "logistic_regression": get_logistic_regression(),
        "random_forest": get_random_forest(),
        "xgboost": get_xgboost(scale_pos_weight),
    }