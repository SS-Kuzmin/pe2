import random
import requests
from PIL import Image
from io import BytesIO

API_KEY_GEOCODING = 'c268d9a3-9e78-48e0-9efe-92641b3236c6'  # API-ключ для геокодирования
API_KEY_STATIC = '84b8e5bf-d168-4871-a2f8-9f88fcb3098c'  # API-ключ для статических карт


def get_city_coordinates(city_name):
    """Получить координаты города по его названию с помощью Яндекс API геокодирования"""
    url = f"https://geocode-maps.yandex.ru/1.x/?geocode={city_name}&format=json&apikey={API_KEY_GEOCODING}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["response"]["GeoObjectCollection"]["featureMember"]:
            # Получаем координаты первого найденного города
            coordinates = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
            lon, lat = map(float, coordinates.split())
            return lat, lon
        else:
            print(f"Город '{city_name}' не найден в ответе.")
    else:
        print(f"Ошибка при запросе к API геокодирования: {response.status_code}")
    return None


def get_map_image(coords, zoom=12):
    """Получение карты города с Яндекс.Карт по координатам с заданным уровнем масштаба"""
    url = f"https://static-maps.yandex.ru/1.x/?ll={coords[1]},{coords[0]}&size=600,400&z={zoom}&l=map&apikey={API_KEY_STATIC}"
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print("Ошибка при получении карты")
        return None


def show_partial_image(image, crop_box):
    """Показать часть карты"""
    cropped_image = image.crop(crop_box)
    cropped_image.show()


def game():
    """Цикл игры с вводом первого города и последующим запросом следующего"""
    while True:
        # Запрос первого города
        first_city = input("Введите первый город: ").strip()

        # Получаем координаты города
        coords = get_city_coordinates(first_city)
        if coords:
            image = get_map_image(coords, zoom=14)

            if image:
                # Вырезаем случайную часть карты (например, 200x200 пикселей)
                width, height = image.size
                left = random.randint(0, width - 200)
                top = random.randint(0, height - 200)
                right = left + 200
                bottom = top + 200
                crop_box = (left, top, right, bottom)

                print(f"Показываем часть карты города...")
                show_partial_image(image, crop_box)

                # Запрос на ввод следующего города
                next_city = input("Введите следующий город (или 'выход' для завершения игры): ").strip()
                if next_city.lower() == 'выход':
                    print("Спасибо за игру!")
                    break  # Завершаем игру, если пользователь вводит 'выход'
                else:
                    first_city = next_city  # Обновляем текущий город на следующий
            else:
                print("Не удалось получить карту города.")
        else:
            print(f"Не удалось получить координаты для города {first_city}.")


# Запуск игры
game()
