import requests
import os
from store_sql import init_db, store_weather
from generate_poem import generate_poem

# Base API URL
BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Locations
locations = {
    "Birth (Delhi)": (28.6139, 77.2090),
    "Previous (Kathmandu)": (27.7172, 85.3240),
    "Current (Aalborg)": (57.0488, 9.9217)
}


def build_weather_url(lat, lon):
    return (
        f"{BASE_URL}?"
        f"latitude={lat}&longitude={lon}&"
        f"daily=temperature_2m_max,windspeed_10m_max,precipitation_sum&"
        f"timezone=auto"
    )


def fetch_weather():
    weather_data = []

    for name, (lat, lon) in locations.items():
        url = build_weather_url(lat, lon)

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()

        weather_data.append({
            "location": name,
            "temperature": data["daily"]["temperature_2m_max"][0],
            "wind_speed": data["daily"]["windspeed_10m_max"][0],
            "precipitation": data["daily"]["precipitation_sum"][0],
            "date": data["daily"]["time"][0]
        })

    return weather_data


def save_html(poem):
    os.makedirs("docs", exist_ok=True)

    html = f"""
    <html>
    <head>
        <title>Weather Poem</title>
    </head>
    <body>
        <h1>Weather Comparison</h1>
        <pre>{poem}</pre>
    </body>
    </html>
    """

    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    # Fetch
    data = fetch_weather()

    print("Weather Data:\n")
    for item in data:
        print(item)

    # Store in DB
    conn = init_db()
    count = store_weather(conn, data)

    # Generate poem
    poem = generate_poem(data)

    print(f"\nInserted {count} rows")
    print("\nPoem:\n")
    print(poem)

    # Save HTML
    save_html(poem)

    conn.close()