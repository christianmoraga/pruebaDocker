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
        database="Recolector"
    )
    return mydb

#############################
def insertarValores(Metrica):
    mydb=conectardb()
    mycursor = mydb.cursor()
    sql = "DELETE FROM `Recolector`.`Indicadores_BCRA` WHERE Metrica='"+Metrica+"'"
    mycursor.execute(sql)

    sql = "INSERT INTO `Recolector`.`Indicadores_BCRA` (Metrica,Fecha, Valor) VALUES (%s,%s, %s)"
    val = [
    ('Peter', 'Lowstreet 4'),
    ('Amy', 'Apple st 652'),
    ('Hannah', 'Mountain 21'),
    ('Michael', 'Valley 345'),
    ('Sandy', 'Ocean blvd 2'),
    ('Betty', 'Green Grass 1'),
    ('Richard', 'Sky st 331'),
    ('Susan', 'One way 98'),
    ('Vicky', 'Yellow Garden 2'),
    ('Ben', 'Park Lane 38'),
    ('William', 'Central st 954'),
    ('Chuck', 'Main Road 989'),
    ('Viola', 'Sideway 1633')
    ]

    mycursor.executemany(sql, valores)

    mydb.commit()

    print(mycursor.rowcount, "was inserted.")


#############################
def insertarCategorias():

    r=requests.get('https://api.mercadolibre.com/categories/MLA1459')
    valoresTemp = json.loads(r.text)
    print(valoresTemp)
    
    for elementoN1 in valoresTemp:
        print("ElementoN1:",elementoN1)
    #print(valoresTemp['children_categories'])
    valores=[]
    for Categoria in valoresTemp['children_categories']:
        print(Categoria)
        valoresTemp2=[Categoria['id'],Categoria['name'],Categoria['total_items_in_this_category']]
        valores.append(valoresTemp2)

    #for Atributo in valoresTemp['settings']:
    #    print(Atributo)

    mydb=conectardb()
    mycursor = mydb.cursor()
    sql = "DELETE FROM `Recolector`.`ML_Categorias`"
    mycursor.execute(sql)
    sql = "INSERT INTO `Recolector`.`ML_Categorias` (id,name,total_items_in_this_category) VALUES (%s,%s, %s)"
    #val = [('Peter', 'Lowstreet 4'),('Amy', 'Apple st 652')] ejemplo de formato
    mycursor.executemany(sql, valores)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")


#############################
def insertarSettings():

    r=requests.get('https://api.mercadolibre.com/categories/MLA1459')
    valoresTemp = json.loads(r.text)
    print(valoresTemp)
    
    for elementoN1 in valoresTemp:
        print("ElementoN1:",elementoN1)
    #print(valoresTemp['children_categories'])
    valores=[]
    y=valoresTemp['settings']
    for Setting in y:
        #print(Setting,y[Setting])
       # print("Nombre ".Setting," valor:",valoresTemp['settings'][Setting])
       
        valoresTemp2=[Setting,str(y[Setting])]
        valores.append(valoresTemp2)
        print(valores)

    mydb=conectardb()
    mycursor = mydb.cursor()
    sql = "DELETE FROM `Recolector`.`ML_Settings`"
    mycursor.execute(sql)
    sql = "INSERT INTO `Recolector`.`ML_Settings` (setting,valor) VALUES (%s,%s)"
    # #val = [('Peter', 'Lowstreet 4'),('Amy', 'Apple st 652')] ejemplo de formato
    mycursor.executemany(sql, valores)
    mydb.commit()
    print(mycursor.lastrowid)
    print(mycursor.rowcount, "was inserted.")





#############################
def insertarProvincias():
    r = requests.get('https://api.mercadolibre.com/classified_locations/countries/AR')
    valoresTemp = json.loads(r.text)
    print(valoresTemp)
    
    for elemento in valoresTemp:
        print("ElementoN1:",elemento)
    print(valoresTemp['states'])
    valores=[]
    for elemento in valoresTemp['states']:
        print(elemento)
        valoresTemp2=[elemento['id'],elemento['name']]
        valores.append(valoresTemp2)

    mydb=conectardb()
    mycursor = mydb.cursor()
    sql = "DELETE FROM `Recolector`.`ML_States`"
    mycursor.execute(sql)
    sql = "INSERT INTO `Recolector`.`ML_States` (id,name) VALUES (%s,%s)"
    mycursor.executemany(sql, valores)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.",mycursor.lastrowid)    


