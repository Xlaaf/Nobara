@echo off
TITLE Nobara bot
:: Enables virtual env mode and then starts kigyo
env\scripts\activate.bat && py -m tg_bot
