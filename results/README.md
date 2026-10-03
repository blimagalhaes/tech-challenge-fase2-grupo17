# results/

| Pasta | Conteúdo | Versionado? |
|---|---|---|
| `figures/` | gráficos exportados (`.png`) | sim |
| `metrics/` | tabelas comparativas (`.csv` / `.json`) | sim |
| `models/` | modelos serializados (`.pkl` / `.joblib`) | **não** (ver `.gitignore`) |

Modelos podem ser regenerados rodando os notebooks; figuras e métricas ficam versionadas
para que o avaliador veja os resultados sem executar nada.
