import networkx as nx
import os
import asyncio
import threading
import time
from utils.interface import Interface
from utils.data_handler import read_xls, verify_file_exists, get_data_by_uf, get_data_by_city, getUF, format_text
from utils.graph_handler import add_edges_between_origin_city_and_cities_to_visit_async, add_edges_between_cities_async, shortest_path_between_two_vertices_passing_through_all, draw_shorter_path

file_path = os.path.join(os.path.dirname(__file__), "..", "data", "mapa.xls")

def clear_term():
    os.system('cls' if os.name == 'nt' else 'clear')

async def main():
    graph = nx.DiGraph()
    graphPath = nx.DiGraph()
    
    # Verifying if the file exists
    if not verify_file_exists(file_path):
        clear_term()
        print("The file does not exist.")
        return
    
    # Reading the Excel file
    df = read_xls(file_path)

    # Getting the possible UF
    ufs = getUF(df)

    # Setting the columns to be used
    columns = ["MUNICIPIO", "REGIAO_TURISTICA"]

    # Draw the interface
    window = Interface("Projeto Grafos")
    window.checkbox_options(ufs, "Escolha as UFs")
    window.dropdown_options(columns, "Escolha o foco do grafo")
    window.text_input("Cidade/Região de origem")

    # Waiting for the user to select the options
    ufs_selected, column_selected, city_origin = window.run()

    # Verifying if the user selected all the options
    if not ufs_selected or not column_selected or not city_origin:
        clear_term()
        print("Incomplete File")
        return
    
    # Getting the data from the selected options
    cities_regions_visit = get_data_by_uf(df, ufs_selected, column_selected)
    city_origin_data = get_data_by_city(df, city_origin, column_selected)

    # Formatting the city_origin
    if city_origin_data:
        if city_origin_data[0] == city_origin_data[1]:
            # String = "Cidade (UF - País)"
            city_origin = f"{city_origin_data[1]} ({city_origin_data[2]} - {city_origin_data[3]})"
        else:
            # String = "Nome (Cidade - UF)"
            city_origin = f"{city_origin_data[0]} ({city_origin_data[1]} - {city_origin_data[2]})"
    else:
        clear_term()
        print("City/Region not found.")
        return

    # Creating the graph
    graph.add_node(city_origin)
    await add_edges_between_origin_city_and_cities_to_visit_async(graph, city_origin_data, cities_regions_visit)
    await add_edges_between_cities_async(graph, cities_regions_visit)

    # Generating .gefx files
    nx.write_gexf(graph, "map.gexf")
    clear_term()
    print("The file map.gexf was generated.\n")
    
    # Getting the shortest path
    shortest_path = await shortest_path_between_two_vertices_passing_through_all(graph, city_origin)

    # Drawing the graph
    await draw_shorter_path(graphPath, shortest_path)

    # Generating .gefx files
    nx.write_gexf(graphPath, "path.gexf")
    clear_term()
    print("The file path.gexf were generated.\n")
    
def loading_animation(stop_event):
    animation = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        print(f"\rGerando arquivo... {animation[idx % len(animation)]}", end="")
        idx += 1
        time.sleep(0.1)
    print("\rArquivo concluído!")

if __name__ == "__main__":
    clear_term()
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    
    loading_thread.start()
    try:
        asyncio.run(main())
    finally:
        stop_event.set()
        loading_thread.join()