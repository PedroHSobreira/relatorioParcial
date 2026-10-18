
from pathlib import Path
import math

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


# ============================================================
# PROJETO DE COMUNICACAO E REDES
# Rede metroviaria de Sao Paulo
# ============================================================

PASTA_RESULTADOS = Path("resultados")
PASTA_RESULTADOS.mkdir(exist_ok=True)


# ============================================================
# 1. DADOS DAS LINHAS
# ============================================================

linhas = {
    "L1": [
        "Jabaquara", "Conceicao", "Sao Judas", "Saude",
        "Praca da Arvore", "Santa Cruz", "Vila Mariana",
        "Ana Rosa", "Paraiso", "Vergueiro", "Sao Joaquim",
        "Japao-Liberdade", "Se", "Sao Bento", "Luz",
        "Tiradentes", "Armenia", "Portuguesa-Tiete",
        "Carandiru", "Santana",
        "Jardim Sao Paulo-Ayrton Senna",
        "Parada Inglesa", "Tucuruvi"
    ],

    "L2": [
        "Vila Prudente", "Tamanduatei", "Sacoma",
        "Alto do Ipiranga", "Santos-Imigrantes",
        "Chacara Klabin", "Ana Rosa", "Paraiso",
        "Brigadeiro", "Trianon-Masp", "Consolacao",
        "Clinicas", "Sumare", "Vila Madalena"
    ],

    "L3": [
        "Corinthians-Itaquera", "Artur Alvim",
        "Patriarca-Vila Re", "Guilhermina-Esperanca",
        "Vila Matilde", "Penha", "Carrao", "Tatuape",
        "Belem", "Bresser-Mooca", "Bras", "Pedro II",
        "Se", "Anhangabau", "Republica", "Santa Cecilia",
        "Marechal Deodoro", "Palmeiras-Barra Funda"
    ],

    "L4": [
        "Vila Sonia", "Sao Paulo-Morumbi", "Butanta",
        "Pinheiros", "Faria Lima", "Fradique Coutinho",
        "Oscar Freire", "Paulista", "Higienopolis-Mackenzie",
        "Republica", "Luz"
    ],

    "L5": [
        "Capao Redondo", "Campo Limpo", "Vila das Belezas",
        "Giovanni Gronchi", "Santo Amaro", "Largo Treze",
        "Adolfo Pinheiro", "Alto da Boa Vista",
        "Borba Gato", "Brooklin", "Campo Belo",
        "Eucaliptos", "Moema", "AACD-Servidor",
        "Hospital Sao Paulo", "Santa Cruz",
        "Chacara Klabin"
    ],

    "L15": [
        "Vila Prudente", "Oratorio", "Sao Lucas",
        "Camilo Haddad", "Vila Tolstoi", "Vila Uniao",
        "Jardim Planalto", "Sapopemba", "Fazenda da Juta",
        "Sao Mateus", "Jardim Colonial"
    ],

    "L17": [
        "Morumbi", "Chucri Zaidan", "Vila Cordeiro",
        "Campo Belo", "Vereador Jose Diniz",
        "Brooklin Paulista", "Aeroporto de Congonhas",
        "Washington Luis"
    ]
}


# ============================================================
# 2. CRIACAO DOS VERTICES
# Cada ocorrencia estacao-linha tem seu proprio identificador.
# ============================================================

G = nx.Graph()

for linha, estacoes in linhas.items():
    for estacao in estacoes:
        identificador = f"{linha}|{estacao}"

        G.add_node(
            identificador,
            nome=estacao,
            linha=linha
        )


# ============================================================
# 3. CONEXOES ENTRE ESTACOES CONSECUTIVAS
# ============================================================

for linha, estacoes in linhas.items():
    for i in range(len(estacoes) - 1):
        origem = f"{linha}|{estacoes[i]}"
        destino = f"{linha}|{estacoes[i + 1]}"

        G.add_edge(
            origem,
            destino,
            tipo="percurso"
        )


# ============================================================
# 4. CONEXOES DE TRANSFERENCIA
# ============================================================

