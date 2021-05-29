# coding=utf-8

import requests
import urllib.request
import json
import datetime

def q():
    print(datetime.datetime.now(), end='\n\n')
    ret = ''
    stocks = ['sh000001', 'sh510050', 'sh510300','sh512500', 'sh515800'
            , 'sz399006',  'sz159949', 'sh000688']
    for stock in stocks:
        ret += '- '+ displayTencent(stock)
    print('')

    indices = [['BDI', '   BDI'], ['CRB', '   CRB']]
    for index in indices:
        ret += '- '+displayEastMoneyIndex(index)

    futures = {
            'C0': ['  Corn', ''],
            'M0': [' Soy M', ''],
            'RM0':['Seed M', ''],
            'SR0':[' Sugar', ''], 
            'CF0':['Cotton', ''], 
            'RU0':['Rubber', ''], 
            'ZC0':['  Coal', ''], 
             'I0':['  Iron', ''], 
            'PP0':['    PP', ''],
            'L0': ['Plstic', ''],
            'V0': ['   PVC', ''],
            'TA0':['   PTA', ''], 
         'nf_PG0':['   LPG', ''],
            'MA0':['    MA', ''], 
            'CU0':['Copper', ''], 
            'ZN0':['  Zinc', ''], 
            'AL0':['Alumin', ''], 
            'AU0':['  Gold', ''], 
            'SC0':[' Crude', ''], 
            }
    futures = {
            'TA0':['   PTA', ''], 
            }
    for future in futures:
        ret += '- ' + displayFuture(getSinaInfo(future), futures[future]) +'\n'
    print('')

    yahooList = ['CL=F']
    for code in yahooList:
        ret += '- '+displayYahoo(code) + '\n'
    print('')

    displayEastMoneyIndex(['UDI', '   DXY'])
    metals = {'hf_XAU': 'XAUUSD'}
    for metal in metals:
        ret += '- ' + displayMetal(getSinaInfo(metal), metals[metal])+'\n'
    print('')

    coins = ['bitcoin', 'xrp', 'eos']
    for coin in coins:
        ret += '- ' + displayCoin(coin)+'\n'
    return ret

def displayEastMoneyIndex(code):
    response = urllib.request.urlopen(
            'http://push2.eastmoney.com/api/qt/clist/get'
            + '?pn=1&pz=9&po=1&np=1&fltt=2&invt=2&fid=f3'
            + '&fs=i:100.' + code[0]
            + '&fields=f1,f2,f3,f4,f5,f12,f13,f14,f152')
    j = json.loads(response.readline().decode('utf-8'))
    d = j['data']['diff'][0]
    return code[1] + ' ' +  f(str(d['f3']) + '%') + ' ' +  str(d['f2']).ljust(10)

def getTencent(code):
    response = urllib.request.urlopen('http://qt.gtimg.cn/q=s_' + code)
    return response.readline().decode('gb2312')

def displayTencent(code):
    resultStr = getTencent(code)
    s = resultStr[14:-3].split('~')
    return s[2] + ' '+ f(s[5]) + '%' + ' ' + s[3].ljust(10)

def displayFuture(resultStr, code):
    s = resultStr.split(',')
    return code[0]+ ' '+ c(s[8], s[10])+ ' '+s[8].ljust(10)+ ' '+ code[1]


def displayMetal(resultStr, code):
    s = resultStr.split(',')
    return code + ' '+ c(s[0], s[1])+ ' '+ s[0].ljust(10)

def displayCoin(code):
    r = requests.request('GET', 'http://web-api.coinmarketcap.com' +
            '/v1/cryptocurrency/quotes/latest?slug=' + code)
    quote = list(r.json()['data'].values())[0]['quote']['USD']
    price = str(quote['price'])
    change = f(str('{:.2f}'.format(quote['percent_change_24h'])) + '%')
    if code == 'bitcoin':
        code = 'btc'
    return code.upper().rjust(6) + ' '+ change+ ' '+ price[:7].ljust(10)

def displayYahoo(code):
    r = requests.request('GET', 'https://query1.finance.yahoo.com' 
            + '/v7/finance/quote?symbols=' + code)
    r = r.json()['quoteResponse']['result'][0]
    cur = r['regularMarketPrice']
    prev = r['regularMarketPreviousClose']
    return code.rjust(6)+ ' '+ c(cur, prev)+ ' '+ str(cur).ljust(10)

def c(a, b):
    return f(str('{:.2f}'.format(
        round((float(a) - float(b)) / float(b), 4) * 100
        ))) + '%'
        
def f(s):
    if not s.startswith('-'):
        return '+' + s
    else:
        return s

def getSinaInfo(code):
    response = urllib.request.urlopen('http://hq.sinajs.cn/list=' + code)
    return response.readline().decode('gb2312').split('"')[1]


if __name__ == '__main__':
    ret = q()

    url = 'https://oapi.dingtalk.com/robot/send?access_token=58fcd70ff1757c3dd3640293f72c45c39432037544837a1904a69ae1de5d3f71'
    body = {
     "msgtype": "markdown",
     "markdown": {
         "title":"大盘天气",
         "text": ret
     }
 }
    html = requests.post(url, data=json.dumps(body), headers={'Content-type': 'application/json; charset=utf-8'})
    print(html.json())






