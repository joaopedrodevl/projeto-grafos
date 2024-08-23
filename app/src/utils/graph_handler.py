from utils.geolocation import calculate_distance_async
import time
from typing import List
import networkx as nx

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
        city1, uf1, country1 = cities_to_visit_data[i]
        for j in range(i+1, len(cities_to_visit_data)):
            city2, uf2, country2 = cities_to_visit_data[j]
            if not graph.has_node(f"{city2} - {uf2}"):
                graph.add_node(f"{city2} - {uf2}")
            
            distance = await calculate_distance_async(f"{city1}, {uf1}, {country1}", f"{city2}, {uf2}, {country2}")
            graph.add_edge(f"{city1} - {uf1}", f"{city2} - {uf2}", weight=distance/1000)
            graph.add_edge(f"{city2} - {uf2}", f"{city1} - {uf1}", weight=distance/1000)
            time.sleep(2)

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
    for city, uf, country in cities_to_visit_data:
        if not graph.has_node(f"{city} - {uf}"):
            graph.add_node(f"{city} - {uf}")
        
        distance = await calculate_distance_async(origin_city, f"{city}, {uf}, {country}")
        graph.add_edge(origin_city, f"{city} - {uf}", weight=distance/1000)
        graph.add_edge(f"{city} - {uf}", origin_city, weight=distance/1000)
        time.sleep(2)