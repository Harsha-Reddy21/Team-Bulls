import requests
import pandas as pd
from datetime import datetime, timedelta

def get_earnings_data(days: int = 7):
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
    from_date = to_date - timedelta(days=days)
    from_str = from_date.strftime("%d-%m-%Y")
    to_str = to_date.strftime("%d-%m-%Y")

    # 4. API URL (JSON endpoint)
    api_url = f"https://www.nseindia.com/api/event-calendar?from_date={from_str}&to_date={to_str}"

    # 5. Get response
    response = session.get(api_url, headers=headers)

    if response.status_code == 200 and "json" in response.headers.get("Content-Type", ""):
        data = response.json()

        # Convert to DataFrame
        if isinstance(data, dict):
            df = pd.DataFrame(data.get("data", []))
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame()

        result = df['symbol'].unique().tolist()
        return result

    else:
        print("❌ Failed to fetch JSON. Got:", response.status_code, response.headers.get("Content-Type"))
        return pd.DataFrame()
    

if __name__ == "__main__":
    result = get_earnings_data(7)
    print(result)
