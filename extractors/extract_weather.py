import os
import json
import requests
import psycopg2
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")

CITIES = [
    "Jakarta", "Surabaya", "Bandung", "Medan",
    "Semarang", "Makassar", "Palembang", "Denpasar"
]

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def init_raw_schema(cursor):
    # Buat schema raw dan tabel penyimpanan JSON mentah
    cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.weather_data (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100),
            payload JSONB,
            extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def main():
    if not API_KEY or API_KEY == "MASUKKAN_API_KEY_KAMU_DISINI":
        raise ValueError("API Key belum diisi di file .env!")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        init_raw_schema(cursor)
        conn.commit()
        print("Schema dan tabel raw siap.")

        for city in CITIES:
            print(f"Mengambil data cuaca: {city}...")
            payload = fetch_weather(city)
            
            cursor.execute(
                "INSERT INTO raw.weather_data (city, payload) VALUES (%s, %s);",
                (city, json.dumps(payload))
            )
        
        conn.commit()
        print("Sukses: Semua data mentah berhasil disimpan ke raw.weather_data!")

    except Exception as e:
        conn.rollback()
        print(f"Error terjadi: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
