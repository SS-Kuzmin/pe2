import requests

# Координаты стадионов
stadiums_location = {
    "Лужники": "37.554191,55.715551",
    "Спартак": "37.440262,55.818015",
    "Динамо": "37.559809,55.791540"
}

# Ваш API-ключ
API_KEY = "84b8e5bf-d168-4871-a2f8-9f88fcb3098c"

# Базовый URL для статической карты Яндекс
BASE_URL = "https://static-maps.yandex.ru/1.x/"

# Параметры карты
map_params = {
    "l": "map",  # Слой карты: схематическая (map), спутник (sat), гибрид (sat,skl)
    "size": "650,450",  # Размер карты (ширина, высота)
    "pt": "~".join(f"{coords},pm2blm" for coords in stadiums_location.values()),  # Метки
    "apikey": API_KEY
}

# Запрос к API
response = requests.get(BASE_URL, params=map_params)

# Сохранение карты в файл
if response.status_code == 200:
    with open("moscow_stadiums_map.png", "wb") as file:
        file.write(response.content)
    print("Карта сохранена как moscow_stadiums_map.png")
else:
    print(f"Ошибка загрузки карты: {response.status_code}, {response.text}")
