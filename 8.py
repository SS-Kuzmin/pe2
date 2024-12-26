import sys
import requests
import math

def get_coordinates(api_key, address):
    geocode_url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        'apikey': api_key,
        'geocode': address,
        'format': 'json'
    }

    response = requests.get(geocode_url, params=params)
    if response.status_code != 200:
        print(f"Ошибка HTTP {response.status_code}: {response.text}")
        sys.exit(1)

    try:
        data = response.json()
        pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        lon, lat = pos.split()
        return float(lat), float(lon)
    except (KeyError, IndexError) as e:
        print(f"Не удалось найти координаты. Ошибка: {e}")
        print(f"Ответ API: {response.json()}")
        sys.exit(1)

def calculate_distance(lat1, lon1, lat2, lon2):
    # Декартова метрика на градусной сетке
    degree_to_km = 111  # 1 градус широты в километрах
    cos_lat = math.cos(math.radians((lat1 + lat2) / 2))  # Средняя широта
    delta_lat = abs(lat1 - lat2) * degree_to_km
    delta_lon = abs(lon1 - lon2) * degree_to_km * cos_lat
    return math.sqrt(delta_lat**2 + delta_lon**2)

def main():
    api_key = 'c268d9a3-9e78-48e0-9efe-92641b3236c6'

    home_address = input("Введите адрес дома: ").strip()
    if not home_address:
        print("Адрес дома не может быть пустым.")
        sys.exit(1)

    university_address = input("Введите адрес университета: ").strip()
    if not university_address:
        print("Адрес университета не может быть пустым.")
        sys.exit(1)

    home_lat, home_lon = get_coordinates(api_key, home_address)
    university_lat, university_lon = get_coordinates(api_key, university_address)

    distance = calculate_distance(home_lat, home_lon, university_lat, university_lon)

    print(f"Расстояние от дома до университета: {distance:.2f} км")

if __name__ == "__main__":
    main()