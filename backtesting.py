import time
import pyupbit
import datetime
import telepot

TOKEN = '2020050827:AAHKyThn-rkBCgbLaPc_O87OfEDZtwTu7ZY'
ID = '1796318367'
bot = telepot.Bot(TOKEN)

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma10(ticker):
    """10개봉 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=10)
    ma10 = df['close'].rolling(10).mean().iloc[-1]
    return ma10

def get_four_hrs_ma10(ticker):
    """10개봉 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=20)
    four_hrs_ma10 = df['close'].rolling(10).mean().iloc[-2]
    return four_hrs_ma10


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

def check_profit_ETH(buy,sell):
    profit = round(((sell/buy)-1)*100,2)
    return profit

def check_profit_BTC(buy,sell):
    profit = round(((sell/buy)-1)*100,2)
    return profit

print("test_autotrade start")
# 시작 메세지 슬랙 전송
bot.sendMessage(ID, "sungyong_autotrade start")

check_buy_ETH = False
check_buy_BTC = False

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-ETH")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            print("in trade time")
            target_price_ETH = get_target_price("KRW-ETH", 0.1)
            target_price_BTC = get_target_price("KRW-BTC", 0.2)
            ma10_ETH = get_ma10("KRW-ETH")
            ma10_BTC = get_ma10("KRW-BTC")
            current_price_ETH = get_current_price("KRW-ETH")
            current_price_BTC = get_current_price("KRW-BTC")
            four_hrs_ma10_ETH = get_four_hrs_ma10("KRW-ETH")
            four_hrs_ma10_BTC = get_four_hrs_ma10("KRW-BTC")

            if check_buy_ETH == False and target_price_ETH < current_price_ETH and ma10_ETH < current_price_ETH and four_hrs_ma10_ETH < current_price_ETH:
                real_target_ETH = round(target_price_ETH,-3)
                if check_buy_BTC == True:
                    bot.sendMessage(ID, "ETH_buy_price(test): "+str(real_target_ETH))
                    check_buy_ETH = True
                elif check_buy_BTC == False:
                    bot.sendMessage(ID, "ETH_buy_price(test): "+str(real_target_ETH))
                    check_buy_ETH = True

            if check_buy_BTC == False and target_price_BTC < current_price_BTC and ma10_BTC < current_price_BTC and four_hrs_ma10_BTC < current_price_BTC:
                real_target_BTC = round(target_price_BTC,-3)
                if check_buy_ETH == True:
                    bot.sendMessage(ID, "BTC_buy_price(test): "+str(real_target_BTC))
                    check_buy_BTC = True
                elif check_buy_ETH == False:
                    bot.sendMessage(ID, "BTC_buy_price(test): "+str(real_target_BTC))
                    check_buy_BTC = True
        else:
            if check_buy_ETH == True:
                sell_price_ETH = get_current_price("KRW-ETH")
                current_ETH_profit = check_profit_ETH(target_price_ETH,sell_price_ETH)
                bot.sendMessage(ID, "ETH_sell_price(test): "+str(sell_price_ETH) + '\n'
                                + "Profit: " + str(current_ETH_profit) + "%")
                check_buy_ETH = False
            if check_buy_BTC == True:
                sell_price_BTC = get_current_price("KRW-BTC")
                current_BTC_profit = check_profit_BTC(target_price_BTC,sell_price_BTC)
                bot.sendMessage(ID, "BTC_sell_price(test): "+str(sell_price_BTC) + '\n'
                                + "Profit: " + str(current_BTC_profit) + "%")
                check_buy_BTC = False
            else:
                check_buy_ETH = False
                check_buy_BTC = False
        time.sleep(1)
    except Exception as e:
        print(e)
        bot.sendMessage(ID, e)
        time.sleep(1)
