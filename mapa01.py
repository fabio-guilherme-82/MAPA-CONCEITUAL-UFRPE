from pathlib import Path
from textwrap import wrap

from pyvis.network import Network

ARQUIVO_SAIDA = Path(__file__).with_name("mapa_conceitual_software.html")
CORES = {
    "central": "#16324F",
    "livre": "#087F5B",
    "proprietario": "#B85C00",
    "licenca": "#6C2E8F",
    "caracteristica": "#D8F3DC",
    "vantagem": "#DDEBF7",
    "risco": "#FFE0E0",
    "exemplo": "#FFF1B8",
}

net = Network(
    height="760px",
    width="100%",
    directed=True,
    bgcolor="#F7FAFC",
    font_color="#17202A",
)


def adicionar_conceito(node_id, label, color, size=18, shape="box", level=None, text_color="#17202A", text_size=16):
    if level is None:
        if node_id == "software":
            level = 0
        elif node_id in {"livre", "proprietario", "licencas"}:
            level = 1
        elif node_id.endswith("-conceito") or node_id.endswith("-grupo"):
            level = 2
        else:
            level = 3
    propriedades = {
        "n_id": node_id,
        "label": label,
        "color": {"background": color, "border": color, "highlight": {"background": "#FFFFFF", "border": color}},
        "size": size,
        "shape": shape,
        "borderWidth": 2,
        "font": {"size": text_size, "face": "Arial", "color": text_color, "multi": "html"},
        "widthConstraint": {"maximum": 190},
        "heightConstraint": {"minimum": 38},
    }
    if level is not None:
        propriedades["level"] = level
    node_id = propriedades.pop("n_id")
    net.add_node(node_id, **propriedades)


def adicionar_descricao(node_id, texto, color):
    label = "<br>".join(wrap(texto, width=30))
    net.add_node(
        node_id,
        label=label,
        color={"background": "#FFFFFF", "border": color, "highlight": {"background": "#FFFFFF", "border": color}},
        size=18,
        shape="box",
        borderWidth=2,
        margin=12,
        font={"size": 12, "face": "Arial", "color": "#17202A", "multi": "html"},
        widthConstraint={"maximum": 250, "minimum": 190},
        heightConstraint={"minimum": 64},
        level=2,
    )


def conectar(origem, destino, relacao, color="#607D8B"):
    net.add_edge(
        origem,
        destino,
        label=relacao,
        title=relacao,
        color=color,
        arrows="to",
        font={"size": 10, "face": "Arial", "color": "#34495E", "strokeWidth": 3, "strokeColor": "#F7FAFC"},
    )


def adicionar_ramo(parent_id, prefix, titulo, itens, color, relacao):
    grupo_id = f"{prefix}-grupo"
    adicionar_conceito(grupo_id, titulo, color, size=20, shape="ellipse")
    conectar(parent_id, grupo_id, relacao, color)
    for indice, item in enumerate(itens, start=1):
        item_id = f"{prefix}-{indice}"
        adicionar_conceito(item_id, item, color, level=3 + (indice % 2))
        conectar(grupo_id, item_id, "inclui", color)


adicionar_conceito("software", "<b>SOFTWARE</b>", CORES["central"], size=32, shape="ellipse", text_color="#FFFFFF", text_size=20)

adicionar_conceito("livre", "SOFTWARE LIVRE", CORES["livre"], size=25, shape="ellipse")
conectar("software", "livre", "pode ser", CORES["livre"])
adicionar_descricao("livre-conceito", "Codigo-fonte disponivel; garante as 4 liberdades de usar, estudar, modificar e compartilhar", CORES["livre"])
conectar("livre", "livre-conceito", "e definido por", CORES["livre"])
adicionar_ramo("livre", "livre-caracteristicas", "CARACTERISTICAS", ["Codigo-fonte acessivel", "Permite estudar e modificar", "Permite copiar e redistribuir"], CORES["caracteristica"], "caracteriza-se por")
adicionar_ramo("livre", "livre-vantagens", "VANTAGENS", ["Autonomia tecnologica", "Reducao de custos", "Auditoria e colaboracao comunitaria"], CORES["vantagem"], "oferece")
adicionar_ramo("livre", "livre-riscos", "RISCOS", ["Suporte formal pode ser limitado", "Qualidade varia entre projetos", "Depende de comunidade ativa"], CORES["risco"], "pode envolver")
adicionar_ramo("livre", "livre-exemplos", "EXEMPLOS", ["GNU/Linux", "LibreOffice", "VLC Media Player"], CORES["exemplo"], "tem como exemplo")

