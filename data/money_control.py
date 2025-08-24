import requests
from bs4 import BeautifulSoup

def get_moneycontrol_stocks_in_news():
    url = "https://www.moneycontrol.com/news/business/stocks/stocks-in-news/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers)
    print(response.text)
    stocks = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Article headlines usually contain stock names
        for headline in soup.select("h2, h3"):  
            text = headline.get_text(strip=True)
            # crude filter: look for capitalized words (likely stock names)
            words = [w for w in text.split() if w.isupper() and len(w) > 2]
            stocks.extend(words)

        return sorted(set(stocks))
    else:
        print("❌ Failed to fetch page:", response.status_code)
        return []

if __name__ == "__main__":
    symbols = get_moneycontrol_stocks_in_news()
    print("Stocks in News:", symbols)
