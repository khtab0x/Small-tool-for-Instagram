# Fast Instagram Comments Cleaner Bot

For people who want to delete comments on their Instagram account, You have come to the right place > you can use this little tool

> **⚠ You should use the tool for a while, then stop it, and after a few minutes start it up again so your account doesn't get banned**

## What can this tool do?

- You can specify the number of comments you want to delete at once `5, 10, 15, 20, 25`.
- Automatic browser cleanup when operations stop
- Privacy-focused behavior: the `sessionid` message is deleted immediately after saving

## Requirements

- Python 3.8+
- Telegram Bot Token from [@BotFather](https://t,me/botfather)
- Instagram `sessionid` cookie from your authenticated browser session

## Repository Structure

- `app.py` — main Telegram bot and automation logic
- `requirements.txt` — project dependencies
- `start.bat` — Windows launcher that installs dependencies and starts the bot

## Installation

1. Clone the repository:

```bash
git clone https://github.com/khtab0x/Small-tool-for-Instagram.git
cd Small-tool-for-Instagram
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
# or
venv\Scripts\activate      # Windows
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Open `app.py` and replace the placeholder token:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

with your actual Telegram bot token.

## Getting the Instagram Session ID

You need a valid Instagram `sessionid`

Typical ways to get it:

- Open Instagram in your browser
- Open Developer Tools
- Go to Application / Storage > Cookies
- Find the `sessionid` cookie for `instagram.com`
- Copy it and save it in the Telegram bot

**⚠ Your `sessionid` it will be deleted after you send it to the Bot for your safe**

## Usage

Run the bot:

```bash
python app.py
```

On Telegram:

1. Start the bot with `/start`
2. Tap `Set Session ID`
3. Paste your Instagram `sessionid`
4. Tap `Start fast cleaning`
5. You can tap `Live screenshot` to see what's going on with your acc.


### Bot not responding

- Verify that `BOT_TOKEN` is set correctly
- Ensure the bot has been started with `python app.py`
- Check terminal output for Python errors

## Windows Quick Start

If you are on Windows, just do this:

```bat
start.bat
```

This script installs dependencies and launches the bot automatically.

## Disclaimer

**⚠This project is for educational and automation experimentation purposes. It is not affiliated with, endorsed by, or sponsored by Instagram or Telegram. Use it responsibly and in compliance with the applicable platform policies.**
