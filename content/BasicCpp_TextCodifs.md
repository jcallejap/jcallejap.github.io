Title: 8 cosas que todo programador de C++ debería saber sobre la codificación de texto
Date: 2019-11-09 13:14
Category: Iniciación C++
Status: draft


# 0. No existe el *texto plano*

Para una persona, un texto es un conjunto de caracteres. 

Para un ordenador, un texto es una lista de números.

Es necesario definir la función que pase de los números a los caracteres y viceversa.
Esta función puede ser tan sencilla como una tabla o tan compleja como un sistema de encriptación.
En cualquier caso, es necesario definirla y que sea conocido por ambas partes.

Si una de las partes no tiene acceso a esta función, no es posible la comunicación.



# 1. Codificar caracteres es complicado

Antes de definir la función de codificación/decodificación del texto, es necesario hacer algunas definiciones.
Vamos a tomar las del estándar Unicode, por ser el más extendido.

## Letra

La letra es la únidad mínima de un texto. 
Por ejemplo, tenemos la letra *a*. 
Esta letra es distinta a la *A* o la *b*.

Cada idioma puede tener sus propias reglas para definir qué es una letra. 

Estas reglas pueden cambiar. Por ejemplo, en español antiguamente existía la letra *che* (ch) o la letra elle (ll). 
Alfabeticamente, *calvo* venía antes que *calle* porque la letra *ll* estaba en el alfabeto después de la *l*.
Sin embargo, ya no es así.

Estas reglas pueden tener disputas políticas o teóricas. 
Por ejemplo, ¿es la letra *á* la misma que la letra *a*?
¿Son los emojis letras?


## Punto de código (code point)

Una vez hemos decidido un conjunto de letras diferenciadas, se le asigna un número a cada una. 


# 2. Existen muchos tipos de codificaciones
ASCII
ANSI
Unicode

# 3. La libraría heredada de C está pensada para ASCII

# 4. Algunas codificaciones necesitan información extra para mostrar el texto
 - Byte order
 - Codepage

# 5. Hay que indicar también la codificación de los archivos de texto

# 6. No todos los sistemas operativos tienen la misma codificación interna y eso importa

Linux utiliza UTF-8 mientras que Windows suele usar UTF-16, aunque es posible cambiarlo en Windows 10.

# 7. La comparación de textos es mucho más complicada de lo que parece


# Referencias

https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/