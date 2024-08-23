from utils.geolocation import get_coordinates, calculate_distance
import pandas as pd
import os
import time
import networkx as nx

file_path = os.path.join(os.path.dirname(__file__), "..", "data", "mapa.xls")

def read_xls(file_path):
    """
    Reads an Excel file and returns a pandas DataFrame.

    Parameters:
        file_path (str): The path to the Excel file.

    Returns:
        pandas.DataFrame: The data read from the Excel file.
    """
    return pd.read_excel(file_path)

def get_data_by_city(df, city):
    """
    Returns the data of a city from a pandas DataFrame.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        city (str): The name of the city.

    Returns:
        pandas.Series: The data of the city.
    """
    return df[df["MUNICIPIO"] == city]

def main():
    graph = nx.DiGraph()
    
    origin_city = "Campina Grande, PB, Brasil"
    cities_to_visit = ["João Pessoa", "Alagoa Grande", "Uiraúna"]
    cities_to_visit_data = []
    
    # Verifying if the file exists
    if not os.path.exists(file_path):
        print("The file does not exist.")
        return
    
    # Reading the Excel file
    df = read_xls(file_path)
    
    # Verifying if cities exist in the DataFrame
    for city in cities_to_visit:
        if city not in df["MUNICIPIO"].values:
            print(f"The city {city} does not exist in the DataFrame.")
            return
        else:
            # Getting the data of the city and add to list of "cities to visit data" with the city name, the city UF and the string Brazil
            city_data = get_data_by_city(df, city)
            cities_to_visit_data.append((city, city_data["UF"].values[0], "Brazil"))
        
    # Calculating the distance between the origin city and the cities to visit
    for city, uf, country in cities_to_visit_data:
        if not graph.has_node(f"{city} - {uf}"):
            graph.add_node(f"{city} - {uf}")
        
        distance = calculate_distance(origin_city, f"{city}, {uf}, {country}")
        graph.add_edge(origin_city, f"{city} - {uf}", weight=distance/1000)
        graph.add_edge(f"{city} - {uf}", origin_city, weight=distance/1000)
        time.sleep(5)
    
    # Add the edges between the cities to visit
    for i in range(len(cities_to_visit_data)):
        city1, uf1, country1 = cities_to_visit_data[i]
        for j in range(i+1, len(cities_to_visit_data)):
            city2, uf2, country2 = cities_to_visit_data[j]
            if not graph.has_node(f"{city2} - {uf2}"):
                graph.add_node(f"{city2} - {uf2}")
            
            distance = calculate_distance(f"{city1}, {uf1}, {country1}", f"{city2}, {uf2}, {country2}")
            graph.add_edge(f"{city1} - {uf1}", f"{city2} - {uf2}", weight=distance/1000)
            graph.add_edge(f"{city2} - {uf2}", f"{city1} - {uf1}", weight=distance/1000)
            time.sleep(5)
                
    # Generating the .gefx file
    nx.write_gexf(graph, "map.gexf")
    print("The file map.gexf was generated.")
    
if __name__ == "__main__":
    main()