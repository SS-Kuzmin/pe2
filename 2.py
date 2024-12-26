import folium
from geopy.distance import geodesic

coordinates = [
    (55.7558, 37.6173),  # Москва
    (59.9343, 30.3351),  # Санкт-Петербург
]

# Рассчитаем длину пути
path_length = 0
for i in range(len(coordinates) - 1):
    path_length += geodesic(coordinates[i], coordinates[i + 1]).kilometers

# Найдем среднюю точку пути
avg_lat = sum(lat for lat, lon in coordinates) / len(coordinates)
avg_lon = sum(lon for lat, lon in coordinates) / len(coordinates)

# Создаем карту
map = folium.Map(location=[avg_lat, avg_lon], zoom_start=2)

# Добавляем точки пути на карту
for lat, lon in coordinates:
    folium.Marker([lat, lon]).add_to(map)

# Добавляем метку в средней точке
folium.Marker([avg_lat, avg_lon], popup="Средняя точка", icon=folium.Icon(color='red')).add_to(map)

# Сохраняем карту в HTML файл
map.save("path_map.html")

# Выводим длину пути
print(f"Длина пути: {path_length:.2f} км")
