# Descipción:
Fever bot es un script programado en Python cuyo objetivo obtener datos de la web de Fever.  Fue usado durante algo más de una año.

Sus principales objetivos son:
- Mandar una notificación cuando había nuevos cupones.
- Obtener los datos de una manera ordenada con el fin de mostrar los datos en un mapa (antigua carencia de Fever).

# Estado actual:

Hasta noviembre de 2016 (FeverScan_old.py) obteniamos los datos mediante scrapping. A partir de noviembre (FeverScan.py) Fever comenzo a usar una APIRest con autenticación Oauth2.

La consecuencia directa de este cambio es que no nos permitia seguir haciendo scrapping a los planes de tipo /p.

Pero esta nueva api cerro una ventana y nos abrio una puerta.

Podemos obtener el token que se esta utlizando para mostrar los datos en el html tomandolo desde el codigo js que usa.
Usando el token podemos hacer peticiones a la API directamente y obtener mucha más cantidad de los planes incluso antes de que estos sean activados.

Fever seguramente podria limitar esto utilizando tokens de un solo uso.


# Funcionalidad del codigo:

El script  detecta los planes que pueden contener cupones, crea un archivo html con su titulo y descripción, y lo envia a traves del bot de telegram incluso antes de que sea visible desde el navegador o la app.
Tambien verifica cuando tienen asistentes los planes que hemos clasificado como potenciales cupones, para avisarnos que dichos planes ya estan activos para todos.
El programa consta de dos metodos:
- LlamarApi: Realizar la peticion de todos los datos.
- NuevoToken: En caso de cambiar el token recupera el que Fever este usando en ese momento.
- LlamarURL: NuevoToken necesita visitar el html de un plan
- Cargar_numero_plan: Carga el ultimo plan visitado
- Guardar_numero_plan: Guarda el ultimo plan visitado

El script _old presentaba (actualmente no es operativo) los datos en un calendario (.ics) con el fin de que otra aplicación pueda recogerlos. Antes se presentaban los datos en otros formatos (excel y organizados por carpetas).
El programa consta de dos metodos:
- Escaner_plan : Recoge el html .
- Extraer_datos : Recorre el html para obtener los datos y realizar la acción de notificar y guardar.

# Limitaciones:
Fever limitaba a un maximo de 700 peticiones/día/IP. (Tanto mediante la api como mediante scrapping)
El script tiene un contador que para cuando llega al limite y continua al día siguiente.

# Uso:
Esta pensado para ser ejecutado de manera constante.
En un comienzo se ejecutaba en local y despues se paso a ejecutar en c9.io (en la nube) por una mayor comodidad.

Tras hacer scrapping sobre los planes de Fever se dejaba el archivo ics en una url.
Cada 30 minutos la web en la que se encontraba el mapa escaneaba en busca de nuevos planes y se añadian a la lista prestando especial interes en la ubicación y la fecha.

Se puede ver en http://www.mapa.cuponesfever.com/events/map (necesario introducir fecha de noviembre)

# Futuro:
No es necesario revisar todos los planes con la misma frecuencia (algunos no se actualizan desde hace dos años y otros mensualmente). Por ello siempre se quiso llevar una registro de la fecha en la que se debia de revisar cada plan:
- Si un plan no esta activo, cuanto más tiempo llevara inactivo menos frecuencia.
- Si un plan estaba activo revisarlo en su fecha de fin.