#############################
def insertarPartidos(Prov):
    r = requests.get('https://api.mercadolibre.com/classified_locations/states/'+Prov)
    valoresTemp = json.loads(r.text)
    print(valoresTemp)
    
    for elemento in valoresTemp:
        print("Elemento:",elemento)
    print(valoresTemp['cities'])
    valores=[]
    for elemento in valoresTemp['cities']:
        print(elemento)
        valoresTemp2=[elemento['id'],Prov,elemento['name']]
        valores.append(valoresTemp2)

    mydb=conectardb()
    mycursor = mydb.cursor()
    #sql = "DELETE FROM `Recolector`.`ML_Partidos`"
    #mycursor.execute(sql)
    sql = "INSERT IGNORE INTO `Recolector`.`ML_Partidos` (id,IdProvincia,name) VALUES (%s,%s,%s)"
    mycursor.executemany(sql, valores)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.",mycursor.lastrowid)    

#############################
def insertarLocalidades(Partido):
    r = requests.get('https://api.mercadolibre.com/classified_locations/cities/'+Partido) 
    valoresTemp = json.loads(r.text)
    print(valoresTemp)
    
    for elemento in valoresTemp:
        print("Elemento:",elemento)
    print(valoresTemp['neighborhoods'])
    valores=[]
    for elemento in valoresTemp['neighborhoods']:
        print(elemento)
        valoresTemp2=[elemento['id'],Partido,elemento['name']]
        valores.append(valoresTemp2)

    mydb=conectardb()
    mycursor = mydb.cursor()
    #sql = "DELETE FROM `Recolector`.`ML_Localidades`"
    #mycursor.execute(sql)
    sql = "INSERT IGNORE INTO `Recolector`.`ML_Localidades` (id,IdPartido,name) VALUES (%s,%s,%s)"
    mycursor.executemany(sql, valores)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.",mycursor.lastrowid)    

#############################
def ConsultarPorLocalidad(Localidad):
    mydb=conectardb()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT a.Id as Localidad, b.Id as Provincia, b.IdProvincia as Provincia FROM `ML_Localidades` a INNER JOIN ML_Partidos b ON a.IdPartido=b.Id where a.Id='"+Localidad+"'")
    myresult = mycursor.fetchone()
    return(myresult)

#############################
def CalcularTotales():
    mydb=conectardb()
    mycursor = mydb.cursor()
    mycursor.execute("DROP TABLE IF EXISTS `Recolector`.`ML_ResumenPrincipal`")
    mycursor.execute("CREATE TABLE ML_ResumenPrincipal as SELECT * FROM ML_resumen3")
    mycursor.execute("DROP TABLE IF EXISTS `Recolector`.`ML_Indicadores1`")
    mycursor.execute("CREATE TABLE ML_Indicadores1 as SELECT Localidad,TipoInmueble,Operación,Moneda,TipoSupTotal,TipoSupCub ,COUNT(IdPublicacion),min(Precio) as Minimo, avg(Precio) as Promedio,max(Precio) as Maximo,STDDEV(Precio) as Desvio FROM `ML_ResumenPrincipal` group by  Localidad,TipoInmueble,Operación,Moneda,TipoSupTotal,TipoSupCub")
    


###############################################################################################33
# MERCADOLIBRE
#############################
def insertarMetricas_ML(datos):
    mydb=conectardb()
    mycursor = mydb.cursor()
    #sql = "DELETE FROM `Recolector`.`Indicadores_BCRA` WHERE Metrica='"+Metrica+"'"
    #mycursor.execute(sql)

    sql = "INSERT IGNORE INTO `Recolector`.`ML_Metricas` (IdPublicacion,Parametro, Valor,Unidad) VALUES (%s, %s,%s,%s)"
    mycursor.executemany(sql, datos)

    mydb.commit()

    print(mycursor.rowcount, "was inserted.")


#############################
def insertarPublicaciones(valores):
    try:
        mydb=conectardb()
        mycursor = mydb.cursor()            

        #sql = "DELETE FROM `Recolector`.`ML_Publicaciones`"
        #mycursor.execute(sql)
        sql = "INSERT IGNORE INTO `Recolector`.`ML_Publicaciones` (`IdPublicacion`, `Descripcion`, `Precio`, `Moneda`, `Latitud`, `Longitud`, `Domicilio`, `CodigoPostal`, `Barrio`, `IdLocalidad`, `IdPartido`, `IdProvincia`, `IdPais`, `SuperficieTotal`, `SuperficieCubierta`)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        print(valores)
        print(sql)
        mycursor.executemany(sql, valores)
        mydb.commit()
        print(mycursor.rowcount, "was inserted.",mycursor.lastrowid)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))   


