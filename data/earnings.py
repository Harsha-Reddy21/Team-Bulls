import requests
import pandas as pd
from datetime import datetime, timedelta
def get_earnings_data():
    # 1. Headers
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.nseindia.com/companies-listing/corporate-filings-event-calendar"
    }

    # 2. Session
    session = requests.Session()
    session.get("https://www.nseindia.com/companies-listing/corporate-filings-event-calendar", headers=headers)

    # 3. Date range
    to_date = datetime.today()
    from_date = to_date - timedelta(days=7)
    from_str = from_date.strftime("%d-%m-%Y")
    to_str = to_date.strftime("%d-%m-%Y")

    # 4. API URL (correct one)
    api_url = f"https://www.nseindia.com/companies-listing/corporate-filings-event-calendar"

    # 5. Get response
    response = session.get(api_url, headers=headers)




    print(response.text)
    if response.status_code == 200 and "json" in response.headers.get("Content-Type", ""):
        data = response.json()
        print(data)

        if isinstance(data, dict):
            df = pd.DataFrame(data.get("data", []))
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame()

        if not df.empty and "symbol" in df.columns:
            symbols = sorted(df['symbol'].dropna().unique().tolist())

    return symbols

if __name__ == "__main__":
    print(get_earnings_data())

