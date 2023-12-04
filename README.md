# Telegram Bot

This is a Telegram bot for scheduled publishing video from Instagram to TikTok written in Python using the `telebot` library.

## Prerequisites

- Python 3.x installed
- `pip` package manager
- Telegram Bot Token (Create a new bot on Telegram and obtain the token)

## Installation

1. **Clone the repository:**

    ```bash
    git clone git@github.com:AlexKojuhar/publisher_telegram_bot.git
    cd publisher_telegram_bot
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Create a `.env` file:**

    ```bash
    cp .env-sample .env
    ```

## Configuration

1. **Open the `.env` file with a text editor:**

    ```bash
    nano .env
    ```

2. **Replace environment variables with your actual data:**

    ```env
   BOT_TOKEN=your_bot_token_should_be_here
   INSTAGRAM_USERNAME=your_instagram_username_should_be_here
   INSTAGRAM_PASSWORD=your_instagram_password_should_be_here
    ```

    Save and exit.

3. **Add cookies.txt**

   Authentication uses your browser's cookies. This workaround was done due to TikTok's stricter stance on authentication by a Selenium-controlled browser.

   [🍪 Get cookies.txt](https://github.com/kairi003/Get-cookies.txt-LOCALLY) makes getting cookies in a [NetScape cookies format](http://fileformats.archiveteam.org/wiki/Netscape_cookies.txt).

   After installing, open the extensions menu on [TikTok.com](https://tiktok.com/) and click `🍪 Get cookies.txt` to reveal your cookies. Select `Export As ⇩` and specify a location - directory `publisher_telegram_bot` and name - `cookies.txt` to save.

## Run the Bot

Run the bot using the following command:

```bash
python bot.py
```

## Run the Scheduled Publishing

Run the tasks using the following command:

```bash
python tasks.py
