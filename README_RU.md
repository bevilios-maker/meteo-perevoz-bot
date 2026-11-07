# Погодный бот для Telegram

Публикует одно сообщение с погодой для Донецка (ДНР) и Ростова-на-Дону дважды в день.

## Расписание
Ежедневно около 07:05 и 19:05 по московскому времени. GitHub Actions может задерживать запланированные запуски.

## Настройка с телефона
1. Создайте аккаунт на https://github.com/ (если его ещё нет).
2. Создайте репозиторий `meteo-perevoz-bot`, выберите Public для простого бесплатного варианта.
3. Загрузите `publish.py`, `requirements.txt`, `README_RU.md` и папку `.github/workflows/weather.yml` через Add file → Upload files.
4. Откройте Settings → Secrets and variables → Actions → New repository secret.
5. Создайте секрет `BOT_TOKEN` и вставьте токен от @BotFather.
6. Создайте секрет `CHANNEL_ID` со значением `@popytkataxibezgranitc`.
7. Откройте Actions и разрешите workflows, если GitHub предложит.
8. Выберите `Publish weather to Telegram` → Run workflow → Run workflow для тестовой публикации.

Токен не помещайте в код, README, обычные сообщения или скриншоты. Бот должен быть администратором канала с правом публикации.
