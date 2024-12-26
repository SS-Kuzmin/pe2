import requests

YANDEX_API_KEY_GEOCODING = "c268d9a3-9e78-48e0-9efe-92641b3236c6"
YANDEX_API_KEY_SEARCH = "6c058cdf-afa0-40e6-8d9f-740452796714"

def find_nearest_pharmacy_yandex(address):

    geocode_url = "https://geocode-maps.yandex.ru/1.x/"
    geocode_params = {
        "geocode": address,
        "format": "json",
        "apikey": YANDEX_API_KEY_GEOCODING
    }
    try:
        response = requests.get(geocode_url, params=geocode_params).json()
        # Получаем координаты
        point = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        coords = tuple(map(float, point.split()))
        print(f"Координаты адреса: {coords}")
    except (KeyError, IndexError, ValueError) as e:
        print(f"Не удалось получить координаты для данного адреса: {e}")
        return

    # Поиск аптек с помощью Yandex API
    search_url = "https://search-maps.yandex.ru/v1/"
    search_params = {
        "apikey": YANDEX_API_KEY_SEARCH,
        "text": "аптека",
        "ll": f"{coords[0]},{coords[1]}",
        "type": "biz",
        "lang": "ru_RU",
        "results": 10,
        "radius": 5000,
    }

    try:
        search_response = requests.get(search_url, params=search_params).json()
        # Проверяем, есть ли результаты поиска
        if 'features' in search_response and search_response['features']:
            for pharmacy in search_response['features']:
                name = pharmacy['properties']['CompanyMetaData']['name']
                address = pharmacy['properties']['CompanyMetaData'].get('address', 'Адрес не указан')
                print(f"Аптека: {name}, адрес: {address}")
        else:
            print("Аптеки поблизости не найдены (Yandex).")
    except (KeyError, IndexError) as e:
        print(f"Ошибка при поиске аптек: {e}")


address = input("Введите адрес: ")
find_nearest_pharmacy_yandex(address)
