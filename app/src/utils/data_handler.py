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

def get_data_by_city(df: pd.DataFrame, city_region: str, column_target: list) -> tuple:
    """
    Verifies if the given city exists in the DataFrame and returns the first tuple with the pattern (nome, cidade, uf, Brazil).

    Parameters:
        df (pandas.DataFrame): The DataFrame to search for cities.
        city_region (str): The city to verify.
        target (str): The column to search for the city.

    Returns:
        tuple: A tuple with (name, city, uf, Brazil) if the city exists.
    """
    city_region = format_text(city_region)
    df[column_target[0]] = df[column_target[0]].apply(format_text)

    # Name(City or Region), City, UF, Country
    dataframe = df[df[column_target[0]] == city_region]

    if dataframe.empty:
        return None
    
    return (str(dataframe[column_target].values[0][0]), str(dataframe["MUNICIPIO"].values[0]), str(dataframe["UF"].values[0]), "Brazil")

def get_data_by_uf(df: pd.DataFrame, ufs: List[str], column_target: list) -> Optional[List[tuple]]:
    """
    Verifies if the given cities exist in the DataFrame and returns a list of tuples with the pattern (nome, cidade, uf, Brazil).

    Parameters:
        df (pandas.DataFrame): The DataFrame to search for cities.
        ufs (List[str]): The list of UFs to verify.
        column_target (list): The column to search for the city.

    Returns:
        Optional[List[tuple]]: A list of tuples with (name, city, uf, Brazil) for each city that exists.
    """
    data = []

    # Formatting the data
    df[column_target[0]] = df[column_target[0]].apply(format_text)
    df["MUNICIPIO"] = df["MUNICIPIO"].apply(format_text)

    for uf in ufs:
        dataframe = df[df["UF"] == uf]
        for index, row in dataframe.iterrows():
            name = str(row[column_target[0]])
            municipio = str(row["MUNICIPIO"])
            uf_value = str(row["UF"])
            data.append((name, municipio, uf_value, "Brazil"))
    
    return data

def verify_file_exists(file_path: str) -> bool:
    """
    Verifies if the file exists.

    Parameters:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)

def getUF(df: pd.DataFrame) -> List[str]:
    """
    Returns the possible UF for a city.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.

    Returns:
        List[str]: The possible UF for the city.
    """
    return sorted(df["UF"].unique().tolist())

def getColumn(df: pd.DataFrame) -> List[str]:
    """
    Returns the possible columns for a city.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.

    Returns:
        List[str]: The possible columns for the city.
    """
    return sorted(df.columns.tolist())

def getDataColumn(df: pd.DataFrame, column: str) -> List[str]:
    """
    Returns the data for a specific column.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        column (str): The column to get the data from.

    Returns:
        List[str]: The data for the specified column.
    """
    return sorted(df[column].unique().tolist())

def format_text(texto: str) -> str:
    """
    Formats the data to be displayed.

    Parameters:
        texto (str): The text to be formatted.

    Returns:
        str: The formatted text.
    """
    return texto.lower().title()