import requests
from datetime import datetime

DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}


def current_weather(lat, lon):
    token = "94d1a809-5df9-45cb-822e-23299cba0751"
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"
    headers = {"X-Yandex-API-Key": f"{token}"}
    response = requests.get(url, headers=headers).json()
    s = f"Город: {response['geo_object']['locality']['name']}\n" \
        f"Время: {datetime.fromtimestamp(response['fact']['uptime'])}\n" \
        f"Температура: {response['fact']['temp']} °C\n" \
        f"Ощущаемая температура: {response['fact']['feels_like']} °C\n" \
        f"Давление: {response['fact']['pressure_mm']} мм рт. ст.\n" \
        f"Влажность: {response['fact']['humidity']} %\n" \
        f"Скорость ветра: {response['fact']['wind_speed']} м/с\n" \
        f"Порывы ветра: {response['fact']['wind_gust']} м/с\n" \
        f"Направление ветра: {DIRECTION_TRANSFORM.get(response['fact']['wind_dir'])}"
    return s

if __name__ == "__main__":
    print(current_weather(59.93, 30.31))
