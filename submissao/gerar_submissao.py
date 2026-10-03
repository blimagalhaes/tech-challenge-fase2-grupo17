#!/usr/bin/env python3
"""Gera o PDF de submissão do Tech Challenge — Fase 2.

Uso:
    pip install reportlab
    python submissao/gerar_submissao.py

Lê `submissao/entrega.json`, valida os campos e escreve
`submissao/submissao_<TURMA>_<GRUPO>.pdf`.

O PDF contém apenas os três links exigidos, mais a identificação do grupo.
Não altere o layout: o formato padronizado é o que permite a correção em lote.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

AQUI = Path(__file__).resolve().parent
CONFIG = AQUI / "entrega.json"

TITULO = "TECH CHALLENGE — FASE 2"
SUBTITULO = "POSTECH · Data Analytics"

PLACEHOLDERS = (
    "usuario/nome-do-repositorio",
    "xxxxxxxxxxx",
    "Nome Completo do Integrante",
    "RM000000",
    "Grupo 00",
)

AZUL = colors.HexColor("#0B3C5D")
CINZA = colors.HexColor("#5A6270")
CINZA_CLARO = colors.HexColor("#E4E7EC")


# ---------------------------------------------------------------- validação --
def erro(msg: str) -> None:
    print(f"  [ERRO] {msg}")


def validar(dados: dict) -> list[str]:
    """Devolve a lista de problemas encontrados. Lista vazia = tudo certo."""
    problemas: list[str] = []

    for campo in ("turma", "grupo", "integrantes", "links"):
        if not dados.get(campo):
            problemas.append(f"Campo obrigatório ausente ou vazio: '{campo}'.")

    integrantes = dados.get("integrantes") or []
    if not integrantes:
        problemas.append("Nenhum integrante informado.")
    for i, pessoa in enumerate(integrantes, start=1):
        if not pessoa.get("nome"):
            problemas.append(f"Integrante {i}: nome ausente.")
        if not re.fullmatch(r"RM\d{6}", str(pessoa.get("rm", "")).strip()):
            problemas.append(
                f"Integrante {i}: RM inválido ('{pessoa.get('rm')}'). "
                "Formato esperado: RM seguido de 6 dígitos."
            )

    links = dados.get("links") or {}
    rotulos = {
        "repositorio": "link do repositório",
        "video": "link do vídeo",
        "apresentacao": "link da apresentação",
    }
    for chave, rotulo in rotulos.items():
        url = (links.get(chave) or "").strip()
        if not url:
            problemas.append(f"{rotulo.capitalize()} não informado.")
        elif not url.startswith("https://"):
            problemas.append(f"O {rotulo} precisa começar com https:// — recebido: '{url}'.")

    texto_completo = json.dumps(dados, ensure_ascii=False)
    for marcador in PLACEHOLDERS:
        if marcador in texto_completo:
            problemas.append(f"Valor de exemplo não substituído: '{marcador}'.")

    return problemas


# --------------------------------------------------------------------- pdf --
def construir_pdf(dados: dict, destino: Path) -> None:
    base = getSampleStyleSheet()

    st_titulo = ParagraphStyle(
        "TituloTC", parent=base["Title"], fontName="Helvetica-Bold",
        fontSize=19, leading=23, textColor=AZUL, alignment=TA_CENTER, spaceAfter=2,
    )
    st_subtitulo = ParagraphStyle(
        "SubtituloTC", parent=base["Normal"], fontName="Helvetica",
        fontSize=10.5, leading=14, textColor=CINZA, alignment=TA_CENTER,
    )
    st_secao = ParagraphStyle(
        "SecaoTC", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=8.5, leading=11, textColor=CINZA, spaceAfter=6,
    )
    st_rotulo = ParagraphStyle(
        "RotuloTC", parent=base["Normal"], fontName="Helvetica-Bold",
        fontSize=10, leading=13, textColor=AZUL,
    )
    st_valor = ParagraphStyle(
        "ValorTC", parent=base["Normal"], fontName="Helvetica",
        fontSize=10, leading=14,
    )
    st_link = ParagraphStyle(
        "LinkTC", parent=st_valor, fontName="Courier", fontSize=8.6, leading=12.5,
    )

    doc = SimpleDocTemplate(
        str(destino), pagesize=A4,
        leftMargin=24 * mm, rightMargin=24 * mm,
        topMargin=26 * mm, bottomMargin=22 * mm,
        title=f"Submissão Tech Challenge Fase 2 — {dados['grupo']}",
        author=dados["grupo"],
    )

    story = [
        Paragraph(TITULO, st_titulo),
        Paragraph(SUBTITULO, st_subtitulo),
        Spacer(1, 5 * mm),
        HRFlowable(width="100%", thickness=1.1, color=AZUL, spaceAfter=8 * mm),
    ]

    # --- identificação ---
    integrantes = "<br/>".join(
        f"{p['nome']} &nbsp;—&nbsp; {p['rm']}" for p in dados["integrantes"]
    )
    ident = Table(
        [
            [Paragraph("Turma", st_rotulo), Paragraph(dados["turma"], st_valor)],
            [Paragraph("Grupo", st_rotulo), Paragraph(dados["grupo"], st_valor)],
            [Paragraph("Integrantes", st_rotulo), Paragraph(integrantes, st_valor)],
        ],
        colWidths=[32 * mm, None],
    )
    ident.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
    ]))
    story += [Paragraph("IDENTIFICAÇÃO", st_secao), ident, Spacer(1, 9 * mm)]

    # --- links ---
    links = dados["links"]
    linhas = [
        [Paragraph("Repositório", st_rotulo),
         Paragraph(f'<link href="{links["repositorio"]}" color="#0B3C5D">{links["repositorio"]}</link>', st_link)],
        [Paragraph("Vídeo", st_rotulo),
         Paragraph(f'<link href="{links["video"]}" color="#0B3C5D">{links["video"]}</link>', st_link)],
        [Paragraph("Apresentação", st_rotulo),
         Paragraph(f'<link href="{links["apresentacao"]}" color="#0B3C5D">{links["apresentacao"]}</link>', st_link)],
    ]
    tabela = Table(linhas, colWidths=[32 * mm, None])
    tabela.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, CINZA_CLARO),
    ]))
    story += [Paragraph("LINKS DA ENTREGA", st_secao), tabela]

    doc.build(story)


# -------------------------------------------------------------------- main --
def main() -> int:
    if not CONFIG.exists():
        erro(f"{CONFIG} não encontrado.")
        return 1

    dados = json.loads(CONFIG.read_text(encoding="utf-8"))

    problemas = validar(dados)
    if problemas:
        print(f"\nSubmissão bloqueada — {len(problemas)} problema(s):\n")
        for p in problemas:
            erro(p)
        print("\nCorrija submissao/entrega.json e rode novamente.\n")
        return 1

    slug = f"{dados['turma']}_{dados['grupo']}".replace(" ", "").replace("/", "-")
    destino = AQUI / f"submissao_{slug}.pdf"
    construir_pdf(dados, destino)

    print(f"\nPDF gerado: {destino}")
    print("\nAntes de enviar, confirme em uma janela anônima:")
    print("  1. o repositório abre sem login;")
    print("  2. o vídeo reproduz sem pedir permissão de acesso;")
    print("  3. a apresentação abre e está em PDF.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
