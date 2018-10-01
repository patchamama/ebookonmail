# ebookonmail
Script que crea una base de datos única a partir de varias bases de datos de calibre y responde a peticiones de emails para enviar libros pedidos, por email.

La idea de este script es distribuir libros o información sin problemas de copyright, de distribución libre o con copyright vencido como la biblioteca Gutenberg.

Se genera un listado de libros en un documento excel que se puede distribuir a una lista de correo definida en emaillist.txt. En el archivo excel se especifica el listado de libros con un código y al pusarse en un libro para pedir, se abre el programa de correo por defecto y se especifica en el asunto el código del libro para ser solicitado y el formato, por ejemplo: GET EPUB GTB345 (solicita en formato Epub el libro con ID 345 en la biblioteca de código GTB -Gutenberg-).

# Probado
Sólo en GNU/Linux probado (debian/ubuntu).

# Para empezar
- Descarga y descomprime todo el contenido en una carpeta.
- Abrir archivo ebookonmail.py y definir todos los parámetros entre las líneas: "## init of definitions variable" y "## end of definitions variable", es decir, datos de acceso ftp para acceder a librerías de calibre (servidor, usuario y contraseña), cuenta de correo que se usará para chequear peticiones por email, ruta a librerías calibre en acceso ftp, nombre de la biblioteca...
- Crear/actualizar la base de datos resumen: # python ebookonmail.py -genlist -gentable
- Ejecutar script para chequear con peridiocidad peticiones, tal como un cronjobs (python ebookonmail.py). 
- Instalar calibre, libreoffice y kindlegen para las conversiones de formato (> mobi, epub, rtf...).

# Line commands
'#Enviar un email a cada dirección de email que aparecen en emaillist.txt con un excel que contiene un listado de los libros existentes en la base de datos resumen.
'# python ebookonmail.py -newsletter 

'#Actualizar y generar un listado de todos los libros en una tabla resumen
'# python ebookonmail.py -genlist -checkebooks -gentable 

'#Enviar novedades de libros nuevos del último mes de una determinada base de datos
'# python ebookonmail.py -sendnew [SEL|GTB|FBS]

'#Envía el listado completo de todos los libros a la lista de emails contenida en emaillist.txt (un email por línea)
'# python ebookonmail.py -sendfulllist

'#Genera un archivo html con todos los libros
'# python ebookonmail.py -gencalibrelist

# Built With
python 

# Authors
Armando Urquiola - https://github.com/patchamama

# License
ebookonmail is licensed under the MIT License, see the LICENSE.md file for details.
