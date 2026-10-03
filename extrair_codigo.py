"""Extrai apenas o código-fonte de um notebook, ignorando outputs e metadados."""
import json
import sys

def extrair(caminho_nb, caminho_txt):
    with open(caminho_nb, "r", encoding="utf-8") as f:
        nb = json.load(f)

    with open(caminho_txt, "w", encoding="utf-8") as f:
        for i, cell in enumerate(nb["cells"], start=1):
            tipo = cell["cell_type"]
            fonte = "".join(cell["source"])
            f.write(f"\n{'='*80}\n")
            f.write(f"CÉLULA {i} [{tipo.upper()}]\n")
            f.write(f"{'='*80}\n")
            f.write(fonte)
            f.write("\n")

    print(f"Extraído para {caminho_txt}")

if __name__ == "__main__":
    extrair(sys.argv[1], sys.argv[2])