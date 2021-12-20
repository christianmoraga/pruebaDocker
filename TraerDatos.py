import mysql.connector
import requests
import json
import threading
import time
from datetime import datetime
import numpy





##########################################################################3
##   funciones
#########################################################################3#

############################
# CONECTAR DB
def conectardb():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
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

    sql = "INSERT IGNORE INTO `binance`.`Precios` (fecha,Moneda,Precio) VALUES (%s,%s, %s)"
    mycursor.executemany(sql, valores)
    mydb.commit()

    #print(mycursor.rowcount, "was inserted.")
#############################
def insertarPromedios(valores):
    mydb=conectardb()
    mycursor = mydb.cursor()
    #sql = "DELETE FROM `Recolector`.`Indicadores_BCRA` WHERE Metrica='"+Metrica+"'"
    #mycursor.execute(sql)

    sql = "INSERT IGNORE INTO `binance`.`Promedios` (fecha,Moneda,Precio,Intervalo) VALUES (%s,%s,%s,%s)"
    mycursor.executemany(sql, valores)
    mydb.commit()

    #print(mycursor.rowcount, "was inserted.")
#############################
def traerMonedas():
    mydb=conectardb()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT a.Moneda FROM `Monedas` a where a.Estado=1")
    myresult = mycursor.fetchall()
    return(myresult)
#############################
def getUrl(url,head):
    r = requests.get(url,headers=head) 
    valoresTemp = json.loads(r.text)
    #print("Respuesta:",valoresTemp)
#############################
def getUrl2(url):
    r = requests.get(url) 
    valoresTemp = json.loads(r.text)
    #print("Respuesta:",valoresTemp)
#############################################    
def UpdateValores():
    url='https://api.binance.com/api/v3/ticker/price'
    valores=[]
    z=1
    Simbolos=traerMonedas()
    
    while z>0:
        Hora=getHora()
        
        r = requests.get(url) 
        Registros = json.loads(r.text)
        #print(Registros)
        valores=[]
        valoresTemp=[]
        #ValoresPercentil=[]
        #varSimbolo=[]
        #varPrecio=[]
        #Hora=datetime.now()
        
        #print(Simbolo2[10])
        #print(Simbolos[1][0])
        for Simbolo in Simbolos:
            for Registro in Registros:
                if Simbolo[0]==Registro['symbol']:    
                    valoresTemp=[Hora,Registro['symbol'],str(Registro['price'])]
                    
                    #print(valoresTemp)
                    valores.append(valoresTemp)
                    #if len(ValoresPercentil)>50:
                    #    ValoresPercentil.pop(0)
                    #varSimbolo.append()    
                    #ValoresPercentil.append(valoresTemp)
                    break

        insertarValores(valores)
        print(valores)
################################################
def getValorMoneda(Simbolo):
    url='https://api.binance.com/api/v3/ticker/price'
    z=1
    
    while z>0:
        for n in range(10):    
            Hora=getHora()
            valores=[]
            r = requests.get(url+'?symbol='+Simbolo) 
            Registro = json.loads(r.text)
            valoresTemp=[]
            valoresTemp=[Hora,Registro['symbol'],str(Registro['price'])]
            valores.append(valoresTemp)
        print(valores)
        insertarValores(valores)



#############################################    
def UpdateValor():
    
    Simbolos=traerMonedas()
    threads2=[]
    #print(Simbolos)
    #Simbolos=['BTCUSDT','ETHUSDT','ETHEUR']
    valores=[]
    
    for Simbolo in Simbolos:
        nSimbolo=Simbolo[0]
        print(nSimbolo)
        tSimbolo=threading.Thread(target=getValorMoneda,args=(nSimbolo,),name="T"+Simbolo[0])
        threads2.append(tSimbolo)
        tSimbolo.start()
          
#############################################    
def UpdatePromedio():
    url='https://api.binance.com/api/v3/avgPrice'
    #Simbolos=['BTCUSDT','ETHUSDT','ETHEUR']
    Simbolos=traerMonedas()
    valores=[]
    y=1
    while y>0:
        Hora=getHora()
        for Simbolo in Simbolos:
            print(Simbolo[0])
            r = requests.get(url+'?symbol='+Simbolo[0]) 
            Registro = json.loads(r.text)
            valoresTemp=[]
            valoresTemp=[Hora,Simbolo[0],str(Registro['price']),'300']
            valores.append(valoresTemp)
        insertarPromedios(valores)
        #print(valores)        
###############################################    
def getHora():
    r = requests.get("https://testnet.binanceops.com/vapi/v1/time") 
    valoresTemp = json.loads(r.text)
    #print("Respuesta:",valoresTemp["data"])
    horatemp=(valoresTemp["data"])/1000  
    horatemp=datetime.fromtimestamp(horatemp).strftime('%Y-%m-%d %H:%M:%S.%f') 
    return horatemp
###################################################3
def ChequeoEstado():
    bucle=1
    while bucle>0:
        time.sleep(2)
        #threading.enumerate()
        for t in threads:
            #if t.is_alive():
                #print(t.name+" Activo")
            if not t.is_alive():
                # get results from thread
                print(t.name+" Caido")
                t.start()

###################################################


#TraerHora    
#getUrl("https://testnet.binanceops.com/vapi/v1/time")
#Hora=getHora()
#print(Hora)

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

    #UpdateValores('https://api.binance.com/api/v3/ticker/price')
threads=[]
    
tValores=threading.Thread(target=UpdateValores,name="TValores")
threads.append(tValores)
tValores.start()
#tPromedios=threading.Thread(target=UpdatePromedio, name="TPromedios")
#threads.append(tPromedios)
#tPromedios.start()
tChequeos=threading.Thread(target=ChequeoEstado,name="ChequeoEstado")
threads.append(tValores)
tChequeos.start()

#getUrl2('https://api.binance.com/api/v3/ticker/bookTicker')




#Precio Promedio
#getUrl2('https://api.binance.com/api/v3/avgPrice?symbol=ETHUSDT')

#curl -v -H "apikey:22BjeOROKiXJ3NxbR3zjh3uoGcaflPu3VMyBXAg8Jj2J1xVSnY0eB4dzacdE9IWn" -H "secretKey:YtP1BudNOWZE1ag5uzCkh4hIC7qSmQOu797r5EJBFGhxBYivjj8HIX0iiiPof5yG" -X GET 'https://testnet.binanceops.com/vapi/v1/position?BTC-200730-9000-C&recvWindow=500000&timestamp=1633710030'

 