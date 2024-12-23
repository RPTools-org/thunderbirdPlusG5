# Thunderbird+G5 para Thunderbird 115 y 128 ESR

* Autores: Pierre-Louis Renaud (de Thunderbird 78 a 115) & Cyrille Bougot (TB 102), Daniel Poiraud (de TB 78 a 91), Yannick (TB 45 a 60);
* URL: [Página de inicio de los complementos thunderbird+ G5 y G4][4];
  [Historial de cambios y complementos de documentación][5];
  [Contacto][6];
* Instalación: menú NVDA / Herramientas / Tienda de Complementos / pestaña Complementos disponibles o Complementos actualizables;
* Descargar: [Última versión en RPTools.org][3];
* Compatibilidad con NVDA: 2021.1 en adelante;
* [Código fuente en GitHub][2]


## Introducción
Thunderbird+G5 es un complemento para NVDA que aumenta significativamente la eficiencia y la comodidad al usar el cliente de correo electrónico Mozilla Thunderbird 115.

Mejora tu productividad al proporcionar órdenes que no existen de forma nativa en Thunderbird:

* Atajos de teclado para acceso directo a las carpetas en vista de árbol, a la lista de mensajes y al panel de vista previa.
* Una navegación sin desvíos entre los paneles de la ventana principal utilizando las teclas Tab y Escape.
* Atajos directos para la  consulta y la copia de los campos de la lista de mensajes y de las cabeceras del mensaje en el panel de vista previa sin cambiar el foco.
* Un acceso directo a los adjuntos.
* Atajos directos para la consulta y el acceso directo a  los campos de dirección de la ventana de Escribir.
* Una gran mejora en el uso del diálogo de Revisar ortografía.
* Una gestión más sencilla de libretas de direcciones y listas de correo (v.2402.14.00).
* Un menú de actualización del complemento (v.2402.14.00)
* Y muchas otras cosas más... 

Esta página documenta los atajos de teclado propuesto por Thunderbird+G5. 

La mayoría de estos atajos de teclado se pueden configurar a través del menú de NVDA / Preferencias / Gestos de Entrada / categoría thunderbirdPlusG5 para Thunderbird 115

## Navegación en la ventana principal

Nota: La tecla nombrada (tecla encima de Tab) en el resto de esta página designa la tecla ubicada debajo de Escape, encima de Tab y a la izquierda del número 1. Su fraseología varía según el idioma del teclado.

### Atajos generales
* (tecla encima de Tab): muestra el menú de varias órdenes para el complemento.
* Shift+(tecla encima de Tab): muestra el menú de opciones del complemento.
* F8 para activar o desactivar el panel de mensajes de vista previa: esta órden es verbalizada por el complemento.
* Control+F1: muestra esta página. Para algunas aclaraciones puedes [visitar la documentación de la versión4][7];

### Navegación entre los paneles de la ventana principal
Estos atajos se refieren a las carpetas en vista de árbol, a la lista de mensajes y al panel de mensajes de vista previa.

* Control+(tecla encima de Tab): Una pulsación coloca el foco en la lista de mensajes, dos pulsaciones coloca el foco en la lista de mensajes y luego selecciona el último mensaje.
* Alt+c : muestra el menú de cuentas y luego el menú de carpetas de la cuenta elegida. Desde la versión 2312.14, soporta el modo "Carpetas unificadas" de las carpetas en vista de árbol.
* Control+Alt+c : muestra el menú de cuentas y luego el menú de carpetas no leídas para la cuenta elegida. (2023.11.15)
* Tab: va al siguiente panel, sin desvío.<br>
Nota: estos dos últimos atajos se pueden modificar o intercambiar a través del cuadro de diálogo Gestos de Entrada.
* alt+Inicio: 1 pulsación selecciona la carpeta actual en las carpetas en vista de árbol, 2 pulsaciones muestra un menú que te permite elegir la cuenta de correo electrónico  para llegar a la vista de árbol.
* Control+Alt+Inicio: Lo mismo pero para carpetas con mensajes no leídos. (2023.10.31)
* Tab: lleva el foco al siguiente panel y en particular:<br>
 Desde la lista de mensajes y si se muestra el panel de vista previa: Una pulsación: lleva el foco al cuerpo del mensaje, Dos pulsaciones: lleva el foco al banner de botones de respuesta y cabeceras del mensaje. (v.2404.23) 