#############################
def insertarAtributos_ML(datosAtributos):
    mydb=conectardb()
    mycursor = mydb.cursor()
    #sql = "DELETE FROM `Recolector`.`Indicadores_BCRA` WHERE Metrica='"+Metrica+"'"
    #mycursor.execute(sql)

    sql = "INSERT IGNORE INTO `Recolector`.`ML_Publicaciones_Atributos` (`IdPublicacion`, `IdAtributo`, `NombreAtributo`, `ValorAtributo`) VALUES (%s, %s,%s,%s)"
    mycursor.executemany(sql, datosAtributos)

    mydb.commit()

    print(mycursor.rowcount, "was inserted.")


#############################
def ParsearPropiedades(url):
    r = requests.get(url+"&limit=1") 
    valoresTemp = json.loads(r.text)
    #print(valoresTemp)
    
    print("Cantidad de registros:",valoresTemp["paging"]["total"])
    
    TotalRegistros=valoresTemp["paging"]["total"]
    #TotalRegistros=1
    RegistroActual=0
    valores=[]
    datosMetricas=[]
    Atributos=[]
    SuperficieCubierta=-1
    SuperficieTotal=-1

    while RegistroActual<(TotalRegistros+50):
        #url2="https://api.mercadolibre.com/sites/MLA/search?city=TUxBQ0FWRTc5OTQ1&category=MLA1466&state=TUxBUEdSQXJlMDNm&neighborhood=TUxBQlNBUjkwMDVa&offset="+str(RegistroActual)+"&limit=50"
        url2=url+"&offset="+str(RegistroActual)+"&limit=50"
        
        #url="https://api.mercadolibre.com/sites/MLA/search?neighborhood=TUxBQlNBUjkwMDVa&category=MLA1466&offset="+str(RegistroActual)+"&limit=50"  esto no funca
        
        print(url2)
        r = requests.get(url2)
        DocumentoCompleto = json.loads(r.text)
        
        
        try:
            for elemento in DocumentoCompleto['results']:
                #print("Elemento:",elemento)
                print("###################################################################")
                print("id:",str(elemento['id']))
                IdPublicacion=str(elemento['id'])
                print("descripcion:",str(elemento['title']))
                Descripcion=str(elemento['title'])
                print("Este es el precio:",str(elemento['price']))
                Precio=str(elemento['price'])
                print("moneda:",str(elemento['currency_id']))
                Moneda=str(elemento['currency_id'])
                print("---------------------------------------------")
                print("ubicacion")
                print("latitud:",elemento["location"]["latitude"])
                Latitud=elemento["location"]["longitude"]
                print("longitud:",elemento["location"]["longitude"])
                Longitud=elemento["location"]["longitude"]
                print("domicilio:",elemento["location"]["address_line"])
                Domicilio=elemento["location"]["address_line"]
                print("zip_code:",elemento["location"]["zip_code"])
                CodigoPostal=elemento["location"]["zip_code"]
                print("barrio:",elemento["location"]["subneighborhood"])
                Barrio=elemento["location"]["subneighborhood"]
                print("Localidad:",elemento["location"]["neighborhood"]["name"],"(",elemento["location"]["neighborhood"]["id"],")")
                IdLocalidad=elemento["location"]["neighborhood"]["id"]
                print("Partido:",elemento["location"]["city"]["name"],"(",elemento["location"]["city"]["id"],")")
                IdPartido=elemento["location"]["state"]["id"]
                print("Provincia:",elemento["location"]["state"]["name"],"(",elemento["location"]["state"]["id"],")")
                IdProvincia=elemento["location"]["state"]["id"]
                print("Pais:",elemento["location"]["country"]["name"],"(",elemento["location"]["country"]["id"],")")
                IdPais=elemento["location"]["country"]["id"]

                for elemento2 in elemento["attributes"]:
                    print("---------------------------------------------------")
                    #print("nivel 2",elemento2)
                    print("id:",elemento2["id"])
                    print("name:",elemento2["name"])
                    print("value_name",elemento2["value_name"])
                    AtributoId=elemento2["id"]
                    AtributoName=elemento2["name"]
                    AtributoValue=elemento2["value_name"]
                    AtributosTemp=[IdPublicacion,AtributoId,AtributoName,AtributoValue]
                    Atributos.append(AtributosTemp)
                    if elemento2["id"]=="TOTAL_AREA":
                        print("value_name",elemento2["values"])
                        for elemento3 in elemento2["values"]:
                            if elemento3["struct"] is None:
                                SuperficieTotal=-1
                                SuperficieTotalUnidad=''
                            else:
                                #print(elemento3["struct"]["number"]) #valor de m2
                                SuperficieTotal=elemento3["struct"]["number"]
                                #print(elemento3["struct"]["unit"]) #unidad m2
                                SuperficieTotalUnidad=elemento3["struct"]["unit"]
                    if elemento2["id"]=="COVERED_AREA":
                        print("value_name",elemento2["values"])
                        for elemento3 in elemento2["values"]:
                            #print(elemento3["struct"]["number"]) #valor de m2
                            if elemento3["struct"] is None:
                                SuperficieCubierta=-1
                                SuperficieCubiertaUnidad=""
                            else:
                                SuperficieCubierta=elemento3["struct"]["number"]
                                SuperficieCubiertaUnidad=elemento3["struct"]["unit"]

                            #print(elemento3["struct"]["unit"]) #unidad m2
                
                datosMetricasTemp=[str(IdPublicacion),'Precio',str(Precio),Moneda]
                datosMetricas.append(datosMetricasTemp)
                datosMetricasTemp=[]
                
                valoresTemp2=[str(IdPublicacion), Descripcion, str(Precio), Moneda, str(Latitud), str(Longitud), Domicilio, 'prueba','prueba2', str(IdLocalidad), str(IdPartido), str(IdProvincia), str(IdPais), str(SuperficieTotal), str(SuperficieCubierta)]
                valores.append(valoresTemp2)
                valoresTemp2=[]
                #print(valores)
            insertarPublicaciones(valores)
            insertarMetricas_ML(datosMetricas)
            insertarAtributos_ML(Atributos)
            valores=[]
            datosMetricas=[]
            Atributos=[]
            
            print("RegistroActual:",RegistroActual,"Totalregistros:",TotalRegistros)
            RegistroActual+=50

        except:
            print("No se pudo ṕrocesar por exceder la cantidad")
            print("RegistroActual:",RegistroActual,"Totalregistros:",TotalRegistros)
            RegistroActual+=50
            
        #for elemento2 in elemento["location"]:
            
              
            #print("value_name",elemento2["value_name"])
            #atributos=json.loads(str(elemento2))
            #print(atributos)
            #print(elemento2["TOAL AREA"])
    # print(valoresTemp['neighborhoods'])
    # valores=[]
    # for elemento in valoresTemp['neighborhoods']:insert

    # mydb=conectardb()
    # mycursor = mydb.cursor()
    # sql = "DELETE FROM `Recolector`.`ML_Localidades`"
    # mycursor.execute(sql)
    # sql = "INSERT INTO `Recolector`.`ML_Localidades` (id,name) VALUES (%s,%s)"
    # mycursor.executemany(sql, valores)
    # mydb.commit()
    # print(mycursor.rowcount, "was inserted.",mycursor.lastrowid)    





