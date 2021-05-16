# main.py
import websocket, json, pprint, talib, numpy

RSI_PERIOD = 3
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

INTERVAL = "1m"
TRADE_SYMBOL = "ethusdt"
TRADE_QUANTITY = 0.05
SOCKET = "wss://stream.binance.com:9443/ws/" + TRADE_SYMBOL + "@kline_" + INTERVAL

closes = []
in_position = False


def on_open(ws):
    print("opened connection")


def on_close(ws):
    print("closed connection")


def on_message(ws, message):

    global closes

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
                    print("Sell! Sell! Sell!")
                    # put binance sell order logic
                else:
                    print("Don't hold position. ")

            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("Already in position.")
                else:
                    print("Buy! Buy! Buy!")
                    # put binance buy order logic


ws = websocket.WebSocketApp(
    SOCKET, on_open=on_open, on_close=on_close, on_message=on_message
)

ws.run_forever()
