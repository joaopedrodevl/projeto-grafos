from geopy.distance import geodesic
import aiohttp

async def get_coordinates_async(address: str) -> tuple:
    """
    Retrieves the latitude and longitude coordinates of a given address.

    Parameters:
    address (str): The address to retrieve the coordinates for.

    Returns:
    tuple: A tuple containing the latitude and longitude coordinates of the address.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://nominatim.openstreetmap.org/search?q={address}&format=json") as response:
            data = await response.json()
            if not data:
                raise ValueError(f"Could not find the coordinates for the address {address}.")
            location = data[0]
            return (float(location["lat"]), float(location["lon"]))

async def calculate_distance_async(address1: str, address2: str) -> float:
    """
    Calculate the distance in kilometers between two addresses.

    Parameters:
    address1 (str): The first address.
    address2 (str): The second address.

    Returns:
    float: The distance in kilometers between the two addresses.
    """
    coords1 = await get_coordinates_async(address1)
    coords2 = await get_coordinates_async(address2)
    return geodesic(coords1, coords2).kilometers