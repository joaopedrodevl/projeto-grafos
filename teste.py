import networkx as nx

def read_graph(file_path):
    return nx.read_gexf(file_path)

def nearest_neighbor_tsp(graph, start):
    path = [start]
    total_length = 0
    current = start
    unvisited = set(graph.nodes)
    unvisited.remove(start)
    
    while unvisited:
        next_city = min(unvisited, key=lambda city: graph[current][city]['weight'])
        total_length += graph[current][next_city]['weight']
        path.append(next_city)
        current = next_city
        unvisited.remove(next_city)
    
    # Voltar para a cidade de partida
    total_length += graph[current][start]['weight']
    path.append(start)
    
    return total_length, path

def save_result(file_path, path, length):
    with open(file_path, 'w') as f:
        f.write(f"Menor caminho: {' -> '.join(path)}\n")
        f.write(f"Comprimento total: {length}\n")

def save_path_as_gexf(graph, path, file_path):
    subgraph = nx.DiGraph()
    for i in range(len(path) - 1):
        subgraph.add_edge(path[i], path[i+1], weight=graph[path[i]][path[i+1]]['weight'])
    nx.write_gexf(subgraph, file_path)

# Exemplo de uso
file_path = 'map.gexf'
graph = read_graph(file_path)
start_city = 'Agreste  (Campina Grande - PB)'
min_path_length, min_path = nearest_neighbor_tsp(graph, start_city)
save_result('resultado.txt', min_path, min_path_length)
save_path_as_gexf(graph, min_path, 'path.gexf')
print(f"O menor caminho que passa por todas as cidades começando de {start_city} é {min_path} com comprimento {min_path_length}")