########################################################################################################33
#       METRICAS

#insertarCategorias()

#insertarSettings()

######################################

#insertarProvincias()

######################################

# Provincias=['TUxBUE1FTmE5OWQ4','TUxBUEdSQXJlMDNm']
# for Provincia in Provincias:
#     insertarPartidos(Provincia)

######################################

# Partidos=["TUxBQ0FWRTc5OTQ1","TUxBQ0xVSjRiOWZh"] #Lujan de Cuyo y Avellaneda
#Partidos=["TUxBQ0xVSjRiOWZh"] #Lujan de Cuyo y Avellaneda
# for Partido in Partidos:
#     insertarLocalidades(Partido)

######################################
#insertarCasas()
######################################


# id	name
# MLA105179	PH
# MLA1466	Casas
# MLA1472	Departamentos
# MLA1475	Depósitos y Galpones
# MLA1493	Terrenos y Lotes
# MLA1496	Campos
# MLA1892	Otros Inmuebles
# MLA374730	Camas Náuticas
# MLA392265	Consultorios
# MLA50536	Tiempo Compartido
# MLA50538	Oficinas
# MLA50541	Cocheras
# MLA50544	Parcelas, Nichos y Bóvedas
# MLA50545	Fondo de Comercio
# MLA50547	Quintas
# MLA79242	Locales
TipoPropiedades=["MLA105179","MLA1466","MLA1472","MLA1475","MLA1493","MLA1496","MLA1892","MLA374730","MLA392265","MLA50536","MLA50538","MLA50541","MLA50544","MLA50545","MLA50547","MLA79242"]

