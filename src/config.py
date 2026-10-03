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
RAW_FILE = DATA_RAW / "dataset.csv"   # PREENCHER: nome real do arquivo
TARGET = "target"                      # PREENCHER: nome da variável alvo

# --- Split -------------------------------------------------------------------
TEST_SIZE = 0.2
CV_FOLDS = 5
