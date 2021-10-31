import mysql.connector
import requests
import json



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
def getPrecio(Moneda):
    mydb=conectardb()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT a.Precio FROM `ML_Localidades` a INNER JOIN ML_Partidos b ON a.IdPartido=b.Id where a.Id='"+Localidad+"'")
    myresult = mycursor.fetchone()
    return(myresult)


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

    sql = "INSERT INTO `binance`.`Promedios` (fecha,Moneda,Precio) VALUES (%s,%s, %s)"
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
def UpdateValores(url):
    Hora=getHora()
    r = requests.get(url) 
    Registros = json.loads(r.text)
    valores=[]
    valoresTemp=[]
    for Registro in Registros:

        valoresTemp=[Hora,Registro['symbol'],str(Registro['price'])]
        print(valoresTemp)
        valores.append(valoresTemp)
    insertarValores(valores)
#############################################    
def UpdateValor(url,Simbolos):
    valores=[]
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
def UpdatePromedio(url,Simbolos):
    valores=[]
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
i=1
while i>0:
    #UpdateValores('https://api.binance.com/api/v3/ticker/price')

    Monedas=['BTCUSDT','ETHUSDT','ETHEUR']
    UpdateValor('https://api.binance.com/api/v3/ticker/price',Monedas)
    UpdatePromedio('https://api.binance.com/api/v3/avgPrice',Monedas)
#getUrl2('https://api.binance.com/api/v3/ticker/bookTicker')




#Precio Promedio
#getUrl2('https://api.binance.com/api/v3/avgPrice?symbol=ETHUSDT')

#curl -v -H "apikey:22BjeOROKiXJ3NxbR3zjh3uoGcaflPu3VMyBXAg8Jj2J1xVSnY0eB4dzacdE9IWn" -H "secretKey:YtP1BudNOWZE1ag5uzCkh4hIC7qSmQOu797r5EJBFGhxBYivjj8HIX0iiiPof5yG" -X GET 'https://testnet.binanceops.com/vapi/v1/position?BTC-200730-9000-C&recvWindow=500000&timestamp=1633710030'
  