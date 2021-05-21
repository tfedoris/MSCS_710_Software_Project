@ECHO OFF
pip install psutil
pip install pandas
pip install sqlalchemy
pip install py-cpuinfo
pip install pycryptodomex
pip install requests
cd computerMetricCollector
pyinstaller --onefile --name ComputerMetricsCollector __init__.py
ECHO Congratulations! The executable has been created! You can now run ComputerMetricsCollector.exe in the path mentioned above!
PAUSE
