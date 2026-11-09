import os
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
TZ = ZoneInfo("Europe/Moscow")
CITIES = [
    {"name": "Донецк (ДНР)", "lat": 48.0159, "lon": 37.8028},
    {"name": "Ростов-на-Дону", "lat": 47.2357, "lon": 39.7015},
]

def emoji(code):
    if code == 0: return "☀️"
    if code in (1, 2): return "🌤"
    if code == 3: return "☁️"
    if code in (45, 48): return "🌫"
    if code in (51, 53, 55, 56, 57): return "🌦"
    if code in (61, 63, 65, 66, 67, 80, 81, 82): return "🌧"
    if code in (71, 73, 75, 77, 85, 86): return "❄️"
    if code in (95, 96, 99): return "⛈"
    return "🌡"

def city_block(city):
    params = {
        "latitude": city["lat"], "longitude": city["lon"],
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "Europe/Moscow", "forecast_days": 1,
    }
    r = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=25)
    r.raise_for_status()
    data = r.json()
    c, d = data["current"], data["daily"]
    code = int(c["weather_code"])
    desc = {
        0:"Ясно", 1:"Преимущественно ясно", 2:"Переменная облачность", 3:"Пасмурно",
        45:"Туман", 48:"Туман", 51:"Морось", 53:"Морось", 55:"Сильная морось",
        61:"Небольшой дождь", 63:"Дождь", 65:"Сильный дождь",
        71:"Небольшой снег", 73:"Снег", 75:"Сильный снег",
        80:"Ливень", 81:"Сильный ливень", 82:"Очень сильный ливень",
        95:"Гроза", 96:"Гроза с градом", 99:"Сильная гроза"
    }.get(code, "Переменная погода")
    temp, feels = round(c["temperature_2m"]), round(c["apparent_temperature"])
    low, high = round(d["temperature_2m_min"][0]), round(d["temperature_2m_max"][0])
    rain = d["precipitation_probability_max"][0]
    rain_text = f"{round(rain)}%" if rain is not None else "нет данных"
    return (
        f"<b>{city['name']}</b>\n{emoji(code)}"
        f"🌡 Сейчас: <b>{temp:+d}°C</b> (ощущается как {feels:+d}°C)\\n"
        f"📈 За день: {low:+d}…{high:+d}°C\\n"
        f"💨 Ветер: {round(c['wind_speed_10m'])} км/ч\\n"
        f"💧 Влажность: {round(c['relative_humidity_2m'])}%\\n"
        f"🌧 Вероятность осадков: {rain_text}"
    )

def main():
    today = datetime.now(TZ).strftime("%d.%m.%Y")
    blocks = []
    for city in CITIES:
        try:
            blocks.append(city_block(city))
        except Exception:
            blocks.append(f"<b>{city['name']}</b>\\n⚠️ Временно не удалось получить прогноз.")
    message = f"🌦 <b>ПОГОДА НА {today}</b>\n\n" + "\n\n────────────\n\n".join(blocks) + "\n\n<i>Источник: Open-Meteo</i>"
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHANNEL_ID, "text": message, "parse_mode": "HTML", "disable_web_page_preview": True},
        timeout=25,
    )
    response.raise_for_status()
    result = response.json()
    if not result.get("ok"):
        raise RuntimeError(f"Telegram API error: {result}")
    print("Weather message published successfully.")

if __name__ == "__main__":
    main()
