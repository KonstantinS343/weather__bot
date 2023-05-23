# Setting up the environment
    cd tg_bot
    poetry shell
    poetry install

# Telegram and Weather settings
To get a telegram bot token, you need to contact the [BotFather](https://t.me/BotFather), after creation he will give you a token. To get the API key of the weather, you need to go to the [OpenWeather](https://openweathermap.org/), register there, then in the **Profile->My API keys** copy the API key.

# Set the enviroment variable
    cd tg_bot/bot_core
    true > .env
    nano .env 
Insert your telegram token and openweather api key in the format `TELEGRAM=your_telegram_token`, `WEATHERAPI=your_weather_api_key`, after saving the file `Ctrl+S` and exiting `Ctrl+X`.


# Project launch
    poetry run start

# Tech used

* [Poetry](https://python-poetry.org/) for more convenient package management
* [aiogram](https://aiogram.dev/) for write the bot itself
* [aiohttp](https://docs.aiohttp.org/en/stable/) for requests
* [asyncio](https://docs.python.org/3/library/asyncio.html) for asynchronous programming
# License

This Telegram bot is open source and available under the [MIT License](LICENCE).

