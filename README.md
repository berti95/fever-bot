# Descipción:
Fever bot es un script programado en Python cuyo objetivo es hacer scrapping a la web de Fever.  Fue usado durante algo más de una año.

Sus principales objetivos eran:
- Mandar una notificación cuando había nuevos cupones.
- Obtener los datos de una manera ordenada con el fin de mostrar los datos en un mapa (carencia de Fever en aquel momento).

# Estado actual:
Fever actualmente muestra su planes mediante una API Rest con autenticación OAuth 2.
Con esta actualización el script ha dejado de funcionar.

La manera de acceder a los datos ahora es algo más compleja aunque por contra devuelve muchos más datos y de una manera estructurada que hace más sencillo su tratamiento posterior.

# Aspectos destacables:

El script presenta los datos en un calendario (.ics) con el fin de que otra aplicación pueda recogerlos. Antes se presentaban los datos en otros formatos (excel y organizados por carpetas).

El programa consta de dos metodos:
- Escaner_plan : Recoge el html .
- Extraer_datos : Recorre el html para obtener los datos y realizar la acción de notificar y guardar.

# Limitaciones:
Fever limitaba a un maximo de 700 peticiones/día/IP.
El script tiene un contador que para cuando llega al limite y continua al día siguiente.

# Uso:
Esta pensado para ser ejecutado de manera constante.
En un comienzo se ejecutaba en local y despues se paso a ejecutar en c9.io (en la nube) por una mayor comodidad.

Tras hacer scrapping sobre los planes de Fever se dejaba el archivo ics en una url.
Cada 30 minutos la web en la que se encontraba el mapa escaneaba en busca de nuevos planes y se añadian a la lista prestando especial interes en la ubicación y la fecha.

Se puede ver en http://www.mapa.cuponesfever.com/events/map

# Futuro:
No es necesario revisar todos los planes con la misma frecuencia (algunos no se actualizan desde hace dos años y otros mensualmente). Por ello siempre se quiso llevar una registro de la fecha en la que se debia de revisar cada plan:
- Si un plan no esta activo, cuanto más tiempo llevara inactivo menos frecuencia.
- Si un plan estaba activo revisarlo en su fecha de fin.
