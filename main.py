# main.py
import websocket, json, pprint, talib, numpy

RSI_PERIOD = 3
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

INTERVAL = "1m"
TRADE_SYMBOL = "ethusdt"
SOCKET = "wss://stream.binance.com:9443/ws/" + TRADE_SYMBOL + "@kline_" + INTERVAL

TRADE_QUANTITY = 1
TRADE_CAPITAL = 4000.0
TRANSACTION_COST = 0.001

money_end = TRADE_CAPITAL
portfolio = 0
investment = []

closes = []
in_position = False


def buy(quantity, price):
    global portfolio, money_end

    print("Buy! Buy! Buy!")

    allocated_money = quantity * price
    money_end = money_end - allocated_money - (TRANSACTION_COST * allocated_money)
    portfolio += quantity

    if investment == []:
        investment.append(allocated_money)
    else:
        investment.append(allocated_money)
        investment[-1] += investment[-2]

    print("Money End is {}".format(money_end))
    print("Invested: {}".format(investment))


def sell(quantity, price):
    global portfolio, money_end

    print("Sell! Sell! Sell!")

    allocated_money = quantity * price
    money_end = money_end + allocated_money - (TRANSACTION_COST * allocated_money)
    portfolio -= quantity
    investment.append(-allocated_money)
    investment[-1] += investment[-2]

    print("Money End is {}".format(money_end))
    print("Invested: {}".format(investment))
    print("P&L: {}".format(money_end - TRADE_CAPITAL))


def on_open(ws):
    print("opened connection")


def on_close(ws):
    print("closed connection")


def on_message(ws, message):

    global closes, portfolio, in_position

    # print("received message")
    json_message = json.loads(message)
    # pprint.pprint(json_message)

    candle = json_message["k"]
    is_candle_closed = candle["x"]  # the value is true if candle is closed
    close = candle["c"]

    if is_candle_closed:
        # print("candle closed at {}".format(close))
        closes.append(float(close))
        print("closes: ")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all RSI's calculated so far:")
            print(rsi)
            last_rsi = rsi[-1]
            print("Current RSI is {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    sell(TRADE_QUANTITY, closes[-1])
                    in_position = False
                else:
                    print("Don't hold position.")

            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("Already in position.")
                else:
                    buy(TRADE_QUANTITY, closes[-1])
                    in_position = True


ws = websocket.WebSocketApp(
    SOCKET, on_open=on_open, on_close=on_close, on_message=on_message
)

ws.run_forever()