* Escape: vuelve al panel anterior, sin desvío. 
Escape también te permite alternar entre las carpetas en vista de árbol y la lista de mensajes. 
* Shift+Tab: su comportamiento nativo se ha conservado en esta versión.

### Navegación por pestañas en la ventana principal

* Control+Tab con o sin la tecla Mayúscula y Control+1 a 9: el complemento intercepta los cambios de pestaña para anunciar su número de órden y el número total de pestañas.<br>
Además, el complemento da el foco al contenido de la pestaña cuando se activa por primera vez. Para la primera pestaña, el foco se puede llevar al último mensaje de la lista de mensajes o al primer mensaje no leído. A través del menú de opciones / Opciones para la ventana principal, puedes marcar la opción titulada: Acceder al primer mensaje no leído al activar por primera vez la primera pestaña; de lo contrario, al último mensaje. (v.2402.14.00);
* Control+la primera tecla a la izquierda de Retroceso: muestra un menú con la lista de pestañas existentes. Pulsa Intro en un elemento del menú para activar la pestaña correspondiente.
* Alt+la primera tecla a la izquierda de la tecla de Retroceso: muestra el menú contextual de la pestaña. Este menú es nativo de Thunderbird.

Nota: La etiqueta de la primera tecla a la izquierda de Retroceso varía según el idioma del teclado.

## Lista de mensajes
<!-- begin 2023.11.10 -->

### Verbalización personalizada de líneas  (2023.11.10)

Este modo personalizado, desactivado por defecto, permite escuchar más cómodamente las líneas de la lista de mensajes.

Puedes activar este modo pulsando shift+ordinal y seleccionando en  l menú el elemento "Opciones para la ventana principal" y luego "Lista de mensajes". En la lista de opciones, marcar la opción "Lista de mensajes: Verbalización personalizada de líneas";

Esta lista de opciones también contiene otras opciones de personalización que solo funcionan si la verbalización personalizada está habilitada.

* La columna "Estado de lectura" anuncia "No leído" no anuncia el estado "Leído";
* La columna "Estado", recomendado, anuncia los estados "Nuevo", "Respondido" y "Transferido".<br>
Nota: Si pulsas la letra "m" para revertir el estado del mensaje, esta columna debe estar presente en la lista de mensajes para que se anuncie el nuevo estado.
* El complemento garantizará que "No leído" solo se anuncie una vez y que "Leído" nunca se anuncie.

