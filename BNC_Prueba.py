import mysql.connector
import requests
from requests.auth import HTTPBasicAuth
import json
import threading
import time
from datetime import datetime


##########################################################################3
##   funciones
#########################################################################3#

############################
# CONECTAR DB
def conectardb():
    mydb = mysql.connector.connect(
        host="localhost",
        user="Christian",
        password="chinito2312",
        database="binance"
    )
    return mydb

#############################
def insertarValores(valores):
    mydb=conectardb()
    mycursor = mydb.cursor()
    #sql = "DELETE FROM `Recolector`.`Indicadores_BCRA` WHERE Metrica='"+Metrica+"'"
    #mycursor.execute(sql)

    sql = "INSERT INTO `binance`.`Precios` (fecha,Moneda,Precio) VALUES (%s,%s, %s)"
    mycursor.executemany(sql, valores)
    mydb.commit()

    #print(mycursor.rowcount, "was inserted.")
#############################
def insertarPromedios(valores):
    mydb=conectardb()
    mycursor = mydb.cursor()
    #sql = "DELETE FROM `Recolector`.`Indicadores_BCRA` WHERE Metrica='"+Metrica+"'"
    #mycursor.execute(sql)

    sql = "INSERT IGNORE INTO `binance`.`Promedios` (fecha,Moneda,Precio) VALUES (%s,%s, %s)"
    mycursor.executemany(sql, valores)
    mydb.commit()

    #print(mycursor.rowcount, "was inserted.")

#############################
def getUrl(url,head):
    r = requests.get(url,headers=head) 
    valoresTemp = json.loads(r.text)
    print("Respuesta:",valoresTemp)
#############################
def getUrl2(url):
    r = requests.get(url) 
    valoresTemp = json.loads(r.text)
    print("Respuesta:",valoresTemp)
#############################################    
def UpdateValores():
    url='https://api.binance.com/api/v3/ticker/price'
    valores=[]
    z=1
    while z>0:
        #Hora=getHora()
        r = requests.get(url) 
        Registros = json.loads(r.text)
        valores=[]
        valoresTemp=[]
        Hora=datetime.now()
        #Hora = Hora.strftime("%d/%m/%Y %H:%M:%S")
        for Registro in Registros:

            valoresTemp=[Hora,Registro['symbol'],str(Registro['price'])]
            #print(valoresTemp)
            valores.append(valoresTemp)
        insertarValores(valores)
#############################################    
def UpdateValor():
    url='https://api.binance.com/api/v3/ticker/price'
    Simbolos=['BTCUSDT','ETHUSDT','ETHEUR']
    
    valores=[]
    z=1
    while z>0:
        Hora=getHora()
        for Simbolo in Simbolos:
            r = requests.get(url+'?symbol='+Simbolo) 
            Registro = json.loads(r.text)
            valoresTemp=[]
            valoresTemp=[Hora,Registro['symbol'],str(Registro['price'])]
            valores.append(valoresTemp)
        insertarValores(valores)
        print(valores)  
#############################################    
def UpdatePromedio():
    url='https://api.binance.com/api/v3/avgPrice'
    Simbolos=['BTCUSDT','ETHUSDT','ETHEUR']
    valores=[]
    y=1
    while y>0:
        Hora=getHora()
        for Simbolo in Simbolos:
            
            r = requests.get(url+'?symbol='+Simbolo) 
            Registro = json.loads(r.text)
            valoresTemp=[]
            valoresTemp=[Hora,Simbolo,str(Registro['price'])]
            valores.append(valoresTemp)
        insertarPromedios(valores)
        print(valores)        
###############################################    
def getHora():
    r = requests.get("https://testnet.binanceops.com/vapi/v1/time") 
    valoresTemp = json.loads(r.text)
    #print("Respuesta:",valoresTemp["data"])
    return valoresTemp["data"]    
###################################################3




#TraerHora    
#getUrl("https://testnet.binanceops.com/vapi/v1/time")
Hora=getHora()
Hora2=Hora/1000
print(datetime.fromtimestamp(Hora2).strftime('%Y-%m-%d %H:%M:%S.%f'))




apikey="ucGsCr6I9ehZn5i51MlOIXThWrM6bObvQ91nkpeiIaKMAgM8N7ZGPLbUXPbBdOuV"
secret="kjTXifn9ny7kAthuWBuBnM6DOVLKTaHOxxldfWjLdK4dqMwrLLnQPh5ygmQ4y6m1"




#getUrl("https://api.binance.com/sapi/v1/capital/config/getall?recvWindow=5000&timestamp="+str(Hora),headers)
#r = requests.get(url,headers=head) 



def get_all(symbol, binance_api_key, binance_secret_key):
    """Get all account orders; active, canceled, or filled.
    Args:   symbol: Symbol name, e.g. `BTCUSDT`.
    Returns:
    """

    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)  # use POSIX epoch
    posix_timestamp_micros = (now - epoch) // timedelta(microseconds=1)
    posix_timestamp_millis = posix_timestamp_micros // 1000  # or `/ 1e3` for float

    import hmac, hashlib
    queryString = "symbol=" + symbol + "&timestamp=" + str(
        posix_timestamp_millis)
    signature = hmac.new(binance_secret_key.encode(), queryString.encode(), hashlib.sha256).hexdigest()
    url = "https://api.binance.com/sapi/v1/capital/config/getall"
    url = url + f"?{queryString}&signature={signature}"
    response = requests.get(url, headers={'X-MBX-APIKEY': binance_api_key})
    return response.json()






def get_all_orders(symbol, binance_api_key, binance_secret_key):
    """Get all account orders; active, canceled, or filled.
    Args:   symbol: Symbol name, e.g. `BTCUSDT`.
    Returns:
    """

    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)  # use POSIX epoch
    posix_timestamp_micros = (now - epoch) // timedelta(microseconds=1)
    posix_timestamp_millis = posix_timestamp_micros // 1000  # or `/ 1e3` for float

    import hmac, hashlib
    queryString = "symbol=" + symbol + "&timestamp=" + str(
        posix_timestamp_millis)
    signature = hmac.new(binance_secret_key.encode(), queryString.encode(), hashlib.sha256).hexdigest()
    url = "https://api.binance.com/api/v3/allOrders"
    url = url + f"?{queryString}&signature={signature}"
    response = requests.get(url, headers={'X-MBX-APIKEY': binance_api_key})
    return response.json()




def get_listen_key_by_REST(binance_api_key):
    url = 'https://api.binance.com/api/v1/userDataStream'
    response = requests.post(url, headers={'X-MBX-APIKEY': binance_api_key})  # ['listenKey']
    json = response.json()
    return json['listenKey']


print(get_listen_key_by_REST(apikey))
ListadoOrdenes=get_all("ETHEUR",apikey,secret)
print(ListadoOrdenes)
