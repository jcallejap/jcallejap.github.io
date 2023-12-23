Title: 8 cosas que todo programador de C++ debería saber sobre la codificación de texto
Date: 2023-12-17 13:14
Category: Iniciación C++
Tags: C++, Unicode
Summary: Dentro de la codificación de texto, hay 8 ideas que todo programador debe conocer...


# 0. No existe el *texto plano*, se necesita conocer la codificación

Para una persona, un texto es un conjunto de caracteres. 

Para un ordenador, un texto es una lista de números.

Es necesario definir la función que transforme de los números a los caracteres y viceversa.
Esta función puede ser tan sencilla como una tabla o tan compleja como un sistema de encriptación.
En cualquier caso, es necesario definirla y que sea conocido por ambas partes.

Si una de las partes no tiene acceso a esta función, no es posible la comunicación. 
Por lo tanto, no puede existir un texto sin una definición de cómo está codificado.

Es cierto que hay algunas codificaciones que se toman por defecto.
Por ejemplo, en ausencia de otra información, podemos suponer que el texto está en ASCII.
Si estamos usando Linux, podemos pensar que la codificación es UTF-8 o, en el caso de Windows, UTF-16.
Pero esto no significa que no necesitamos la codificación. 
Sólo que podemos *adivinar* cuál estamos usando.


# 1. Existen muchos tipos de codificaciones

