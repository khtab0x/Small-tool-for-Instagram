# Fast Instagram Comments Cleaner Bot

A powerful, automated Telegram bot built with Python and Playwright that allows you to bulk-delete your Instagram comments directly from the Instagram Activity Center. It uses headless browser automation, bypassing the need for the official Instagram API.

## Features

* **Interactive Telegram Panel:** Control everything directly from Telegram with an inline button interface.
* **High-Speed Deletion:** Automatically selects and deletes comments in batches without manual intervention.
* **Live Monitoring:** Request live screenshots from the headless browser to see what the bot is doing in real-time.
* **Adjustable Batch Sizes:** Change the number of comments deleted per batch (5, 10, 15, 20, or 25) with a single click.
* **Secure:** The bot immediately deletes the message containing your `sessionid` for privacy.

## Prerequisites

* **Python 3.8+** installed on your system.
* A **Telegram Bot Token** (Get it from @BotFather on Telegram).
* Your **Instagram `sessionid`** cookie.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/khtab0x/Small-tool-for-Instagram.git
   cd Small-tool-for-Instagram