<br>
Lea también la sección [Elegir y organizar columnas](#cols) 

### Atajos para la lista de mensajes

<!-- end 2023.11.10 -->

* Tab si se muestra el panel de vista previa: una pulsación: lleva el foco al cuerpo del mensaje, dos pulsaciones: lleva el foco al banner de botones de respuesta y cabeceras del mensaje. (v.2404.23) 
* Escape en la lista de mensajes: si hay un filtro activo, se desactiva y la lista de mensajes permanece seleccionada. De lo contrario, este atajo da el foco en las carpetas en vista de árbol.
* NVDA+flecha arriba o NVDA+l (portátil) en la lista de mensajes:<br>
Una pulsación: anuncia la línea actual de la lista de mensajes. El atajo NVDA+Tab produce el mismo resultado pero sin usar este complemento.<br>
Dos pulsaciones: muestra los detalles de la línea en una ventana de texto que permite el análisis de la línea usando el teclado. A partir de la version 2404.23, esta trata de la línea original si la verbalización personalizada de líneas está activa.
* Control+flecha derecha en modo conversación grupal: selecciona el último mensaje de la conversación. Esto primero está expandido si está contraído. (2312.14.00)
* Control+flecha izquierda en modo conversación grupal: selecciona el primer mensaje de la conversación. Esto primero está expandido si está contraído.<br>Estos dos últimos atajos necesitan la columna "Total" para funcionar.
* Espacio, F4 o Alt+flecha abajo: lectura de una versión depurada o traducida del mensaje en el panel de vista previa, sin salir de la lista de mensajes.<br>
Nota: Si un mensaje contiene más de 75 elementos HTML, se emitirá un pitido por cada elemento de texto recuperado. Con solo pulsar la tecla Control, se puede comenzar a anunciar inmediatamente el mensaje incompleto. (2401.09.0)
* Bloq Despl: Activa o desactiva el modo de traducción de mensajes para una lectura rápida con Espacio, F4 o Alt+flecha abajo. Tenga en cuenta que el complemento Instant Translate debe estar instalado y activado. (2401.02.0)
* Shift+Bloq Despl: Activa o desactiva la visualización de la traducción en una ventana de texto consultable. Este modo permite leer el mensaje completo en Braille.  (2401.02.0)<br>
Nota: La traducción de mensajes también está disponible en ventanas y pestañas que muestran un mensaje.
* Alt+flecha arriba: coloca el mensaje en el Navegador de citas virtual;<br>
* Windows+flecha abajo o arriba: lectura de la cita siguiente o anterior. Si el modo de traducción está activo, la cita se traducirá. 

Nota: Este navegador de citas se puede utilizar desde la lista de mensajes, desde el mensaje de la ventana separada de lectura, desde la Ventana de Escribir y desde el diálogo de Revisar ortografía.

### Anuncio, deletreo y copia de los campos de la lista de mensajes

Cada fila de la lista se divide en varios campos correspondientes a las columnas. Se puede comparar un campo con una celda en una tabla de Excel.

Los atajos siguientes se pueden realizar sin cambiar el foco:

* número 1 al 9 de la fila encima de las letras: con el número correspondiente a la fila de la columna de la lista de mensajes, están disponibles las siguientes acciones:<br>
Una pulsación: anuncia el valor del campo. Por ejemplo, dependiendo del orden de sus columnas, 1 anuncia el remitente y 2 anuncia el asunto.<br>
Dos pulsaciones: deletrea el valor del campo.<br>
Tres pulsaciones: copia el valor del campo al portapapeles.

Consejo: Si utilizas varias carpetas, aplica el mismo orden de columnas a todas estas,, de esta forma siempre corresponderá un número a la misma columna.

### Anuncio y copia de cabeceras del panel de vista previa o de la ventana separada de lectura
* Alt+1 a Alt+6 desde la lista y la ventana separada de lectura:<br>
Una pulsación anuncia el valor de la cabecera,<br>
Dos pulsaciones abre un cuadro de edición que contiene el valor de la cabecera. Al cerrar este cuadro de diálogo con Intro, este valor se copia al portapapeles, lo que resulta muy práctico para recuperar la dirección de correo electrónico de un correspondiente.<br>
Tres pulsaciones abre el menú contextual de la cabecera correspondiente. Este es un menú nativo de Thunderbird.

### Panel de adjuntos en la ventana principal y la ventana separada de lectura
Los siguientes atajos te permiten anunciar  los adjuntos, abrirlos o guardarlos.

* Alt+9 o Alt+Avance página:<br>
Una pulsación: indica el número de adjuntos y los nombres de todos los archivos adjuntos. (2312.18.00)<br>Si Thunderbird no muestra automáticamente el panel de archivos adjuntos, el complemento lo hará y Thunderbird seleccionará el primer archivo adjunto.<br>
Dos pulsaciones:<br>
Si solo hay un archivo adjunto, mueve el foco hacia él luego muestra su menú contextual.<br>
Si hay varios archivos adjuntos, selecciona el primero de la lista. (2312.18.00)

### Administrar etiquetas desde la lista de mensajes
Los atajos de abajo   permite administrar con verbalización las etiquetas sin tener que navegar por el menú contextual de Thunderbird.

* Shift+1 a Shift+9: Agrega y elimina las etiquetas con verbalización.
* Shift+0: Elimina todas las etiquetas del mensaje seleccionado.
* Alt+0: Anuncia todas las etiquetas del mensaje.

### Verbalización de los atajos a, c, j y m de la lista de mensajes

A partir de la versión 2023.11.10, el complemento ya no verbaliza estos atajos de marcado. NVDA anuncia inmediatamente el cambio en el contenido de la línea en cuestión.

### Filtrado rápido de mensajes (2023.11.10)

letra f: alternativa ergonómica a Control+Shift+K para mostrar o ir a la barra de filtrado rápido. Este atajo se puede configurar en el diálogo Gestos de Entrada.
<br>Nota: El foco debe estar en una lista de mensajes que no esté vacía. Pulsa Escape para desactivar el filtro activo.

Para acceder directamente a los resultados del filtrado desde el campo de entrada de palabras clave, pulsa flecha abajo.

Cuando un filtro está activo, se reproduce un sonido el cual se asemeja a una respiración cada vez que la lista de mensajes tiene el foco. Esto es especialmente útil cuando se cambia de ventana o pestaña y luego se regresa a la lista de mensajes.

Si este sonido te molesta tienes dos opciones:

1. Abra el menú Shift+ (tecla encima de Tab) y en el submenú de Desactivaciones, marque la opción:<br>
Lista de mensajes: no reproducir sonido cuando la lista se filtra y se enfoca.

2. Abra el menú Shift+ (tecla encima de Tab) luego pulse Intro en el elemento: Abrir carpeta de sonido. 
<br>Esta carpeta se abrirá en el Explorador de archivos,
<br>Allí encontrarás el archivo filter.wav.
<br>Puedes reemplazar este archivo por otro siempre que tu archivo tenga el mismo nombre: filter.wav.
<br>Una vez hecho esto, reinicia NVDA.

<!-- end 2023.10.31 -->

### Anuncio de la barra de estado e información de filtrado rápido
* Alt+fin o Alt+(segunda tecla a la izquierda de Retroceso): 
Desde la lista de mensajes o barra de filtrado rápido: anuncia el número total o el de los mensajes filtrados, el número de mensajes seleccionados si hay más de uno y la expresión del filtro si se ha definido un filtro. Esta información proviene de la barra de filtrado rápido y ya no de la barra de estado.<br>
Desde otra pestaña o ventana: anuncia la barra de estado.
* Cuando la lista de mensajes recibe el foco, se reproduce  un  sonido el cual se asemeja a una respiración cuando el filtrado rápido está activo.


### SmartReply: responda a las listas de correo con Control+R
Para responder a determinadas listas de correo es necesario pulsar Control+Shift+L. Para evitar responder al remitente equivocado, pulsar Control+R para responder a la lista y dos veces Control+R para responder en privado al remitente del mensaje. 

Nota: groups.io no se ve afectado por esta función.

<a name="cols">
<!-- begin 2023.10.31 -->

### Elegir y organizar columnas (2023.10.31)

Este procedimiento es nativo de Thunderbird 115 pero se explica aquí porque está mal documentado.

* Pulsar Shift+tab desde la lista de mensajes para colocarte en la lista de encabezados de columna.
* Utilice las flechas izquierda y derecha para seleccionar una columna.
* Cuando llegues a la columna especial "Seleccione las columnas que desea mostrar", pulse Intro sobre él.
* En el menú, marque o desmarque las columnas y luego pulsse Escape para cerrar este menú. 
* De vuelta en la lista de encabezados de columna, pulse  flecha izquierda para mover una columna.
* Luego pulse Alt+flecha izquierda o derecha para colocarlo en la ubicación deseada. Este será verbalizado correctamente.
* Repita estas operaciones para mover otras columnas.
* Cuando la organización de las columnas este terminada, pulse Tab para regresar a la lista de mensajes.

## Carpetas en vista de árbol: navegación rápida (2023.10.31)

Algunas órdenes muestran un menú que contiene carpetas en vista de árbol para permitir la navegación por letras iniciales. Por razones de rendimiento, el script no muestra subcarpetas de ramas contraídas.

Además, si el nombre de una cuenta o carpeta termina con un guión, no se incluirá en el menú de carpetas no leídas. 

Por lo tanto, es aconsejable excluir cuentas y carpetas cerrando ramas poco utilizadas o cambiando el nombre de las cuentas para añadir un guión al final de su nombre.

<br>
Desde la versión 2312.14.00, el modo "Carpetas unificadas" esta soportado. En este modo, es necesario que todos los nombres de cuentas contengan el carácter @. Para cambiar el nombre de una cuenta, selecciónela en la vista en árbol, pulse la tecla Aplicaciones y luego pulse Configuración en el menú contextual. Luego vaya con Tab al campo "Nombre de la cuenta".

### Órdenes disponibles en las carpetas en vista de árbol:

* NVDA+flecha arriba o NVDA+l (portátil): anuncia el nombre de la carpeta seleccionada. NVDA ya no lo hace por si solo.  
* Espacio en una carpeta no leída: coloca el foco en el primer mensaje no leído en la lista de mensajes.
* Tecla Intro o Alt+flecha arriba: muestra un menú de todas las carpetas de la cuenta a la que pertenece la carpeta seleccionada.
* Control+Intro o Alt+flecha abajo: muestra un menú de las carpetas no leídas para la cuenta a la que pertenece la carpeta seleccionada.
<br>En ambos casos, el último elemento del menú muestra el menú de las cuentas. Puedes pulsar la barra espaciadora para elegir una cuenta desde allí.
* Shift+Intro: muestra un menú que contiene todas las cuentas y carpetas en vista de árbol.
* Shift+Control+Intro: muestra un menú que contiene todas las cuentas y carpetas no leídas en vista de árbol.

Observaciones:

Para estas dos últimas órdenes, pasará algún tiempo antes de que se muestre el menú porque el script debe recorrer todo el árbol para crear el menú.

En su lugar, utilice uno de estos dos pequeños consejos:

1. Pulsar Alt+C para mostrar el menú de cuentas, 
<br>Elija una cuenta y luego pulsa Intro. 
<br>Se abrirá un nuevo menú que contiene las carpetas de esta cuenta y podrás usar una letra para activar una.
2. Pulsar Control+Alt+Inicio dos veces en sucesión rápida para mostrar el menú de cuentas con carpetas no leídas, 
<br>Elija una cuenta y luego pulsa Intro. 
<br>Se abrirá un nuevo menú que contiene las carpetas no leídas de esta cuenta y podrás usar una letra para activar una.

<!-- end 2023.10.31 -->

## Cerrar ventanas y pestañas
* La tecla Escape  te permite cerrar la ventana separada de lectura de un mensaje y la ventana  de Escribir. Vea las opciones relevantes.
* Control+Retroceso : También se utiliza para cerrar pestañas y ventanas. Al editar texto, este atajo elimina la palabra anterior.

## Ventana de Escribir
Los atajos en esta ventana se refieren a  los campos de dirección y el panel de adjuntos.

* Alt+1 a Alt+8:<br>
Una pulsación: anuncia el valor de los campos de dirección o del panel de adjuntos,<br>
Dos pulsaciones: coloca el foco en  los campos de dirección o en el panel de adjuntos.
* Alt+avance página: igual que Alt+3 para el panel de adjuntos. 
* Observaciones:<br>
El anuncio del panel de adjuntos con Alt+3 cita una lista numerada de los nombres de los archivos y su tamaño total,<br>
Cuando el foco está en la lista de adjuntos, la tecla  Escape regresa al cuerpo del mensaje.
* Alt+flecha arriba: coloca el mensaje que se está escribiendo en el Navegador de citas virtual;
* Windows+flechas verticales: anuncia la línea anterior o siguiente del navegador de citas; Esto te permite escuchar el mensaje que estás respondiendo sin cambiar de ventana.
* Windows+flecha horizontal: va a la cita anterior o siguiente sin cambiar de ventana.<br>

## Diálogo de Revisar ortografía
Cuando se abre este  diálogo, el complemento anuncia automáticamente las palabras y su deletreo. Esto se puede desactivar en las opciones de la ventana de Escribir.

Los siguientes atajos están disponibles desde el campo de edición de la palabra de reemplazo:

* Alt+flecha arriba: deletrea la palabra mal escrita y la propuesta de reemplazo. 
* Alt+flecha arriba pulsado dos veces: anuncia la frase  en la que se encuentra la palabra mal escrita, gracias al navegador de citas virtual que se inicializa automáticamente en este contexto.
* Intro:  pulsa el botón "Reemplazar", sin salir del campo de edición.
* Shift+Intro: pulsa el botón "Reemplazar todo".
* Control+Intro: pulsa el botón "Ignorar".
* Shift+Control+Intro: pulsa el botón "Ignorar todo".
* Alt+Intro: agrega al diccionario la palabra declarada como mal escrita.

## Libreta de direcciones, una gestión más sencilla (v.2024.02.07)

El complemento mejora los anuncios de la libreta de direcciones y te proporciona órdenes  de teclado que te permiten organizar libretas de direcciones y listas de correo mediante arrastrar y soltar  virtualmente.

### Anuncios mejorados

* Árbol de libretas de direcciones y listas de correo: el complemento también anuncia el tipo de elemento: libreta de direcciones o lista de la libreta de direcciones personal,
* lista de contactos: al pulsar  Espacio se anuncia la ficha detallada del contacto, al pulsar dos veces se anuncia y se copia la ficha al portapapeles.<br>
Nota: si esta lista está en modo "Disposición de la tabla", desmarque esta casilla mediante el botón "Opciones de visualización de la lista" que se encuentra encima de la lista de contactos. 

### Resumen de órdenes

* Tab desde el árbol de libretas de direcciones y listas de correo: accede al campo de búsqueda en la libreta o la lista seleccionada en la vista de árbol. 
* Tab desde el campo de búsqueda: accede directamente a la tabla de contactos saltando el botón "Opciones de visualización de la lista". Esto permanece accesible con Shift+Tab desde la tabla de contactos.  
* Escape:

	* Desde el árbol de la libreta de direcciones, lleva el foco en el botón "Crear una nueva libreta de direcciones" desde la barra de botones encima del árbol. Desde uno de estos botones, la tecla Escape lleva el foco a la vista en árbol;
	* Desde el campo de búsqueda, lleva el foco al árbol de la libreta de direcciones;
	* Desde la tabla de contactos, lleva el foco al campo de búsqueda;
 
* Control+Aplicaciones o tecla encima de Tab: abre un menú contextual que incluye: Ir a la vista en árbol de libretas de direcciones y listas de correo, Ir a la tabla de contactos, Crear una nueva libreta de direcciones, Nuevo contacto, Crear una nueva lista de correo, Importar. Aparte de los dos primeros, estos elementos provienen de la barra de herramientas de la Libreta de direcciones. 
* letra "a" desde la tabla de contactos: arrastra y suelta los contactos seleccionados en la lista de correo o la libreta de direcciones establecida como destino. La primera vez que pulse esta tecla, se le preguntará el destino a través de un menú. Entonces no se le volverá a preguntar el destino hasta que cambie la lista   o la libreta de direcciones personal.
* letra "d" desde la tabla de contactos: muestra el menú de listas  y libretas de direcciones de destino.


Consejo: También puedes utilizar las teclas de navegación en una página web.   La letra "e" te lleva directamente al campo de búsqueda y la letra "t" te lleva a la tabla de contactos.


### Ejemplo 1: creación de una lista de correo en la libreta  de direcciones personal

* Vaya a la libreta de direcciones en vista de árbol y seleccione "Libreta de direcciones personal". Se crea una nueva lista de correo solo en la libreta   seleccionada;
* Pulse Control+Aplicaciones o tecla encima de Tab y en el menú, pulse Intro en: Crear una nueva lista de correo;
* En el cuadro de diálogo que se abrió, ingrese el nombre de la lista, por ejemplo: Mi familia. Puede agregar contactos a través de este cuadro de diálogo pero, por ejemplo, ciérrelo con el botón Aceptar;
* De vuelta en el árbol de listas de correo y libretas de direcciones, observará la aparición de: Mi familia, lista de direcciones personal,<br>
Seleccione "Libreta de direcciones personal";;
* Pulse la tecla Tab para ingresar una palabra clave de búsqueda o Tab en la tabla de contactos o use el menú Control+Aplicaciones o la tecla arriba de Tab;
* En la tabla de contactos, seleccione uno o más contactos mediante el método estándar de Control+Espacio, Control+flecha  abajo, Control+Espacio, etc.
* Pulse la letra a para arrastrarlos y soltarlos en la lista de correo. La primera vez se mostrará el menú de destinos autorizados. Seleccione el elemento "Nombre de lista" y luego pulse Intro. La próxima vez que pulse la letra a, se utilizará el mismo destino sin mostrar este menú.
* Al final de la operación de arrastrar y soltar, se reproducirá un pitido y se enfocará el cuadro de búsqueda.
* Ingrese una nueva palabra, pulse Tab, seleccione contactos y luego pulse la letra a nuevamente para agregarlos a la lista "Nombre de lista".

### Mover contactos de Direcciones recopiladas a diferentes libretas de direcciones

1.  Vaya a la libreta de direcciones en vista de árbol y seleccione "Direcciones recopiladas";
2.  Tabula a la tabla de contactos;
3.  Seleccione uno o más contactos;
4.  Opcionalmente pulse la letra "d" para preseleccionar un nuevo destino;
5.  De vuelta en la tabla de contactos, pulse la letra "a" para arrastrar y soltar;
6.  Una vez hecho esto, se enfocará el cuadro de búsqueda. Opcionalmente, ingrese un nombre y luego repita las operaciones 2 a 5.


## Menú de actualización del complemento (eliminado en la versión 2411.27)

Para acceder a este menú, puede pulsar AltGr+Mayús+tecla encima de la tecla Tab o proceder de la siguiente manera:

* Ir a la ventana principal de Thunderbird,
* Pulse la tecla encima de la tecla Tab,
* En el menú contextual, pulse  flecha  arriba para seleccionar el elemento Actualización luego pulse Intro,
* Un nuevo menú contextual le ofrece la posibilidad de elegir entre: Buscar una actualización, Activar o Desactivar la actualización automática y  Instalar la versión AAMM.DD donde AAMM.DD es la versión disponible para descargar. Esta última puede ser más reciente que la disponible en actualización automática.

## Complementos externos

### Complemento Start With inbox para Thunderbird 115 (2023.10.31)

Cuando se inicia Thunderbird, este complemento selecciona automáticamente la opción:

* la carpeta "Bandeja de entrada" de la cuenta según tu elección en las carpetas en vista de árbol.
* El último mensaje en la carpeta Bandeja de entrada de la cuenta elegida.
* El primer mensaje no leído en la carpeta Bandeja de entrada de la cuenta elegida.

Instalación:

* en Thunderbird, abra el menú "Herramientas" y luego valide en: Complementos y temas;
* En la página Administrador de complementos, colóquese en el campo de búsqueda. En modo exploración, puede pulsar la letra e para llegar rápidamente;
* escribir: Start with Inbox y luego pulse Intro;
* seleccione manualmente la pestaña "Start with Inbox :: Búsqueda :: Complementos para Thunderbird", por ejemplo. Luego pulse la tecla 3 o comilla hasta llegar al encabezado de nivel 3 que se anunciará con el nombre del complemento que ha buscado;
* Con la flecha abajo, desplácese hasta el enlace "Agregar a Thunderbird" y luego pulse Intro en él;
* Siga el procedimiento y luego reinicie Thunderbird;
* Si todo salió bien, Thunderbird se abrirá en la pestaña principal y le dará el foco a la lista de mensajes;


Establecer opciones para Start with Inbox:

* Volver a la pestaña "Administrador de complementos";
* Si es necesario, salir del campo de búsqueda para ponerse en modo exploración;
* Pulse la tecla 3 tantas veces como sea necesario para llegar al encabezado de nivel 3 que se anunciará como "Start with Inbox" en la lista de complementos instalados;
* Luego valide en el botón: Opciones del complemento. Esto abre una nueva pestaña que se anunciará como: Start with Inbox, Settings ;
* Ajuste las opciones y luego reinicie Thunderbird.


[1]: https://github.com/RPTools-org/thunderbirdPlusG5/releases/download/v2404.23.00/thunderbirdPlusG5-2404.23.00.nvda-addon

[2]: https://github.com/RPTools-org/thunderbirdPlusG5/

[3]: https://www.rptools.org/?p=9514

[4]: https://www.rptools.org/NVDA-Thunderbird/index.html

[5]: https://www.rptools.org/NVDA-Thunderbird/get.php?pg=changes&v=G5&lang=es

[6]: https://www.rptools.org/NVDA-Thunderbird/toContact.html

[7]: https://www.rptools.org/NVDA-Thunderbird/get.php?pg=manual&lang=es
