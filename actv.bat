@echo off
call %~dp0schBot\venv\Scripts\activate

cd %~dp0schBot

set TOKEN= 5825193393:AAFmktYEBi_aTilQdrvIY493NliAdm4Yb7U

python bot_start.py

pause