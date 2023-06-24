Title: 8 cosas que todo programador de C++ debería saber sobre el comportamiento indefinido
Date: 2019-11-18
Category: Iniciación C++
Status: draft

# 0. ¿Qué  tipos de comportamiento hay en C++?

*Resumen: existen distintos tipos de construcciones en C++ y existe un tipo cuyo comportamiento es impredecible y el compilador no puede detectarlo.*

Existen tres tipos de construcciones en C++:

 - Código mal formado (ill-formed): el código no se corresponde con C++ válido. El programa no es válido y el compilador genera un mensaje.
 - Código mal formado sin diagnóstico (ill-formed no diagnostic required): el código contiene un error que no se ha podido detectar (por ejemplo, violación de ODR). La resultado de la ejecución es indefinido.
 - Código bien formado (well-formed): el código se adhiere a las reglas de C++ y su ejecución se puede determinar dentro del estándar.

Además de estas construcciones, se dan cuatro tipos de comportamiento:

 - Comportamiento definido: la ejecución del programa es completamente predecible.
 - Comportamiento definido por la implementación (implementation-defined behavior): la ejecución es predecible, pero depende del compilador o del entorno dentro de ciertos márgenes y estas variaciones deben estar documentadas.  Por ejemplo, el valor de sizeof(int).
 - Comportamiento no especificado (unspecified behavior): la ejecución no es predecible pero está dentro de ciertas opciones. Por ejemplo, el orden de evaluación de los argumentos de una función.
 - Comportamiento sin definir (undefined behavior): la ejecución no es predecible y puede suceder cualquier cosa.


#1 ¿Qué significa comportamiento indefinido?

*Resumen: El compilador tiene libertad total si se encuentra con comportamiento indefinido: puede no hacer nada o borrar el disco duro.*

Es un comportamiento en el que el estándar no define el resultado de una operación y da libertad **completa** al compilador para decidir qué hacer.
Cuando un programa pasa por alguno de estos casos, se dice que *el programa está mal formado y tiene comportamiento indefinido*.

Por ejemplo, queremos saber qué hace el siguiente código:

```
signed int next(signed int a) {
  return a + 1;
}
```

A primera vista, parece fácil. 
Está definiendo una función f, a la que se le pasa un entero con signo y devuelve el siguiente número.

Sin embargo, ¿qué pasa si el entero ya está en su valor máximo?

En este caso, se produce un desbordamiento de un entero con signo. Cuando esto ocurrr, el estándar no define cómo tiene que comportarse el programa por lo que el compilador tiene libertad total para decidir qué va que pasar con el programa.

Hay que notar que no sólo tiene libertad para decidir lo que ocurre al pasar por esa línea.
Si pasa por esa línea, puede cambiar cualquier otra parte del programa, ya que a partir de ahí, tiene libertad total.
Podría:

 - Poner la variable a cero.
 - Poner la variable en negativo.
 - Cerrar la aplicación.
 - Cerrar la aplicación 1 hora más tarde.
 - Insultar al programador.

Además, podría hacer cosas distinta cada vez que se compila.
Podría cambiar el comportamiento si se actualiza o se cambia el sistema operativo.


#2 ¿Por qué existe el comportamiento indefinido?

*Resumen: El comportamiento indefinido da libertad al compilador para ajustarse a su hardware objetivo.*

En general, el comportamiento indefinido permite que el compilador se adapte mejor al hardware que se está usando y, 
por lo tanto, genere código más optimizado para diferentes plataformas.

Por ejemplo, en el caso anterior:

```
signed int f(signed int a) {
  return a + 1;
}
```

Puede que una arquitectura use complemento a dos para los enteros con signo y el resultado obvio sería que el la función devuelva un número negativo.
Sin embargo, otras arquitecturas podrían lanzar una excepción. Incluso podría pasar que alguna arquitectura se bloquease si se le pide esa operación.

