@echo off
TITLE Smart Inventory Advisor - Launch Script
CLS
echo ====================================================================
echo             SMART INVENTORY ADVISOR - EOQ DASHBOARD                 
echo ====================================================================
echo.

echo [1/2] Running Backend Unit Tests...
python -m unittest test_eoq_model.py

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Unit tests failed! Stopping launch.
    pause
    EXIT /B %ERRORLEVEL%
)

echo.
echo [SUCCESS] Backend unit tests passed cleanly!
echo.
echo [2/2] Launching Streamlit Application...
echo Access the dashboard in your browser at http://localhost:8501
echo.

streamlit run app.py

PAUSE
