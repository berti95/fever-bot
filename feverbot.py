# -*- coding: iso-8859-15 -*-

##TO-DO:Aceptar al leer caracteres que representan iconos
#No es un problema porque alerta sin problemas pero despues se cierra
#Solo da error en planes aislados

import urllib.request
from bs4 import BeautifulSoup #Para LlamarURL
import telebot #necesario para telegram
from telebot import types # Tipos para la API del bot.
import time #Necesario para hacer esperas

def LlamarAPI(url,headers): 
    req = urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read()
    return html

def LlamarURL(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    headers = {'User-Agent' : user_agent}

    req = urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read()

    return html

#Aparentemente no es necesario, hace bastante que Fever no cambia el Token
##No devuelve el token, edita el archivo donde se guarda el token
def NuevoToken():
    try:
        #Comenzamos a estudiar el html del plan
        numero_plan = cargar_numero_plan()
        url="http://fvr.to/m/"+ str(numero_plan)+"/"
        html=LlamarURL(url)
        soup = BeautifulSoup(html, 'html.parser')
        soup = str(soup).split("</div>")[1].split("</script>")[2].replace("<script src=\"","").replace("\">","")
        js_url = "http://fvr.to"+soup

        try:
            req = urllib.request.Request(js_url)
            response = urllib.request.urlopen(req)
            #Es importante hacer justo este encoding para aceptar el simbolo del euro
            respuesta = str(response.read(),'cp850')
            #ESTA INFORMACION NO ES EL ULTIMO PLAN
            token_nuevo = respuesta.split("{method:\"GET\",mode:\"cors\",headers:{\"Accept-language\":y(window.navigator.language),Authorization:\"")[1].split("\",Screen:\"android@xhdpi\"")[0].replace("\n","")
            #Guardamos el nuevo token
            print ("Hemos actualizado el token")
            f = open("token.txt", 'w')
            f.write(str(token_nuevo))
            f.close

        except urllib.error.HTTPError:
            print("Error en js al buscar el token")
            exit()
    except urllib.error.HTTPError:
        soup = "null"
        #return soup
        print("Error general al buscar el nuevo token")
        exit()

def cargar_numero_plan():
    #Cargamos el numero de plan por el que vamos
    ##Devuelve: Numero de ultimo plan
    infile = open('ultimo_plan.txt', 'r')
    numero_plan = int(infile.readline())
    infile.close()
    return numero_plan

def guardar_numero_plan(numero_plan):
    #Guardamos el numero de plan por el que vamos
    ##No devuelve nada
    ##No es necesario tratamiento de errores
    f = open("ultimo_plan.txt", 'w')
    f.write(str(numero_plan))
    f.close()




numero_plan = cargar_numero_plan()
contador = 0;
#Lo utilizamos para contar cuantos planes no estan operativos
planes_ko= 0;

#Clave de Telegram
TOKEN_TELEGRAM = 'Tienes que poner la tuya'


verdadero=False
while True:
    try:




        #Recibimos la url
        url="http://fvr.to/api/4.0/plans/"+ str(numero_plan)+"/"
        #Obtenemos el Token guardado
        infile = open('token.txt', 'r')
        token = str(infile.readline())
        infile.close()
        #Anadimos el token a la llamada
        headers = dict([('Authorization', token)])
        #Llamamos a la api
        html=LlamarAPI(url,headers)
        html = html.decode("utf-8")  #Mediante esto transformamos el formato
        
        #Contamos cuantos planes lleva visitados
        contador = contador +1 
        #Imprimimos estado del sistema
        print("Escaneando el plan: " + str(numero_plan)+"  Llevamos: "+str(contador)+" planes")
        #Esperamos 3 segundos para no sobrecargar y ver los resultados tranquilamente
        time.sleep(3)
        ###El modo de obtener los datos no es el optimo pero al no haber cambios y ser pocos los campos necesarios es suficiente
        #Obtenemos categoria
        categoria = html.split("category\":")[1].split(",\"cover_image")[0].replace("\"","")
        #Obtenemos descripcion
        descripcion = html.split("description\":\"")[1].split("\",\"hashtags")[0].replace(u"\u2022", "*").replace("\\r\\n","<br>")
        #Obtenemos el titulo
        titulo = html.split("name\":\"")[1].split("\",\"category")[0]        
        #Obtenemos si es secret
        secret_ciudad = html.split("place")[1].split("city")[0]
        plan_es_secret = False
        #print(secret_ciudad)
        if "Secret" in secret_ciudad:
            plan_es_secret = True
        if plan_es_secret == True :

            #Añadimos el plan a vigilancia si esta activo
            f = open("planes_vigilados.txt", 'a')
            f.write(str(numero_plan)+"\n")
            f.close

            #Mostramos estado por consola
            print("--------PLAN SECRETO ENCONTRADO-------- "+str(numero_plan))
            #Avisamos la creacion del nuevo plan
            tb = telebot.TeleBot(TOKEN_TELEGRAM) 
            tb.send_message("TU BOT DE TELEGRAM", "Posible nuevo cupon: \n http://fvr.to/m/"+str(numero_plan)+"/")
            #Mandar el archivo
            ##Creamos el archivo html para mandar por telegram
            filename= "mandar_telegram/"+str(numero_plan)+".html"
            f = open( filename, 'w')
            f.write("<!DOCTYPE html>")
            f.write("<h1>"+titulo+"</h1>")
            f.write(descripcion)
            f.close()
            #Enviamos el archivo
            doc = open("mandar_telegram/"+str(numero_plan)+".html", 'rb')
            tb = telebot.TeleBot(TOKEN_TELEGRAM) 
            tb.send_document("TU BOT DE TELEGRAM", doc)
            doc.close     
            #exit()
        print(categoria)    #Lo imprimimos para tener un feedback
        guardar_numero_plan(numero_plan)
        #Pasamos a escanear el siguiente plan
        numero_plan = numero_plan +1
        #Ponemos el contador de planes_ko a 0, si hemos pasado por aquí. Seguro que hemos podido leer el plan
        planes_ko = 0







    except urllib.error.HTTPError:


        #Contamos cuantos errores de este tipo van para ver si el problema esta en el token o simplemente el plan esta ko
        planes_ko = planes_ko +1
        print("Plan: "+str(numero_plan)+" esta KO")
        time.sleep(30)
        numero_plan = numero_plan +1
        if planes_ko == 20 :  #Solo recargamos el token si llevamos 10 SEGUIDOS mal


            ####Comprovamos si nuestros planes vigilados han sido activados
            ##Vamos linea por linea viendo si ha sido activado
            ##TO-DO: El tratamiento del archivo no es el mas optimo pero es un archivo muy pequeno
            # abrimos el archivo solo de lectura
            f = open("planes_vigilados.txt","r")
            # Creamos una lista con cada una de sus lineas
            lineas = f.readlines()
            # cerramos el archivo
            f.close()
            # abrimos el archivo pero vacio
            f = open("planes_vigilados.txt","w")
            # recorremos todas las lineas
            for linea in lineas:

                try:
                    #Recibimos la url
                    print(str(linea).replace("\n",""))
                    url="http://fvr.to/api/4.0/plans/"+ str(linea).replace("\n","")+"/"
                    #TO-DO: Usar los metodos para llamar a la API que ya teniamos
                    ##TO-DO:Necesitariamos volver a recoger el Token pero al no haber cambios en los ultimos meses no es un problema
                    token ="- - - - - - - - " 
                    headers = dict([('Authorization', token)])
                    #Llamamos a la api
                    html=LlamarAPI(url,headers)
                    html = str(html)
                    asistentes = html.split("people_attending\":")[1].split(",\"friends_attending")[0].replace("\"","")
                    print(asistentes)
                    # miramos si el contenido de la linea es diferente a la linea a eliminar
                    # añadimos al final \n que es el salto de linea
                    if int(asistentes) <20: #TO-DO: Ahora Fever genera planes con menos asistentes
                        # Si no es la linea que queremos eliminar, guardamos la linea en el archivo
                        f = open("planes_vigilados.txt", 'a')
                        f.write(linea)
                        f.close()
                    else:
                        print("El plan: http://fvr.to/m/"+str(linea)+"/ ha sido activado y ya tiene "+asistentes+" asitentes")
                        tb = telebot.TeleBot(TOKEN_TELEGRAM) 
                        tb.send_message("TU bot de TELEGRAM", "El plan: http://fvr.to/m/"+str(linea)+" ha sido activado y ya tiene "+asistentes+" asitentes")

                except urllib.error.HTTPError:
                    print("Error con busqueda de planes activos")


            #Comprobamos si el ultimo plan (el guadado en ultimo_plan) funciona para ver si es de la Token o no
            try:
                #Obtenemos el numero de plan que necesitamos
                numero_plan = cargar_numero_plan()
                #Damos formato a la url a acceder
                url="http://fvr.to/api/4.0/plans/"+ str(numero_plan)+"/"
                html=LlamarAPI(url,headers)
                #Si el token fuciona seguimos aquí
                print("PLAN VACIO DETECTADO: Esperando 30min " +time.strftime("%X"))
                planes_ko = 0
                print("Volvemos al plan:"+str(numero_plan))
                time.sleep(1800)
            except urllib.error.HTTPError:
                #Solo llegaremos aqui si el token no funciona
                print("Nuevo token necesario " +time.strftime("%X"))
                NuevoToken()
                tb = telebot.TeleBot(TOKEN_TELEGRAM) 
                tb.send_message("@fevbot", "ACTUALIZANDO SALUDO :)")
                time.sleep(1800) #Esperamos 30 minutos