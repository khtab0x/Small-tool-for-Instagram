@echo off
title Instagram Bot Launcher
color 0a

echo =========================================
echo Checking and installing required packages...
echo =========================================
pip install -r requirements.txt

echo.
echo =========================================
echo Checking and installing Playwright browser...
echo =========================================
playwright install chromium

echo.
echo =========================================
echo Starting the bot now...
echo =========================================
python app.py

pause