import configparser
from bs4 import BeautifulSoup
from restock import StockCheck
from telegram_bot import TelegramBot
from datetime import datetime
import time

# Loading config
config = configparser.ConfigParser()
config.read('config.ini')

# Initialize scraping classes
# TODO Cosider function to lambda


# 자주 변할 부분
def zara_check(res):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(res.text, 'html.parser')
    stock = soup.find("li", id="product-detail-size-selector-product-detail-product-size-selector-139867711-item-3")

    if stock['data-qa-action'] == 'size-in-stock':
        return True
    return False


if __name__ == "__main__": # 자주 변하지 않을 부분
    bot = TelegramBot(config['TELEGRAM']['TOKEN'])
    bot.sendMessage(config['TELEGRAM']['RECEIVER_ID'], "Monitoring started.")

    zara_cardigan = StockCheck("Pocket Cardigan XL",
                               "https://www.zara.com/kr/ko/%ED%8F%AC%EC%BC%93-%EA%B0%80%EB%94%94%EA%B1%B4-p00077306.html?v1=139867711&v2=2011851",
                               zara_check,
                               "utf-8")

    sleep_mins = config['DEFAULT']['INTERVAL_MINS']


    def check(checkTargetArray):
        return list(map(lambda item: item.statusChanged(), checkTargetArray))


    while True:
        returns = check([zara_cardigan])

        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), returns)

        alerts = list(filter(lambda item: item[0], returns))

        for item in alerts:
            bot.sendMessage(config['TELEGRAM']['RECEIVER_ID'], "{} status has cahgned to {}".format(item[3].name, item[0]))

        time.sleep(int(sleep_mins)*60)