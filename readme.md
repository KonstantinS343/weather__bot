# **Setting up the environment**
    cd tg_bot
    poetry shell
    poetry install

# **Telegram and Weather settings**
To get a telegram bot token, you need to contact the [BotFather](https://t.me/BotFather), after creation he will give you a token. To get the API key of the weather, you need to go to the [OpenWeather](https://openweathermap.org/), register there, then in the **Profile->My API keys** copy the API key.

# **Set the enviroment variable**
    export TELEGRAM=your_telegram_token
    export WEATHER=your_weather_api_key

# **Project launch**
    poetry run start