La codificación más famosa, por ser sencilla y relativamente antigua es [ASCII](https://es.wikipedia.org/wiki/ASCII).
Da un valor numérico a cada letra del alfabeto inglés, a los números y alguno de los caracteres especiales (como símbolos matemáticos o de control).

La codificación ASCII sólo utiliza los primeros 7 bits de un byte, por lo que deja 127 números libres para asignar otros símbolos.
El uso de estos números libres se estandarizó en la norma [ISO 8859](https://es.wikipedia.org/wiki/ISO/IEC_8859).
Esta norma tiene 16 modos, en función de qué tipo de idioma se está codificando.
Por ejemplo, para el alfabeto español se puede usar la norma 8859-1, donde se tiene la *ñ* o caracteres con acentos.
Si se está usando hebreo, se utiliza la 8859-8 que tiene estos caracteres.

El problema con ASCII o ISO-8859 es que sólo utilizan un byte por caracter, lo que impide que se puedan usar caracteres como el chino o el japonés que tienen miles de caracteres.
Para solucionar este problema, existen diferentes codificaciones, siendo la más extendida la [Unicode](https://es.wikipedia.org/wiki/Unicode).


# 2. Codificar caracteres es complicado

Antes de definir la función de codificación/decodificación del texto, es necesario hacer algunas definiciones.
Vamos a tomar las del estándar Unicode, por ser el más extendido.

## Letra

La letra es la únidad mínima de un texto. 
Por ejemplo, tenemos la letra *a*. 
Esta letra es distinta a la *A* (a mayúscula) o la *b*, pero es independiente de su grafía.
Es decir, la letra *A* en Arial es la misma que la letra *A* en Times New Roman.

Cada idioma puede tener sus propias reglas para definir qué es una letra, por lo que ya aparecen varias complicaciones:

- Estas reglas pueden cambiar en el tiempo. 
  Por ejemplo, en español antiguamente existía la letra *che* (ch) o la letra elle (ll). 
  Alfabeticamente, *calvo* venía antes que *calle* porque la letra *ll* estaba en el alfabeto después de la *l*.
  Sin embargo, ya no es así.

- Estas reglas pueden tener disputas políticas o teóricas. 
  Por ejemplo, ¿es la letra *á* la misma que la letra *a*?
  ¿Son los emojis letras?

- Algunos idiomas cambian las letras en función de su posición dentro en una frase.
  Entonces, ¿son letras distintas o son las mismas con distinta grafía?

## Punto de código (code point)

Una vez hemos decidido un conjunto de letras diferenciadas, se le asigna un número a cada una, que llamaremos punto de código (code point). 
Por ejemplo, la letra A tiene el número 41.
Normalmente, se escribe como U+0041, donde U significa Unicode y después se indica el número en base 16.

Algunos de los puntos de código se consideran modificadores.
Por ejemplo, hay un punto de código que indica que hay se añade un acento.

Con esto, aparece una problemática nueva, ya que algunas letras pueden codificarse de formas distintas siendo la misma letra.
Por ejemplo, la letra *Á* tiene su propio punto de código pero también puede ser una *A* + *acento*.

Se denomina normalización a la modificación de una secuencia de letras para que todas utilicen un mismo tipo de puntos de código para las letras compuestas.

## Codificación

Una vez tenemos todas las letras de un texto codificadas con sus puntos de código y normalizadas, hay que decidir cómo convertir los puntos de código a números.

La forma más directa sería escribir directamente los números de cada punto. Esto se llama UTF-32, ya que se utilizan 32 bits para cada número (a pesar de que Unicode no usa los 32 bits).
Sin embargo, esto presenta varios problemas:

- Las letras de origen latino (inglés, español, ...) tienen números pequeños dentro de los puntos de código, por lo que la mayoría de los números serán ceros.
  Podría parecer un desperdicio de espacio.
- Hay arquitecturas que escriben los números como LSB o HSB, por lo que habría que especificar la arquitectura.

Otra opción es utilizar una cierta compresión, donde se utilice 1 byte para las primeras letras y más bytes para las que tienen un punto de código mayor.
Este formato se denomina UTF-8. 
Sus principales ventajas son:

- Los textos de alfabetos latinos ocupan menos espacio que en UTF-32.
- No es necesario especificar si es LSB o HSB.

Su principal desventaja es que es más complicado de decodificar porque cada letra ahora tiene un tamaño variable en función de su punto de código.

También se puede usar UTF-16, donde se utilizan 2 bytes para las letras de puntos pequeños y 4 para las mayores. 


# 3. La libraría heredada de C está pensada para ASCII

Todas las librerías heredadas de C asumen que la codificación del texto es ASCII por lo que, en general, no pueden usarse de forma segura usando otra codificación.

Por ejemplo:

- ```strlen``` asume que un byte a cero indica el final de la cadena pero en UTF-16 pueden aparecer fácilmente ceros en mitad de la cadena.
  Si se usa UTF-8, no aparecen ceros extra, pero ```strlen``` cuenta el número de bytes, no el número de caracteres ya que puede haber caracteres que empleen dos o más bytes.
- ```strcmp``` realiza una comparación byte a byte de la cadena.  
  Sin embargo, si la cadena no está normalizada, dos textos idénticos pueden usar distintos bytes.
  
Por lo tanto, es necesario usar funciones que sí estén preparadas para la codificación que se ha usado en el texto.


# 4. Algunas codificaciones necesitan información extra para mostrar el texto

Algunas codificciones necesitan información extra para poder decodificarse.
Por ejemplo:

- La codificación ISO 8859 necesita que se indique qué caracteres se almacenan en el grupo superior.
  Si no se hace, no se puede decodificar el texto y podríamos terminar mostrando caracteres latinos cuando el texto necesita caracteres griegos.
  No hay una forma estándar de indicar esta información en un archivo.
- La codificación UTF-16 utiliza números de 16 bits como base. 
  Estos números se almacenan como dos bytes, por lo que existen dos formas de guardar el número: LSB y MSB.
  Para especificar cuál se está usando, existe un caracter de control de Unicode denominado [BOM](https://es.wikipedia.org/wiki/Marca_de_orden_de_bytes).
  El BOM tiene como valor *U+FEFF*. El caracter *U+FFFE* no existe, por lo que si se encuentra este conjunto de bytes, podemos saber el orden. 
 
Si guardamos un archivo de texto, tenemos que indicar la codificación en el propio archivo.
Por ejemplo, para UTF-16, se suele guardar el BOM justo al principio del archivo.

Algunos formatos también tienen un lugar donde especificar la codificación.
Por ejemplo, en la cabecera de los archivos XML se puede especificar usando el parámetro encoding:

```
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
```


# 5. C++ no tuvo un tipo de dato para Unicode hasta C++11

Originalmente, C++ tenía dos [tipos de datos](https://en.cppreference.com/w/cpp/language/types) para caracteres:

- char
- wchar_t

El primero estaba pensado para ASCII y es el tipo de dato básico de C++, siendo su tamaño, generalmente, 1 byte.
El segundo estaba pensado para *caracteres anchos* y, como muchos datos de C, no estaba completamente definido.
Windows decidió que su tamaño fuese 2 bytes y lo empleó para UTF-16LE. 
Linux, por el contrario le dio un tamaño de 4 bits.

A partir de C++11, se hicieron algunos avances hacia una estandarización de los tipos de datos de las codificaciones, añadiendo:

- ```char16_t``` para UTF-16.
- ```char32_t``` paraUTF-32.
- ```char8_t``` para UTF-8 (C++20, tardó en oficializarse porque originalmente se pensó en usar char para UTF-8).

Estos nuevos tipos de datos también trajeron una ampliación en los [formatos de los literales](https://en.cppreference.com/w/cpp/language/character_literal).


# 6. No todos los sistemas operativos tienen la misma codificación interna y eso importa

Linux utiliza UTF-8 mientras que Windows suele usar UTF-16 (aunque es posible cambiarlo en Windows 10, no se suele recomendar).
Esto plantea un problema extra para escribir texto portable porque hay que tener en cuenta la codificación del texto que se pasa al interfaz.

La tendencia actual es escribir todo el texto en UTF-8 y cambiar de codificación sólo cuando se va a interactuar con el sistema operativo.
Existen algunas librerías para ayudarnos como [boost::nowide](https://www.boost.org/doc/libs/1_84_0/libs/nowide/doc/html/index.html).

La introducción en C++17 de la librería [FileSystem](https://en.cppreference.com/w/cpp/filesystem) permitió también simplificar el hecho de que 
Windows utiliza rutas de archivo en UTF-16 y Linux en UTF-8.


# 7. La comparación de textos es mucho más complicada de lo que parece

En los alfabetos latinos se establece un orden de los caracteres y después se ordenan las palabras según ese orden empezando por el primer caracter o los siguientes si los primeros coinciden.
Este algoritmo, tan sencillo y conocido, tiene ya varios problemas al llevarlo a la práctica:

- ¿Influye que una letra sea mayúscula?
- ¿Influye que una letra esté acentuada?
- ¿Influye el país? (Por ejemplo, en España durante mucho tiempo la letra *ll* fue distinta a la *l*).
- ¿Qué ocurre si se intercalan caracteres de otros alfabetos? Por ejemplo, los caracteres *@*, *&*, *$*.
- ¿Cómo se ordenan los emojis?

Por otro lado, existen sistemas de escritura más complicados que los latinos.
Por ejemplo, los caracteres chinos se ordenan según el número de trazos necesarios para escribirlos.

Esto hace que sea necesario definir reglas complejas para la comparación de textos.
De esto se encarga el consorcio de [Unicode](https://es.wikipedia.org/wiki/Consorcio_Unicode) aunque la implementación de la norma depende del lenguaje de programación.


# Referencias para saber más

[The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets (No Excuses!)](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/)

[The Absolute Minimum Every Software Developer Must Know About Unicode in 2023 (Still No Excuses!)](https://tonsky.me/blog/unicode/)

[Unicode FAQs](https://unicode.org/faq/basic_q.html)

[UTF-8 Everywhere](https://utf8everywhere.org/)
