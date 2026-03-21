import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def generate_poem(weather_data):
    api_key = os.getenv("GROQ_API_KEY")

    client = Groq(api_key=api_key)

    # Convert weather data into text
    info = ""
    for item in weather_data:
        info += (
            f"{item['location']}: "
            f"{item['temperature']}°C, "
            f"wind {item['wind_speed']} m/s, "
            f"precipitation {item['precipitation']} mm\n"
        )

    prompt = f"""
Here is the weather for three places:

{info}

Write a short poem comparing these places.
Mention temperature, wind, and precipitation.
Suggest where it is nicest to be tomorrow.

Structure:

Part 1: English (simple and clear)

Part 2: Hindi:
- Use simple natural Hindi (daily conversation style)
- Keep it easy to read
- No complex words

Keep both parts short.
"""

    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}]
)
    
    return response.choices[0].message.content


# test run (optional)
if __name__ == "__main__":
    sample = [
        {
            "location": "Delhi",
            "temperature": 30,
            "wind_speed": 10,
            "precipitation": 0,
            "date": "2026-03-21",
        }
    ]

    poem = generate_poem(sample)
    print(poem)