# -*- coding: utf-8 *-*

#USAR EN PYTHON3

import urllib.request
import os
import operator
import sys #Es necesario para detener el programa
import time #Para mostrar en que momentos estamos
import smtplib #necesaria para mail
import telebot #necesario para telegram
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller
#Mensaje antiguo  --> 224218425
def requestp(url,proxyuse=True):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    headers = {'User-Agent' : user_agent}
    if proxyuse:
        #No esta activada esta función
        proxy = urllib.request.ProxyHandler({"http" : "127.0.0.1:8118"})
        opener = urllib.request.build_opener(proxy)
        opener.addheaders = [('User-agent', user_agent)]
        urllib.request.install_opener(opener)#si esta linea esta comentada, no utilizará TOR
        html=opener.open(url)
    else:
        req = urllib.request.Request(url,headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read()
    return html
def renew_connection(): #mejor no hacerlo mucho, ralentiza el proceso
    with Controller.from_port(port = 9151) as controller:
        controller.authenticate(password = 'wordref')
        controller.signal(Signal.NEWNYM)

#Cargamos valor del tipo p
infile = open('ultimo_m.txt', 'r')
numplan_m = int(infile.readline())
infile.close() #CERRAMOS
#Forzamos que elija nuestro plan
#Planes de ejamplo
#Español --> 49989 , Londres --> 50253 , Gratis-->50223, NuevaYork --> 51610, España con from --> 51606, euros en nombre_plan--> 49991
TOKEN = 'Introduce tu token de telegram' 



#Creamos el archivo de ics y añadimos la primera linea --> Necesario en la primera vez
    #Ya creado
#ics = open("mi_ics.ics", 'a')
#ics.write("BEGIN:VCALENDAR"+"\n")
#ics.write("X-WR-TIMEZONE:Europe/Madrid"+"\n")
#ics.close() #CERRAMOS

#Inicializamos varible
planes_vacios=0
#numero_de_preticiones
numero_de_peticiones=0
#Contador de planes correctos
escaneados=0
#Avisamos comiezo
print("Empezamos por el plan "+str(numplan_m))

def extraer_datos(numplan_m,soup):
    #VARIABLES A USAR:
        ### plan_titulo --> Titulo del plan
        ### plan_es_secret --> Si el plan es secret o no
        ### plan_es_sorteo --> Si el plan tiene un sorteo o no
        ### plan_es_multiple --> Tiene más de un horario al día (en general)
        ### plan_es_gratis --> Devuelve si el plan es gratis
        ### plan_es_euros --> Devuelve si el plan esta en euros
        ### plan_es_libras --> Devuelve si el plan esta en libras
        ### plan_es_dolares --> Devuelve si el plan esta en dolares
        ### plan_direccion --> Direccion del plan
        ### plan_precio --> Es cuanto cuesta el plan (en general)
        #######PENDIENTE
        ##Plan activo,  pais, precio, varios_planes, ultima fecha visitado

        ####Desgranamos lo que queremos obtener####
        ###Extraemos el titulo del plan
        plan_titulo = str(soup.find_all("div",{"id":"info"})[0].find_all("h1",)[0]).replace("<h1>","").replace("</h1>","")
        ###Vemos si es es un plan secret
        plan_es_secret = False
        secret_direccion=str(soup.find_all("div",{"class":"place"})[0].find_all("span",{"class":"address"})[0]).split(", ")
        secret_campos=len(secret_direccion)
        secret_ciudad=secret_direccion[secret_campos-1].replace("</span>","").replace(" ","")
        #if str(ciudad)=='<spanclass="address">Secret':
        if str(secret_ciudad)=='<spanclass="address">Secret':
            plan_es_secret = True
        ###Vemos si hay un sorteo
        plan_es_sorteo = False
        sorteo_en_descripcion=str(soup.find_all("div",{"class":"text"}))
        if "sorteo" in sorteo_en_descripcion or "concurso" in sorteo_en_descripcion:
            plan_es_sorteo = True
        ###Obtenemos la direccion del plan
        plan_direccion=str(soup.find_all("div",{"class":"place"})[0].find_all("span",{"class":"address"})[0]).replace("<span class=\"address\">","").replace("</span>","")
        ###Obtenemos si hay varios planes, el pais y el precio
        #Vemos si el plan es multimple (Generico)
        plan_es_multiple = False
        multiple_preciofrom = str(soup.find_all("div",{"id":"info"})[0].find_all("span",{"class":"price"})[0])
        if "From " in multiple_preciofrom:
            plan_es_multiple= True
        #Unificamos tanto el tipo multiple como el normal para realizar las siguientes operaciones
        precio_simplificado = multiple_preciofrom.replace("From ","")
        #Iniciamos las variables True/False de gratis, euros, dolares...
        plan_es_gratis = False
        plan_es_euros = False
        plan_es_libras = False
        plan_es_dolares = False
        #Obtenemos si el plan es gratis
        if "Free" in precio_simplificado:
            plan_es_gratis = True
            plan_precio = 0
        if "None" in precio_simplificado:
            plan_es_gratis = True
            plan_precio = 0
        #Obtenemos si el plan es en euros
        if "€" in precio_simplificado:
            plan_es_euros = True
            plan_precio_split=precio_simplificado.split("€")
            plan_precio = plan_precio_split[0].replace("<span class=\"price\">\n                    ","")
        #Obtenemos si el plan esta en libras
        if "£" in precio_simplificado:
            plan_es_libras = True
            plan_precio_split=precio_simplificado.split("£")
            plan_precio=plan_precio_split[1].replace("\n                </span>","")
        #Obtenemos si el plan esta en dolares
        if "$" in precio_simplificado:
            plan_es_dolares = True
            plan_precio_split=precio_simplificado.split("$")
            plan_precio=plan_precio_split[1].replace("\n                </span>","")


        ###Hemos acabado las busquedas y creamos la url para presentarlo

        plan_url = "http://fvr.to/m/"+str(numplan_m)+"/"

        ###Comenzamos a obtener todas las distintas fechas con sus planes




        #####AQUI COMIENZA EL CODIGO PARA OBTENER LA FECHA#####
        #Comenzamos obteniendo las distintas lineas de fecha
        #todas_fechas=str(soup.find_all("div",{"id":"dates"})[0].find_all("select",{"id":"date_selector"})[0]).splitlines()
        todas_fechas=str(soup.find_all("div",{"id":"sessions"})[0]).splitlines()
        ###todas_fechas = str(soup.find_all("div",{"id":"choices"}))
        #Obtenemos el numero de lineas para hacer el while, tenemos que quitar dos por los select del codigo
        ##Empezamos desde la linea 3
        cantidad_fechas = len(todas_fechas)-2
        i=3
        while i < cantidad_fechas:
            #Antiguo solo dia linea=todas_fechas[i].replace("<option value=\"","").split("\">")
            #Primero separamos en numero y descripcion y despues analizamos por separado
            linea=todas_fechas[i].split("\">")
            plan_numero=linea[0].replace("<li class=\"choice date_","").replace("style=\"display:none;","").replace("\"","")
            plan_descripcion=linea[1].replace("</li>","").replace("€","")
            #print(plan_numero)
            if plan_es_multiple == False:
                print(plan_descripcion+" Precio:"+str(plan_precio))
            #print(plan_descripcion)
            #print(plan_direccion)
            
            
            print("Plan"+str(i))
            
            print(plan_numero)
            print(plan_descripcion)
            print(str(numplan_m))
            print(plan_direccion)
            
            #Comenzamos a crear el ics
            ics = open("mi_ics.ics", 'a') #ABRIMOS
            ics.write("BEGIN:EVENT"+"\n")  #Inicializamos el evento
            ics.write("DTSTART;TZID=America/New_York:20"+plan_numero+"T193000"+"\n")
            ics.write("DTEND;TZID=America/New_York:20"+plan_numero+"T194000"+"\n")
            ##OLD  ics.write("SUMMARY:"+plan_descripcion+"\n")
            ics.write("SUMMARY:"+plan_titulo+"\n")
            ##OLD  ics.write("DESCRIPTION:"+str(numplan_m)+"\n")
            ics.write("DESCRIPTION:Sesion: "+plan_descripcion+"<!--more--> <br>Mucha más info en: <a href=\""+plan_url+"\">"+plan_url+"</a>\n")
            ics.write("LOCATION:"+plan_direccion+"\n")
            ics.write("END:EVENT"+"\n")  #Cerramos el evento
            ics.close() #CERRAMOS
            
            #Fin lineas para calendario
            i=i+1
        
        #Recorremos todas las fechas

        if plan_es_sorteo == True:
            ciudad_sorteo = ""
            if plan_es_libras == True:
                ciudad_sorteo = "Londres "
            if plan_es_dolares == True:
                ciudad_sorteo = "New York "
            if plan_es_euros == True:
                ciudad_sorteo = "España "
            print("Sorteo en:"+ciudad_sorteo+str(numplan_m))
            tb = telebot.TeleBot(TOKEN) 
            tb.send_message("@fevbot","Posible sorteo o concurso: "+ciudad_sorteo+plan_url)

        if plan_es_secret == True:
            print("--------PLAN SECRETO ENCONTRADO--------"+str(numplan_m))
            ##Escribir en el archivo de secrets
            f = open("Secret_m.txt", 'a')
            f.write(plan_url+"\r\n")
            f.close
            #Destruya numeros anteriores para no repetir mensajes de secret
            f = open("ultimo_m.txt", 'w')
            f.write(str(numplan_m+1)+"\r\n")
            f.close
            #Mensajito por telegram
            tb = telebot.TeleBot(TOKEN) 
            tb.send_message("@fevbot", plan_url) # Ejemplo tb.send_message('109556849', 'Hola mundo!')


def escanear_plan(numplan_m,):
    global numero_de_peticiones
    numero_de_peticiones= numero_de_peticiones +1
    print ("Peticion numero:"+str(numero_de_peticiones)+" - "+time.strftime("%X") )
    try:
        url="http://fvr.to/m/"+str(numplan_m)+"/"
        html=requestp(url,False)
        soup = BeautifulSoup(html, 'html.parser')
        return soup;

    except urllib.error.HTTPError:
        soup = "null"
        return soup


verdadero=False
while True:

    ####Mostramos el estado del bot: Plan, tiempo de espera y hora actual####
    print(str(numplan_m)+" Esperando 30s "+time.strftime("%X"))

    ####Guardamos 30 segundos por restricciones de servidor####
    time.sleep(30) # Con 60 aguanta 700 planes
    ###Paramos a los 700 que es el limite
    if numero_de_peticiones%700==0:
        print(time.strftime("%X"))
        while ( "09:30:00" != time.strftime("%X") ):
            time.sleep(1) #No es lo mejor pero es lo más sencillo
        #Ahora duerme hasta las 9:30 
    ###Añadimos 10 minutos de descanso cada 100 planes --> NO necesario
    #escaneados = escaneados +1
    #if escaneados == 100:
    #    escaneados = 0
    #    print("####Durmiendo 10 min, plan: "+str(numplan_m))
    #    time.sleep(600)


    ##Llamamos a la funcion para sacar de la web
    soup = escanear_plan(numplan_m)


    if soup == "null": #En funcion de si da error al escanear la web
        print("ATENCIÓN: ERROR CON PLAN"+str(numplan_m))
        time.sleep(30)
        planes_vacios = planes_vacios +1

        #Con la limitación de los 700 planes ya no es necesario.
        #if ( planes_vacios == 50 ):
            #time.sleep(3600)
            #planes_vacios = 0
            #numplan_m=numplan_m-50 #En lugar de usar un numero volvemos a sacar cual desde el archivo

            #tb = telebot.TeleBot(TOKEN) 
            #tb.send_message("@fevbot", "C9, volviendo a plan" +str(numplan_m)+" "+time.strftime("%X"))
    else:
        ##Llamamos a la funcion para desgranar##
        extraer_datos(numplan_m, soup)
		
        #Guardamos cada 10 planes para saber desde cual volver a empezar
        if operator.mod(numplan_m,20)==0: #20 en lugar de 100 - Decicimos no saturar tanto los servers de fever
            print("Tipo M "+str(numplan_m)+" "+time.strftime("%H:%M:%S"))
            f = open("ultimo_m.txt", 'w')
            f.write(str(numplan_m)+"\r\n")
            f.close
        else:
            f = open("ultimo_m.txt", 'a')
            f.write(str(numplan_m)+"\r\n")
            f.close
    
    numplan_m=numplan_m+1
   


        