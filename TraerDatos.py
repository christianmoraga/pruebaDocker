import mysql.connector
import requests
import json


def getUrl(url,head):
    r = requests.get(url,headers=head) 
    valoresTemp = json.loads(r.text)
    print("Respuesta:",valoresTemp)
def getUrl2(url):
    r = requests.get(url) 
    valoresTemp = json.loads(r.text)
    print("Respuesta:",valoresTemp)    
def getHora():
    r = requests.get("https://testnet.binanceops.com/vapi/v1/time") 
    valoresTemp = json.loads(r.text)
    #print("Respuesta:",valoresTemp["data"])
    return valoresTemp["data"]    

#TraerHora    
#getUrl("https://testnet.binanceops.com/vapi/v1/time")
Hora=getHora()
print(Hora)

#headers = {"apikey": "22BjeOROKiXJ3NxbR3zjh3uoGcaflPu3VMyBXAg8Jj2J1xVSnY0eB4dzacdE9IWn","secretKey":"YtP1BudNOWZE1ag5uzCkh4hIC7qSmQOu797r5EJBFGhxBYivjj8HIX0iiiPof5yG"}
headers = {"apikey": "ucGsCr6I9ehZn5i51MlOIXThWrM6bObvQ91nkpeiIaKMAgM8N7ZGPLbUXPbBdOuV","secretKey":"kjTXifn9ny7kAthuWBuBnM6DOVLKTaHOxxldfWjLdK4dqMwrLLnQPh5ygmQ4y6m1"}

h2 = {"prueba": "prueba"}
#getUrl("https://testnet.binanceops.com/vapi/v1/position?BTC-200730-9000-C&recvWindow=500000&timestamp="+str(Hora),headers)
#getUrl2("https://api.binance.com/api/v3/exchangeInfo?symbol=BNBBTC&symbol=BTCUSDT")
#getUrl2('https://api.binance.com/api/v3/exchangeInfo?symbols=["BNBBTC","BTCUSDT","ETHUSDT"]')
#getUrl2('https://api.binance.com/api/v3/exchangeInfo?symbols=["ETHUSDT"]')

#Precio Actual
#getUrl2('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT')
#getUrl2('https://api.binance.com/api/v3/ticker/price?symbol=ETHEUR')
getUrl2('https://api.binance.com/api/v3/ticker/price')

#getUrl2('https://api.binance.com/api/v3/ticker/bookTicker')




#Precio Promedio
getUrl2('https://api.binance.com/api/v3/avgPrice?symbol=ETHUSDT')

#curl -v -H "apikey:22BjeOROKiXJ3NxbR3zjh3uoGcaflPu3VMyBXAg8Jj2J1xVSnY0eB4dzacdE9IWn" -H "secretKey:YtP1BudNOWZE1ag5uzCkh4hIC7qSmQOu797r5EJBFGhxBYivjj8HIX0iiiPof5yG" -X GET 'https://testnet.binanceops.com/vapi/v1/position?BTC-200730-9000-C&recvWindow=500000&timestamp=1633710030'
  