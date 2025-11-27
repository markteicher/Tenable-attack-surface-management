import requests
import logging
import time

# Configurations
API_URL = "https://asm.cloud.tenable.com/api/1.0/assets"
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1IjoyMjcxMCwidiI6MCwiYyI6MzAwNjIsImYiOmZhbHNlLCJhIjpudWxsfQ.c4wP75bggVzMdE8Mgehl7tm0WW4g6x2rNidFMAIIsbw"
OUTPUT_FILE = "asm_pass1_output.csv"
LOG_FILE = "asm_pass1.log"

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def main():
    start_time = time.time()
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": AUTH_TOKEN
    }
    payload = {
        "columns": ["bd.domain"],
        "pagination": {
            "start": 0,
            "size": 4
        }
    }

    try:
        logging.info("Sending request to ASM API...")
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        rows = data.get("results", [])
        record_count = len(rows)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("bd.domain\n")
            for row in rows:
                f.write(f"{row.get('bd.domain', '')}\n")

        elapsed = time.time() - start_time
        logging.info(f"✅ Retrieved {record_count} records and wrote to {OUTPUT_FILE}")
        logging.info(f"⏱️ Script execution time: {elapsed:.2f} seconds")
    except Exception as e:
        logging.error(f"❌ Failed to retrieve assets: {e}")

if __name__ == "__main__":
    main()
