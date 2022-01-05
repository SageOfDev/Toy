import requests


class StockCheck:
    def __init__(self, name, url, checkMethod, encoding):
        self.name = name
        self.url = url
        self.checkMethod = checkMethod
        self.encoding = encoding
        self.last_status = False

    def getResponse(self):
        URL = self.url
        agent = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
        return requests.get(URL, headers=agent)

    def check(self):
        res = self.getResponse()
        if res.encoding != self.encoding:
            res.encoding = self.encoding
        return self.checkMethod(res)

    def statusChanged(self):
        status = self.check()

        if self.last_status != status:
            self.last_status = status
            return (True, not(self.last_status), self.last_status, self)
        return (False, self.last_status, status, self)

    def __str__(self):
        return "{} is {}".format(self.name, self.last_status)


if __name__ == "__main__":
    def zara_check(res):
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(res.text, 'html.parser')
        stock = soup.find("li", id="product-detail-size-selector-product-detail-product-size-selector-139867711-item-3")

        if stock['data-qa-action'] == 'size-in-stock':
            return True
        return False

    zara_cardigan = StockCheck("Pocket Cardigan XL",
                               "https://www.zara.com/kr/ko/%ED%8F%AC%EC%BC%93-%EA%B0%80%EB%94%94%EA%B1%B4-p00077306.html?v1=139867711&v2=2011851",
                               zara_check,
                               "utf-8")
    stock = zara_cardigan.check()
    print(zara_cardigan.name, "Available? ", stock)
    (status_changed, last_status, current_status) = zara_cardigan.statusChanged()
    print(zara_cardigan.name, "Status Changed? ", status_changed, ", Last Status? ", last_status, ", Current Status?", current_status)