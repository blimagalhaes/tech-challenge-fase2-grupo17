"""Limpeza, definição do alvo e engenharia de features.

O pipeline de pré-processamento do Tech Challenge tem 6 etapas:
1. Mapeamento de STATUS para valor numérico.
2. Construção do target (mau_pagador).
3. Agregações do histórico mensal por cliente.
4. Proporções derivadas.
5. Deduplicação do application_record.
6. Merge final 1:1.
"""

import numpy as np
import pandas as pd

from src.config import LIMIAR_DIAS, TARGET

# Mapeamento de STATUS (string) para escala numérica de severidade.
# C e X significam "sem atraso" (0). Os valores '0' a '5' seguem a escala
# de dias em atraso: 0=1-29, 1=30-59, 2=60-89, 3=90-119, 4=120-149, 5=150+.
MAPA_STATUS = {
    "C": 0,  # pago no mês
    "X": 0,  # sem empréstimo no mês
    "0": 0,  # 1-29 dias
    "1": 1,  # 30-59 dias
    "2": 2,  # 60-89 dias
    "3": 3,  # 90-119 dias
    "4": 4,  # 120-149 dias
    "5": 5,  # 150+ dias
}


def check_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Resumo de nulos por coluna, em contagem e percentual."""
    total = df.isna().sum()
    pct = (total / len(df) * 100).round(2)
    return (
        pd.DataFrame({"nulos": total, "pct": pct})
        .query("nulos > 0")
        .sort_values("nulos", ascending=False)
    )


def mapear_status(cred: pd.DataFrame) -> pd.DataFrame:
    """Cria a coluna status_num a partir do STATUS (string)."""
    out = cred.copy()
    out["status_num"] = out["STATUS"].map(MAPA_STATUS)
    if out["status_num"].isna().any():
        valores = sorted(out.loc[out["status_num"].isna(), "STATUS"].unique())
        raise ValueError(f"STATUS com valor inesperado: {valores}")
    return out


def construir_target(cred: pd.DataFrame) -> pd.DataFrame:
    """Constrói o target binário por cliente.

    mau_pagador = 1 se o cliente atingiu atraso >= LIMIAR_DIAS (status_num >= 2)
    em pelo menos um mês do histórico. A definição é "ever bad" (algum dia).
    """
    cred = cred.copy()
    cred["ind_mau"] = (cred["status_num"] >= 2).astype(int)
    target = (
        cred.groupby("ID")["ind_mau"]
        .max()
        .reset_index()
        .rename(columns={"ind_mau": TARGET})
    )
    return target


def agregar_historico(cred: pd.DataFrame) -> pd.DataFrame:
    """Agrega o histórico mensal em uma linha por cliente.

    As features cobrem três dimensões: volume/tempo de relacionamento,
    severidade do atraso e contagens por tipo de status.
    """
    cred = cred.copy()
    agg = cred.groupby("ID").agg(
        hist_meses_total=("MONTHS_BALANCE", "count"),
        hist_mes_mais_antigo=("MONTHS_BALANCE", "min"),
        hist_mes_mais_recente=("MONTHS_BALANCE", "max"),
        hist_status_max=("status_num", "max"),
        hist_status_medio=("status_num", "mean"),
        hist_status_desvio=("status_num", "std"),
        hist_qtd_pago=("STATUS", lambda s: (s == "C").sum()),
        hist_qtd_sem_emprestimo=("STATUS", lambda s: (s == "X").sum()),
        hist_qtd_atraso=("status_num", lambda s: (s >= 1).sum()),
        hist_qtd_atraso_grave=("status_num", lambda s: (s >= 3).sum()),
    ).reset_index()

    # Desvio-padrão é NaN quando só há 1 mês observado -> 0
    agg["hist_status_desvio"] = agg["hist_status_desvio"].fillna(0)

    # Proporções derivadas
    agg["hist_prop_pago"] = agg["hist_qtd_pago"] / agg["hist_meses_total"]
    agg["hist_prop_sem_emprestimo"] = (
        agg["hist_qtd_sem_emprestimo"] / agg["hist_meses_total"]
    )
    agg["hist_prop_atraso"] = agg["hist_qtd_atraso"] / agg["hist_meses_total"]
    agg["hist_prop_atraso_grave"] = (
        agg["hist_qtd_atraso_grave"] / agg["hist_meses_total"]
    )
    return agg


def deduplicar_app(app: pd.DataFrame) -> pd.DataFrame:
    """Remove IDs duplicados do application_record, mantendo a primeira ocorrência."""
    return app.drop_duplicates(subset="ID", keep="first").reset_index(drop=True)


def montar_base(app: pd.DataFrame, cred: pd.DataFrame) -> pd.DataFrame:
    """Executa o pipeline completo e devolve o df_final (1 linha por cliente)."""
    app = deduplicar_app(app)
    cred = mapear_status(cred)
    target = construir_target(cred)
    hist = agregar_historico(cred)

    base = (
        app.merge(target, on="ID", how="inner", validate="one_to_one")
        .merge(hist, on="ID", how="left", validate="one_to_one")
    )
    return base


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Cria features derivadas do cadastro.

    Nesta versão inicial, mantemos apenas as features do histórico já
    calculadas em agregar_historico(). Features derivadas de cadastro
    (idade em anos, anos de emprego, renda per capita) são criadas no
    notebook 02, onde a decisão de cada uma é justificada.
    """
    return df.copy()