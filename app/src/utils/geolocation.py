from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def get_coordinates(address):
    """
    Retrieves the latitude and longitude coordinates of a given address.

    Parameters:
    address (str): The address to retrieve the coordinates for.

    Returns:
    tuple: A tuple containing the latitude and longitude coordinates of the address.
    """
    geolocator = Nominatim(user_agent="my_app_decoded")
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude)

def calculate_distance(address1, address2):
    """
    Calculate the distance in kilometers between two addresses.

    Parameters:
    address1 (str): The first address.
    address2 (str): The second address.

    Returns:
    float: The distance in kilometers between the two addresses.
    """
    coords1 = get_coordinates(address1)
    coords2 = get_coordinates(address2)
    return geodesic(coords1, coords2).kilometers