transferencias = [
    ("L1|Ana Rosa", "L2|Ana Rosa"),
    ("L1|Paraiso", "L2|Paraiso"),
    ("L1|Se", "L3|Se"),
    ("L1|Luz", "L4|Luz"),
    ("L1|Santa Cruz", "L5|Santa Cruz"),
    ("L2|Consolacao", "L4|Paulista"),
    ("L2|Chacara Klabin", "L5|Chacara Klabin"),
    ("L2|Vila Prudente", "L15|Vila Prudente"),
    ("L3|Republica", "L4|Republica"),
    ("L5|Campo Belo", "L17|Campo Belo")
]

for origem, destino in transferencias:
    G.add_edge(
        origem,
        destino,
        tipo="transferencia"
    )


# ============================================================
# 5. VALIDACAO DA ESTRUTURA
# ============================================================

numero_vertices = G.number_of_nodes()
numero_arestas = G.number_of_edges()

arestas_percurso = [
    (u, v)
    for u, v, dados in G.edges(data=True)
    if dados.get("tipo") == "percurso"
]

arestas_transferencia = [
    (u, v)
    for u, v, dados in G.edges(data=True)
    if dados.get("tipo") == "transferencia"
]

arestas_sem_tipo = [
    (u, v)
    for u, v, dados in G.edges(data=True)
    if dados.get("tipo") not in {"percurso", "transferencia"}
]

vertices_isolados = list(nx.isolates(G))
componentes = list(nx.connected_components(G))

transferencias_invalidas = [
    (origem, destino)
    for origem, destino in transferencias
    if origem not in G or destino not in G
]

print("\n========== VALIDACAO DO GRAFO ==========")
print(f"Vertices: {numero_vertices}")
print(f"Arestas totais: {numero_arestas}")
print(f"Arestas de percurso: {len(arestas_percurso)}")
print(f"Arestas de transferencia: {len(arestas_transferencia)}")
print(f"Componentes conexas: {len(componentes)}")
print(f"Vertices isolados: {len(vertices_isolados)}")
print(f"Arestas sem tipo valido: {len(arestas_sem_tipo)}")
print(f"Transferencias invalidas: {len(transferencias_invalidas)}")

if vertices_isolados:
    print("Vertices isolados:", vertices_isolados)

if len(componentes) > 1:
    print("\nO grafo possui componentes desconectadas:")
    for i, componente in enumerate(componentes, start=1):
        print(f"Componente {i}: {len(componente)} vertices")

assert numero_vertices == 102, "Quantidade inesperada de vertices."
assert len(arestas_percurso) == 95, "Quantidade inesperada de percursos."
assert len(arestas_transferencia) == 10, "Quantidade inesperada de transferencias."
assert numero_arestas == 105, "Quantidade inesperada de arestas."
assert len(vertices_isolados) == 0, "Existem vertices isolados."
assert len(arestas_sem_tipo) == 0, "Existe aresta sem tipo valido."
assert len(transferencias_invalidas) == 0, "Transferencia invalida."

print(
    "Estado do grafo:",
    "conectado" if len(componentes) == 1 else "desconectado"
)
print("========================================")


# ============================================================
# 6. BUSCAS BFS E DFS
# ============================================================

origem_busca = "L1|Jabaquara"

arvore_bfs_inicial = nx.bfs_tree(G, origem_busca)
arvore_dfs_inicial = nx.dfs_tree(G, origem_busca)

bfs = list(arvore_bfs_inicial.nodes())
dfs = list(arvore_dfs_inicial.nodes())

print("\n--- BUSCA EM LARGURA (BFS) ---")
print(f"Origem: {G.nodes[origem_busca]['nome']}")
print(f"Vertices alcancados: {len(bfs)}")
print("Primeiros 20 vertices:")
print(" -> ".join(bfs[:20]))

print("\n--- BUSCA EM PROFUNDIDADE (DFS) ---")
print(f"Origem: {G.nodes[origem_busca]['nome']}")
print(f"Vertices alcancados: {len(dfs)}")
print("Primeiros 20 vertices:")
print(" -> ".join(dfs[:20]))


