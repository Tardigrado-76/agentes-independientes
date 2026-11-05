@echo off
TITLE QUANTIGRADE - Agent Evaluation Framework - TAU-bench / GAIA (PORT 8509)
COLOR 0B

echo ===============================================================================
echo     QUANTIGRADE - AGENT EVALUATION FRAMEWORK (PORT 8509)
echo     TAU-bench / GAIA Enterprise Benchmark - Detalle Iwan
echo     Capgemini Engineering / White Coding Architecture Practice
echo ===============================================================================
echo.
echo [1/3] Verificando entorno de ejecucion Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta disponible en el PATH del sistema.
    pause
    exit /b 1
)

echo [2/3] Verificando dependencias requeridas...
python -c "import streamlit, pandas, plotly, pydantic, reportlab, pytest" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Instalando dependencias de requirements.txt...
    python -m pip install -r requirements.txt
)

echo [3/3] Iniciando Consola Ejecutiva en Puerto Dedicado 8509...
echo.
echo URL de acceso local: http://localhost:8509
echo Presiona Ctrl+C en esta ventana para detener el servidor.
echo ===============================================================================
echo.

python -m streamlit run app_streamlit.py --server.port 8509 --server.headless false

pause
