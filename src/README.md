# src/

Funções reutilizadas por mais de um notebook. Se você copiou e colou um bloco de código
entre notebooks, ele deveria estar aqui.

| Arquivo | Responsabilidade |
|---|---|
| `config.py` | caminhos, semente, constantes |
| `data.py` | carregar e salvar datasets |
| `preprocessing.py` | limpeza, escala, feature engineering |
| `models.py` | definição e treino dos modelos |
| `evaluation.py` | métricas e gráficos de avaliação |

Nos notebooks: `from src.config import RANDOM_STATE`
