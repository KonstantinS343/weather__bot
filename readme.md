# **Setting up the environment**
    cd tg_bot
    poetry shell
    poetry install

# **Telegram and Weather settings**
To get a telegram bot token, you need to contact the [BotFather](https://t.me/BotFather), after creation he will give you a token. To get the API key of the weather, you need to go to the [OpenWeather](https://openweathermap.org/), register there, then in the **Profile->My API keys** copy the API key.

# **Set the enviroment variable**
    cd tg_bot/bot_core
    true > .env
    nano .env 
Insert your telegram token in the format `TELEGRAM=your_telegram_token`, after saving the file `Ctrl+S` and exiting `Ctrl+X`.

# **Project launch**
    poetry run start