adicionar_conceito("proprietario", "SOFTWARE PROPRIETARIO", CORES["proprietario"], size=25, shape="ellipse")
conectar("software", "proprietario", "pode ser", CORES["proprietario"])
adicionar_descricao("proprietario-conceito", "Codigo-fonte controlado pelo titular; o uso depende das condicoes da licenca", CORES["proprietario"])
conectar("proprietario", "proprietario-conceito", "e definido por", CORES["proprietario"])
adicionar_ramo("proprietario", "proprietario-caracteristicas", "CARACTERISTICAS", ["Codigo-fonte fechado", "Uso restrito por licenca", "Direitos autorais controlados pelo titular"], CORES["caracteristica"], "caracteriza-se por")
adicionar_ramo("proprietario", "proprietario-vantagens", "VANTAGENS", ["Suporte tecnico dedicado", "Interface padronizada", "Integracao e suporte comercial"], CORES["vantagem"], "oferece")
adicionar_ramo("proprietario", "proprietario-riscos", "RISCOS", ["Custo de licenca e assinatura", "Aprisionamento tecnologico", "Pouca customizacao pelo usuario"], CORES["risco"], "pode envolver")
adicionar_ramo("proprietario", "proprietario-exemplos", "EXEMPLOS", ["Microsoft Windows", "Adobe Photoshop", "macOS"], CORES["exemplo"], "tem como exemplo")

adicionar_conceito("licencas", "TIPOS DE LICENCA", CORES["licenca"], size=25, shape="ellipse")
conectar("software", "licencas", "e distribuido sob", CORES["licenca"])
adicionar_ramo("licencas", "licenca-gpl", "GPL (copyleft)", ["Permite usar, estudar, modificar e redistribuir", "Exige que derivados mantenham a mesma liberdade"], CORES["licenca"], "garante")
adicionar_ramo("licencas", "licenca-mit", "MIT/BSD (permissiva)", ["Permite reutilizar e modificar com poucas condicoes", "Pode ser incorporada a produtos proprietarios"], CORES["licenca"], "permite")
adicionar_ramo("licencas", "licenca-eula", "EULA (proprietaria)", ["Define uso conforme contrato do titular", "Geralmente restringe copia, alteracao e redistribuicao"], CORES["licenca"], "restringe")

net.set_options("""
{
    "layout": {"hierarchical": {"enabled": true, "direction": "UD", "sortMethod": "directed", "levelSeparation": 180, "nodeSpacing": 300, "treeSpacing": 520, "blockShifting": true, "edgeMinimization": true}},
  "physics": {"enabled": false},
  "interaction": {"hover": true, "navigationButtons": true, "keyboard": true, "zoomView": true},
    "nodes": {"margin": 10, "widthConstraint": {"maximum": 190}, "heightConstraint": {"minimum": 38}, "font": {"size": 12, "face": "Arial", "color": "#17202A", "multi": "html"}, "shadow": {"enabled": true, "color": "rgba(22,50,79,0.16)", "size": 6, "x": 2, "y": 2}},
  "edges": {"smooth": {"type": "cubicBezier", "forceDirection": "vertical", "roundness": 0.35}, "width": 1.5, "selectionWidth": 3}
}
""")

net.write_html(str(ARQUIVO_SAIDA), open_browser=False, notebook=False)
html = ARQUIVO_SAIDA.read_text(encoding="utf-8")
html = html.replace(
    '"font": {"color": "#17202A"}, "heightConstraint": {"minimum": 44}, "id": "software"',
    '"font": {"color": "#FFFFFF", "size": 20, "face": "Arial", "multi": "html"}, "heightConstraint": {"minimum": 44}, "id": "software"',
    1,
)
html = html.replace("<center>\n<h1></h1>\n</center>\n", "")
html = html.replace("        <center>\n          <h1></h1>\n        </center>\n", "")
html = html.replace(
    "    <body>",
    "    <body>\n        <h1 style=\"margin: 12px 0; text-align: center; font-family: Arial, sans-serif; font-size: 24px; color: #16324F;\">Mapa conceitual: software livre e proprietario</h1>",
)
html = html.replace(
    "</head>",
    """<style>
        @page { size: A4 landscape; margin: 8mm; }
        @media print {
            html, body { width: 100%; height: 100%; margin: 0; overflow: hidden; }
            body > h1 { margin: 0 0 3mm 0 !important; font-size: 16px !important; }
            .card, .card-body, #mynetwork { width: 100% !important; }
            #mynetwork { height: 175mm !important; border: 0 !important; }
        }
    </style>
    </head>""",
)
html = html.replace(
    "                  network = new vis.Network(container, data, options);",
    "                  network = new vis.Network(container, data, options);\n                  network.fit({animation: false});",
)
ARQUIVO_SAIDA.write_text(html, encoding="utf-8")
print(f"Mapa conceitual gerado com sucesso: {ARQUIVO_SAIDA}")