# Pares de estacoes usados nos testes.
pares_estacoes = [
    ("L1|Jabaquara", "L3|Palmeiras-Barra Funda"),
    ("L2|Vila Madalena", "L15|Jardim Colonial"),
    ("L5|Capao Redondo", "L4|Vila Sonia")
]

resultados_buscas = []


for indice_teste, (origem_teste, destino_teste) in enumerate(
    pares_estacoes, start=1
):
    print("\n========================================")
    print(f"TESTE {indice_teste}")
    print(f"Origem: {origem_teste}")
    print(f"Destino: {destino_teste}")

    if origem_teste not in G or destino_teste not in G:
        print("Erro: origem ou destino nao existe no grafo.")
        continue

    # Caminho minimo: grafo nao ponderado.
    caminho_bfs = nx.shortest_path(
        G,
        source=origem_teste,
        target=destino_teste
    )

    # Caminho na arvore produzida pela busca DFS.
    arvore_dfs = nx.dfs_tree(G, source=origem_teste)

    if destino_teste in arvore_dfs:
        caminho_dfs = nx.shortest_path(
            arvore_dfs,
            source=origem_teste,
            target=destino_teste
        )
    else:
        caminho_dfs = []

    arestas_bfs = len(caminho_bfs) - 1
    arestas_dfs = len(caminho_dfs) - 1 if caminho_dfs else None

    print("\nCaminho BFS:")
    print(" -> ".join(
        f"{G.nodes[v]['nome']} ({G.nodes[v]['linha']})"
        for v in caminho_bfs
    ))
    print(f"Estacoes no caminho: {len(caminho_bfs)}")
    print(f"Arestas no caminho: {arestas_bfs}")

    print("\nCaminho na arvore DFS:")
    if caminho_dfs:
        print(" -> ".join(
            f"{G.nodes[v]['nome']} ({G.nodes[v]['linha']})"
            for v in caminho_dfs
        ))
        print(f"Estacoes no caminho: {len(caminho_dfs)}")
        print(f"Arestas no caminho: {arestas_dfs}")
    else:
        print("Destino nao alcancado pela DFS.")

    resultados_buscas.append({
        "Teste": indice_teste,
        "Origem": origem_teste,
        "Destino": destino_teste,
        "Caminho_BFS": " -> ".join(caminho_bfs),
        "Estacoes_BFS": len(caminho_bfs),
        "Arestas_BFS": arestas_bfs,
        "Caminho_DFS": " -> ".join(caminho_dfs) if caminho_dfs else "",
        "Estacoes_DFS": len(caminho_dfs) if caminho_dfs else 0,
        "Arestas_DFS": arestas_dfs,
        "Vertices_alcancados_BFS": len(nx.bfs_tree(G, origem_teste)),
        "Vertices_alcancados_DFS": len(arvore_dfs)
    })


# ============================================================
# 7. EXPORTACAO DOS RESULTADOS DAS BUSCAS
# ============================================================

df_buscas = pd.DataFrame(resultados_buscas)

