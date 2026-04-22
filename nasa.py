import requests
from datetime import datetime, timedelta
import time

API_KEY = "SUA CHAVE API"
URL = "https://api.nasa.gov/neo/rest/v1/feed"

# últimos 30 dias
end_date = datetime.today()
start_date = end_date - timedelta(days=30)

all_asteroids = []
current_start = start_date

print("Coletando dados da NASA...\n")

# loop de 7 dias
while current_start <= end_date:

    current_end = current_start + timedelta(days=6)

    if current_end > end_date:
        current_end = end_date

    params = {
        "start_date": current_start.strftime("%Y-%m-%d"),
        "end_date": current_end.strftime("%Y-%m-%d"),
        "api_key": API_KEY
    }

    print(f"Buscando: {params['start_date']} até {params['end_date']}")

    response = requests.get(URL, params=params)
    data = response.json()

    if "near_earth_objects" in data:
        for date in data["near_earth_objects"]:
            all_asteroids.extend(data["near_earth_objects"][date])

    current_start = current_end + timedelta(days=1)
    time.sleep(1)

print("\nTotal de asteroides:", len(all_asteroids))

mais_proximo = min(
    all_asteroids,
    key=lambda x: float(
        x["close_approach_data"][0]["miss_distance"]["kilometers"]
    )
)

maior = max(
    all_asteroids,
    key=lambda x: x["estimated_diameter"]["meters"]["estimated_diameter_max"]
)

mais_rapido = max(
    all_asteroids,
    key=lambda x: float(
        x["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"]
    )
)

perigosos = [
    a for a in all_asteroids
    if a["is_potentially_hazardous_asteroid"]
]

distancias = [
    float(a["close_approach_data"][0]["miss_distance"]["kilometers"])
    for a in all_asteroids
]

velocidades = [
    float(a["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"])
    for a in all_asteroids
]

# =========================
# Resultados
# =========================

print("\n===== RESULTADOS =====")

print("\nTotal de asteroides:", len(all_asteroids))

print("\nMais próximo:", mais_proximo["name"])
print(
    "Distância:",
    mais_proximo["close_approach_data"][0]["miss_distance"]["kilometers"],
    "km"
)

print("\nMaior:", maior["name"])
print(
    "Diâmetro máximo:",
    maior["estimated_diameter"]["meters"]["estimated_diameter_max"],
    "m"
)

print("\nMais rápido:", mais_rapido["name"])
print(
    "Velocidade:",
    mais_rapido["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"],
    "km/s"
)

print("\nPotencialmente perigosos:", len(perigosos))

print("\nDistância média:", sum(distancias)/len(distancias), "km")
print("Velocidade média:", sum(velocidades)/len(velocidades), "km/s")
