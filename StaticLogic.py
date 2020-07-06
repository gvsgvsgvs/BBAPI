from abc import ABC, abstractmethod
import requests, json
import hmac, hashlib, urllib
import time


class MainMethodExchangeStatic(ABC):
    def __init__(self, api_key, sign_key):
        self.api_key = api_key
        self.sign_key = sign_key

    '''Пост запрос публичный'''
    def post_req_public_return(self, address, message, head):
        with requests.Session() as s:
            try:
                info = s.post(address, data=message, headers=head)
            except ConnectionError:
                print(info.status_code)
                return 0
            data = json.loads(info.text)
            return data

    '''геты публичные'''
    def get_req_public_return(self, address, message, head):
        with requests.Session() as s:
            info = s.get(address + '?' + message, headers=head)
            d = json.loads(info.text)
        return d


class Poloinex(MainMethodExchangeStatic):
    MethodsPublic = {
        '': {'': '', '': ''}
    }
    MethodsPrivate = {
        'returnBalances': {'command': 'returnBalances', 'method': 'POST'},
        'returnTradeHistory': {'command': 'returnTradeHistory', 'currencyPair': 'all', 'method': 'POST'}
    }

    def __init__(self, api_key, sign_key):
        MainMethodExchangeStatic.__init__(self, api_key, sign_key)

    def __getattr__(self, item):
        def redirection(*args, **kwargs):
            kwargs.update(command=item)
            if kwargs['command'] in self.MethodsPublic.keys():
                return self.main_method_public(**kwargs)
            elif kwargs['command'] in self.MethodsPrivate.keys():
                return self.main_method_private(**kwargs)
            else:
                return 0

        return redirection

    def main_method_public(self, **kwargs):
        pass

    def main_method_private(self, **kwargs):
        command = kwargs.pop('command')
        dict_message = self.MethodsPrivate[command].copy()
        del dict_message['method']
        if self.MethodsPrivate[command]['method'] == 'GET':
            pass
        else:
            dict_message['nonce'] = int(time.time() * 1000)
            message = urllib.parse.urlencode(dict_message)
            sign = hmac.new(self.sign_key.encode(), msg=message.encode(), digestmod=hashlib.sha512).hexdigest().upper()
            head = {'Content-type': 'application/x-www-form-urlencoded', 'Key': self.api_key, 'Sign': sign}
            result = MainMethodExchangeStatic.post_req_public_return(self, 'https://poloniex.com/tradingApi', message, head)
            return result


def main_method(keyapi, signkey, class_name):
    class_title = {'Poloinex': Poloinex}
    A = class_title[class_name](keyapi, signkey)
    d = A.returnBalances()
    print(d)


if __name__ == '__main__':
    keyapi, signkey = 'keyapi', 'signkey'  # poloinex
    main_method(keyapi, signkey, 'Poloinex')
