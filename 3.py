import requests

# Ввод объекта и его координат
name = input("Введите название объекта: ")
coords = input(f"Введите координаты для объекта '{name}' (например, '37.554191,55.715551'): ")

API_KEY = "84b8e5bf-d168-4871-a2f8-9f88fcb3098c"

# Базовый URL для статической карты Яндекс
BASE_URL = "https://static-maps.yandex.ru/1.x/"

# Параметры карты
map_params = {
    "l": "map",  # Слой карты: схематическая (map), спутник (sat), гибрид (sat,skl)
    "size": "650,450",  # Размер карты (ширина, высота)
    "pt": f"{coords},pm2blm",  # Метка для одного объекта
    "spn": "0.009,0.009",  # Радиус
    "apikey": API_KEY
}

# Запрос к API
response = requests.get(BASE_URL, params=map_params)

# Сохранение карты в файл
if response.status_code == 200:
    with open("img по координатам.png", "wb") as file:
        file.write(response.content)
    print("Карта сохранена как img по координатам.png")
else:
    print(f"Ошибка загрузки карты: {response.status_code}, {response.text}")
