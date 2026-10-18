
from pathlib import Path

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
# A ordem representa a sequencia usada no modelo inicial.
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
# Cada ocorrencia de uma estacao em uma linha tem ID proprio.
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


# Modelo simplificado da ramificacao da Linha 17.
# Washington Luis e conectado a Brooklin Paulista.
# A operacao real precisa ser consultada separadamente.

G.remove_edge(
    "L17|Aeroporto de Congonhas",
    "L17|Washington Luis"
)

G.add_edge(
    "L17|Brooklin Paulista",
    "L17|Washington Luis",
    tipo="percurso"
)


# ============================================================
# 4. CONEXOES DE TRANSFERENCIA
# Estas conexoes formam a hipotese inicial do modelo.
# Devem ser conferidas com as fontes oficiais.
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
# 5. VALIDACAO DOS DADOS E DA ESTRUTURA
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

# Conferir se todas as transferencias referenciam vertices existentes.
transferencias_invalidas = [
    (origem, destino)
    for origem, destino in transferencias
    if origem not in G.nodes or destino not in G.nodes
]

# Conferir IDs duplicados na lista de vertices esperados.
ids_esperados = [
    f"{linha}|{estacao}"
    for linha, estacoes in linhas.items()
    for estacao in estacoes
]

ids_duplicados = sorted({
    identificador
    for identificador in ids_esperados
    if ids_esperados.count(identificador) > 1
})

print("\n========== VALIDACAO DO GRAFO ==========")
print(f"Vertices: {numero_vertices}")
print(f"Arestas totais: {numero_arestas}")
print(f"Arestas de percurso: {len(arestas_percurso)}")
print(f"Arestas de transferencia: {len(arestas_transferencia)}")
print(f"Componentes conexas: {len(componentes)}")
print(f"Vertices isolados: {len(vertices_isolados)}")
print(f"Arestas sem tipo valido: {len(arestas_sem_tipo)}")
print(f"Transferencias invalidas: {len(transferencias_invalidas)}")
print(f"IDs duplicados: {len(ids_duplicados)}")

if vertices_isolados:
    print("Vertices isolados:", vertices_isolados)

if len(componentes) > 1:
    print("\nO grafo possui componentes desconectadas:")
    for i, componente in enumerate(componentes, start=1):
        print(f"Componente {i}: {len(componente)} vertices")

# Estas verificacoes confirmam os totais esperados para
# os dados cadastrados, nao a fidelidade da rede real.
assert numero_vertices == 102, "Quantidade inesperada de vertices."
assert len(arestas_percurso) == 95, "Quantidade inesperada de percursos."
assert len(arestas_transferencia) == 10, "Quantidade inesperada de transferencias."
assert numero_arestas == 105, "Quantidade inesperada de arestas."
assert len(arestas_sem_tipo) == 0, "Existe aresta sem tipo valido."
assert len(transferencias_invalidas) == 0, "Existe transferencia com vertice inexistente."
assert len(ids_duplicados) == 0, "Existem IDs duplicados."
assert len(vertices_isolados) == 0, "Existem vertices isolados."

if len(componentes) == 1:
    print("Conectividade estrutural: grafo conectado.")
else:
    print("Conectividade estrutural: grafo desconectado.")

print("Validacao estrutural concluida.")
print("========================================")


# ============================================================
# 6. BUSCA EM LARGURA (BFS) E PROFUNDIDADE (DFS)
# ============================================================

origem_busca = "L1|Jabaquara"

bfs = list(nx.bfs_tree(G, origem_busca).nodes())
dfs = list(nx.dfs_tree(G, origem_busca).nodes())

print("\n--- BUSCA EM LARGURA (BFS) ---")
print("Origem: Jabaquara")
print(f"Vertices visitados: {len(bfs)}")
print("Primeiros 20 vertices:")
print(" -> ".join(bfs[:20]))

print("\n--- BUSCA EM PROFUNDIDADE (DFS) ---")
print("Origem: Jabaquara")
print(f"Vertices visitados: {len(dfs)}")
print("Primeiros 20 vertices:")
print(" -> ".join(dfs[:20]))


# ============================================================
# 7. CAMINHO MINIMO
# O resultado conta arestas, nao minutos de viagem.
# ============================================================

origem = "L1|Jabaquara"
destino = "L3|Palmeiras-Barra Funda"

print("\n--- CAMINHO MINIMO ---")

try:
    caminho = nx.shortest_path(
        G,
        source=origem,
        target=destino
    )

    print(f"Origem: {G.nodes[origem]['nome']}")
    print(f"Destino: {G.nodes[destino]['nome']}")
    print(f"Numero de arestas: {len(caminho) - 1}")

    for vertice in caminho:
        linha = G.nodes[vertice]["linha"]
        nome = G.nodes[vertice]["nome"]
        print(f"{linha} - {nome}")

except nx.NetworkXNoPath:
    print("Nao existe caminho entre as estacoes escolhidas.")


# ============================================================
# 8. GRAU E CENTRALIDADE DE INTERMEDIACAO
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

df = pd.DataFrame(dados_estacoes)

df = df.sort_values(
    by="Centralidade_intermediacao",
    ascending=False
)

print("\n--- 10 VERTICES COM MAIOR CENTRALIDADE ---")
print(
    df.head(10).to_string(
        index=False,
        formatters={
            "Centralidade_intermediacao": "{:.4f}".format
        }
    )
)


# ============================================================
# 9. EXPORTACAO DOS DADOS
# ============================================================

df.to_csv(
    PASTA_RESULTADOS / "metricas_estacoes.csv",
    index=False,
    encoding="utf-8-sig"
)

dados_arestas = []

for origem_aresta, destino_aresta, atributos in G.edges(data=True):
    dados_arestas.append({
        "Origem": origem_aresta,
        "Destino": destino_aresta,
        "Tipo": atributos.get("tipo", "nao informado")
    })

df_arestas = pd.DataFrame(dados_arestas)

df_arestas.to_csv(
    PASTA_RESULTADOS / "conexoes.csv",
    index=False,
    encoding="utf-8-sig"
)

# Exportar tambem os vertices para documentar a base utilizada.
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


# ============================================================
# 10. VISUALIZACAO SIMPLES DO GRAFO
# Sem nomes de estacoes, apenas vertices numerados.
# A disposicao circular e visual, nao geografica.
# ============================================================

plt.figure(figsize=(12, 12))

posicoes = nx.circular_layout(G, scale=1)

nx.draw_networkx_edges(
    G,
    posicoes,
    edge_color="blue",
    width=1.0,
    alpha=0.8
)

nx.draw_networkx_nodes(
    G,
    posicoes,
    node_color="lightgreen",
    edgecolors="black",
    node_size=300,
    linewidths=0.8
)

rotulos = {
    vertice: str(i + 1)
    for i, vertice in enumerate(G.nodes())
}

nx.draw_networkx_labels(
    G,
    posicoes,
    labels=rotulos,
    font_size=8,
    font_color="black"
)

plt.title("Rede metroviaria de Sao Paulo - Modelo em grafo")
plt.axis("off")
plt.tight_layout()

plt.savefig(
    PASTA_RESULTADOS / "grafo_rede_metroviaria.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 11. RESUMO FINAL
# ============================================================

print("\n========== EXECUCAO CONCLUIDA ==========")
print(f"Arquivos salvos em: {PASTA_RESULTADOS.resolve()}")
print("- estacoes.csv")
print("- conexoes.csv")
print("- metricas_estacoes.csv")
print("- grafo_rede_metroviaria.png")
print("========================================")
