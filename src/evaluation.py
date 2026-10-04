"""Métricas, comparação entre modelos e gráficos de avaliação.

Este módulo concentra as funções de avaliação que serão usadas no notebook
04_avaliacao.ipynb. Além das métricas padrão (accuracy, precision, recall,
f1, roc_auc), inclui métricas específicas para classificação desbalanceada:

- KS (Kolmogorov-Smirnov): separação entre as distribuições de scores dos
  bons e maus pagadores. Padrão em risco de crédito.
- Average precision (PR-AUC): área sob a curva precision-recall, robusta
  ao desbalanceamento.
- Curva de captura top-k%: fração dos inadimplentes capturada ao sinalizar
  os k% clientes mais arriscados.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import ks_2samp
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

from src.config import FIGURES, METRICS

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (10, 5)
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 10


# --------------------------------------------------------------- métricas --
def score(y_true, y_pred, y_proba=None) -> dict[str, float]:
    """Conjunto de métricas para classificação binária.

    Acurácia sozinha engana em base desbalanceada, por isso precisão, recall,
    F1, AUC-ROC e average precision vêm junto. O KS é calculado sobre as
    probabilidades previstas.
    """
    out = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
    }
    if y_proba is not None:
        out["roc_auc"] = roc_auc_score(y_true, y_proba)
        out["average_precision"] = average_precision_score(y_true, y_proba)
        out["ks"] = ks_statistic(y_true, y_proba)
    return out


def ks_statistic(y_true, y_proba) -> float:
    """KS = maior distância entre as CDFs de bons e maus pagadores.

    Quanto maior, melhor a separação. Em risco de crédito, valores acima
    de 0,30 são considerados bons; acima de 0,40, muito bons.
    """
    y_true = np.asarray(y_true)
    y_proba = np.asarray(y_proba)
    return ks_2samp(y_proba[y_true == 1], y_proba[y_true == 0]).statistic


def capture_at_k(y_true, y_proba, k: float) -> dict[str, float]:
    """Fração dos positivos capturada ao sinalizar os k% mais arriscados.

    Exemplo: k=0.10 → olhamos para os 10% de clientes com maior
    probabilidade prevista e contamos quantos dos inadimplentes reais
    estão nessa fatia.
    """
    y_true = np.asarray(y_true)
    y_proba = np.asarray(y_proba)
    ordem = np.argsort(-y_proba)
    y_ordenado = y_true[ordem]
    n_flag = int(np.ceil(len(y_true) * k))
    capturados = int(y_ordenado[:n_flag].sum())
    n_positivos = int(y_true.sum())
    precisao_fatia = capturados / n_flag if n_flag > 0 else 0.0
    taxa_base = y_true.mean()
    return {
        "k": k,
        "n_sinalizados": n_flag,
        "capturados": capturados,
        "captura": capturados / n_positivos if n_positivos else 0.0,
        "precision_fatia": precisao_fatia,
        "lift": precisao_fatia / taxa_base if taxa_base else 0.0,
    }


# ---------------------------------------------------------- comparação ----
def comparison_table(results: dict[str, dict]) -> pd.DataFrame:
    """Monta a tabela comparativa e salva em results/metrics/."""
    df = pd.DataFrame(results).T.round(4).sort_values("roc_auc", ascending=False)
    METRICS.mkdir(parents=True, exist_ok=True)
    df.to_csv(METRICS / "comparacao_modelos.csv")
    return df


# -------------------------------------------------------------- gráficos --
def plot_roc_curve(y_true, y_proba, nome_modelo: str, ax=None):
    """Curva ROC do modelo. Salva em results/figures/ se ax=None."""
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    auc = roc_auc_score(y_true, y_proba)
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(fpr, tpr, color="#2a78d6", linewidth=2, label=f"AUC = {auc:.3f}")
    ax.plot([0, 1], [0, 1], color="#898781", linestyle="--", linewidth=1.2)
    ax.set_xlabel("Taxa de falsos positivos")
    ax.set_ylabel("Taxa de verdadeiros positivos")
    ax.set_title(f"Curva ROC : {nome_modelo}")
    ax.legend(frameon=False, loc="lower right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if ax is None:
        plt.tight_layout()
        plt.savefig(FIGURES / f"roc_{nome_modelo}.png", dpi=150, bbox_inches="tight")
        plt.close()
    return ax


def plot_pr_curve(y_true, y_proba, nome_modelo: str, ax=None):
    """Curva precision-recall do modelo."""
    precisao, recall, _ = precision_recall_curve(y_true, y_proba)
    ap = average_precision_score(y_true, y_proba)
    taxa_base = np.mean(y_true)
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(recall, precisao, color="#2a78d6", linewidth=2, label=f"AP = {ap:.3f}")
    ax.axhline(taxa_base, color="#898781", linestyle="--", linewidth=1.2,
               label=f"Taxa base = {taxa_base:.1%}")
    ax.set_xlabel("Recall (mau pagador)")
    ax.set_ylabel("Precision (mau pagador)")
    ax.set_title(f"Curva Precision-Recall : {nome_modelo}")
    ax.legend(frameon=False, loc="upper right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if ax is None:
        plt.tight_layout()
        plt.savefig(FIGURES / f"pr_{nome_modelo}.png", dpi=150, bbox_inches="tight")
        plt.close()
    return ax


def plot_capture_curve(y_true, y_proba, nome_modelo: str, ax=None):
    """Curva de captura acumulada dos inadimplentes."""
    y_true = np.asarray(y_true)
    y_proba = np.asarray(y_proba)
    ordem = np.argsort(-y_proba)
    y_ordenado = y_true[ordem]
    n = len(y_true)
    n_pos = int(y_true.sum())
    fracao_sinalizada = np.arange(1, n + 1) / n
    captura_acumulada = np.cumsum(y_ordenado) / n_pos
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(fracao_sinalizada, captura_acumulada, color="#2a78d6",
            linewidth=2, label=nome_modelo)
    ax.plot([0, 1], [0, 1], color="#898781", linestyle="--",
            linewidth=1.2, label="Ordenação aleatória")
    ax.set_xlabel("Fração da carteira sinalizada (mais arriscados primeiro)")
    ax.set_ylabel("Fração dos inadimplentes capturada")
    ax.set_title("Curva de captura")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.legend(frameon=False, loc="lower right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if ax is None:
        plt.tight_layout()
        plt.savefig(FIGURES / f"captura_{nome_modelo}.png", dpi=150, bbox_inches="tight")
        plt.close()
    return ax

# ----------------------------------------------------- validação cruzada --
from sklearn.model_selection import StratifiedGroupKFold


def cross_validate_model(
    pipeline,
    X: pd.DataFrame,
    y: pd.Series,
    groups: pd.Series,
    cv_folds: int = 5,
    random_state: int = 42,
) -> pd.DataFrame:
    """Roda StratifiedGroupKFold e retorna métricas por fold.

    Parâmetros
    ----------
    pipeline : sklearn Pipeline
        Modelo já encapsulado (com scaler, se aplicável).
    X : pd.DataFrame
        Features.
    y : pd.Series
        Target binário.
    groups : pd.Series
        Grupo de cada amostra (para evitar que gêmeos caiam em folds diferentes).
    cv_folds : int
        Número de folds.
    random_state : int
        Semente para reprodutibilidade.

    Retorna
    -------
    pd.DataFrame
        Uma linha por fold, com as colunas de `score()` + coluna "fold".
    """
    sgkf = StratifiedGroupKFold(
        n_splits=cv_folds,
        shuffle=True,
        random_state=random_state,
    )

    metricas_por_fold = []

    for fold, (idx_train, idx_val) in enumerate(sgkf.split(X, y, groups=groups)):
        X_train, X_val = X.iloc[idx_train], X.iloc[idx_val]
        y_train, y_val = y.iloc[idx_train], y.iloc[idx_val]

        # Treina no fold de treino e prevê no fold de validação
        pipeline.fit(X_train, y_train)
        y_proba = pipeline.predict_proba(X_val)[:, 1]
        y_pred = (y_proba >= 0.5).astype(int)

        # Calcula métricas
        m = score(y_val, y_pred, y_proba)
        m["fold"] = fold
        metricas_por_fold.append(m)

    return pd.DataFrame(metricas_por_fold)


def summarize_folds(df_metricas: pd.DataFrame) -> pd.Series:
    """Agrega as métricas por fold em média + desvio-padrão.

    Útil para comparar modelos na tabela final.
    """
    return df_metricas.drop(columns="fold").agg(["mean", "std"]).T.round(4)