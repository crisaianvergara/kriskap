import requests
from operator import itemgetter


def search_province():
    """Returns a list of tuples containing the province code and name."""

    response = requests.get(url="https://psgc.gitlab.io/api/provinces/")
    response.raise_for_status()
    province = [(province["code"], province["name"]) for province in response.json()]
    return sorted(province, key=itemgetter(1))


def search_municipality(province_code):
    """Returns a list of tuples containing the municipality code and name."""

    response = requests.get(
        url=f"https://psgc.gitlab.io/api/provinces/{province_code}/cities-municipalities/"
    )
    response.raise_for_status()
    city = [(city["code"], city["name"]) for city in response.json()]
    return sorted(city, key=itemgetter(1))


def search_barangay(city_code):
    """Returns a list of tuples containing the barangay code and name."""

    response = requests.get(
        url=f"https://psgc.gitlab.io/api/cities-municipalities/{city_code}/barangays/"
    )
    response.raise_for_status()
    barangay = [(barangay["code"], barangay["name"]) for barangay in response.json()]
    return sorted(barangay, key=itemgetter(1))
