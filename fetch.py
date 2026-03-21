import requests

# Base API URL
BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Your 3 locations
locations = {
    "Birth (Delhi)": (28.6139, 77.2090),
    "Previous (Kathmandu)": (27.7172, 85.3240),
    "Current (Aalborg)": (57.0488, 9.9217)
}


def build_weather_url(lat, lon):
    """
    Build the Open-Meteo API URL
    """
    return (
        f"{BASE_URL}?"
        f"latitude={lat}&longitude={lon}&"
        f"daily=temperature_2m_max,windspeed_10m_max,precipitation_sum&"
        f"timezone=auto"
    )


def fetch_weather():
    """
    Fetch weather data and return cleaned results
    """
    weather_data = []

    for name, (lat, lon) in locations.items():
        url = build_weather_url(lat, lon)

        response = requests.get(url, timeout=30)
        response.raise_for_status()  # good practice like lecturer

        data = response.json()

        # Extract required values
        temperature = data["daily"]["temperature_2m_max"][0]
        wind_speed = data["daily"]["windspeed_10m_max"][0]
        precipitation = data["daily"]["precipitation_sum"][0]
        date = data["daily"]["time"][0]

        # Store clean dictionary
        weather_data.append({
            "location": name,
            "temperature": temperature,
            "wind_speed": wind_speed,
            "precipitation": precipitation,
            "date": date
        })

    return weather_data


# Run file directly (for testing)
if __name__ == "__main__":
    data = fetch_weather()

    print("Weather Data:\n")
    for item in data:
        print(item)

    from store_sql import init_db, store_weather

if __name__ == "__main__":
    data = fetch_weather()

    conn = init_db()
    count = store_weather(conn, data)

    print(f"Inserted {count} rows")
    conn.close()

    #connectpoemtofetch
    from store_sql import init_db, store_weather
from generate_poem import generate_poem

if __name__ == "__main__":
    data = fetch_weather()

    conn = init_db()
    count = store_weather(conn, data)

    poem = generate_poem(data)

    print(f"Inserted {count} rows\n")
    print("Poem:\n")
    print(poem)

    conn.close()

    #add html 
    import os

os.makedirs("docs", exist_ok=True)

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(f"""
    <html>
    <head>
        <title>Weather Poem</title>
    </head>
    <body>
        <h1>Weather Comparison</h1>
        <pre>{poem}</pre>
    </body>
    </html>
    """)