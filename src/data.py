"""Carregamento e persistência de dados."""

import pandas as pd

from src.config import DATA_PROCESSED, RAW_FILE


def load_raw() -> pd.DataFrame:
    """Lê o dataset bruto de data/raw/ sem nenhuma transformação."""
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"{RAW_FILE} não encontrado. Veja data/README.md para baixar o dataset."
        )
    return pd.read_csv(RAW_FILE)


def save_processed(df: pd.DataFrame, name: str) -> None:
    """Grava um dataset tratado em data/processed/."""
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(DATA_PROCESSED / f"{name}.parquet", index=False)


def load_processed(name: str) -> pd.DataFrame:
    return pd.read_parquet(DATA_PROCESSED / f"{name}.parquet")
