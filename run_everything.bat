@echo off
echo Starting Video Forge Pipeline (ComfyUI + FastAPI)...

:: 1. Start Headless ComfyUI in a new minimized window
echo Starting ComfyUI Engine...
start /min "ComfyUI_Engine" cmd /c "cd ComfyUI_Backend && ..\venv_comfy\Scripts\python main.py --listen 127.0.0.1 --port 8188 --lowvram"

:: 2. Wait for ComfyUI to initialize (usually 30 seconds on first run)
echo Waiting for engine to warm up (this takes longer on the first run)...
timeout /t 30 /nobreak > nul

:: 3. Start our FastAPI Bridge Server (minimized)
echo Starting API Bridge...
start /min "VideoForge_API" cmd /c "venv_comfy\Scripts\python server.py"

echo.
echo ===================================================
echo   VIDEO FORGE IS RUNNING!
echo   Open your browser to: http://localhost:8001
echo ===================================================
echo.
pause
