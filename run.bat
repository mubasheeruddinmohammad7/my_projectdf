@echo off
echo ====================================
echo   DIGITAL FASHION - SIH 2024
echo ====================================
echo.
echo [1] Starting Backend Server...
start cmd /k "cd backend && python main.py"
echo.
echo [2] Starting Frontend...
timeout /t 3
start http://localhost:8501
streamlit run app.py