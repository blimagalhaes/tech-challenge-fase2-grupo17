"""Limpeza, escala e feature engineering.

Se você decidir NÃO criar features novas, documente a decisão e o porquê —
a justificativa da não-aplicação é tão importante quanto a aplicação.
"""

import pandas as pd


def check_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Resumo de nulos por coluna, em contagem e percentual."""
    total = df.isna().sum()
    pct = (total / len(df) * 100).round(2)
    return (
        pd.DataFrame({"nulos": total, "pct": pct})
        .query("nulos > 0")
        .sort_values("nulos", ascending=False)
    )


def binarize_target(df: pd.DataFrame, column: str, threshold: float) -> pd.DataFrame:
    """Converte uma variável contínua em binária a partir de um limiar.

    O limiar é uma decisão de modelagem: justifique-o no README com base na
    distribuição observada, não apenas por convenção.
    """
    out = df.copy()
    out[f"{column}_bin"] = (out[column] >= threshold).astype(int)
    return out


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """PREENCHER: crie aqui as features derivadas, uma função por ideia."""
    return df.copy()
