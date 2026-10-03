# notebooks/

Ordem numerada obrigatória. Cada notebook deve rodar de cima para baixo em ambiente limpo
(`Kernel → Restart & Run All`) sem erro — é isso que caracteriza reprodutibilidade.

| Arquivo | Escopo |
|---|---|
| `01_eda.ipynb` | distribuições, correlações, outliers, balanceamento |
| `02_preprocessamento.ipynb` | nulos, definição do alvo, normalização, features |
| `03_modelagem.ipynb` | split/CV, treino de ≥ 2 modelos, comparação |
| `04_avaliacao.ipynb` | métricas, feature importance, implicações de negócio |

## Regras

- **Antes do commit:** verifique que a numeração das células está em ordem crescente
  (`[1]`, `[2]`, `[3]`...). Células fora de ordem indicam execução caótica.
- Mantenha as saídas dos gráficos salvas no notebook — o avaliador precisa ver os
  resultados sem executar nada.
- Todo gráfico precisa de um parágrafo de interpretação em markdown logo abaixo.
  Gráfico solto, sem leitura, não comunica nada.
- A primeira célula de cada notebook define `RANDOM_STATE = 42` e os caminhos.
  Não mude o valor entre notebooks.
