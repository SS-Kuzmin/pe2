import sys
import requests

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
        return lat, lon
    except (KeyError, IndexError) as e:
        print(f"Не удалось найти координаты. Ошибка: {e}")
        print(f"Ответ API: {response.json()}")
        sys.exit(1)

def get_district(api_key, lat, lon):
    geocode_url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        'apikey': api_key,
        'geocode': f"{lon},{lat}",
        'format': 'json',
        'kind': 'district'
    }

    response = requests.get(geocode_url, params=params)
    if response.status_code != 200:
        print(f"Ошибка HTTP {response.status_code}: {response.text}")
        sys.exit(1)

    try:
        data = response.json()
        district = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']
        return district
    except (KeyError, IndexError) as e:
        print(f"Не удалось определить район. Ошибка: {e}")
        print(f"Ответ API: {response.json()}")
        sys.exit(1)

def main():
    address = input("Введите адрес: ").strip()
    if not address:
        print("Адрес не может быть пустым.")
        sys.exit(1)

    api_key = 'c268d9a3-9e78-48e0-9efe-92641b3236c6'

    lat, lon = get_coordinates(api_key, address)
    district = get_district(api_key, lat, lon)

    print(f"Адрес: {address}")
    print(f"Район: {district}")

if __name__ == "__main__":
    main()
