import requests
import time
import json

def geocode_location(api_key, location):
    # Normalize the location string to handle any casing
    # This will properly capitalize city and state names
    try:
        # Split by comma and strip whitespace
        parts = [part.strip() for part in location.split(',')]
        if len(parts) >= 2:
            # Title case the city, uppercase the state
            city = parts[0].title()
            state = parts[1].strip().upper()
            location = f"{city}, {state}"
        else:
            # If only one part, just title case it
            location = location.strip().title()
    except Exception:
        # If any error in formatting, use the original string
        location = location.strip()

    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location,
        "key": api_key
    }
    response = requests.get(endpoint, params=params)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return {"lat": location["lat"], "lng": location["lng"]}
    else:
        raise ValueError(f"Could not find location: {location}")

def fetch_place_details(api_key, place_id):
    endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,international_phone_number,website,opening_hours,rating,user_ratings_total,price_level",
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
        "Currently Open": place_details.get("opening_hours", {}).get("open_now", False),
        "Rating": place_details.get("rating", "N/A"),
        "User Ratings Total": place_details.get("user_ratings_total", "N/A"),
        "Price Level": place_details.get("price_level", "N/A"),
    }
    return details

def fetch_places_nearby(api_key, location, radius, niche, open_now=False, next_page_token=None):
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{location['lat']},{location['lng']}",
        "radius": radius,
        "keyword": niche,
        "key": api_key,
        "opennow": open_now
    }
    if next_page_token:
        params["pagetoken"] = next_page_token

    response = requests.get(endpoint, params=params)
    data = response.json()

    if "results" not in data or not data["results"]:
        print(f"No results found for location {location} and radius {radius}.")
        return [], None

    places = []
    for place in data["results"]:
        places.append({
            "Name": place.get("name", "N/A"),
            "Address": place.get("vicinity", "N/A"),
            "Place ID": place.get("place_id", "N/A"),
            "Rating": place.get("rating", "N/A"),
        })

    next_page_token = data.get("next_page_token")
    return places, next_page_token

def search_businesses(api_key, location_query, niche, radius=50000, max_results=100, website_filter='all', min_rating=0, open_now=False):
    try:
        location = geocode_location(api_key, location_query)
    except ValueError as e:
        raise ValueError(f"Location error: {str(e)}")

    detailed_places = []
    next_page_token = None
    total_places = 0

    while next_page_token is not None or total_places == 0:
        places, next_page_token = fetch_places_nearby(api_key, location, radius, niche, open_now, next_page_token)
        
        for place in places:
            if min_rating > 0 and (place["Rating"] == "N/A" or place["Rating"] < min_rating):
                continue

            print(f"Fetching details for {place['Name']}...")
            details = fetch_place_details(api_key, place["Place ID"])
            
            if details:
                place.update(details)
                
                # Apply website filter
                has_website = place.get("Website", "N/A") != "N/A"
                if website_filter == 'with' and not has_website:
                    continue
                if website_filter == 'without' and has_website:
                    continue
                
                detailed_places.append(place)
                total_places += 1
                if total_places >= max_results:
                    print(f"Reached max result limit of {max_results}.")
                    return detailed_places

        if next_page_token:
            print("Fetching next page of results...")
            time.sleep(2)

    return detailed_places 