Si el estándard definiese el comportamiento, estaría penalizando a las arquitecturas que no siguien su definición. 
Por ejemplo, si se lanzase una excepción, tendría que comprobar el valor del número antes de realizar el incremento por lo que la función se volvería mucho más lenta.

Además, el programador puede saber que ese caso nunca se da, por lo que sería una penalización sin motivo.

Pongamos otro ejemplo:

```
int f() {
  g();
}
```

El estándar no dice lo que tiene que pasar si una función que debe devolver un valor no devuelve nada.
Tal vez el programador sepa que g() nunca retorna porque siempre lanza una excepción o cierra la aplicación, por lo que no va a haber problemas.
Pero el compilador no lo sabe y tiene que decidir qué hacer. Aquí se encuentra un problema:

 - Si el estándar definiese el comportamiento, le obligaría a añadir código que nunca se va a usar.
 - Si no se define, podría spasar cualquier cosa.

Así pues, el estándard no indica qué debe pasar y el desarrollador del compilador puede hacer lo que más le convenga para su plataforma.


#3 ¿Por qué es tan peligroso el comportamiento indefinido?

*Resumen: El comportamiento indefinido permite que pase cualquier cosa con el programa. El estándar no pone límites a lo que puede pasar.*

El comportamiento indefinido es una de las caracteristicas más peligrosas C++.

Los motivos son varios, aunque los dos principales son:

 - Al dar libertad total al compilador, un programa indefinido podría listar todas las contraseñas del sistema.
   Obviamente, el error no va a ser tan directo, pero nadie te asegura que no lo haga.
   De hecho, muchos errores de seguridad se basan en el comportamiento indefinido de C o C++.
   
 - Cuando hay un comportamiento indefinido, es muy difícil depurar el error.
   Hay que entender que, si se da un comportamiento indefinido, todo el programa es indefinido.
   Por lo que el error puede darse en la línea problemática o podría comportarse según lo esperado durante un tiempo y fallar más adelante.

De hecho, el comportamiento indefinido es una de las mayores quejas de los programadores de C++ y, a la vez, 
lo que le da a C++ la capacidad de generar código optimizado en muchas arquitecturas.


#4. ¿El compilador puede avisar del comportamiento indefinido?

*Resumen: El compilador no está obligado a avisar del comportamiento indefinido.*

El compilador no tiene obligación de avisar del comportamiento indefinido en todos los casos.

Algunos compiladores avisan de los casos sencilos de detectar como:

```
int f() {}
```

Es comportamiento indefinido porque claramente la función no devuelve nada pese a que está declarada para devolver un entero.

Sin embargo, algunos casos son muy complicados de detectar o sólo pueden detectarse en tiempo de ejecución, como por ejemplo:

```
void f(T *object)
{
  object->f();
}
```

Si object es nulo, el programa es indefinido.

En estos casos, para detectarlo, habría que añadir instrucciones que comprobasen que la variable no es nula. Si el programador ya sabe que nunca lo será, se está penalizando la ejecución.


#5 Ejemplos de comportamiento indefinido

Desbordamiento de signo




#6. ¿Qué se puede hacer para minimizar los riesgos?

En general, hay que seguir un conjunto de buenas prácticas de C++. 
Por ejemplo:

 - Activar todos los avisos del compilador.
 - No usar punteros en bruto sino alguna de las múltiples alternativas para gestionar la memoria (std::vector, std::unique_ptr, std::shared_ptr, ...).
 - Usar std::array en vez de arrays de C. 
 - Usar conversiones de C++ (static_cast, ...) en vez de conversiones de C.
 
 
#7 ¿Cómo está relacionado el comportamiento indefinido con el optimizador?




# Referencias

https://stackoverflow.com/q/22180312/218774
https://stackoverflow.com/q/2397984/218774
https://gist.github.com/Earnestly/7c903f481ff9d29a3dd1
https://en.cppreference.com/w/c/language/behavior

