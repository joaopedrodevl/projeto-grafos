import pandas as pd
import os
from typing import List, Optional

def read_xls(file_path: str) -> pd.DataFrame:
    """
    Reads an Excel file and returns a pandas DataFrame.

    Parameters:
        file_path (str): The path to the Excel file.

    Returns:
        pandas.DataFrame: The data read from the Excel file.
    """
    return pd.read_excel(file_path)

def get_data_by_city(df: pd.DataFrame, city: str, target: str) -> pd.Series:
    """
    Returns the data of a city from a pandas DataFrame.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        city (str): The name of the city.

    Returns:
        pandas.Series: The data of the city.
    """
    return df[df[target] == city]

def verify_city_exists(df: pd.DataFrame, cities_to_visit: List[str], target: str) -> Optional[List[tuple]]:
    """
    Verifies if the given cities exist in the DataFrame.
    Parameters:
    - df (pandas.DataFrame): The DataFrame to search for cities.
    - cities_to_visit (list): A list of cities to verify.
    Returns:
    - cities_to_visit_data (list): A list of tuples containing the city name, state, and country for each existing city.
    Raises:
    - None
    """
    cities_to_visit_data = []
    
    for city in cities_to_visit:
        if city not in df[target].values:
            print(f"The city {city} does not exist in the DataFrame.")
            return
        else:
            city_data = get_data_by_city(df, city, target)

            if target == "MUNICIPIO":
                cities_to_visit_data.append((city, city, city_data["UF"].values[0], "Brazil"))
            
            elif target == "REGIAO_TURISTICA":
                cities_to_visit_data.append((city, city_data["MUNICIPIO"].values[0], city_data["UF"].values[0], "Brazil"))
            
    return cities_to_visit_data

def verify_file_exists(file_path: str) -> bool:
    """
    Verifies if the file exists.

    Parameters:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)