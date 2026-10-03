"""Configuração central do projeto: caminhos, semente e constantes.

Importe daqui em todos os notebooks para que os resultados sejam reproduzíveis.
"""

from pathlib import Path

# --- Semente -----------------------------------------------------------------
# Use em TODO ponto que envolva aleatoriedade: train_test_split, modelos, CV.
RANDOM_STATE = 42

# --- Caminhos ----------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]

DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
RESULTS = ROOT / "results"
FIGURES = RESULTS / "figures"
MODELS = RESULTS / "models"
METRICS = RESULTS / "metrics"

# --- Dataset -----------------------------------------------------------------
# O dataset do Tech Challenge tem DOIS arquivos CSV, não um.
RAW_FILE_APP = DATA_RAW / "application_record.csv"
RAW_FILE_CRED = DATA_RAW / "credit_record.csv"

# Nome do arquivo tratado, salvo em data/processed/ pelo notebook 02.
PROCESSED_FILE = "dataset_tratado.parquet"

# --- Variável alvo -----------------------------------------------------------
# TARGET = 1 se o cliente atingiu atraso >= 60 dias (status_num >= 2) em algum mês.
# Justificativa: 60 dias é o ponto em que a inadimplência se torna grave e
# persistente, sem esvaziar a classe positiva (o critério de 90 dias produziria
# poucos positivos; o de 30 dias incluiria atrasos leves que o mercado não
# considera inadimplência real).
TARGET = "mau_pagador"

# Limiar em dias de atraso para classificar como mau pagador.
# Mapeamento de STATUS: 0=1-29, 1=30-59, 2=60-89, 3=90-119, 4=120-149, 5=150+.
LIMIAR_DIAS = 60

# --- Split -------------------------------------------------------------------
TEST_SIZE = 0.2
CV_FOLDS = 5