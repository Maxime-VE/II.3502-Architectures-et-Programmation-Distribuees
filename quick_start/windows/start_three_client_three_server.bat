@echo off
start powershell -NoExit -Command "cd ..\..\Python; py server.py"
timeout /T 1 /NOBREAK >nul
start powershell -NoExit -Command "cd ..\..\Python; py server.py"
timeout /T 1 /NOBREAK >nul
start powershell -NoExit -Command "cd ..\..\Python; py server.py"
timeout /T 2 /NOBREAK >nul
start powershell -NoExit -Command "cd ..\..\Python; py client.py"
timeout /T 1 /NOBREAK >nul
start powershell -NoExit -Command "cd ..\..\Python; py client.py"
timeout /T 1 /NOBREAK >nul
start powershell -NoExit -Command "cd ..\..\Python; py client.py"

