# submissao/

O PDF de submissão contém **apenas três links**: repositório, vídeo e apresentação.
Ele não é gerado à mão — preencha o JSON e rode o script, para que todos os grupos
entreguem exatamente o mesmo formato.

## Passo a passo

```bash
pip install reportlab
# 1. edite submissao/entrega.json
python submissao/gerar_submissao.py
```

Saída: `submissao/submissao_<TURMA>_<GRUPO>.pdf`

O script **recusa** gerar o PDF se algum valor de exemplo continuar no JSON, se um RM
estiver fora do formato `RM000000` ou se algum link não começar com `https://`.

## Sobre os links

| Link | Requisito |
|---|---|
| Repositório | público. Repositório privado inviabiliza a avaliação da entrega |
| Vídeo | máximo 5 minutos, com ao menos um integrante narrando ou aparecendo. YouTube "não listado" ou Drive com acesso para qualquer pessoa com o link |
| Apresentação | PDF. Pode apontar para o arquivo em `docs/` do próprio repositório |

Teste os três em uma **janela anônima** antes de enviar. É o erro mais comum da entrega:
o link funciona na máquina de quem criou e falha para o avaliador.
