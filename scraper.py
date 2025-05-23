import requests
import time
import json

def fetch_place_details(api_key, place_id):
    endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,international_phone_number,website,opening_hours,rating,user_ratings_total",
        "key": api_key,
    }
    response = requests.get(endpoint, params=params)
    data = response.json()

    if "result" not in data:
        print(f"Details not found for place ID: {place_id}")
        return None

    place_details = data["result"]
    details = {
        "Name": place_details.get("name", "N/A"),
        "Address": place_details.get("formatted_address", "N/A"),
        "Phone": place_details.get("international_phone_number", "N/A"),
        "Website": place_details.get("website", "N/A"),
        "Opening Hours": place_details.get("opening_hours", {}).get("weekday_text", "N/A"),
        "Rating": place_details.get("rating", "N/A"),
        "User Ratings Total": place_details.get("user_ratings_total", "N/A"),
    }
    return details

def fetch_places_nearby(api_key, location, radius, niche, next_page_token=None):
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{location['lat']},{location['lng']}",
        "radius": radius,
        "keyword": niche,
        "key": api_key,
    }
    if next_page_token:
        params["pagetoken"] = next_page_token

    response = requests.get(endpoint, params=params)
    data = response.json()

    if "results" not in data or not data["results"]:
        print(f"No results found for location {location} and radius {radius}.")
        return [], data.get("next_page_token")

    places = []
    for place in data["results"]:
        places.append({
            "Name": place.get("name", "N/A"),
            "Address": place.get("vicinity", "N/A"),
            "Place ID": place.get("place_id", "N/A"),
        })

    next_page_token = data.get("next_page_token")
    return places, next_page_token

def statewide_search(api_key, niche, radius=50000, max_results=100, include_websites=False):
    state_locations = [
        {"lat": 40.7128, "lng": -74.0060},  # NYC
        {"lat": 42.6526, "lng": -73.7562},  # Albany
        {"lat": 43.0481, "lng": -76.1474},  # Syracuse
        {"lat": 42.8864, "lng": -78.8784},  # Buffalo
        {"lat": 40.9176, "lng": -72.8330},  # Long Island
    ]

    detailed_places = []
    for location in state_locations:
        print(f"Fetching places near {location}...")
        next_page_token = None
        total_places = 0

        while next_page_token is not None or total_places == 0:
            places, next_page_token = fetch_places_nearby(api_key, location, radius, niche, next_page_token)
            
            for place in places:
                place_id = place["Place ID"]
                print(f"Fetching details for {place['Name']}...")
                details = fetch_place_details(api_key, place_id)
                if details:
                    place.update(details)
                    if (include_websites and place.get("Website", "N/A") != "N/A") or \
                       (not include_websites and place.get("Website", "N/A") == "N/A"):
                        detailed_places.append(place)
                        total_places += 1
                        if total_places >= max_results:
                            print(f"Reached max result limit of {max_results}.")
                            break

            if next_page_token:
                print("Fetching next page of results...")
                time.sleep(2)

            if total_places >= max_results:
                break

    return detailed_places 