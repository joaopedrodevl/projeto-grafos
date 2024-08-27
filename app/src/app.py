import networkx as nx
import os
import asyncio
import threading
import time
from utils.data_handler import read_xls, verify_file_exists, verify_city_exists
from utils.graph_handler import add_edges_between_origin_city_and_cities_to_visit_async, add_edges_between_cities_async, shortest_path_between_two_vertices_passing_through_all, draw_shorter_path
from utils.interface import Interface

file_path = os.path.join(os.path.dirname(__file__), "..", "data", "mapa.xls")

target_list = ["MUNICIPIO", "REGIAO_TURISTICA"]

async def main():
    graph = nx.DiGraph()
    graphPath = nx.DiGraph()
    
    interface = Interface(target_list)
    selected_target = interface.run()

    if selected_target == "MUNICIPIO":
        origin_city = "Campina Grande"
        cities_to_visit = ["João Pessoa", "Alagoa Grande", "Uiraúna"]
    elif selected_target == "REGIAO_TURISTICA":
        origin_city = "Cariri"
        cities_to_visit = ["Brejo", "Agreste", "Vale dos Sertões"]
    else:
        print("Invalid target.")
        return
    
    # Verifying if the file exists
    if not verify_file_exists(file_path):
        print("The file does not exist.")
        return
    
    # Reading the Excel file
    df = read_xls(file_path)
    
    # Verifying if cities exist in the DataFrame
    origin_city_data = verify_city_exists(df, [origin_city], selected_target)
    cities_to_visit_data = verify_city_exists(df, cities_to_visit, selected_target)

    # Getting the origin city data
    if selected_target == "MUNICIPIO":
        origin_city = f"{origin_city_data[0][0]} ({origin_city_data[0][2]} - {origin_city_data[0][3]})"
    else:
        origin_city = f"{origin_city_data[0][0]} ({origin_city_data[0][1]} - {origin_city_data[0][2]})"

    # Calculating the distance between the origin city and the cities to visit
    await add_edges_between_origin_city_and_cities_to_visit_async(graph, origin_city, cities_to_visit_data, selected_target)
    
    graph.add_node(origin_city)
    
    # Add the edges between the cities to visit
    await add_edges_between_cities_async(graph, cities_to_visit_data, selected_target)

    # Calculating the shortest path between two vertices passing through all other vertices
    shortest_path = await shortest_path_between_two_vertices_passing_through_all(graph, origin_city)
    
    # Drawing the shortest path
    await draw_shorter_path(graphPath, shortest_path)

    # Generating .gefx files
    nx.write_gexf(graph, "map.gexf")
    nx.write_gexf(graphPath, "path.gexf")
    print("\nThe files map.gexf and path.gexf were generated.")
    
def loading_animation(stop_event):
    animation = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        print(f"\rGerando arquivo... {animation[idx % len(animation)]}", end="")
        idx += 1
        time.sleep(0.1)
    print("\rArquivo concluído!   ")
    
if __name__ == "__main__":
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    
    loading_thread.start()
    try:
        asyncio.run(main())
    finally:
        stop_event.set()
        loading_thread.join()