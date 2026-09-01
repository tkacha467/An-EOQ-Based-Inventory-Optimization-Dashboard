@echo off
TITLE Smart Inventory Advisor - Launch System
CLS
COLOR 0A

echo ======================================================================
echo           SMART INVENTORY ADVISOR - EOQ OPTIMIZATION SYSTEM
echo           Presenter: Tushar Pankajbhai Kacha (ID: 92500567015)
echo ======================================================================
echo.

echo [1/3] Preparing Real Kaggle 100-SKU Dataset...
python data_generator.py
python data_pipeline.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Data Pipeline failed. Exiting...
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Executing Automated Unit Test Suite...
python -m unittest test_eoq_model.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Unit Tests failed. Exiting...
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [3/3] Opening New Presentation Web App (index.html)...
start index.html

echo.
echo ======================================================================
echo SUCCESS: The New Web Application (index.html) has launched!
echo ======================================================================
echo.
pause
