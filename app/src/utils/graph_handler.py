from utils.geolocation import calculate_distance_async
import time
from typing import List
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

async def add_edges_between_cities_async(graph: nx.DiGraph, cities_to_visit_data: List[tuple]) -> None:
    """
    Adds edges between cities in a graph based on the given cities_to_visit_data.
    Parameters:
    - graph: The graph object to add edges to.
    - cities_to_visit_data: A list of tuples containing city, uf, and country data.
    Returns:
    None
    """
    for i in range(len(cities_to_visit_data)):
        name1, city1, uf1, country1 = cities_to_visit_data[i]
        for j in range(i+1, len(cities_to_visit_data)):
            name2, city2, uf2, country2 = cities_to_visit_data[j]
            if not graph.has_node(f"{name2} ({city2} - {uf2})") or not graph.has_node(f"{name2} ({uf2} - {country2})"):
                if name2 == city2:
                    graph.add_node(f"{name2} ({uf2} - {country2})")
                else:
                    graph.add_node(f"{name2} ({city2} - {uf2})")
            
            if name1 == city1:
                # String = "Cidade (UF - País)"
                origin = f"{name1} ({uf1} - {country1})"
            else:
                # String = "Região (Cidade - Uf)"
                origin = f"{name1} ({city1} - {uf1})"

            if name2 == city2:
                # String = "Cidade (UF - País)"
                node = f"{name2} ({uf2} - {country2})"
            else:
                # String = "Região (Cidade - Uf)"
                node = f"{name2} ({city2} - {uf2})"

            # Avoid ties
            if origin == node:
                continue

            distance = await calculate_distance_async(f"{city1}, {uf1}, {country1}", f"{city2}, {uf2}, {country2}")
            graph.add_edge(origin, node, weight=distance/1000)
            graph.add_edge(node, origin, weight=distance/1000)

async def add_edges_between_origin_city_and_cities_to_visit_async(graph: nx.DiGraph, origin_city: str, cities_to_visit_data: List[tuple]) -> None:
    """
    Adds edges between the origin city and the cities to visit in the graph asynchronously.
    Parameters:
    - graph: The graph object to add the edges to.
    - origin_city: The origin city to connect with the cities to visit.
    - cities_to_visit_data: A list of tuples containing the city, uf, and country for each city to visit.
    Returns:
    None
    """
    ...

    # String = "Cidade, UF, País"
    data_origin = f"{origin_city[1]}, {origin_city[2]}, {origin_city[3]}"

    if origin_city[0] == origin_city[1]:
        # String = "Cidade (UF - País)"
        origin_city = f"{origin_city[1]} ({origin_city[2]} - {origin_city[3]})"
    else:
        # String = "Região (Cidade - Uf)"
        origin_city = f"{origin_city[0]} ({origin_city[1]} - {origin_city[2]})"

    for name, city, uf, country in cities_to_visit_data:
        if not graph.has_node(f"{name} ({city} - {uf})") or not graph.has_node(f"{name} ({uf} - {country})"):
            if name == city:
                graph.add_node(f"{name} ({uf} - {country})")
            else:
                graph.add_node(f"{name} ({city} - {uf})")
        
        if name == city:
            # String = "Cidade (UF - País)"
            node = f"{name} ({uf} - {country})"
        else:
            # String = "Região (Cidade - Uf)"
            node = f"{name} ({city} - {uf})"

        # Avoid ties
        if origin_city == node:
            continue

        distance = await calculate_distance_async(data_origin, f"{city}, {uf}, {country}")
        graph.add_edge(origin_city, node, weight=distance/1000)
        graph.add_edge(node, origin_city, weight=distance/1000)

async def shortest_path_between_two_vertices_passing_through_all (graph: nx.DiGraph, origin_city: str) -> List[str]:
    """
    Calculates the shortest path between two vertices passing through all other vertices in the graph.
    Parameters:
    - graph: The graph object to calculate the shortest path on.
    - origin_city: The origin city of the path.
    - destination_city: The destination city of the path.
    Returns:
    A list of strings representing the shortest path between the two vertices.
    """
    ...
    
    n = len(graph.nodes)
    
    memo = {}
    path_memo = {}
    
    def visit(visited, last):
        if visited == (1 << n) - 1:
            return graph[last][origin_city]['weight'], [origin_city]
        
        if (visited, last) in memo:
            return memo[(visited, last)], path_memo[(visited, last)]
        
        min_dist = float('inf')
        min_path = []
        
        for city in range(n):
            if not visited & (1 << city):
                next_city = index_to_city[city]
                try:
                    dist, path = visit(visited | (1 << city), next_city)
                    dist += graph[last][next_city]['weight']

                    if dist < min_dist:
                        min_dist = dist
                        min_path = [next_city] + path
                except KeyError:
                    continue
        
        memo[(visited, last)] = min_dist
        path_memo[(visited, last)] = min_path
        return min_dist, min_path
    
    city_to_index = {city: idx for idx, city in enumerate(graph.nodes)}
    index_to_city = {idx: city for city, idx in city_to_index.items()}
    
    start_index = city_to_index[origin_city]
    min_path_length, min_path = visit(1 << start_index, origin_city)
    
    min_path = [origin_city] + min_path[:-1]
    
    return min_path

async def draw_shorter_path (graph: nx.DiGraph, shortest_path: List[str]) -> nx.DiGraph:
    """
    Draws the shortest path on the graph.
    Parameters:
    - graph: The graph object to draw the shortest path on.
    - shortest_path: A list of strings representing the shortest path.
    Returns:
    A new graph object with the shortest path drawn.
    """
    ...
    
    for v in shortest_path:
        graph.add_node(v)

    for i in range(len(shortest_path) - 1):
        graph.add_edge(shortest_path[i], shortest_path[i+1])