# TUxBQkFWRTgzNjFa	Avellaneda
# TUxBQkNSVTgxNjFa	Crucesita
# TUxBQkRPQzIxMjJa	Dock Sud
# TUxBQkdFUjY5ODBa	Gerli
# TUxBQlBJ0Tg1NDla	Piñeyro
# TUxBQlNBUjkwMDVa	Sarandí
# TUxBQlZJTDM1OTha	Villa Domínico
# TUxBQldJTDg5NTda	Wilde
# TUxBQsFSRTc3Nzha	Área Cinturón Ecológico

Localidades=["TUxBQkFWRTgzNjFa","TUxBQkNSVTgxNjFa","TUxBQkRPQzIxMjJa","TUxBQkdFUjY5ODBa","TUxBQlBJ0Tg1NDla","TUxBQlNBUjkwMDVa","TUxBQlZJTDM1OTha","TUxBQldJTDg5NTda","TUxBQsFSRTc3Nzha","TUxBQkxVSjI3OTBa"]
#Localidades=["TUxBQkxVSjI3OTBa"]


#Insertar casas de Sarandi
#url="https://api.mercadolibre.com/sites/MLA/search?category=MLA1466&city=TUxBQ0FWRTc5OTQ1&state=TUxBUEdSQXJlMDNm&neighborhood=TUxBQlNBUjkwMDVa"
#ParsearPropiedades(url)

#Insertar PH de Sarandi
#TipoPropiedad="MLA105179"

#Provincia="TUxBUE1FTmE5OWQ4" #Mendoza
#Provincia="TUxBUEdSQXJlMDNm" #Buenos Aires sur
# Provincias=["TUxBUE1FTmE5OWQ4","TUxBUEdSQXJlMDNm"]

for Localidad in Localidades:
    datosGeo=ConsultarPorLocalidad(Localidad)
    Partido=datosGeo[1]
    Provincia=datosGeo[2]
    for TipoPropiedad in TipoPropiedades:
        url="https://api.mercadolibre.com/sites/MLA/search?category="+TipoPropiedad+"&city="+Partido+"&state="+Provincia+"&neighborhood="+Localidad
        ParsearPropiedades(url)

# for Provincia in Provincias:
#     for Partido in Partidos:
#         for Localidad in Localidades:
#             for TipoPropiedad in TipoPropiedades:
#                 url="https://api.mercadolibre.com/sites/MLA/search?category="+TipoPropiedad+"&city="+Partido+"&state="+Provincia+"&neighborhood="+Localidad
#                 ParsearPropiedades(url)

CalcularTotales()
#########################################################################################################3

#RegistroActual=100
#r = requests.get("https://api.mercadolibre.com/sites/MLA/search?attribute_id=OPERATION&attribute_value_name=Alquiler&category=MLA1466&offset=10&limit=1")
#r = requests.get("https://api.mercadolibre.com/sites/MLA/search?search_type=scan&category=MLA1466&domain=MLA-APARTMENTS_FOR_RENT&limit=1")
#r = requests.get("https://api.mercadolibre.com/sites/MLA/domains")
#r = requests.get("https://api.mercadolibre.com/sites/MLAdomains")
#r = requests.get("https://api.mercadolibre.com/sites/MLA/search?item_location=neighborhood_id:TUxBQlNBUjkwMDVa&category=MLA1466&limit=1")
#r = requests.get("https://api.mercadolibre.com/sites/MLA/search?attributes:OPERATION:Venta&category=MLA1466&limit=1")

#r = requests.get("https://api.mercadolibre.com/categories/MLA1459")



#r = requests.get("https://api.mercadolibre.com/sites/MLA/search?q=propiedades&FilterID=FilterValue&limit=1")

#print(r.text)

