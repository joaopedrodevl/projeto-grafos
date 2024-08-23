import networkx as nx
import os
import asyncio
import threading
import time
from utils.data_handler import read_xls, verify_file_exists, verify_city_exists
from utils.graph_handler import add_edges_between_origin_city_and_cities_to_visit_async, add_edges_between_cities_async

file_path = os.path.join(os.path.dirname(__file__), "..", "data", "mapa.xls")

async def main():
    graph = nx.DiGraph()
    
    origin_city = "Campina Grande, PB, Brasil"
    cities_to_visit = ["João Pessoa", "Alagoa Grande", "Uiraúna"]
    
    # Verifying if the file exists
    if not verify_file_exists(file_path):
        print("The file does not exist.")
        return
    
    # Reading the Excel file
    df = read_xls(file_path)
    
    # Verifying if cities exist in the DataFrame
    cities_to_visit_data = verify_city_exists(df, cities_to_visit)
        
    # Calculating the distance between the origin city and the cities to visit
    await add_edges_between_origin_city_and_cities_to_visit_async(graph, origin_city, cities_to_visit_data)
    
    graph.add_node(origin_city)
    
    # Add the edges between the cities to visit
    await add_edges_between_cities_async(graph, cities_to_visit_data)
                
    # Generating the .gefx file
    nx.write_gexf(graph, "map.gexf")
    print("\nThe file map.gexf was generated.")
    
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