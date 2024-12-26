import requests


# Функция для получения координат города через API Яндекса
def get_coordinates(city_name, api_key):
    url = f'https://geocode-maps.yandex.ru/1.x/?format=json&geocode={city_name}&apikey={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        if json_data['response']['GeoObjectCollection']['featureMember']:
            # Получаем координаты первого найденного города
            coordinates = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            longitude, latitude = map(float, coordinates.split())
            return latitude, longitude
    return None


# Основная программа
def find_southernmost_city(cities, api_key):
    southernmost_city = None
    southernmost_latitude = 90

    for city in cities:
        coordinates = get_coordinates(city.strip(), api_key)
        if coordinates:
            latitude = coordinates[0]
            if latitude < southernmost_latitude:
                southernmost_latitude = latitude
                southernmost_city = city

    return southernmost_city


# Ввод списка городов
cities_input = input("Введите города через запятую: ")
cities = cities_input.split(',')

api_key = 'c268d9a3-9e78-48e0-9efe-92641b3236c6'

# Нахождение самого южного города
southernmost = find_southernmost_city(cities, api_key)

if southernmost:
    print(f"Самый южный город: {southernmost}")
else:
    print("Не удалось определить города.")
