Title: 8 cosas que todo programador de C++ debería saber sobre la codificación de texto
Date: 2019-11-09 13:14
Category: Iniciación C++
Status: draft

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
Sólo que podemos *adivinar* cual estamos usando.


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
Normalmente, se escribe como U+0041, donde U significa Unicode y después se indica el número en base 10.

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

Otra opción es utilizar una cierta compresión, donde se utilice sólo 7 bits de 1 byte para los códigos pequeños y usar más bytes para letras de mayor punto de código.
Este formato se denomina UTF-8. 
Sus principales ventajas son:

- Los textos de alfabetos latinos ocupan menos espacio que en UTF-32.
- No es necesario especificar si es LSB o HSB.

Mientras que su principal desventaja es que es más complicado de decodificar porque cada letra ahora tiene un tamaño variable en función de su punto de código.

También se puede usar UTF-16, donde se utilizan 2 bytes para las letras de puntos pequeños y 4 para las mayores. 


# 3. La libraría heredada de C está pensada para ASCII

Todas las librerías antiguas de C asumían que la codificación del texto es ASCII, por lo que no pueden usarse de forma segura usando otra codificación.

Por ejemplo:

- ```strlen``` asume que un byte a cero indica el final de la cadena pero en UTF-16 pueden aparecer fácilmente ceros en mitad de la cadena.
  Si se usa UTF-8, no aparecen ceros extra, pero el número de caracteres no se corresponde con el número de bytes, ya que puede haber caracteres que empleen dos o más bytes.
- ```strcmp``` realiza una comparación byte a byte de la cadena. 
  Sin embargo, si la cadena no está normalizada, dos textos idénticos pueden usar distintos bytes.
  
Por lo tanto, es necesario usar funciones que sí estén preparadas para la codificación usada.



# 4. Algunas codificaciones necesitan información extra para mostrar el texto
 - Byte order
 - Codepage

# 5. Hay que indicar también la codificación de los archivos de texto


# 6. No todos los sistemas operativos tienen la misma codificación interna y eso importa

Linux utiliza UTF-8 mientras que Windows suele usar UTF-16, aunque es posible cambiarlo en Windows 10.


# 7. La comparación de textos es mucho más complicada de lo que parece


# Referencias

[The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets (No Excuses!)](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/)

[Unicode FAQs](https://unicode.org/faq/basic_q.html)

