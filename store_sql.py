import sqlite3
from pathlib import Path

DB_PATH = "weather.db"


def init_db():
    db_path = Path(DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            temperature REAL,
            wind_speed REAL,
            precipitation REAL,
            date TEXT,
            UNIQUE(location, date)
        )
    """)

    conn.commit()
    return conn


def store_weather(conn, weather_data):
    cursor = conn.cursor()
    inserted = 0

    sql = """
        INSERT OR IGNORE INTO weather (
            location, temperature, wind_speed, precipitation, date
        )
        VALUES (?, ?, ?, ?, ?)
    """

    for item in weather_data:
        cursor.execute(sql, (
            item["location"],
            item["temperature"],
            item["wind_speed"],
            item["precipitation"],
            item["date"],
        ))
        inserted += cursor.rowcount

    conn.commit()
    return inserted


if __name__ == "__main__":
    sample = [
        {
            "location": "Test",
            "temperature": 20,
            "wind_speed": 10,
            "precipitation": 0,
            "date": "2026-03-21",
        }
    ]

    conn = init_db()
    count = store_weather(conn, sample)
    print(f"Inserted {count} rows")
    conn.close()