#&attributes={OPERATION,}
#&attributes={id,price,category_id,title}
#applied_filter_id%3DPROPERTY_TYPE%26applied_filter_name%3DInmueble%26applied_filter_order%3D2%26applied_value_id%3D242060%26applied_value_name%3DCasas%26applied_value_order%3D1%26applied_value_results%3D9373
#applied_filter_id%3DOPERATION%26applied_filter_name%3DOperación%26applied_filter_order%3D2%26applied_value_id%3D242073%26applied_value_name%3DAlquiler%26applied_value_order%3D1%26applied_value_results%3D9373



#r = requests.get('https://api.mercadolibre.com/users/me', headers={'Authorization': 'BEARER APP_USR-4019497100814564-x-81zwMaVb7bMjTv94T7EVlQ1v2CHtXtPl'})
#r = requests.get('https://api.mercadolibre.com/users/me', headers={'Authorization': 'BEARER 81zwMaVb7bMjTv94T7EVlQ1v2CHtXtPl'})
#r = requests.get('https://api.mercadolibre.com/items/MLA791791729')
#r = requests.get('https://api.mercadolibre.com/sites/MLA/categories')
#r = requests.get('https://api.mercadolibre.com/sites/MLA/search?item_location=lat:-34.6499114_-34.700734,lon:-58.3980469_-58.3363347&category=MLA1459&limit=2')

#https://api.mercadolibre.com/classified_locations/cities/$CITY_ID

#print(r.text)


#Id categoria inmuebles 
# detalles de categorias y atributos para inmuebles
#r=requests.get('https://api.mercadolibre.com/categories/MLA1459')
#print(r.text)





#Listado de provincias
#r = requests.get('https://api.mercadolibre.com/classified_locations/countries/AR')
#print(r.text)

#Listado de partidos de la provincia de Buenos aires
#r = requests.get('https://api.mercadolibre.com/classified_locations/states/TUxBUEdSQXJlMDNm') 
#print(r.text)

#Listado de ciudades del Partido de Avellaneda
#r = requests.get('https://api.mercadolibre.com/classified_locations/cities/TUxBQ0FWRTc5OTQ1') 
#print(r.text)

#Listado de Barrios de Sarandi (sarandi no tiene barrios)
#r = requests.get('https://api.mercadolibre.com/classified_locations/neighborhoods/TUxBQlNBUjkwMDVa')
#print(r.text)


#Busco por lat lon informadas en la busqueda por neighborhoods
#r = requests.get('https://api.mercadolibre.com/sites/MLA/search?item_location=lat:-34.6832581,lon:-34.6832581&category=MLA1459&limit=2')
#print(r.text)

#Busco casas que superen los 300m2
#https://api.mercadolibre.com/sites/MLA/search?city=TUxBQ0FWRTc5OTQ1&category=MLA1466&OPERATION=242075&TOTAL_AREA=300m%C2%B2-*&limit=1#json


#Busco las casas en venta en partido de avellaneda
#https://api.mercadolibre.com/sites/MLA/search?city=TUxBQ0FWRTc5OTQ1&category=MLA1466&OPERATION=242075&limit=1#json

#Buscar casas en Sarandi
#https://api.mercadolibre.com/sites/MLA/search?city=TUxBQ0FWRTc5OTQ1&category=MLA1466&OPERATION=242075&state=TUxBUEdSQXJlMDNm&neighborhood=TUxBQlNBUjkwMDVa&limit=1#json

#api.mercadolibre.com/sites/MLA/search?


#Buscar propiedades de sarandi
#r=requests.get('https://api.mercadolibre.com/sites/MLA/search?city=TUxBQ0FWRTc5OTQ1&category=MLA1459&limit=3')
#print(r.text)

#r=requests.get('https://api.mercadolibre.com/sites/MLA/search?city=TUxBQ0FWRTc5OTQ1&category=MLA1475&limit=50&q=ipod nano')
#print(r.text)
#r=requests.get('https://api.mercadolibre.com/sites/MLA/search?city=TUxBQ0FWRTc5OTQ1&category=MLA1459&limit=1')
#print(r.text)

#r=requests.get('https://api.mercadolibre.com/sites/MLA/search?city=TUxBQ0FWRTc5OTQ1&category=MLA1475&limit=1')
#print(r.text)



#r=requests.get('https://api.mercadolibre.com/sites/MLA/search?city=TUxBQlNBUjkwMDVa&category=MLA1459&limit=1')
#print(r.text)




# for elementoN1 in valoresTemp:
#     print("ElementoN1:",elementoN1)
#     if elementoN1=='children_categories':
#         print(elementoN1["name"])
    #print(elementoN1["name"])