df_buscas.to_csv(
    PASTA_RESULTADOS / "resultados_buscas.csv",
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# 8. IMAGENS DOS CAMINHOS BFS
# Circulos numerados; legenda proxima, alinhada em tres colunas.
# ============================================================

for resultado in resultados_buscas:

    caminho = resultado["Caminho_BFS"].split(" -> ")
    indice_teste = resultado["Teste"]

    # Criar somente as arestas consecutivas do caminho.
    grafo_caminho = nx.Graph()
    grafo_caminho.add_nodes_from(caminho)

    grafo_caminho.add_edges_from(
        (caminho[i], caminho[i + 1])
        for i in range(len(caminho) - 1)
    )

    # Posicoes horizontais para manter a ordem do percurso.
    posicoes = {
        estacao: (i, 0)
        for i, estacao in enumerate(caminho)
    }

    # A legenda fica em um eixo separado, logo abaixo do desenho.
    fig = plt.figure(
        figsize=(max(13, len(caminho) * 0.72), 8)
    )

    grade = fig.add_gridspec(
        2, 1,
        height_ratios=[2.1, 1.35],
        hspace=0.04
    )

    ax_grafo = fig.add_subplot(grade[0])
    ax_legenda = fig.add_subplot(grade[1])

    # Desenhar as ligacoes do caminho.
    nx.draw_networkx_edges(
        grafo_caminho,
        posicoes,
        ax=ax_grafo,
        width=1.8
    )

    # Desenhar as estacoes.
    nx.draw_networkx_nodes(
        grafo_caminho,
        posicoes,
        ax=ax_grafo,
        node_size=650,
        edgecolors="black",
        linewidths=1
    )

    # Numeracao dos circulos na ordem do caminho.
    rotulos_numericos = {
        estacao: str(i + 1)
        for i, estacao in enumerate(caminho)
    }

    nx.draw_networkx_labels(
        grafo_caminho,
        posicoes,
        labels=rotulos_numericos,
        ax=ax_grafo,
        font_size=10,
        font_weight="bold"
    )

    nome_origem = G.nodes[caminho[0]]["nome"]
    nome_destino = G.nodes[caminho[-1]]["nome"]

    ax_grafo.set_title(
        f"Caminho BFS {indice_teste}: "
        f"{nome_origem} -> {nome_destino}\n"
        f"{len(caminho)} ocorrencias de estacao | "
        f"{resultado['Arestas_BFS']} arestas",
        fontsize=13,
        fontweight="bold",
        pad=12
    )

    ax_grafo.set_xlim(-0.7, len(caminho) - 0.3)
    ax_grafo.set_ylim(-0.8, 0.8)
    ax_grafo.axis("off")

    # Montar legenda em tres colunas.
    ax_legenda.axis("off")

    quantidade_colunas = 3
    quantidade_linhas = math.ceil(
        len(caminho) / quantidade_colunas
    )

    for indice, estacao in enumerate(caminho):
        coluna = indice // quantidade_linhas
        linha_legenda = indice % quantidade_linhas

        x = 0.02 + coluna * 0.33
        y = 0.96 - linha_legenda * (
            0.90 / max(quantidade_linhas, 1)
        )

        nome = G.nodes[estacao]["nome"]
        linha = G.nodes[estacao]["linha"]

        texto = f"{indice + 1}. {nome} ({linha})"

        ax_legenda.text(
            x,
            y,
            texto,
            transform=ax_legenda.transAxes,
            fontsize=9,
            fontweight="bold",
            ha="left",
            va="top"
        )

    plt.savefig(
        PASTA_RESULTADOS / f"caminho_bfs_{indice_teste}.png",
        dpi=250,
        bbox_inches="tight"
    )

    plt.close(fig)


# ============================================================
# 9. GRAU E CENTRALIDADE DE INTERMEDIACAO
# ============================================================

graus = dict(G.degree())
centralidade = nx.betweenness_centrality(G)

dados_estacoes = []

for vertice in G.nodes():
    dados_estacoes.append({
        "Vertice": vertice,
        "Estacao": G.nodes[vertice]["nome"],
        "Linha": G.nodes[vertice]["linha"],
        "Grau": graus[vertice],
        "Centralidade_intermediacao": centralidade[vertice]
    })

df_metricas = pd.DataFrame(dados_estacoes)

df_metricas = df_metricas.sort_values(
    by="Centralidade_intermediacao",
    ascending=False
)

print("\n--- 10 VERTICES COM MAIOR CENTRALIDADE ---")
print(
    df_metricas.head(10).to_string(
        index=False,
        formatters={
            "Centralidade_intermediacao": "{:.4f}".format
        }
    )
)

df_metricas.to_csv(
    PASTA_RESULTADOS / "metricas_estacoes.csv",
    index=False,
    encoding="utf-8-sig"
)


# Grafico das dez maiores centralidades.
dez_maiores = df_metricas.head(10).sort_values(
    by="Centralidade_intermediacao",
    ascending=True
)

fig, ax = plt.subplots(figsize=(10, 6))

ax.barh(
    dez_maiores["Vertice"],
    dez_maiores["Centralidade_intermediacao"]
)

ax.set_title(
    "Dez vertices com maior centralidade de intermediacao"
)
ax.set_xlabel("Centralidade de intermediacao")
ax.set_ylabel("Vertice (linha e estacao)")

plt.tight_layout()

plt.savefig(
    PASTA_RESULTADOS / "centralidade_intermediacao.png",
    dpi=250,
    bbox_inches="tight"
)

plt.close(fig)


# ============================================================
# 10. EXPORTACAO DE VERTICES E CONEXOES
# ============================================================

df_vertices = pd.DataFrame([
    {
        "Vertice": vertice,
        "Estacao": dados["nome"],
        "Linha": dados["linha"]
    }
    for vertice, dados in G.nodes(data=True)
])

df_vertices.to_csv(
    PASTA_RESULTADOS / "estacoes.csv",
    index=False,
    encoding="utf-8-sig"
)

df_arestas = pd.DataFrame([
    {
        "Origem": origem,
        "Destino": destino,
        "Tipo": dados.get("tipo", "nao informado")
    }
    for origem, destino, dados in G.edges(data=True)
])

df_arestas.to_csv(
    PASTA_RESULTADOS / "conexoes.csv",
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# 11. TABELA COMPARATIVA BFS E DFS
# ============================================================

if resultados_buscas:
    dados_tabela = []

    for resultado in resultados_buscas:
        dados_tabela.append([
            resultado["Teste"],
            G.nodes[resultado["Origem"]]["nome"],
            G.nodes[resultado["Destino"]]["nome"],
            resultado["Estacoes_BFS"],
            resultado["Arestas_BFS"],
            resultado["Estacoes_DFS"],
            resultado["Arestas_DFS"]
            if resultado["Arestas_DFS"] is not None else "-"
        ])

    colunas = [
        "Teste", "Origem", "Destino",
        "Estacoes BFS", "Arestas BFS",
        "Estacoes DFS", "Arestas DFS"
    ]

    fig, ax = plt.subplots(figsize=(13, 4.5))
    ax.axis("off")

    tabela = ax.table(
        cellText=dados_tabela,
        colLabels=colunas,
        loc="center",
        cellLoc="center"
    )

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(9)
    tabela.scale(1, 1.8)

    ax.set_title(
        "Comparacao dos caminhos BFS e DFS",
        fontsize=14,
        fontweight="bold",
        pad=18
    )

    plt.tight_layout()

    plt.savefig(
        PASTA_RESULTADOS / "comparacao_buscas.png",
        dpi=250,
        bbox_inches="tight"
    )

    plt.close(fig)


# ============================================================
# 12. GRAFO GERAL
# ============================================================

fig, ax = plt.subplots(figsize=(12, 12))

posicoes_gerais = nx.circular_layout(G, scale=1)

nx.draw_networkx_edges(
    G,
    posicoes_gerais,
    ax=ax,
    width=1.0,
    alpha=0.8
)

nx.draw_networkx_nodes(
    G,
    posicoes_gerais,
    ax=ax,
    node_size=300,
    edgecolors="black",
    linewidths=0.8
)

rotulos_gerais = {
    vertice: str(i + 1)
    for i, vertice in enumerate(G.nodes())
}

nx.draw_networkx_labels(
    G,
    posicoes_gerais,
    labels=rotulos_gerais,
    ax=ax,
    font_size=8
)

ax.set_title("Rede metroviaria de Sao Paulo - Modelo em grafo")
ax.axis("off")
plt.tight_layout()

plt.savefig(
    PASTA_RESULTADOS / "grafo_rede_metroviaria.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# ============================================================
# 13. RESUMO FINAL
# ============================================================

print("\n========== EXECUCAO CONCLUIDA ==========")
print(f"Arquivos salvos em: {PASTA_RESULTADOS.resolve()}")

arquivos_gerados = [
    "estacoes.csv",
    "conexoes.csv",
    "metricas_estacoes.csv",
    "resultados_buscas.csv",
    "comparacao_buscas.png",
    "centralidade_intermediacao.png",
    "grafo_rede_metroviaria.png"
]

for arquivo in arquivos_gerados:
    print(f"- {arquivo}")

for resultado in resultados_buscas:
    print(f"- caminho_bfs_{resultado['Teste']}.png")

print("========================================")
