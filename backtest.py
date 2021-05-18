from numpy import positive
import yfinance as yf
import datetime
import order

symbol = "Tatamotors"

start = datetime.date(2021, 3, 20)
end = datetime.date(2021, 5, 18)
interval = "5m"
quatity = 1

# print(start)

# df = yf.Ticker(f"{symbol}.NS").history(period="2y")
df = yf.Ticker(f"{symbol}.NS").history(start=start, end=end, interval=interval)

df["Ma_10"] = round(df["Close"].rolling(window=10).mean(), 2)
df["Ma_50"] = round(df["Close"].rolling(window=50).mean(), 2)

position = None

for i in df.index[49:]:
    if df["Ma_10"][i] > df["Ma_50"][i] and position != "Buy":
        position = "Buy"
        print(f"{position} : at {round(df['Close'][i], 2)} and Date {i}")
        order.buy(quantity=quatity, price=df["Close"][i])
    elif df["Ma_10"][i] <= df["Ma_50"][i] and position == "Buy":
        position = "Sell"
        print(f"{position} : at {round(df['Close'][i], 2)} and Date {i}")
        order.sell(quantity=quatity, price=df["Close"][i])

print(
    f"Returns are {round(100 * (order.portfolio_value - order.amount) / order.amount, 2)}"
)
