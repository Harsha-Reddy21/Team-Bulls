import pyotp
import pandas as pd 
from thefirstock import thefirstock
from datetime import datetime

# Firstock credentials
token = 'A65W576GV27T76X723H7AU4F556C2Q77'
userID = 'GR2102'
Password = 'Harsha@108'
apiKey = '04969b4e229274d33bba4cfd278bbf7a'
vendorCode = 'GR2102_API'

# Initialize Firstock login

TOTP = pyotp.TOTP(token).now()
login = thefirstock.firstock_login(
    userId=userID,
    password=Password,
    TOTP=TOTP,
    vendorCode=vendorCode,
    apiKey=apiKey,
)

# Get time series data
def get_results():
    lastBusDay = datetime(2025, 8, 23)
    lastBusDay = lastBusDay.replace(hour=0, minute=0, second=0, microsecond=0)
    results = thefirstock.firstock_TimePriceSeries(
        userId=userID,
        exchange="NFO",
        tradingSymbol="NIFTY29MAY25F",
        startTime="31/03/2025 09:45:45",
        endTime="1/2/2026 13:56:34",
        interval="5"
    )
    return results

def get_stock_results(stock_token):
    results = thefirstock.firstock_TimePriceSeries(
        userId=userID,
        exchange="NSE",
        tradingSymbol=stock_token,
        startTime="31/03/2025 09:45:45",
        endTime="1/2/2026 13:56:34",
        interval="15"
    )
    return results

# Initialize Firstock connection when module is imported
