import websocket
from binance import Client
import config

SOCKET = "wss://stream.binance.com:9443/ws/crvbusd@depth20@1000ms"
client = Client(config.API_KEY, config.API_SECRET)
first_buy_order = False

coin_name = 'CRVBUSD'
my_buy_price = 2.82

buy_percent = 0.99
sell_percent = 1.01

my_quantity = 4

order_buy_checker_ = {}
order_sell_checker_ = {}

order_buy = {}
order_sell = {}
order_cancel = {}
order_cancel_s = {}


def main_check_status():
    global order_buy_checker_, my_buy_price

    order_buy_checker_ = client.get_order(
        symbol=coin_name,
        orderId=order_buy["orderId"]
    )
    buy_checker_price = float(order_buy_checker_["price"])

    if order_buy_checker_["status"] == "FILLED":
        cancel_order_sell()
        print("Buy Order Filled", order_buy_checker_["price"])
        order_suc_buy = buy_order(quantity=my_quantity,
                                  fiyat=buy_checker_price * buy_percent)
        order_su_sell = sell_order(quantity=my_quantity,
                                   fiyat=buy_checker_price * sell_percent)

    check_status_sell()

    if order_sell_checker_["status"] == "FILLED":
        print("Sell Order Filled", order_sell_checker_["price"])
        sell_checker_price = float(order_sell_checker_["price"])
        cancel_order()
        order_suc_buy = buy_order(quantity=my_quantity,
                                  fiyat=sell_checker_price * buy_percent)
        order_suc_sell_x = sell_order(quantity=my_quantity, fiyat=sell_checker_price * sell_percent)


def sell_order(quantity, fiyat):
    global order_sell
    try:
        print("Sending Order SELL")
        order_sell = client.order_limit_sell(
            quantity=quantity, symbol=coin_name,
            price=float(round(fiyat, 3)))
        print(f"SELL Ordered at:{fiyat}")
        print("-------------------------------")

    except Exception as e:
        print("an exception occured - {}".format(e))
        return False
    return True


def buy_order(quantity, fiyat):
    global order_buy
    try:
        print("Sending Order BUY")
        order_buy = client.order_limit_buy(
            quantity=quantity, symbol=coin_name,
            price=float(round(fiyat, 3)))
        print("Buy Ordered at:", {fiyat})
        print("-------------------------------")

    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True


def check_status_sell():
    global order_sell_checker_

    order_sell_checker_ = client.get_order(
        symbol=coin_name,
        orderId=order_sell["orderId"]
    )


def cancel_order():
    global order_cancel
    try:
        order_cancel = client.cancel_order(
            symbol=coin_name,
            orderId=order_buy['orderId'])
    except Exception as e:
        print("an exception occured - {}".format(e))


def cancel_order_sell():
    global order_cancel_s

    try:
        order_cancel_s = client.cancel_order(
            symbol=coin_name,
            orderId=order_sell['orderId'])
    except Exception as e:
        print("an exception occured - {}".format(e))


def on_message(ws, message):
    global first_buy_order

    if first_buy_order:
        main_check_status()

    else:
        order_succeeded_sell_1 = sell_order(quantity=my_quantity, fiyat=my_buy_price * sell_percent)
        order_succeeded_buy_1 = buy_order(quantity=my_quantity, fiyat=my_buy_price * buy_percent)
        first_buy_order = True


def on_open(ws):
    print('opened connection')


def on_close(ws):
    print('closed connection')


ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
