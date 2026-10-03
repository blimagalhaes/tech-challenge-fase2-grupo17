"""Carregamento e persistência de dados.

O dataset do Tech Challenge tem DOIS arquivos CSV:
- application_record.csv : dados cadastrais (1 linha por ID)
- credit_record.csv : histórico mensal de pagamento (N linhas por ID)
"""

import pandas as pd

from src.config import (
    DATA_PROCESSED,
    PROCESSED_FILE,
    RAW_FILE_APP,
    RAW_FILE_CRED,
)


def load_application() -> pd.DataFrame:
    """Lê application_record.csv sem nenhuma transformação."""
    if not RAW_FILE_APP.exists():
        raise FileNotFoundError(
            f"{RAW_FILE_APP} não encontrado. "
            "Veja data/README.md para baixar o dataset."
        )
    return pd.read_csv(RAW_FILE_APP)


def load_credit() -> pd.DataFrame:
    """Lê credit_record.csv sem nenhuma transformação."""
    if not RAW_FILE_CRED.exists():
        raise FileNotFoundError(
            f"{RAW_FILE_CRED} não encontrado. "
            "Veja data/README.md para baixar o dataset."
        )
    return pd.read_csv(RAW_FILE_CRED)


def save_processed(df: pd.DataFrame, name: str | None = None) -> None:
    """Grava um dataset tratado em data/processed/."""
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    arquivo = name or PROCESSED_FILE
    df.to_parquet(DATA_PROCESSED / arquivo, index=False)


def load_processed(name: str | None = None) -> pd.DataFrame:
    """Lê o dataset tratado de data/processed/."""
    arquivo = name or PROCESSED_FILE
    return pd.read_parquet(DATA_PROCESSED / arquivo)