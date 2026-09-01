@echo off
TITLE Smart Inventory Advisor - Launch System
CLS
COLOR 0A

echo ======================================================================
echo           SMART INVENTORY ADVISOR - EOQ OPTIMIZATION SYSTEM
echo           Presenter: Tushar Pankajbhai Kacha (ID: 92500567015)
echo ======================================================================
echo.

echo [1/4] Preparing Real Kaggle 100-SKU Dataset...
python data_generator.py
python data_pipeline.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Data Pipeline failed. Exiting...
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/4] Executing Automated Unit Test Suite...
python -m unittest test_eoq_model.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Unit Tests failed. Exiting...
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [3/4] Launching HTML Presentation & Dashboard Web Application...
start index.html

echo.
echo [4/4] Starting Streamlit Analytics Engine...
streamlit run app.py

pause
